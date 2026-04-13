import { apiGet } from "@/lib/api-client";

export default async function DashboardPage() {
  const dashboard = await apiGet("/users/demo_user_1/dashboard");

  return (
    <main>
      <h1>Dashboard</h1>
      <pre>{JSON.stringify(dashboard, null, 2)}</pre>
    </main>
  );
}
