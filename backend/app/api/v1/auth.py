from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.core.errors import AppError
from app.repositories.auth_repository import AuthRepository
from app.schemas.auth import LoginRequest

router = APIRouter()


@router.post("/auth/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    repo = AuthRepository(db)
    user = repo.authenticate(payload)
    if not user:
        raise AppError("Invalid email or password", code="INVALID_CREDENTIALS", status_code=401)

    access_token, token_row = repo.issue_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_at": token_row.expires_at.isoformat() + "Z",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        },
    }


@router.get("/auth/me")
def me(user=Depends(get_current_user)):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
    }
