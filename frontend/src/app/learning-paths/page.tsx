import { apiGet } from "@/lib/api-client";

export default async function LearningPathsPage() {
  const progress = await apiGet("/users/demo_user_1/learning-paths/path_demo/progress").catch(() => ({
    message: "Create a learning path first via API.",
  }));

  return (
    <main>
      <h1>Learning Paths</h1>
      <pre>{JSON.stringify(progress, null, 2)}</pre>
    </main>
  );
}
