import uuid

from fastapi import APIRouter

from app.core.errors import AppError
from app.schemas.certificate import CertificateGenerate
from app.services import state

router = APIRouter()


@router.post("/certificates/generate")
def generate_certificate(payload: CertificateGenerate):
    if payload.course_id not in state.courses:
        raise AppError("Course not found", code="COURSE_NOT_FOUND", status_code=404)
    if (payload.user_id, payload.course_id) not in state.enrollments:
        raise AppError("User not enrolled in course", code="ENROLLMENT_NOT_FOUND", status_code=400)

    cert_id = f"CERT-{uuid.uuid4().hex[:10].upper()}"
    certificate = {
        "certificate_id": cert_id,
        "user_id": payload.user_id,
        "course_id": payload.course_id,
        "generated_at": state.now_iso(),
        "status": "generated",
        "preview": {
            "title": "Course Completion Certificate",
            "recipient": payload.user_id,
            "course": state.courses[payload.course_id]["title"],
        },
    }
    state.certificates[cert_id] = certificate
    return {
        "certificate_id": cert_id,
        "status": "generated",
        "preview": certificate["preview"],
    }


@router.get("/certificates/{certificate_id}/preview")
def certificate_preview(certificate_id: str):
    certificate = state.certificates.get(certificate_id)
    if not certificate:
        raise AppError("Certificate not found", code="CERT_NOT_FOUND", status_code=404)
    return certificate
