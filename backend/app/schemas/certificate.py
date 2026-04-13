from pydantic import BaseModel


class CertificateGenerate(BaseModel):
    course_id: str
