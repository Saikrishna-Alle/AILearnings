from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def login(email: str, password: str) -> str:
    res = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert res.status_code == 200, res.text
    return res.json()["access_token"]


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_student_journey_end_to_end() -> None:
    admin_token = login("admin@ail.dev", "admin123")
    student_token = login("student@ail.dev", "student123")

    course = client.post(
        "/api/v1/courses",
        json={"title": "PyTest Course", "description": "Flow", "level": "beginner"},
        headers=auth_headers(admin_token),
    )
    assert course.status_code == 200, course.text
    course_id = course.json()["id"]

    module = client.post(
        f"/api/v1/courses/{course_id}/modules",
        json={"title": "Module 1"},
        headers=auth_headers(admin_token),
    )
    assert module.status_code == 200, module.text
    module_id = module.json()["id"]

    lesson = client.post(
        f"/api/v1/modules/{module_id}/lessons",
        json={"title": "Lesson 1", "type": "text", "content_text": "abc"},
        headers=auth_headers(admin_token),
    )
    assert lesson.status_code == 200, lesson.text
    lesson_id = lesson.json()["id"]

    enroll = client.post(f"/api/v1/courses/{course_id}/enroll", headers=auth_headers(student_token))
    assert enroll.status_code == 200, enroll.text

    complete = client.post(f"/api/v1/lessons/{lesson_id}/complete", headers=auth_headers(student_token))
    assert complete.status_code == 200, complete.text

    cert = client.post(
        "/api/v1/certificates/generate",
        json={"course_id": course_id},
        headers=auth_headers(student_token),
    )
    assert cert.status_code == 200, cert.text


def test_admin_permissions_enforced() -> None:
    student_token = login("student@ail.dev", "student123")

    forbidden = client.post(
        "/api/v1/courses",
        json={"title": "Should Fail", "description": "x", "level": "beginner"},
        headers=auth_headers(student_token),
    )
    assert forbidden.status_code == 403

    no_auth = client.get("/api/v1/courses")
    assert no_auth.status_code == 401
