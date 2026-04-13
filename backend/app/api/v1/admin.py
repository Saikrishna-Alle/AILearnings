from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db, require_role
from app.core.errors import AppError
from app.db.models.user import User
from app.repositories.assessment_repository import AssessmentRepository
from app.repositories.dashboard_repository import AdminRepository
from app.repositories.progress_repository import ProgressRepository

router = APIRouter()


@router.get("/admin/users/{user_id}/progress")
def admin_user_progress(user_id: str, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    repo = AdminRepository(db)
    return repo.user_progress(user_id=user_id)


@router.get("/admin/users/progress")
def admin_users_progress(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    role: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin")),
):
    repo = AdminRepository(db)
    return repo.list_user_progress(page=page, limit=limit, role=role)


@router.post("/admin/courses/{course_id}/assessments")
def create_assessment(course_id: str, title: str, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
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
