"use client";

import { FormEvent, useState } from "react";

import { apiPost } from "@/lib/api-client";
import { saveAuth } from "@/lib/auth";

export default function LoginPage() {
  const [email, setEmail] = useState("student@ail.dev");
  const [password, setPassword] = useState("student123");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit(e: FormEvent) {
    e.preventDefault();
    setError(null);

    if (!email.includes("@")) {
      setError("Enter a valid email address.");
      return;
    }
    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }

    setLoading(true);
    try {
      const res = await apiPost("/auth/login", { email, password });
      saveAuth(res.access_token, res.user);
      window.location.href = "/dashboard";
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <div className="card">
        <h1>Login</h1>
        <form onSubmit={submit} style={{ display: "grid", gap: 10 }}>
          <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
          <button disabled={loading} type="submit">{loading ? "Signing in..." : "Sign In"}</button>
        </form>
        {error && <p style={{ color: "crimson" }}>{error}</p>}
      </div>
    </main>
  );
}
