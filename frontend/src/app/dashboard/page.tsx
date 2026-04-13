"use client";

import { useEffect, useState } from "react";

import { AppShell } from "@/components/AppShell";
import { RequireAuth } from "@/components/RequireAuth";
import { apiGet } from "@/lib/api-client";
import { getUser } from "@/lib/auth";

export default function DashboardPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const user = getUser();
    if (!user) return;
    apiGet(`/users/${user.id}/dashboard`)
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <RequireAuth>
      <AppShell>
        <div className="card">
          <h1>Dashboard</h1>
          {loading && <p>Loading dashboard...</p>}
          {error && <p style={{ color: "crimson" }}>{error}</p>}
          {!loading && !error && data && (
            <>
              <p>Enrolled Courses: {data.enrolled_courses}</p>
              <p>Average Progress: {data.avg_progress_percent}%</p>
              <h3>Recent Scores</h3>
              {data.recent_scores.length === 0 ? <p>No scores yet.</p> : data.recent_scores.map((s: any) => (
                <div className="card" key={s.attempt_id}>{s.attempt_id}: {s.score}/{s.max_score}</div>
              ))}
            </>
          )}
        </div>
      </AppShell>
    </RequireAuth>
  );
}
