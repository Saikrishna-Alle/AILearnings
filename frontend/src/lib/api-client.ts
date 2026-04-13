import { getToken } from "@/lib/auth";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000/api/v1";

async function request(path: string, options: RequestInit = {}) {
  const token = typeof window !== "undefined" ? getToken() : null;
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string> | undefined),
  };
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  const isJson = response.headers.get("content-type")?.includes("application/json");
  const payload = isJson ? await response.json() : await response.text();

  if (!response.ok) {
    const message = typeof payload === "object" ? payload?.error?.message || payload?.detail?.[0]?.msg || "Request failed" : "Request failed";
    throw new Error(message);
  }

  return payload;
}

export function apiGet(path: string) {
  return request(path, { method: "GET" });
}

export function apiPost(path: string, body?: unknown) {
  return request(path, { method: "POST", body: body ? JSON.stringify(body) : undefined });
}

export function apiPut(path: string, body?: unknown) {
  return request(path, { method: "PUT", body: body ? JSON.stringify(body) : undefined });
}

export function apiDelete(path: string) {
  return request(path, { method: "DELETE" });
}
