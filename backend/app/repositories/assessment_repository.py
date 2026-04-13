import json
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.assessment import Assessment, AssessmentAttempt
from app.schemas.assessment import AssessmentSubmit


class AssessmentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_assessment(self, course_id: str, title: str) -> Assessment:
        assessment = Assessment(
            id=f"asm_{uuid.uuid4().hex[:8]}",
            course_id=course_id,
            title=title,
        )
        self.db.add(assessment)
        self.db.commit()
        self.db.refresh(assessment)
        return assessment

    def get_assessment(self, assessment_id: str) -> Assessment | None:
        return self.db.execute(select(Assessment).where(Assessment.id == assessment_id)).scalar_one_or_none()

    def start_attempt(self, assessment_id: str, user_id: str) -> AssessmentAttempt:
        attempt = AssessmentAttempt(
            id=f"att_{uuid.uuid4().hex[:8]}",
            assessment_id=assessment_id,
            user_id=user_id,
            status="in_progress",
            score=0,
            max_score=0,
        )
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)
        return attempt

    def get_attempt(self, attempt_id: str) -> AssessmentAttempt | None:
        return self.db.execute(select(AssessmentAttempt).where(AssessmentAttempt.id == attempt_id)).scalar_one_or_none()

    def submit_attempt(self, attempt: AssessmentAttempt, payload: AssessmentSubmit) -> tuple[AssessmentAttempt, list[dict[str, str]]]:
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
        attempt.status = "evaluated"
        attempt.score = min(score, max_score)
        attempt.max_score = max_score
        attempt.feedback = json.dumps(
            [{"question_id": a["question_id"], "comment": "Phase 1 rule-based feedback."} for a in answers]
        )
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)
        feedback = json.loads(attempt.feedback) if attempt.feedback else []
        return attempt, feedback
