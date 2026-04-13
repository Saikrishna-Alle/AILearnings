import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models.course import Course
from app.db.models.learning_path import LearningPath, LearningPathCourse
from app.db.models.progress import Enrollment
from app.schemas.learning_path import LearningPathCreate


class LearningPathRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_path(self, payload: LearningPathCreate) -> LearningPath:
        path = LearningPath(
            id=f"path_{uuid.uuid4().hex[:8]}",
            title=payload.title,
            role=payload.role,
            description=payload.description,
        )
        self.db.add(path)
        self.db.commit()
        self.db.refresh(path)
        return path

    def get_path(self, path_id: str) -> LearningPath | None:
        return self.db.execute(select(LearningPath).where(LearningPath.id == path_id)).scalar_one_or_none()

    def get_course(self, course_id: str) -> Course | None:
        return self.db.execute(select(Course).where(Course.id == course_id)).scalar_one_or_none()

    def list_course_ids(self, path_id: str) -> list[str]:
        rows = self.db.execute(
            select(LearningPathCourse.course_id)
            .where(LearningPathCourse.path_id == path_id)
            .order_by(LearningPathCourse.position.asc())
        ).all()
        return [row[0] for row in rows]

    def map_course(self, path_id: str, course_id: str) -> None:
        existing = self.db.execute(
            select(LearningPathCourse).where(
                LearningPathCourse.path_id == path_id,
                LearningPathCourse.course_id == course_id,
            )
        ).scalar_one_or_none()
        if existing:
            return

        count = self.db.execute(
            select(func.count(LearningPathCourse.id)).where(LearningPathCourse.path_id == path_id)
        ).scalar_one()

        mapping = LearningPathCourse(
            id=f"lpc_{uuid.uuid4().hex[:8]}",
            path_id=path_id,
            course_id=course_id,
            position=count + 1,
        )
        self.db.add(mapping)
        self.db.commit()

    def path_progress(self, user_id: str, path_id: str) -> dict[str, int | str]:
        course_ids = self.list_course_ids(path_id)
        total = len(course_ids)
        if total == 0:
            return {
                "path_id": path_id,
                "completed_courses": 0,
                "total_courses": 0,
                "completion_percent": 0,
            }

        enrolled_count = self.db.execute(
            select(func.count(Enrollment.id)).where(
                Enrollment.user_id == user_id,
                Enrollment.course_id.in_(course_ids),
            )
        ).scalar_one()
        completion_percent = int((enrolled_count / total) * 100)
        return {
            "path_id": path_id,
            "completed_courses": enrolled_count,
            "total_courses": total,
            "completion_percent": completion_percent,
        }

    def next_course(self, user_id: str, path_id: str) -> str | None:
        for course_id in self.list_course_ids(path_id):
            enrolled = self.db.execute(
                select(Enrollment.id).where(
                    Enrollment.user_id == user_id,
                    Enrollment.course_id == course_id,
                )
            ).scalar_one_or_none()
            if not enrolled:
                return course_id
        return None
