"use client";

import Link from "next/link";

import { AppShell } from "@/components/AppShell";

export default function HomePage() {
  return (
    <AppShell>
      <div className="card">
        <h1>AI Skill Platform</h1>
        <p>Login with seeded users:</p>
        <ul>
          <li><code>admin@ail.dev / admin123</code></li>
          <li><code>student@ail.dev / student123</code></li>
        </ul>
        <Link href="/login">Go to Login</Link>
      </div>
    </AppShell>
  );
}
