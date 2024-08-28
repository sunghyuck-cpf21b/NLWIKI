from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
import datetime

from database import get_db
from models import Weeklymemo, User
from domain.weeklymemo import weeklymemo_schema, weeklymemo_crud
from domain.user import user_crud
from domain.user.user_router import get_current_user
from typing import List
from starlette import status

router = APIRouter(
    prefix='/api/weeklymemo'
)

@router.get('/list', response_model=list[weeklymemo_schema.Weeklymemo])
def get_weekly_memo_list(db: Session = Depends(get_db)):
    memo_list = weeklymemo_crud.get_weekly_memo_list(db=db)
    return memo_list

@router.get('/memo', response_model=weeklymemo_schema.Weeklymemo)
def get_weekly_memo(date: datetime.date,
                    username: str,
                    db: Session = Depends(get_db)):
    user_id = user_crud.get_user_id(db=db, username=username)
    memo = weeklymemo_crud.get_weekly_memo(db=db, date=date, user_id=user_id)
    return memo

@router.get('/month_memo', response_model=list[weeklymemo_schema.Weeklymemo])
def get_month_weekly_memo(start_date: datetime.date, end_date: datetime.date,
                          username: str,
                          db: Session = Depends(get_db)):
    user_id = user_crud.get_user_id(db=db, username=username)
    memo_list = weeklymemo_crud.get_month_weekly_memo(db=db, start_date=start_date, end_date=end_date, user_id=user_id)
    return memo_list

@router.post('/create', status_code=status.HTTP_204_NO_CONTENT)
def weekly_memo_create(memo_create: weeklymemo_schema.WeeklymemoCreate,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    if memo_create.sunday_date.weekday() != 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='메모 데이터는 일요일로 저장되어야 합니다.')
    db_memo = weeklymemo_crud.get_weekly_memo(db=db, date=memo_create.sunday_date, user_id=current_user.id)
    if db_memo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='이미 존재하는 메모입니다.')
    if memo_create.sunday_date.weekday() != 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='일요일이 아닙니다.')
    memo = weeklymemo_crud.create_weekly_memo(db=db, memo_create=memo_create, user=current_user)



@router.put('/update', status_code=status.HTTP_204_NO_CONTENT)
def weekly_memo_update(memo_update: weeklymemo_schema.WeeklymemoUpdate,
                       current_user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    db_memo = weeklymemo_crud.get_weekly_memo(db=db, date=memo_update.sunday_date, user_id=current_user.id)
    if not db_memo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='존재하지 않는 데이터입니다.')
    weeklymemo_crud.update_weekly_memo(db=db, db_memo=db_memo, memo_update=memo_update)


@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
def weekly_memo_delete(memo_date: weeklymemo_schema.WeeklymemoDelete,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    db_memo = weeklymemo_crud.get_weekly_memo(db=db, date=memo_date.sunday_date, user_id=current_user.id)
    if not db_memo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='존재하지 않는 데이터입니다.')
    weeklymemo_crud.delete_weekly_memo(db=db, db_memo=db_memo)




