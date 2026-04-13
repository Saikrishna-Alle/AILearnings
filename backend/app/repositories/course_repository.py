import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models.course import Course, Lesson, Module
from app.schemas.course import CourseCreate, CourseUpdate, LessonCreate, ModuleCreate


class CourseRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_course(self, payload: CourseCreate) -> Course:
        course = Course(
            id=f"course_{uuid.uuid4().hex[:8]}",
            title=payload.title,
            description=payload.description,
            level=payload.level,
            status="draft",
        )
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course

    def get_course(self, course_id: str) -> Course | None:
        stmt = select(Course).where(Course.id == course_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def list_courses(self, page: int, limit: int) -> tuple[list[Course], int]:
        total = self.db.execute(select(func.count(Course.id))).scalar_one()
        offset = (page - 1) * limit
        stmt = select(Course).order_by(Course.created_at.desc()).offset(offset).limit(limit)
        items = self.db.execute(stmt).scalars().all()
        return items, total

    def update_course(self, course: Course, payload: CourseUpdate) -> Course:
        update_data = payload.model_dump(exclude_none=True)
        for key, value in update_data.items():
            setattr(course, key, value)
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course

    def delete_course(self, course: Course) -> None:
        self.db.delete(course)
        self.db.commit()

    def create_module(self, course_id: str, payload: ModuleCreate) -> Module:
        existing_count = self.db.execute(select(func.count(Module.id)).where(Module.course_id == course_id)).scalar_one()
        module = Module(
            id=f"mod_{uuid.uuid4().hex[:8]}",
            course_id=course_id,
            title=payload.title,
            position=existing_count + 1,
        )
        self.db.add(module)
        self.db.commit()
        self.db.refresh(module)
        return module

    def get_module(self, module_id: str) -> Module | None:
        stmt = select(Module).where(Module.id == module_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def create_lesson(self, module_id: str, payload: LessonCreate) -> Lesson:
        existing_count = self.db.execute(select(func.count(Lesson.id)).where(Lesson.module_id == module_id)).scalar_one()
        lesson = Lesson(
            id=f"lesson_{uuid.uuid4().hex[:8]}",
            module_id=module_id,
            title=payload.title,
            lesson_type=payload.type,
            content_url=payload.content_url,
            content_text=payload.content_text,
            duration_sec=payload.duration_sec,
            position=existing_count + 1,
        )
        self.db.add(lesson)
        self.db.commit()
        self.db.refresh(lesson)
        return lesson
