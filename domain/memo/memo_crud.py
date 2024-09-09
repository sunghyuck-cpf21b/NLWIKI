import datetime


from models import Weeklymemo, User, PersonalMemo
from domain.memo import memo_schema
from sqlalchemy.orm import Session
from sqlalchemy import distinct, and_


from typing import List
''' 주간 메모 '''
def get_weeklymemo_list(db: Session):
    memo_list = db.query(Weeklymemo).order_by(Weeklymemo.sunday_date).all()
    return memo_list

def get_weeklymemo(db: Session, date: datetime.date, user_id: int):
    memo = (db.query(Weeklymemo)
            .filter(and_(
        Weeklymemo.sunday_date == date,
        Weeklymemo.user_id == user_id
    ))).first()
    return memo

def get_month_weeklymemo(db: Session, start_date: datetime.date, end_date: datetime.date, user_id: int):
    memo_list = (db.query(Weeklymemo)
                 .filter(and_(
        start_date <= Weeklymemo.sunday_date, Weeklymemo.sunday_date <= end_date,
        Weeklymemo.user_id == user_id
    )).all())
    return memo_list


def create_weeklymemo(db: Session, weeklymemo_create: memo_schema.WeeklymemoCreate, user: User):
    memo = Weeklymemo(sunday_date=weeklymemo_create.sunday_date,
                      content=weeklymemo_create.content,
                      user=user)
    db.add(memo)
    db.commit()


def update_weeklymemo(db: Session, db_weeklymemo: Weeklymemo, weeklymemo_update: memo_schema.WeeklymemoUpdate):
    db_weeklymemo.content = weeklymemo_update.content
    db.add(db_weeklymemo)
    db.commit()


def delete_weeklymemo(db: Session, db_memo: Weeklymemo):
    db.delete(db_memo)
    db.commit()

''' 개인 메모 '''
def get_personalmemo_list(db: Session):
    data = db.query(PersonalMemo).order_by(PersonalMemo.user_id).all()
    return data

def get_personalmemo(user_id: int, db: Session):
    data = (db.query(PersonalMemo)
            .filter(PersonalMemo.user_id == user_id).first())
    return data

def create_personalmemo(db: Session, create_data: memo_schema.PersonalmemoCreate, user: User):
    data = PersonalMemo(content=create_data.content,
                        user=user)
    db.add(data)
    db.commit()

def update_personalmemo(db: Session, db_exist: PersonalMemo, update_data: memo_schema.PersonalmemoUpdate):
    db_exist.content = update_data.content
    db.add(db_exist)
    db.commit()

def delete_personalmemo(db: Session, db_exise: PersonalMemo):
    db.delete(db_exise)
    db.commit()