import { apiGet } from "@/lib/api-client";

export default async function CoursesPage() {
  const courses = await apiGet("/courses?page=1&limit=20");

  return (
    <main>
      <h1>Courses</h1>
      <pre>{JSON.stringify(courses, null, 2)}</pre>
    </main>
  );
}
