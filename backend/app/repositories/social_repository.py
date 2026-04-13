import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models.social import Post, PostComment, PostLike
from app.schemas.social import CommentCreate, PostCreate


class SocialRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_post(self, payload: PostCreate) -> Post:
        post = Post(
            id=f"post_{uuid.uuid4().hex[:8]}",
            user_id=payload.user_id,
            content=payload.content,
        )
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def get_post(self, post_id: str) -> Post | None:
        return self.db.execute(select(Post).where(Post.id == post_id)).scalar_one_or_none()

    def like_post(self, post_id: str, user_id: str) -> None:
        existing = self.db.execute(
            select(PostLike).where(PostLike.post_id == post_id, PostLike.user_id == user_id)
        ).scalar_one_or_none()
        if existing:
            return

        like = PostLike(id=f"plk_{uuid.uuid4().hex[:8]}", post_id=post_id, user_id=user_id)
        self.db.add(like)
        self.db.commit()

    def comment_post(self, post_id: str, payload: CommentCreate) -> PostComment:
        comment = PostComment(
            id=f"com_{uuid.uuid4().hex[:8]}",
            post_id=post_id,
            user_id=payload.user_id,
            content=payload.content,
        )
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def feed(self) -> dict:
        posts = self.db.execute(select(Post).order_by(Post.created_at.desc())).scalars().all()
        items = []
        for post in posts:
            like_count = self.db.execute(
                select(func.count(PostLike.id)).where(PostLike.post_id == post.id)
            ).scalar_one()
            comment_count = self.db.execute(
                select(func.count(PostComment.id)).where(PostComment.post_id == post.id)
            ).scalar_one()
            items.append(
                {
                    "id": post.id,
                    "user_id": post.user_id,
                    "content": post.content,
                    "created_at": post.created_at.isoformat() + "Z",
                    "like_count": like_count,
                    "comment_count": comment_count,
                }
            )

        return {"items": items}
