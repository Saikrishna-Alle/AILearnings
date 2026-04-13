from pydantic import BaseModel


class AssessmentStart(BaseModel):
    user_id: str | None = None


class AnswerItem(BaseModel):
    question_id: str
    answer: str


class AssessmentSubmit(BaseModel):
    answers: list[AnswerItem]
