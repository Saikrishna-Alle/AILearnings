from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.errors import AppError
from app.repositories.assessment_repository import AssessmentRepository
from app.repositories.dashboard_repository import AdminRepository
from app.repositories.progress_repository import ProgressRepository

router = APIRouter()


@router.get("/admin/users/{user_id}/progress")
def admin_user_progress(user_id: str, db: Session = Depends(get_db)):
    repo = AdminRepository(db)
    return repo.user_progress(user_id=user_id)


@router.post("/admin/courses/{course_id}/assessments")
def create_assessment(course_id: str, title: str, db: Session = Depends(get_db)):
    progress_repo = ProgressRepository(db)
    course = progress_repo.get_course(course_id)
    if not course:
        raise AppError("Course not found", code="COURSE_NOT_FOUND", status_code=404)

    repo = AssessmentRepository(db)
    assessment = repo.create_assessment(course_id=course_id, title=title)
    return {
        "id": assessment.id,
        "course_id": assessment.course_id,
        "title": assessment.title,
    }
