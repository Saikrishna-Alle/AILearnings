from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    level: Mapped[str] = mapped_column(String(32), default="beginner")
    status: Mapped[str] = mapped_column(String(32), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Module(Base):
    __tablename__ = "modules"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    course_id: Mapped[str] = mapped_column(String(32), ForeignKey("courses.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    position: Mapped[int] = mapped_column(Integer, default=0)


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    module_id: Mapped[str] = mapped_column(String(32), ForeignKey("modules.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    lesson_type: Mapped[str] = mapped_column(String(32))
    content_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_sec: Mapped[int | None] = mapped_column(Integer, nullable=True)
    position: Mapped[int] = mapped_column(Integer, default=0)
