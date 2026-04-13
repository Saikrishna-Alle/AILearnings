from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.core.errors import AppError
from app.db.models.user import User
from app.repositories.dashboard_repository import DashboardRepository

router = APIRouter()


@router.get("/users/{user_id}/dashboard")
def get_dashboard(user_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role != "admin" and user.id != user_id:
        raise AppError("Forbidden", code="FORBIDDEN", status_code=403)
    repo = DashboardRepository(db)
    return repo.get_dashboard(user_id=user_id)
