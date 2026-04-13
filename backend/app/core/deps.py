from typing import Generator

from fastapi import Header
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

DUMMY_USER_ID = "demo_user_1"


def get_user_id(x_user_id: str | None = Header(default=None)) -> str:
    return x_user_id or DUMMY_USER_ID


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
