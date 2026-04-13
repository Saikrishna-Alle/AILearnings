import uuid

from fastapi import APIRouter

from app.core.errors import AppError
from app.schemas.learning_path import LearningPathCreate, MapCourseToPath
from app.services import state

router = APIRouter()


@router.post("/learning-paths")
def create_learning_path(payload: LearningPathCreate):
    path_id = f"path_{uuid.uuid4().hex[:8]}"
    state.learning_paths[path_id] = {
        "id": path_id,
        "title": payload.title,
        "role": payload.role,
        "description": payload.description,
        "course_ids": [],
    }
    return state.learning_paths[path_id]


@router.post("/learning-paths/{path_id}/courses")
def map_course(path_id: str, payload: MapCourseToPath):
    path = state.learning_paths.get(path_id)
    if not path:
        raise AppError("Learning path not found", code="PATH_NOT_FOUND", status_code=404)
    if payload.course_id not in state.courses:
        raise AppError("Course not found", code="COURSE_NOT_FOUND", status_code=404)

    if payload.course_id not in path["course_ids"]:
        path["course_ids"].append(payload.course_id)
    return path


@router.get("/users/{user_id}/learning-paths/{path_id}/progress")
def get_path_progress(user_id: str, path_id: str):
    path = state.learning_paths.get(path_id)
    if not path:
        raise AppError("Learning path not found", code="PATH_NOT_FOUND", status_code=404)

    total = len(path["course_ids"])
    completed = 0
    for course_id in path["course_ids"]:
        enrolled = (user_id, course_id) in state.enrollments
        if enrolled:
            completed += 1

    percent = int((completed / total) * 100) if total else 0
    return {
        "path_id": path_id,
        "completed_courses": completed,
        "total_courses": total,
        "completion_percent": percent,
    }


@router.get("/users/{user_id}/learning-paths/{path_id}/next-course")
def recommend_next_course(user_id: str, path_id: str):
    path = state.learning_paths.get(path_id)
    if not path:
        raise AppError("Learning path not found", code="PATH_NOT_FOUND", status_code=404)

    for course_id in path["course_ids"]:
        if (user_id, course_id) not in state.enrollments:
            return {"next_course_id": course_id}

    return {"next_course_id": None}
