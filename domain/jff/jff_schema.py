import datetime

from pydantic import BaseModel, field_validator
from domain.user.user_schema import User

# DP : DotPaint
class DP(BaseModel):
    id: int
    x: int
    y: int
    color: str
    user: User

class DPCreate(BaseModel):
    x: int
    y: int
    color: str
# DP는 update 없이 계속 새로운 데이터로 만들어짐



