from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db, require_role
from app.core.errors import AppError
from app.db.models.user import User
from app.repositories.learning_path_repository import LearningPathRepository
from app.schemas.learning_path import LearningPathCreate, MapCourseToPath

router = APIRouter()


@router.post("/learning-paths")
def create_learning_path(payload: LearningPathCreate, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    repo = LearningPathRepository(db)
    path = repo.create_path(payload)
    return {
        "id": path.id,
        "title": path.title,
        "role": path.role,
        "description": path.description,
        "course_ids": [],
    }


@router.post("/learning-paths/{path_id}/courses")
def map_course(path_id: str, payload: MapCourseToPath, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    repo = LearningPathRepository(db)
    path = repo.get_path(path_id)
    if not path:
        raise AppError("Learning path not found", code="PATH_NOT_FOUND", status_code=404)

    course = repo.get_course(payload.course_id)
    if not course:
        raise AppError("Course not found", code="COURSE_NOT_FOUND", status_code=404)

    repo.map_course(path_id=path_id, course_id=payload.course_id)
    return {
        "id": path.id,
        "title": path.title,
        "role": path.role,
        "description": path.description,
        "course_ids": repo.list_course_ids(path_id),
    }


@router.get("/users/{user_id}/learning-paths/{path_id}/progress")
def get_path_progress(user_id: str, path_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role != "admin" and user.id != user_id:
        raise AppError("Forbidden", code="FORBIDDEN", status_code=403)

    repo = LearningPathRepository(db)
    path = repo.get_path(path_id)
    if not path:
        raise AppError("Learning path not found", code="PATH_NOT_FOUND", status_code=404)

    return repo.path_progress(user_id=user_id, path_id=path_id)


@router.get("/users/{user_id}/learning-paths/{path_id}/next-course")
def recommend_next_course(user_id: str, path_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role != "admin" and user.id != user_id:
        raise AppError("Forbidden", code="FORBIDDEN", status_code=403)

    repo = LearningPathRepository(db)
    path = repo.get_path(path_id)
    if not path:
        raise AppError("Learning path not found", code="PATH_NOT_FOUND", status_code=404)

    return {"next_course_id": repo.next_course(user_id=user_id, path_id=path_id)}

