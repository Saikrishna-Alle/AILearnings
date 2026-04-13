from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_user_id
from app.core.errors import AppError
from app.repositories.assessment_repository import AssessmentRepository
from app.schemas.assessment import AssessmentSubmit

router = APIRouter()


@router.post("/assessments/{assessment_id}/start")
def start_assessment(assessment_id: str, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    repo = AssessmentRepository(db)
    assessment = repo.get_assessment(assessment_id)
    if not assessment:
        raise AppError("Assessment not found", code="ASSESSMENT_NOT_FOUND", status_code=404)

    attempt = repo.start_attempt(assessment_id=assessment_id, user_id=user_id)
    return {
        "attempt_id": attempt.id,
        "assessment_id": attempt.assessment_id,
        "status": attempt.status,
        "answers": [],
    }


@router.post("/assessments/{attempt_id}/submit")
def submit_assessment(attempt_id: str, payload: AssessmentSubmit, db: Session = Depends(get_db)):
    repo = AssessmentRepository(db)
    attempt = repo.get_attempt(attempt_id)
    if not attempt:
        raise AppError("Attempt not found", code="ATTEMPT_NOT_FOUND", status_code=404)

    saved_attempt, feedback = repo.submit_attempt(attempt, payload)

    return {
        "attempt_id": saved_attempt.id,
        "score": saved_attempt.score,
        "max_score": saved_attempt.max_score,
        "status": saved_attempt.status,
        "feedback": feedback,
    }
