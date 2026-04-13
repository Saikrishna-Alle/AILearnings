from fastapi import FastAPI

from app.api.v1 import admin, assessments, certificates, courses, dashboard, learning_paths, progress, social
from app.core.errors import register_exception_handlers

app = FastAPI(title="AI Skill Platform API", version="0.1.0")

register_exception_handlers(app)

app.include_router(courses.router, prefix="/api/v1", tags=["Courses"])
app.include_router(progress.router, prefix="/api/v1", tags=["Progress"])
app.include_router(learning_paths.router, prefix="/api/v1", tags=["Learning Paths"])
app.include_router(assessments.router, prefix="/api/v1", tags=["Assessments"])
app.include_router(certificates.router, prefix="/api/v1", tags=["Certificates"])
app.include_router(dashboard.router, prefix="/api/v1", tags=["Dashboard"])
app.include_router(social.router, prefix="/api/v1", tags=["Social"])
app.include_router(admin.router, prefix="/api/v1", tags=["Admin"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
