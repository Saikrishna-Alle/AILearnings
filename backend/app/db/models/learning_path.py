from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class LearningPath(Base):
    __tablename__ = "learning_paths"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    role: Mapped[str] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)


class LearningPathCourse(Base):
    __tablename__ = "learning_path_courses"
    __table_args__ = (UniqueConstraint("path_id", "course_id", name="uq_path_course"),)

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    path_id: Mapped[str] = mapped_column(String(32), ForeignKey("learning_paths.id", ondelete="CASCADE"), index=True)
    course_id: Mapped[str] = mapped_column(String(32), ForeignKey("courses.id", ondelete="CASCADE"), index=True)
    position: Mapped[int] = mapped_column(Integer, default=0)
