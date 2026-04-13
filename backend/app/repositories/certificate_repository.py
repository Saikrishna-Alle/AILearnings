import json
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.certificate import Certificate
from app.repositories.progress_repository import ProgressRepository


class CertificateRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.progress_repo = ProgressRepository(db)

    def generate(self, user_id: str, course_id: str) -> Certificate:
        course = self.progress_repo.get_course(course_id)
        if not course:
            raise ValueError("COURSE_NOT_FOUND")

        progress = self.progress_repo.course_progress(user_id=user_id, course_id=course_id)
        if int(progress["progress_percent"]) < 100:
            raise ValueError("COURSE_NOT_COMPLETED")

        preview = {
            "title": "Course Completion Certificate",
            "recipient": user_id,
            "course": course.title,
        }

        cert = Certificate(
            id=f"CERT-{uuid.uuid4().hex[:10].upper()}",
            user_id=user_id,
            course_id=course_id,
            status="generated",
            preview_json=json.dumps(preview),
        )
        self.db.add(cert)
        self.db.commit()
        self.db.refresh(cert)
        return cert

    def get_certificate(self, certificate_id: str) -> Certificate | None:
        return self.db.execute(select(Certificate).where(Certificate.id == certificate_id)).scalar_one_or_none()
