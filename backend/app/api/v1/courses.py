import uuid

from fastapi import APIRouter, Query

from app.core.errors import AppError
from app.schemas.course import CourseCreate, CourseUpdate, LessonCreate, ModuleCreate
from app.services import state

router = APIRouter()


@router.post("/courses")
def create_course(payload: CourseCreate):
    course_id = f"course_{uuid.uuid4().hex[:8]}"
    course = {
        "id": course_id,
        "title": payload.title,
        "description": payload.description,
        "level": payload.level,
        "status": "draft",
        "created_at": state.now_iso(),
    }
    state.courses[course_id] = course
    return course


@router.get("/courses")
def get_courses(page: int = Query(default=1, ge=1), limit: int = Query(default=20, ge=1, le=100)):
    items = list(state.courses.values())
    start = (page - 1) * limit
    end = start + limit
    return {"items": items[start:end], "page": page, "limit": limit, "total": len(items)}


@router.get("/courses/{course_id}")
def get_course(course_id: str):
    course = state.courses.get(course_id)
    if not course:
        raise AppError("Course not found", code="COURSE_NOT_FOUND", status_code=404)
    return course


@router.put("/courses/{course_id}")
def update_course(course_id: str, payload: CourseUpdate):
    course = state.courses.get(course_id)
    if not course:
        raise AppError("Course not found", code="COURSE_NOT_FOUND", status_code=404)

    update_data = payload.model_dump(exclude_none=True)
    course.update(update_data)
    return course


@router.delete("/courses/{course_id}")
def delete_course(course_id: str):
    if course_id not in state.courses:
        raise AppError("Course not found", code="COURSE_NOT_FOUND", status_code=404)
    del state.courses[course_id]
    return {"deleted": True, "course_id": course_id}


@router.post("/courses/{course_id}/modules")
def create_module(course_id: str, payload: ModuleCreate):
    if course_id not in state.courses:
        raise AppError("Course not found", code="COURSE_NOT_FOUND", status_code=404)

    module_id = f"mod_{uuid.uuid4().hex[:8]}"
    module = {"id": module_id, "course_id": course_id, "title": payload.title}
    state.modules[module_id] = module
    return module


@router.post("/modules/{module_id}/lessons")
def create_lesson(module_id: str, payload: LessonCreate):
    if module_id not in state.modules:
        raise AppError("Module not found", code="MODULE_NOT_FOUND", status_code=404)

    lesson_id = f"lesson_{uuid.uuid4().hex[:8]}"
    lesson = {
        "id": lesson_id,
        "module_id": module_id,
        "title": payload.title,
        "type": payload.type,
        "content_url": payload.content_url,
        "content_text": payload.content_text,
        "duration_sec": payload.duration_sec,
    }
    state.lessons[lesson_id] = lesson
    return lesson
