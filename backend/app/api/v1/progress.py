from fastapi import APIRouter, Depends

from app.core.deps import get_user_id
from app.core.errors import AppError
from app.services import state

router = APIRouter()


@router.post("/courses/{course_id}/enroll")
def enroll_in_course(course_id: str, user_id: str = Depends(get_user_id)):
    if course_id not in state.courses:
        raise AppError("Course not found", code="COURSE_NOT_FOUND", status_code=404)

    key = (user_id, course_id)
    state.enrollments[key] = {
        "user_id": user_id,
        "course_id": course_id,
        "enrolled_at": state.now_iso(),
    }
    return {"enrolled": True, "user_id": user_id, "course_id": course_id}


@router.post("/lessons/{lesson_id}/complete")
def mark_lesson_complete(lesson_id: str, user_id: str = Depends(get_user_id)):
    if lesson_id not in state.lessons:
        raise AppError("Lesson not found", code="LESSON_NOT_FOUND", status_code=404)

    state.lesson_completion[(user_id, lesson_id)] = state.now_iso()
    return {"completed": True, "user_id": user_id, "lesson_id": lesson_id}


@router.get("/users/{user_id}/courses/{course_id}/progress")
def course_progress(user_id: str, course_id: str):
    if course_id not in state.courses:
        raise AppError("Course not found", code="COURSE_NOT_FOUND", status_code=404)

    module_ids = [m["id"] for m in state.modules.values() if m["course_id"] == course_id]
    lesson_ids = [l["id"] for l in state.lessons.values() if l["module_id"] in module_ids]

    completed = [lid for lid in lesson_ids if (user_id, lid) in state.lesson_completion]
    total = len(lesson_ids)
    percent = int((len(completed) / total) * 100) if total else 0

    return {
        "progress_percent": percent,
        "completed_lessons": len(completed),
        "total_lessons": total,
        "last_lesson_id": completed[-1] if completed else None,
    }


@router.get("/users/{user_id}/courses/{course_id}/resume")
def resume_course(user_id: str, course_id: str):
    progress = course_progress(user_id, course_id)
    return {
        "course_id": course_id,
        "resume_lesson_id": progress["last_lesson_id"],
    }
