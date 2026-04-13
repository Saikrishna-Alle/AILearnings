import { apiGet } from "@/lib/api-client";

export default async function AdminPage() {
  const data = await apiGet("/admin/users/demo_user_1/progress");

  return (
    <main>
      <h1>Admin</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </main>
  );
}
