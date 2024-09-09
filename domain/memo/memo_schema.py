import datetime
from typing import List

from pydantic import BaseModel

from domain.user.user_schema import User



''' 주간 메모 '''
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

''' 개인 메모 '''
class Personalmemo(BaseModel):
    id: int
    content: str
    user: User

class PersonalmemoCreate(BaseModel):
    content: str

class PersonalmemoUpdate(BaseModel):
    content: str

class PersonalmemoDelete(BaseModel):
    id: int