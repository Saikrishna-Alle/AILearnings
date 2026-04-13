from pydantic import BaseModel


class PostCreate(BaseModel):
    user_id: str
    content: str


class CommentCreate(BaseModel):
    user_id: str
    content: str
