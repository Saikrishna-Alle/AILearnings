from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.core.errors import AppError
from app.db.models.user import User
from app.repositories.social_repository import SocialRepository
from app.schemas.social import CommentCreate, PostCreate

router = APIRouter()


@router.post("/posts")
def create_post(payload: PostCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    repo = SocialRepository(db)
    post = repo.create_post(user_id=user.id, content=payload.content)
    return {
        "id": post.id,
        "user_id": post.user_id,
        "content": post.content,
        "created_at": post.created_at.isoformat() + "Z",
    }


@router.get("/feed")
def get_feed(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    user_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    repo = SocialRepository(db)
    return repo.feed(page=page, limit=limit, user_id=user_id)


@router.post("/posts/{post_id}/like")
def like_post(post_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    repo = SocialRepository(db)
    post = repo.get_post(post_id)
    if not post:
        raise AppError("Post not found", code="POST_NOT_FOUND", status_code=404)

    repo.like_post(post_id=post_id, user_id=user.id)
    return {"liked": True, "post_id": post_id, "user_id": user.id}


@router.post("/posts/{post_id}/comments")
def comment_post(post_id: str, payload: CommentCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    repo = SocialRepository(db)
    post = repo.get_post(post_id)
    if not post:
        raise AppError("Post not found", code="POST_NOT_FOUND", status_code=404)

    comment = repo.comment_post(post_id=post_id, user_id=user.id, payload=payload)
    return {
        "id": comment.id,
        "post_id": comment.post_id,
        "user_id": comment.user_id,
        "content": comment.content,
        "created_at": comment.created_at.isoformat() + "Z",
    }
