import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Callable, Generator

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.db.models.user import AuthToken, User
from app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def get_current_user(authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise AppError("Missing or invalid Authorization header", code="AUTH_REQUIRED", status_code=401)

    token = authorization.split(" ", 1)[1].strip()
    token_hash = _hash_token(token)

    session = db.query(AuthToken).filter(AuthToken.token_hash == token_hash).first()
    if not session:
        raise AppError("Invalid token", code="INVALID_TOKEN", status_code=401)
    if session.expires_at < datetime.utcnow():
        raise AppError("Token expired", code="TOKEN_EXPIRED", status_code=401)

    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise AppError("User not found", code="USER_NOT_FOUND", status_code=401)

    return user


def require_role(required: str) -> Callable:
    def _checker(user: User = Depends(get_current_user)) -> User:
        if user.role != required:
            raise AppError("Forbidden", code="FORBIDDEN", status_code=403)
        return user

    return _checker


def create_auth_token(user_id: str) -> tuple[str, str, datetime]:
    raw = secrets.token_urlsafe(32)
    token_hash = _hash_token(raw)
    expires_at = datetime.utcnow() + timedelta(days=7)
    return raw, token_hash, expires_at

