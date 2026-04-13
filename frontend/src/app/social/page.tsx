"use client";

import { FormEvent, useEffect, useState } from "react";

import { AppShell } from "@/components/AppShell";
import { RequireAuth } from "@/components/RequireAuth";
import { apiGet, apiPost } from "@/lib/api-client";

export default function SocialPage() {
  const [content, setContent] = useState("");
  const [items, setItems] = useState<any[]>([]);
  const [page, setPage] = useState(1);
  const [filterUser, setFilterUser] = useState("");
  const [comment, setComment] = useState<Record<string, string>>({});
  const [error, setError] = useState<string | null>(null);

  async function load() {
    const q = new URLSearchParams({ page: String(page), limit: "10" });
    if (filterUser) q.set("user_id", filterUser);
    const res = await apiGet(`/feed?${q.toString()}`);
    setItems(res.items);
  }

  useEffect(() => { load().catch((e) => setError(e.message)); }, [page]);

  async function createPost(e: FormEvent) {
    e.preventDefault();
    if (content.trim().length < 3) return setError("Post must be at least 3 chars.");
    await apiPost("/posts", { content });
    setContent("");
    await load();
  }

  async function like(postId: string) {
    await apiPost(`/posts/${postId}/like`);
    await load();
  }

  async function addComment(postId: string) {
    const value = comment[postId] || "";
    if (value.trim().length < 2) return setError("Comment too short.");
    await apiPost(`/posts/${postId}/comments`, { content: value });
    setComment((prev) => ({ ...prev, [postId]: "" }));
    await load();
  }

  return (
    <RequireAuth>
      <AppShell>
        <div className="card">
          <h1>Social Feed</h1>
          {error && <p style={{ color: "crimson" }}>{error}</p>}
          <form onSubmit={createPost} style={{ display: "flex", gap: 8 }}>
            <input value={content} onChange={(e) => setContent(e.target.value)} placeholder="Write a post..." />
            <button type="submit">Post</button>
          </form>
          <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
            <input value={filterUser} onChange={(e) => setFilterUser(e.target.value)} placeholder="Filter by user id" />
            <button onClick={load}>Apply</button>
          </div>
          {items.length === 0 ? <p>No feed items.</p> : items.map((p) => (
            <div className="card" key={p.id}>
              <p><strong>{p.user_id}</strong>: {p.content}</p>
              <p>Likes: {p.like_count} | Comments: {p.comment_count}</p>
              <button onClick={() => like(p.id)}>Like</button>
              <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
                <input value={comment[p.id] || ""} onChange={(e) => setComment((prev) => ({ ...prev, [p.id]: e.target.value }))} placeholder="Add comment" />
                <button onClick={() => addComment(p.id)}>Comment</button>
              </div>
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
