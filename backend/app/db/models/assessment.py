from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    course_id: Mapped[str] = mapped_column(String(32), ForeignKey("courses.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    assessment_id: Mapped[str] = mapped_column(String(32), ForeignKey("assessments.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[str] = mapped_column(String(64), index=True)
    status: Mapped[str] = mapped_column(String(32), default="in_progress")
    score: Mapped[int] = mapped_column(Integer, default=0)
    max_score: Mapped[int] = mapped_column(Integer, default=0)
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
