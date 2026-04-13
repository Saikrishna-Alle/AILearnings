import hashlib
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import create_auth_token
from app.db.models.user import AuthToken, User
from app.schemas.auth import LoginRequest


class AuthRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.execute(select(User).where(User.email == email)).scalar_one_or_none()

    def authenticate(self, payload: LoginRequest) -> User | None:
        user = self.get_user_by_email(payload.email)
        if not user or not user.is_active:
            return None
        if user.password_hash != self.hash_password(payload.password):
            return None
        return user

    def issue_token(self, user_id: str) -> tuple[str, AuthToken]:
        raw_token, token_hash, expires_at = create_auth_token(user_id)
        row = AuthToken(
            id=f"tok_{uuid.uuid4().hex[:8]}",
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return raw_token, row
