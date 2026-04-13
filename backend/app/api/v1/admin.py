from fastapi import APIRouter

from app.services import state

router = APIRouter()


@router.get("/admin/users/{user_id}/progress")
def admin_user_progress(user_id: str):
    enrolled = [k[1] for k in state.enrollments.keys() if k[0] == user_id]
    completed_lessons = len([1 for key in state.lesson_completion.keys() if key[0] == user_id])
    return {
        "user_id": user_id,
        "enrolled_courses": enrolled,
        "completed_lessons": completed_lessons,
    }


@router.post("/admin/courses/{course_id}/assessments")
def create_assessment(course_id: str, title: str):
    assessment_id = f"asm_{len(state.assessments) + 1}"
    state.assessments[assessment_id] = {
        "id": assessment_id,
        "course_id": course_id,
        "title": title,
    }
    return state.assessments[assessment_id]
