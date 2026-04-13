from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db, require_role
from app.core.errors import AppError
from app.db.models.user import User
from app.repositories.common import to_iso
from app.repositories.course_repository import CourseRepository
from app.schemas.course import CourseCreate, CourseUpdate, LessonCreate, ModuleCreate

router = APIRouter()


@router.post("/courses")
def create_course(payload: CourseCreate, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    repo = CourseRepository(db)
    course = repo.create_course(payload)
    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "level": course.level,
        "status": course.status,
        "created_at": to_iso(course.created_at),
    }


@router.get("/courses")
def get_courses(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None),
    level: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    repo = CourseRepository(db)
    items, total = repo.list_courses(page=page, limit=limit, search=search, level=level)
    response_items = [
        {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "level": item.level,
            "status": item.status,
            "created_at": to_iso(item.created_at),
        }
        for item in items
    ]
    return {"items": response_items, "page": page, "limit": limit, "total": total}


@router.get("/courses/{course_id}")
def get_course(course_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    repo = CourseRepository(db)
    course = repo.get_course(course_id)
    if not course:
        raise AppError("Course not found", code="COURSE_NOT_FOUND", status_code=404)
    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "level": course.level,
        "status": course.status,
        "created_at": to_iso(course.created_at),
    }


@router.put("/courses/{course_id}")
def update_course(course_id: str, payload: CourseUpdate, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    repo = CourseRepository(db)
    course = repo.get_course(course_id)
    if not course:
        raise AppError("Course not found", code="COURSE_NOT_FOUND", status_code=404)

    updated = repo.update_course(course, payload)
    return {
        "id": updated.id,
        "title": updated.title,
        "description": updated.description,
        "level": updated.level,
        "status": updated.status,
        "created_at": to_iso(updated.created_at),
    }


@router.delete("/courses/{course_id}")
def delete_course(course_id: str, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    repo = CourseRepository(db)
    course = repo.get_course(course_id)
    if not course:
        raise AppError("Course not found", code="COURSE_NOT_FOUND", status_code=404)

    repo.delete_course(course)
    return {"deleted": True, "course_id": course_id}


@router.post("/courses/{course_id}/modules")
def create_module(course_id: str, payload: ModuleCreate, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    repo = CourseRepository(db)
    course = repo.get_course(course_id)
    if not course:
        raise AppError("Course not found", code="COURSE_NOT_FOUND", status_code=404)

    module = repo.create_module(course_id=course_id, payload=payload)
    return {
        "id": module.id,
        "course_id": module.course_id,
        "title": module.title,
    }


@router.post("/modules/{module_id}/lessons")
def create_lesson(module_id: str, payload: LessonCreate, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    repo = CourseRepository(db)
    module = repo.get_module(module_id)
    if not module:
        raise AppError("Module not found", code="MODULE_NOT_FOUND", status_code=404)

    lesson = repo.create_lesson(module_id=module_id, payload=payload)
    return {
        "id": lesson.id,
        "module_id": lesson.module_id,
        "title": lesson.title,
        "type": lesson.lesson_type,
        "content_url": lesson.content_url,
        "content_text": lesson.content_text,
        "duration_sec": lesson.duration_sec,
    }
