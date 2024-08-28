import datetime
import math
from sqlalchemy.orm import Session
from sqlalchemy import extract, and_
from starlette import status
from fastapi import HTTPException

from typing import Union

from database import SessionLocal
from domain.Sep_Program.sep_program_schema import (
    ProgramDateCreate, ProgramDateUpdate, ProgramDateDelete,
    ExerciseCreate, ExerciseUpdate, ExerciseDelete,
    VolumeCreate, VolumeUpdate, VolumeDelete
)
from models import ProgramDate, Exercise, Volume, User

from domain.Sep_Program.organize import organize

db = SessionLocal()

''' basic function '''
def isit_float(volume: Union[Volume, VolumeCreate]):
    try:
        float(volume.set)
        float(volume.rep)
        float(volume.weight)
        return True
    except:
        return False
''' get list '''
def get_program_date_list(db: Session):
    return db.query(ProgramDate).order_by(ProgramDate.id).all()

def get_exercise_list(db: Session):
    return db.query(Exercise).all()

def get_volume_list(db: Session):
    return db.query(Volume).all()

''' get '''
def get_program_date(db: Session, program_date: datetime.date):
    return db.query(ProgramDate).filter_by(date=program_date).first()

def get_exercise(db: Session, exercise_id: int):
    return db.query(Exercise).get(exercise_id)

def get_volume(db: Session, volume_id: int):
    return db.query(Volume).get(volume_id)

def get_program(db: Session, program_date: datetime.date):
    exs = db.query(Exercise).filter_by(date=program_date).all()
    ex_list = []
    vol_list = []
    for ex in exs:
        ex_list.append({'id':ex.id, 'exercise':ex.exercise})
        temp_vols = db.query(Volume).filter_by(exercise_id=ex.id).all()
        temp_vol_list = []
        for vol in temp_vols:
            temp_vol_dict = {'id': vol.id, 'set': vol.set, 'rep': vol.rep, 'weight': vol.weight, 'weight_kind': vol.weight_kind}
            temp_vol_list.append(temp_vol_dict)
        vol_list.append(temp_vol_list)
    return ex_list, vol_list
''' 
수정할 때 인덱싱으로 수정할 데이터를 찾으면 불필요하게 불러와야 하는 데이터들이 있을 수 있기 때문에
전송할 때 exercise, volume의 id번호까지 전송하자
네트워킹을 희생하는 듯 하지만 
수정 데이터를 프론트엔드에서 전송받을 때 
필요한 데이터가 더 적어져서 
기존 : 날짜, 인덱스 번호, 수정 데이터
id 사용 : id 번호, 수정 데이터
오히려 좋을수도
'''

def get_month_data(db: Session, year: int, month: int):
    next_year, next_month = year, month+1
    if month == 12:
        next_year, next_month = year+1, 1
    a = datetime.date(year, month, 1)
    b = datetime.date(next_year, next_month, 1)
    cells = 7 * math.ceil((b-a).days/7)
    start_date = a - datetime.timedelta(days=(a.weekday()+1)&7)
    end_date = start_date + datetime.timedelta(days=cells-1)
    exs = db.query(Exercise).filter(start_date <= Exercise.date, Exercise.date <= end_date)
    dict = {}

    for ex in exs:
        if ex.date not in dict.keys():
            dict[ex.date] = {'exercises': [], 'volumes': []}
        temp_ex = {i.name: getattr(ex, i.name) for i in ex.__table__.columns if not i.name=='date'}
        # 위의 딕셔너리 만드는 코드는 따로 함수로 만들기
        # 매개변수는 데이터(위에서는 ex), 제외해야 할 column의 리스트 (if i.name not in [~~] 으로 변경해서)
        vols = db.query(Volume).filter_by(exercise_id=ex.id).all()
        temp_vol_list = []
        for vol in vols:
            temp_vol = {i.name: getattr(vol, i.name) for i in vol.__table__.columns if not i.name=='exercise_id'}
            temp_vol_list.append(temp_vol)
        dict[ex.date]['exercises'].append(temp_ex)
        dict[ex.date]['volumes'].append(temp_vol_list)
    return dict

def get_month_data_2(db: Session, start_date: datetime.date, end_date: datetime.date, user_id: int):
    data_list = (db.query(ProgramDate)
                 .filter(and_(start_date <= ProgramDate.date, ProgramDate.date <= end_date,
                              ProgramDate.user_id == user_id))
                 .all())
    return data_list

def get_all_ex(db: Session):
    exercises = db.query(Exercise).all()
    data = []
    for exercise in exercises:
        data.append(exercise.exercise)
    data = list(sorted(set(data)))
    return data

''' create '''
def create_program_date(db: Session, program_date_create: ProgramDateCreate, user: User):
    program_date_data = ProgramDate(date=program_date_create.date,
                                    user=user)
    db.add(program_date_data)
    db.commit()
    return program_date_data
def create_exercise(db: Session, program_date: ProgramDate, exercise_create: ExerciseCreate, user: User):
    organize.exercise_replace(date=exercise_create.date, index=exercise_create.order, db=db, create=True)
    exercise_data = Exercise(exercise=exercise_create.exercise,
                             order=exercise_create.order,
                             program_date=program_date,
                             user= user)
    db.add(exercise_data)
    db.commit()
    organize.exercise_reorder(date=exercise_create.date, db=db)
    return exercise_data

def create_volume(db: Session, exercise: Exercise, volume_create: VolumeCreate, user: User):
    volume_data = Volume(set=volume_create.set,
                        rep=volume_create.rep,
                        weight=volume_create.weight,
                        weight_kind=volume_create.weight_kind,
                        isit_float=isit_float(volume_create),
                        exercise=exercise,
                        user= user)
    db.add(volume_data)
    db.commit()
    return volume_data

''' update '''
def update_program_date(db: Session, db_program_date: ProgramDate, update_data: ProgramDateUpdate):
    return # 연결된 exercise가 있을 때 foreignkey가 어떻게 변하는지 확인해보기

def update_exercise(db: Session, db_exercise: Exercise, update_data: ExerciseUpdate):
    setattr(db_exercise, update_data.key, update_data.update_data)
    db.add(db_exercise)
    db.commit()

def update_volume(db: Session, db_volume: Volume, update_data: VolumeUpdate):
    setattr(db_volume, update_data.key, update_data.update_data)
    db_volume.isit_float = isit_float(db_volume)
    db.add(db_volume)
    db.commit()

''' delete '''
''' delete를 따로 분리해서 만들지, 아니면 지금처럼 통합으로 운영할지 고민해보기 '''
''' 문제점 : 분리하면 db 를 all로 선택하는 함수를 따로 만들어야해서, 함수 개수가 늘어날 수 있음 '''
''' date, exercise.all, exercise.firsst, volume.all, volume.first '''
''' 아니면 어차피 단일 데이터도 all로 선택할 수 있으니까 그냥 해도 될까? => all 검색방식이 성능에 어떤 영향을 주는지 알아보고 결정하기 '''
def delete_program_date(db: Session, data: ProgramDate):
    db.delete(data)
    db.commit()


def delete_exercise(db: Session, data: Exercise):
    db.delete(data)
    db.commit()


def delete_volume(db: Session, data: Volume):
    db.delete(data)
    db.commit()


