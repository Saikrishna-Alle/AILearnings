"use client";

import { useEffect, useState } from "react";

import { AppShell } from "@/components/AppShell";
import { RequireAuth } from "@/components/RequireAuth";
import { apiGet } from "@/lib/api-client";
import { getUser } from "@/lib/auth";

export default function CertificatesPage() {
  const [courseId, setCourseId] = useState("");
  const [certId, setCertId] = useState("");
  const [preview, setPreview] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  async function generate() {
    if (!courseId.trim()) return setError("Course ID required.");
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000/api/v1"}/certificates/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("ail_token") || ""}`,
      },
      body: JSON.stringify({ course_id: courseId }),
    });
    const body = await res.json();
    if (!res.ok) return setError(body.error?.message || "Failed");
    setCertId(body.certificate_id);
    setPreview(body);
  }

  async function fetchPreview() {
    if (!certId.trim()) return setError("Certificate ID required.");
    const res = await apiGet(`/certificates/${certId}/preview`);
    setPreview(res);
  }

  return (
    <RequireAuth>
      <AppShell>
        <div className="card">
          <h1>Certificates</h1>
          {error && <p style={{ color: "crimson" }}>{error}</p>}
          <div style={{ display: "flex", gap: 8 }}>
            <input value={courseId} onChange={(e) => setCourseId(e.target.value)} placeholder="Course ID" />
            <button onClick={generate}>Generate Certificate</button>
          </div>
          <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
            <input value={certId} onChange={(e) => setCertId(e.target.value)} placeholder="Certificate ID" />
            <button onClick={fetchPreview}>Preview</button>
          </div>
          {preview && <pre>{JSON.stringify(preview, null, 2)}</pre>}
        </div>
      </AppShell>
    </RequireAuth>
  );
}
