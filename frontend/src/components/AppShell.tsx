"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { clearAuth, getUser, type AuthUser } from "@/lib/auth";

const links = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/courses", label: "Courses" },
  { href: "/learning-paths", label: "Learning Paths" },
  { href: "/assessments", label: "Assessments" },
  { href: "/certificates", label: "Certificates" },
  { href: "/social", label: "Social" },
  { href: "/admin", label: "Admin" },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);

  useEffect(() => {
    setUser(getUser());
  }, []);

  function logout() {
    clearAuth();
    window.location.href = "/login";
  }

  return (
    <main>
      <div className="card" style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12 }}>
        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          {links.map((item) => (
            <Link key={item.href} href={item.href}>
              {item.label}
            </Link>
          ))}
        </div>
        <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <span>{user ? `${user.name} (${user.role})` : "Not logged in"}</span>
          {user ? <button onClick={logout}>Logout</button> : <Link href="/login">Login</Link>}
        </div>
      </div>
      {children}
    </main>
  );
}
