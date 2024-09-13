import datetime

from pydantic import BaseModel, field_validator
from domain.user.user_schema import User

class Comment(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    post_id: int

    subcomments: list['SubComment'] = [] # 문자열로 지정하면 파이썬이 해당 타입을 나중에 평가하게 만들어 순서로 인한 오류를 피할 수 있다
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


''' 대댓글 '''
class SubComment(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    comment_id: int
    user: User


class SubCommentCreate(BaseModel):
    content: str
    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('내용을 작성해야 합니다.')
        return v

class SubCommentUpdate(SubCommentCreate):
    data_id: int

class SubCommentDelete(BaseModel):
    data_id: int


''' post_list 를 위한 스키마 '''
class SubCommentForPL(BaseModel):
    id: int
class CommentForPL(BaseModel): # comment for post list
    subcomments: list[SubCommentForPL]


