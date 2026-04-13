from pydantic import BaseModel


class CertificateGenerate(BaseModel):
    user_id: str
    course_id: str
