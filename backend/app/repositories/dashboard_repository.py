from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models.assessment import AssessmentAttempt
from app.db.models.progress import Enrollment, LessonCompletion
from app.db.models.social import Post
from app.db.models.user import User
from app.repositories.progress_repository import ProgressRepository


class DashboardRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.progress_repo = ProgressRepository(db)

    def get_dashboard(self, user_id: str) -> dict:
        enrolled_course_ids = [
            row[0]
            for row in self.db.execute(select(Enrollment.course_id).where(Enrollment.user_id == user_id)).all()
        ]

        progress_values = []
        for course_id in enrolled_course_ids:
            progress = self.progress_repo.course_progress(user_id=user_id, course_id=course_id)
            progress_values.append(int(progress["progress_percent"]))

        avg_progress = int(sum(progress_values) / len(progress_values)) if progress_values else 0

        attempts = self.db.execute(
            select(AssessmentAttempt)
            .where(AssessmentAttempt.user_id == user_id, AssessmentAttempt.status == "evaluated")
            .order_by(AssessmentAttempt.created_at.desc())
            .limit(5)
        ).scalars().all()

        post_count = self.db.execute(select(func.count(Post.id))).scalar_one()

        recent_scores = [
            {"attempt_id": a.id, "score": a.score, "max_score": a.max_score}
            for a in attempts
        ]

        return {
            "enrolled_courses": len(enrolled_course_ids),
            "avg_progress_percent": avg_progress,
            "recent_activity": [
                {"type": "enrollments", "count": len(enrolled_course_ids)},
                {"type": "posts", "count": post_count},
            ],
            "recent_scores": recent_scores,
        }


class AdminRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def user_progress(self, user_id: str) -> dict:
        enrolled = [
            row[0]
            for row in self.db.execute(select(Enrollment.course_id).where(Enrollment.user_id == user_id)).all()
        ]
        completed_lessons = self.db.execute(
            select(func.count(LessonCompletion.id)).where(LessonCompletion.user_id == user_id)
        ).scalar_one()

        return {
            "user_id": user_id,
            "enrolled_courses": enrolled,
            "completed_lessons": completed_lessons,
        }

    def list_user_progress(self, page: int, limit: int, role: str | None = None) -> dict:
        base = select(User)
        if role:
            base = base.where(User.role == role)

        total_stmt = select(func.count()).select_from(base.subquery())
        total = self.db.execute(total_stmt).scalar_one()

        offset = (page - 1) * limit
        users = self.db.execute(base.order_by(User.created_at.desc()).offset(offset).limit(limit)).scalars().all()

        items = []
        for user in users:
            progress = self.user_progress(user.id)
            items.append(
                {
                    "user_id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                    "enrolled_courses": progress["enrolled_courses"],
                    "completed_lessons": progress["completed_lessons"],
                }
            )

        return {"items": items, "page": page, "limit": limit, "total": total}
