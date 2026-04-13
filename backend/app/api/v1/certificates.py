from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.core.errors import AppError
from app.db.models.user import User
from app.repositories.certificate_repository import CertificateRepository
from app.schemas.certificate import CertificateGenerate

router = APIRouter()


@router.post("/certificates/generate")
def generate_certificate(payload: CertificateGenerate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    repo = CertificateRepository(db)

    try:
        certificate = repo.generate(user_id=user.id, course_id=payload.course_id)
    except ValueError as exc:
        if str(exc) == "COURSE_NOT_FOUND":
            raise AppError("Course not found", code="COURSE_NOT_FOUND", status_code=404) from exc
        if str(exc) == "COURSE_NOT_COMPLETED":
            raise AppError("Course completion validation failed", code="COURSE_NOT_COMPLETED", status_code=400) from exc
        raise

    return {
        "certificate_id": certificate.id,
        "status": certificate.status,
        "preview": certificate.preview(),
    }


@router.get("/certificates/{certificate_id}/preview")
def certificate_preview(certificate_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    repo = CertificateRepository(db)
    certificate = repo.get_certificate(certificate_id)
    if not certificate:
        raise AppError("Certificate not found", code="CERT_NOT_FOUND", status_code=404)
    if user.role != "admin" and certificate.user_id != user.id:
        raise AppError("Forbidden", code="FORBIDDEN", status_code=403)

    return {
        "certificate_id": certificate.id,
        "user_id": certificate.user_id,
        "course_id": certificate.course_id,
        "generated_at": certificate.generated_at.isoformat() + "Z",
        "status": certificate.status,
        "preview": certificate.preview(),
    }
