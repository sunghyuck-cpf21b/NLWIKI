import datetime

from pydantic import BaseModel, field_validator
from fastapi import Query
from domain.user.user_schema import User

from typing import List



''' basic form '''
class Volume(BaseModel):
    id: int
    set: str
    rep: str
    weight: str
    weight_kind: str
    isit_float: bool
    exercise_id: int
    user: User

class Exercise(BaseModel):
    id: int
    exercise: str
    date: datetime.date
    order: int
    volumes: list[Volume] = []
    user: User

class ProgramDate(BaseModel):
    id: int
    date: datetime.date
    exercises: list[Exercise] = []
    user: User

class NewProgram(BaseModel):
    program_data: ProgramDate
    exercise: Exercise
    volume: Volume

class NewExercise(BaseModel):
    exercise: Exercise
    volume: Volume
''' create '''
# User는 별도로 추가되므로 schema에는 추가하지 않음
class ProgramDateCreate(BaseModel):
    date: datetime.date

class ExerciseCreate(BaseModel):
    date: datetime.date
    exercise: str
    order: int

class VolumeCreate(BaseModel):
    exercise_id: int
    set: str
    rep: str
    weight: str
    weight_kind: str

''' update '''
''' key 수정해야함 '''
class ProgramDateUpdate(ProgramDateCreate):
    date_id: int

class ExerciseUpdate(BaseModel):
    id: int
    key: str
    update_data: str

class VolumeUpdate(BaseModel):
    id: int
    key: str
    update_data: str

''' delete '''
class ProgramDateDelete(BaseModel):
    date: datetime.date

class ExerciseDelete(BaseModel):
    exercise_id: int


class VolumeDelete(BaseModel):
    volume_id: int


''' others '''
class Test(BaseModel):
    num_1: int