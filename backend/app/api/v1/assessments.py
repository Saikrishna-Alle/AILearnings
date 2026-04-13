from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.core.errors import AppError
from app.db.models.user import User
from app.repositories.assessment_repository import AssessmentRepository
from app.schemas.assessment import AssessmentSubmit

router = APIRouter()


@router.post("/assessments/{assessment_id}/start")
def start_assessment(assessment_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    repo = AssessmentRepository(db)
    assessment = repo.get_assessment(assessment_id)
    if not assessment:
        raise AppError("Assessment not found", code="ASSESSMENT_NOT_FOUND", status_code=404)

    attempt = repo.start_attempt(assessment_id=assessment_id, user_id=user.id)
    return {
        "attempt_id": attempt.id,
        "assessment_id": attempt.assessment_id,
        "status": attempt.status,
        "answers": [],
    }


@router.post("/assessments/{attempt_id}/submit")
def submit_assessment(attempt_id: str, payload: AssessmentSubmit, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    repo = AssessmentRepository(db)
    attempt = repo.get_attempt(attempt_id)
    if not attempt:
        raise AppError("Attempt not found", code="ATTEMPT_NOT_FOUND", status_code=404)
    if user.role != "admin" and attempt.user_id != user.id:
        raise AppError("Forbidden", code="FORBIDDEN", status_code=403)

    saved_attempt, feedback = repo.submit_attempt(attempt, payload)

    return {
        "attempt_id": saved_attempt.id,
        "score": saved_attempt.score,
        "max_score": saved_attempt.max_score,
        "status": saved_attempt.status,
        "feedback": feedback,
    }
