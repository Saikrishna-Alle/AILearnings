from pydantic import BaseModel


class ProgressOut(BaseModel):
    progress_percent: int
    completed_lessons: int
    total_lessons: int
    last_lesson_id: str | None
