from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_user_id
from app.core.errors import AppError
from app.repositories.progress_repository import ProgressRepository

router = APIRouter()


@router.post("/courses/{course_id}/enroll")
def enroll_in_course(course_id: str, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    repo = ProgressRepository(db)
    course = repo.get_course(course_id)
    if not course:
        raise AppError("Course not found", code="COURSE_NOT_FOUND", status_code=404)

    repo.enroll(user_id=user_id, course_id=course_id)
    return {"enrolled": True, "user_id": user_id, "course_id": course_id}


@router.post("/lessons/{lesson_id}/complete")
def mark_lesson_complete(lesson_id: str, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    repo = ProgressRepository(db)
    lesson = repo.get_lesson(lesson_id)
    if not lesson:
        raise AppError("Lesson not found", code="LESSON_NOT_FOUND", status_code=404)

    repo.complete_lesson(user_id=user_id, lesson_id=lesson_id)
    return {"completed": True, "user_id": user_id, "lesson_id": lesson_id}


@router.get("/users/{user_id}/courses/{course_id}/progress")
def course_progress(user_id: str, course_id: str, db: Session = Depends(get_db)):
    repo = ProgressRepository(db)
    course = repo.get_course(course_id)
    if not course:
        raise AppError("Course not found", code="COURSE_NOT_FOUND", status_code=404)

    return repo.course_progress(user_id=user_id, course_id=course_id)


@router.get("/users/{user_id}/courses/{course_id}/resume")
def resume_course(user_id: str, course_id: str, db: Session = Depends(get_db)):
    progress = course_progress(user_id, course_id, db)
    return {
        "course_id": course_id,
        "resume_lesson_id": progress["last_lesson_id"],
    }
