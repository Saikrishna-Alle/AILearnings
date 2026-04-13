"use client";

import { useEffect, useState } from "react";

import { AppShell } from "@/components/AppShell";
import { RequireAuth } from "@/components/RequireAuth";
import { apiGet } from "@/lib/api-client";
import { getUser } from "@/lib/auth";

export default function AdminPage() {
  const user = getUser();
  const [page, setPage] = useState(1);
  const [role, setRole] = useState("");
  const [items, setItems] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    const q = new URLSearchParams({ page: String(page), limit: "10" });
    if (role) q.set("role", role);
    const res = await apiGet(`/admin/users/progress?${q.toString()}`);
    setItems(res.items);
  }

  useEffect(() => { load().catch((e) => setError(e.message)); }, [page]);

  return (
    <RequireAuth>
      <AppShell>
        <div className="card">
          <h1>Admin</h1>
          {user?.role !== "admin" && <p style={{ color: "crimson" }}>Admin access required.</p>}
          {error && <p style={{ color: "crimson" }}>{error}</p>}
          <div style={{ display: "flex", gap: 8 }}>
            <select value={role} onChange={(e) => setRole(e.target.value)}>
              <option value="">All roles</option>
              <option value="admin">Admin</option>
              <option value="student">Student</option>
            </select>
            <button onClick={load}>Apply</button>
          </div>
          {items.map((x) => (
            <div className="card" key={x.user_id}>
              <p>{x.name} ({x.role})</p>
              <p>{x.email}</p>
              <p>Completed Lessons: {x.completed_lessons}</p>
              <p>Enrolled: {(x.enrolled_courses || []).join(", ")}</p>
            </div>
          ))}
          <div style={{ display: "flex", gap: 8 }}>
            <button disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>Prev</button>
            <span>Page {page}</span>
            <button onClick={() => setPage((p) => p + 1)}>Next</button>
          </div>
        </div>
      </AppShell>
    </RequireAuth>
  );
}
