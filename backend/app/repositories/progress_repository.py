import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models.course import Course, Lesson, Module
from app.db.models.progress import Enrollment, LessonCompletion


class ProgressRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_course(self, course_id: str) -> Course | None:
        return self.db.execute(select(Course).where(Course.id == course_id)).scalar_one_or_none()

    def get_lesson(self, lesson_id: str) -> Lesson | None:
        return self.db.execute(select(Lesson).where(Lesson.id == lesson_id)).scalar_one_or_none()

    def enroll(self, user_id: str, course_id: str) -> Enrollment:
        stmt = select(Enrollment).where(Enrollment.user_id == user_id, Enrollment.course_id == course_id)
        enrollment = self.db.execute(stmt).scalar_one_or_none()
        if enrollment:
            return enrollment

        enrollment = Enrollment(id=f"enr_{uuid.uuid4().hex[:8]}", user_id=user_id, course_id=course_id)
        self.db.add(enrollment)
        self.db.commit()
        self.db.refresh(enrollment)
        return enrollment

    def complete_lesson(self, user_id: str, lesson_id: str) -> LessonCompletion:
        stmt = select(LessonCompletion).where(LessonCompletion.user_id == user_id, LessonCompletion.lesson_id == lesson_id)
        completion = self.db.execute(stmt).scalar_one_or_none()
        if completion:
            return completion

        completion = LessonCompletion(id=f"cmp_{uuid.uuid4().hex[:8]}", user_id=user_id, lesson_id=lesson_id)
        self.db.add(completion)
        self.db.commit()
        self.db.refresh(completion)
        return completion

    def course_progress(self, user_id: str, course_id: str) -> dict[str, int | str | None]:
        module_ids_stmt = select(Module.id).where(Module.course_id == course_id)
        module_ids = [row[0] for row in self.db.execute(module_ids_stmt).all()]
        if not module_ids:
            return {
                "progress_percent": 0,
                "completed_lessons": 0,
                "total_lessons": 0,
                "last_lesson_id": None,
            }

        lesson_ids_stmt = select(Lesson.id).where(Lesson.module_id.in_(module_ids))
        lesson_ids = [row[0] for row in self.db.execute(lesson_ids_stmt).all()]
        if not lesson_ids:
            return {
                "progress_percent": 0,
                "completed_lessons": 0,
                "total_lessons": 0,
                "last_lesson_id": None,
            }

        completion_count_stmt = select(func.count(LessonCompletion.id)).where(
            LessonCompletion.user_id == user_id,
            LessonCompletion.lesson_id.in_(lesson_ids),
        )
        completed_lessons = self.db.execute(completion_count_stmt).scalar_one()

        last_completion_stmt = (
            select(LessonCompletion.lesson_id)
            .where(
                LessonCompletion.user_id == user_id,
                LessonCompletion.lesson_id.in_(lesson_ids),
            )
            .order_by(LessonCompletion.completed_at.desc())
            .limit(1)
        )
        last_lesson_id = self.db.execute(last_completion_stmt).scalar_one_or_none()

        total_lessons = len(lesson_ids)
        progress_percent = int((completed_lessons / total_lessons) * 100) if total_lessons else 0

        return {
            "progress_percent": progress_percent,
            "completed_lessons": completed_lessons,
            "total_lessons": total_lessons,
            "last_lesson_id": last_lesson_id,
        }
