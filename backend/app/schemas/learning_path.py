from pydantic import BaseModel


class LearningPathCreate(BaseModel):
    title: str
    role: str
    description: str | None = None


class MapCourseToPath(BaseModel):
    course_id: str
