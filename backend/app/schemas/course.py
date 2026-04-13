from pydantic import BaseModel


class CourseCreate(BaseModel):
    title: str
    description: str
    level: str = "beginner"


class CourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    level: str | None = None


class CourseOut(BaseModel):
    id: str
    title: str
    description: str
    level: str
    status: str
    created_at: str


class ModuleCreate(BaseModel):
    title: str


class LessonCreate(BaseModel):
    title: str
    type: str
    content_url: str | None = None
    content_text: str | None = None
    duration_sec: int | None = None
