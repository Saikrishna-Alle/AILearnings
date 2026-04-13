"use client";

import { FormEvent, useState } from "react";

import { AppShell } from "@/components/AppShell";
import { RequireAuth } from "@/components/RequireAuth";
import { apiPost } from "@/lib/api-client";
import { getUser } from "@/lib/auth";

export default function AssessmentsPage() {
  const user = getUser();
  const isAdmin = user?.role === "admin";
  const [courseId, setCourseId] = useState("");
  const [title, setTitle] = useState("");
  const [assessmentId, setAssessmentId] = useState("");
  const [attemptId, setAttemptId] = useState("");
  const [answer, setAnswer] = useState("A");
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  async function createAssessment(e: FormEvent) {
    e.preventDefault();
    if (!courseId || !title) return setError("Course ID and title required.");
    const res = await apiPost(`/admin/courses/${courseId}/assessments?title=${encodeURIComponent(title)}`);
    setAssessmentId(res.id);
  }

  async function start() {
    if (!assessmentId) return setError("Assessment ID required.");
    const res = await apiPost(`/assessments/${assessmentId}/start`);
    setAttemptId(res.attempt_id);
  }

  async function submit() {
    if (!attemptId || !answer) return setError("Attempt ID and answer required.");
    const res = await apiPost(`/assessments/${attemptId}/submit`, {
      answers: [{ question_id: "q1", answer }],
    });
    setResult(res);
  }

  return (
    <RequireAuth>
      <AppShell>
        <div className="card">
          <h1>Assessments</h1>
          {error && <p style={{ color: "crimson" }}>{error}</p>}
          {isAdmin && (
            <form onSubmit={createAssessment} style={{ display: "flex", gap: 8 }}>
              <input value={courseId} onChange={(e) => setCourseId(e.target.value)} placeholder="Course ID" />
              <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Assessment title" />
              <button type="submit">Create Assessment</button>
            </form>
          )}
          <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
            <input value={assessmentId} onChange={(e) => setAssessmentId(e.target.value)} placeholder="Assessment ID" />
            <button onClick={start}>Start</button>
          </div>
          <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
            <input value={attemptId} onChange={(e) => setAttemptId(e.target.value)} placeholder="Attempt ID" />
            <input value={answer} onChange={(e) => setAnswer(e.target.value)} placeholder="Answer" />
            <button onClick={submit}>Submit</button>
          </div>
          {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
        </div>
      </AppShell>
    </RequireAuth>
  );
}
