from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), index=True)
    course_id: Mapped[str] = mapped_column(String(32), ForeignKey("courses.id", ondelete="CASCADE"), index=True)
    enrolled_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class LessonCompletion(Base):
    __tablename__ = "lesson_completion"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), index=True)
    lesson_id: Mapped[str] = mapped_column(String(32), ForeignKey("lessons.id", ondelete="CASCADE"), index=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
