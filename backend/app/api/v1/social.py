from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.errors import AppError
from app.repositories.social_repository import SocialRepository
from app.schemas.social import CommentCreate, PostCreate

router = APIRouter()


@router.post("/posts")
def create_post(payload: PostCreate, db: Session = Depends(get_db)):
    repo = SocialRepository(db)
    post = repo.create_post(payload)
    return {
        "id": post.id,
        "user_id": post.user_id,
        "content": post.content,
        "created_at": post.created_at.isoformat() + "Z",
    }


@router.get("/feed")
def get_feed(db: Session = Depends(get_db)):
    repo = SocialRepository(db)
    return repo.feed()


@router.post("/posts/{post_id}/like")
def like_post(post_id: str, user_id: str, db: Session = Depends(get_db)):
    repo = SocialRepository(db)
    post = repo.get_post(post_id)
    if not post:
        raise AppError("Post not found", code="POST_NOT_FOUND", status_code=404)

    repo.like_post(post_id=post_id, user_id=user_id)
    return {"liked": True, "post_id": post_id, "user_id": user_id}


@router.post("/posts/{post_id}/comments")
def comment_post(post_id: str, payload: CommentCreate, db: Session = Depends(get_db)):
    repo = SocialRepository(db)
    post = repo.get_post(post_id)
    if not post:
        raise AppError("Post not found", code="POST_NOT_FOUND", status_code=404)

    comment = repo.comment_post(post_id=post_id, payload=payload)
    return {
        "id": comment.id,
        "post_id": comment.post_id,
        "user_id": comment.user_id,
        "content": comment.content,
        "created_at": comment.created_at.isoformat() + "Z",
    }
