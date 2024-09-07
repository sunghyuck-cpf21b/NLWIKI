import datetime

from pydantic import BaseModel, field_validator
# pydantic은 FastAPI의 입출력 스펙을 정의하고 그 값을 검증하기 위해 사용된다.
from domain.comment.comment_schema import Comment
from domain.user.user_schema import User


'''
스키마는 출력 항목을 정의하고 타입을 지정한다.
'''

class Post(BaseModel):        # BaseModel : 입력된 데이터가 모델의 기대하는 형식과 일치하는지 확인할 수 있다.
    id: int                     # 스키마 타입에 따라 입력된 값의 속성을 정의 -> 베이스 모델로 모델의 타입과 일치하는지 검사?
    category: str
    subject: str
    content: str
    create_date: datetime.datetime

    person: str
    occ_date: datetime.datetime

    comments: list[Comment] = []
    user: User
    #content_info: str

    # 필수항목이 아니게 하기 위해서는
    # subject: str | None = None
    # 이렇게 하면 된다.
    # 타입이 필수가 아니라는 얘기?


class PostCreate(BaseModel):
    category: str
    subject: str
    content: str

    person: str
    occ_date: datetime.datetime
    #content_info: str


    @field_validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('내용을 작성하세요.')
        return v

class PostList(BaseModel):
    total: int = 0
    post_list: list[Post] = []


class PostDelete(BaseModel):
    post_id: int


class PostUpdate(PostCreate):
    post_id: int



