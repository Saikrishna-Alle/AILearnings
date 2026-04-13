import { apiGet } from "@/lib/api-client";

export default async function SocialPage() {
  const feed = await apiGet("/feed");

  return (
    <main>
      <h1>Social Feed</h1>
      <pre>{JSON.stringify(feed, null, 2)}</pre>
    </main>
  );
}
