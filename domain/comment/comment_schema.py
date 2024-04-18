import datetime

from pydantic import BaseModel, field_validator
from domain.user.user_schema import User

class Comment(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    nonlan_id: int
    user: User


class CommentCreate(BaseModel):
    content: str

    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('내용을 작성해야 합니다.')
        return v

class CommentUpdate(CommentCreate):
    comment_id: int


class CommentDelete(BaseModel):
    comment_id: int
