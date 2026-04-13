from fastapi import APIRouter

from app.services import state

router = APIRouter()


@router.get("/users/{user_id}/dashboard")
def get_dashboard(user_id: str):
    enrolled_courses = [k[1] for k in state.enrollments.keys() if k[0] == user_id]
    course_progress = []
    for course_id in enrolled_courses:
        module_ids = [m["id"] for m in state.modules.values() if m["course_id"] == course_id]
        lesson_ids = [l["id"] for l in state.lessons.values() if l["module_id"] in module_ids]
        total = len(lesson_ids)
        completed = len([lid for lid in lesson_ids if (user_id, lid) in state.lesson_completion])
        percent = int((completed / total) * 100) if total else 0
        course_progress.append(percent)

    avg_progress = int(sum(course_progress) / len(course_progress)) if course_progress else 0

    scored_attempts = [a for a in state.attempts.values() if a.get("status") == "evaluated"]

    return {
        "enrolled_courses": len(enrolled_courses),
        "avg_progress_percent": avg_progress,
        "recent_activity": [
            {"type": "enrollments", "count": len(enrolled_courses)},
            {"type": "posts", "count": len(state.posts)},
        ],
        "recent_scores": [
            {"attempt_id": a["attempt_id"], "score": a["score"], "max_score": a["max_score"]}
            for a in scored_attempts[-5:]
        ],
    }
