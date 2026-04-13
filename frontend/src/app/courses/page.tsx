"use client";

import { FormEvent, useEffect, useState } from "react";

import { AppShell } from "@/components/AppShell";
import { RequireAuth } from "@/components/RequireAuth";
import { apiGet, apiPost } from "@/lib/api-client";
import { getUser } from "@/lib/auth";

export default function CoursesPage() {
  const user = getUser();
  const isAdmin = user?.role === "admin";

  const [items, setItems] = useState<any[]>([]);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [level, setLevel] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const q = new URLSearchParams({ page: String(page), limit: "10" });
      if (search) q.set("search", search);
      if (level) q.set("level", level);
      const res = await apiGet(`/courses?${q.toString()}`);
      setItems(res.items);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, [page]);

  async function createCourse(e: FormEvent) {
    e.preventDefault();
    if (!title.trim() || !description.trim()) {
      setError("Title and description are required.");
      return;
    }
    await apiPost("/courses", { title, description, level: "beginner" });
    setTitle("");
    setDescription("");
    await load();
  }

  async function enroll(courseId: string) {
    await apiPost(`/courses/${courseId}/enroll`);
    alert("Enrolled");
  }

  return (
    <RequireAuth>
      <AppShell>
        <div className="card">
          <h1>Courses</h1>
          <div style={{ display: "flex", gap: 8 }}>
            <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search title" />
            <select value={level} onChange={(e) => setLevel(e.target.value)}>
              <option value="">All levels</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
            <button onClick={load}>Apply</button>
          </div>
          {isAdmin && (
            <form onSubmit={createCourse} style={{ display: "grid", gap: 8, marginTop: 12 }}>
              <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Course title" />
              <input value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Course description" />
              <button type="submit">Create Course</button>
            </form>
          )}
          {loading && <p>Loading...</p>}
          {error && <p style={{ color: "crimson" }}>{error}</p>}
          {!loading && items.length === 0 && <p>No courses found.</p>}
          {items.map((c) => (
            <div className="card" key={c.id}>
              <strong>{c.title}</strong>
              <p>{c.description}</p>
              <small>{c.level}</small>
              {!isAdmin && <div><button onClick={() => enroll(c.id)}>Enroll</button></div>}
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
