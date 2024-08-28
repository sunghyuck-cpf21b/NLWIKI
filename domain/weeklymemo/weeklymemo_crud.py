import datetime


from models import Weeklymemo, User
from domain.weeklymemo import weeklymemo_schema
from sqlalchemy.orm import Session
from sqlalchemy import distinct, and_


from typing import List

def get_weekly_memo_list(db: Session):
    memo_list = db.query(Weeklymemo).order_by(Weeklymemo.sunday_date).all()
    return memo_list

def get_weekly_memo(db: Session, date: datetime.date, user_id: int):
    memo = (db.query(Weeklymemo)
            .filter(and_(
        Weeklymemo.sunday_date == date,
        Weeklymemo.user_id == user_id
    ))).first()
    return memo

def get_month_weekly_memo(db: Session, start_date: datetime.date, end_date: datetime.date, user_id: int):
    memo_list = (db.query(Weeklymemo)
                 .filter(and_(
        start_date <= Weeklymemo.sunday_date, Weeklymemo.sunday_date <= end_date,
        Weeklymemo.user_id == user_id
    )).all())
    return memo_list


def create_weekly_memo(db: Session, memo_create: weeklymemo_schema.WeeklymemoCreate, user: User):
    memo = Weeklymemo(sunday_date=memo_create.sunday_date,
                      content=memo_create.content,
                      user=user)
    db.add(memo)
    db.commit()


def update_weekly_memo(db: Session, db_memo: Weeklymemo, memo_update: weeklymemo_schema.WeeklymemoUpdate):
    db_memo.content = memo_update.content
    db.add(db_memo)
    db.commit()


def delete_weekly_memo(db: Session, db_memo: Weeklymemo):
    db.delete(db_memo)
    db.commit()

