import uuid

from fastapi import APIRouter

from app.core.errors import AppError
from app.schemas.assessment import AssessmentSubmit
from app.services import state

router = APIRouter()


@router.post("/assessments/{assessment_id}/start")
def start_assessment(assessment_id: str):
    attempt_id = f"att_{uuid.uuid4().hex[:8]}"
    state.attempts[attempt_id] = {
        "attempt_id": attempt_id,
        "assessment_id": assessment_id,
        "status": "in_progress",
        "answers": [],
    }
    return state.attempts[attempt_id]


@router.post("/assessments/{attempt_id}/submit")
def submit_assessment(attempt_id: str, payload: AssessmentSubmit):
    attempt = state.attempts.get(attempt_id)
    if not attempt:
        raise AppError("Attempt not found", code="ATTEMPT_NOT_FOUND", status_code=404)

    answers = [a.model_dump() for a in payload.answers]
    score = 0
    for answer in answers:
        value = answer["answer"].strip().lower()
        if value in {"a", "b", "c", "d"}:
            score += 10
        elif len(value) > 20:
            score += 8
        else:
            score += 4

    max_score = max(len(answers) * 10, 10)
    attempt.update(
        {
            "status": "evaluated",
            "answers": answers,
            "score": min(score, max_score),
            "max_score": max_score,
        }
    )

    return {
        "attempt_id": attempt_id,
        "score": attempt["score"],
        "max_score": attempt["max_score"],
        "status": attempt["status"],
        "feedback": [{"question_id": a["question_id"], "comment": "Phase 1 rule-based feedback."} for a in answers],
    }
