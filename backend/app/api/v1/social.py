import uuid

from fastapi import APIRouter

from app.core.errors import AppError
from app.schemas.social import CommentCreate, PostCreate
from app.services import state

router = APIRouter()


@router.post("/posts")
def create_post(payload: PostCreate):
    post_id = f"post_{uuid.uuid4().hex[:8]}"
    post = {
        "id": post_id,
        "user_id": payload.user_id,
        "content": payload.content,
        "created_at": state.now_iso(),
    }
    state.posts[post_id] = post
    return post


@router.get("/feed")
def get_feed():
    items = []
    for post_id, post in state.posts.items():
        like_count = len([1 for x in state.likes if x[0] == post_id])
        comment_count = len([1 for c in state.comments.values() if c["post_id"] == post_id])
        items.append({**post, "like_count": like_count, "comment_count": comment_count})

    items.sort(key=lambda p: p["created_at"], reverse=True)
    return {"items": items}


@router.post("/posts/{post_id}/like")
def like_post(post_id: str, user_id: str):
    if post_id not in state.posts:
        raise AppError("Post not found", code="POST_NOT_FOUND", status_code=404)

    state.likes.add((post_id, user_id))
    return {"liked": True, "post_id": post_id, "user_id": user_id}


@router.post("/posts/{post_id}/comments")
def comment_post(post_id: str, payload: CommentCreate):
    if post_id not in state.posts:
        raise AppError("Post not found", code="POST_NOT_FOUND", status_code=404)

    comment_id = f"com_{uuid.uuid4().hex[:8]}"
    comment = {
        "id": comment_id,
        "post_id": post_id,
        "user_id": payload.user_id,
        "content": payload.content,
        "created_at": state.now_iso(),
    }
    state.comments[comment_id] = comment
    return comment
