import datetime
from typing import List

from pydantic import BaseModel

from domain.user.user_schema import User




class Weeklymemo(BaseModel):
    id: int
    sunday_date: datetime.date
    content: str
    user: User


class WeeklymemoCreate(BaseModel):
    sunday_date: datetime.date
    content: str


class WeeklymemoDelete(BaseModel):
    sunday_date: datetime.date

class WeeklymemoUpdate(BaseModel):
    sunday_date: datetime.date
    content: str