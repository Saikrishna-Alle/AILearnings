import hashlib

from app.db.models.user import User
from app.db.session import SessionLocal


ADMIN_ID = "usr_admin_001"
STUDENT_ID = "usr_student_001"
ADMIN_EMAIL = "admin@ail.dev"
STUDENT_EMAIL = "student@ail.dev"
ADMIN_HASH = hashlib.sha256("admin123".encode("utf-8")).hexdigest()
STUDENT_HASH = hashlib.sha256("student123".encode("utf-8")).hexdigest()


def ensure_seed_users() -> None:
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.id == ADMIN_ID).first()
        if not admin:
            admin = db.query(User).filter(User.email.in_(["admin@ail.local", ADMIN_EMAIL])).first()
        if not admin:
            admin = User(id=ADMIN_ID)
            db.add(admin)

        admin.name = "Admin User"
        admin.email = ADMIN_EMAIL
        admin.password_hash = ADMIN_HASH
        admin.role = "admin"
        admin.is_active = True

        student = db.query(User).filter(User.id == STUDENT_ID).first()
        if not student:
            student = db.query(User).filter(User.email.in_(["student@ail.local", STUDENT_EMAIL])).first()
        if not student:
            student = User(id=STUDENT_ID)
            db.add(student)

        student.name = "Demo Student"
        student.email = STUDENT_EMAIL
        student.password_hash = STUDENT_HASH
        student.role = "student"
        student.is_active = True

        db.commit()
    finally:
        db.close()
