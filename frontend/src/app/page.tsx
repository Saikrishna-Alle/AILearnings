const sections = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/courses", label: "Courses" },
  { href: "/learning-paths", label: "Learning Paths" },
  { href: "/assessments", label: "Assessments" },
  { href: "/social", label: "Social" },
  { href: "/admin", label: "Admin" },
];

export default function HomePage() {
  return (
    <main>
      <h1>AI Skill Platform - Phase 1 Starter</h1>
      <p>Dummy user: <code>demo_user_1</code></p>
      {sections.map((item) => (
        <div className="card" key={item.href}>
          <a href={item.href}>{item.label}</a>
        </div>
      ))}
    </main>
  );
}
