"use client";

import { FormEvent, useEffect, useState } from "react";

import { AppShell } from "@/components/AppShell";
import { RequireAuth } from "@/components/RequireAuth";
import { apiGet, apiPost } from "@/lib/api-client";
import { getUser } from "@/lib/auth";

export default function LearningPathsPage() {
  const user = getUser();
  const isAdmin = user?.role === "admin";
  const [pathId, setPathId] = useState("");
  const [courseId, setCourseId] = useState("");
  const [title, setTitle] = useState("");
  const [role, setRole] = useState("backend");
  const [progress, setProgress] = useState<any>(null);
  const [next, setNext] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  async function createPath(e: FormEvent) {
    e.preventDefault();
    if (!title.trim()) return setError("Path title required.");
    const res = await apiPost("/learning-paths", { title, role, description: "" });
    setPathId(res.id);
  }

  async function mapCourse(e: FormEvent) {
    e.preventDefault();
    if (!pathId || !courseId) return setError("Path ID and Course ID required.");
    await apiPost(`/learning-paths/${pathId}/courses`, { course_id: courseId });
  }

  async function loadProgress() {
    if (!pathId || !user) return;
    const p = await apiGet(`/users/${user.id}/learning-paths/${pathId}/progress`);
    const n = await apiGet(`/users/${user.id}/learning-paths/${pathId}/next-course`);
    setProgress(p);
    setNext(n);
  }

  useEffect(() => {
    if (pathId) loadProgress();
  }, [pathId]);

  return (
    <RequireAuth>
      <AppShell>
        <div className="card">
          <h1>Learning Paths</h1>
          {error && <p style={{ color: "crimson" }}>{error}</p>}
          {isAdmin && (
            <>
              <form onSubmit={createPath} style={{ display: "flex", gap: 8 }}>
                <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Path title" />
                <input value={role} onChange={(e) => setRole(e.target.value)} placeholder="Role" />
                <button type="submit">Create Path</button>
              </form>
              <form onSubmit={mapCourse} style={{ display: "flex", gap: 8, marginTop: 8 }}>
                <input value={pathId} onChange={(e) => setPathId(e.target.value)} placeholder="Path ID" />
                <input value={courseId} onChange={(e) => setCourseId(e.target.value)} placeholder="Course ID" />
                <button type="submit">Map Course</button>
              </form>
            </>
          )}
          {!isAdmin && <input value={pathId} onChange={(e) => setPathId(e.target.value)} placeholder="Enter Path ID" />}
          <div style={{ marginTop: 8 }}>
            <button onClick={loadProgress}>Refresh Progress</button>
          </div>
          {progress && <pre>{JSON.stringify(progress, null, 2)}</pre>}
          {next && <pre>{JSON.stringify(next, null, 2)}</pre>}
        </div>
      </AppShell>
    </RequireAuth>
  );
}
