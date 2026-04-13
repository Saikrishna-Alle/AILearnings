from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.repositories.dashboard_repository import DashboardRepository

router = APIRouter()


@router.get("/users/{user_id}/dashboard")
def get_dashboard(user_id: str, db: Session = Depends(get_db)):
    repo = DashboardRepository(db)
    return repo.get_dashboard(user_id=user_id)
