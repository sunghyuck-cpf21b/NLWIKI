from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
import datetime

from database import get_db
from models import Weeklymemo, User
from domain.memo import memo_schema, memo_crud
from domain.user import user_crud
from domain.user.user_router import get_current_user
from typing import List, Optional
from starlette import status

router = APIRouter(
    prefix='/api/memo'
)

@router.get('/weekly/list', response_model=list[memo_schema.Weeklymemo])
def get_weeklymemo_list(db: Session = Depends(get_db)):
    memo_list = memo_crud.get_weeklymemo_list(db=db)
    return memo_list

@router.get('/weekly/memo', response_model=memo_schema.Weeklymemo)
def get_memo(date: datetime.date,
                    username: str,
                    db: Session = Depends(get_db)):
    user_id = user_crud.get_user_id(db=db, username=username)
    memo = memo_crud.get_weeklymemo(db=db, date=date, user_id=user_id)
    return memo

@router.get('/weekly/month_memo', response_model=list[memo_schema.Weeklymemo])
def get_month_memo(start_date: datetime.date, end_date: datetime.date,
                          username: str,
                          db: Session = Depends(get_db)):
    user_id = user_crud.get_user_id(db=db, username=username)
    memo_list = memo_crud.get_month_weeklymemo(db=db, start_date=start_date, end_date=end_date, user_id=user_id)
    return memo_list

@router.post('/weekly/create', status_code=status.HTTP_204_NO_CONTENT)
def weeklymemo_create(weeklymemo_create: memo_schema.WeeklymemoCreate,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    if weeklymemo_create.sunday_date.weekday() != 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='메모 데이터는 일요일로 저장되어야 합니다.')
    db_memo = memo_crud.get_weeklymemo(db=db, date=weeklymemo_create.sunday_date, user_id=current_user.id)
    if db_memo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='이미 존재하는 메모입니다.')
    if weeklymemo_create.sunday_date.weekday() != 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='일요일이 아닙니다.')
    memo = memo_crud.create_weeklymemo(db=db, weeklymemo_create=weeklymemo_create, user=current_user)



@router.put('/weekly/update', status_code=status.HTTP_204_NO_CONTENT)
def weeklymemo_update(weeklymemo_update: memo_schema.WeeklymemoUpdate,
                       current_user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    db_memo = memo_crud.get_weeklymemo(db=db, date=weeklymemo_update.sunday_date, user_id=current_user.id)
    if not db_memo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='존재하지 않는 데이터입니다.')
    memo_crud.update_weeklymemo(db=db, db_weeklymemo=db_memo, weeklymemo_update=weeklymemo_update)


@router.delete('/weekly/delete', status_code=status.HTTP_204_NO_CONTENT)
def weeklymemo_delete(weeklymemo_date: memo_schema.WeeklymemoDelete,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    db_memo = memo_crud.get_weeklymemo(db=db, date=weeklymemo_date.sunday_date, user_id=current_user.id)
    if not db_memo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='존재하지 않는 데이터입니다.')
    memo_crud.delete_weeklymemo(db=db, db_memo=db_memo)


@router.get('/personal/list', response_model=list[memo_schema.Personalmemo])
def get_personalmemo_list(db: Session = Depends(get_db)):
    data = memo_crud.get_personalmemo_list(db=db)
    return data

@router.get('/personal/detail', response_model=Optional[memo_schema.Personalmemo])
def get_personalmemo(db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    data = memo_crud.get_personalmemo(user_id=current_user.id, db=db)
    return data

@router.post('/personal/create', status_code=status.HTTP_204_NO_CONTENT)
def create_personalmemo(create_data: memo_schema.PersonalmemoCreate,
                        db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    db_exist = memo_crud.get_personalmemo(user_id=current_user.id,db=db)
    if db_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='사용자당 하나의 개인 메모만 생성됩니다.')
    memo_crud.create_personalmemo(db=db, create_data=create_data, user=current_user)

@router.put('/personal/update', status_code=status.HTTP_204_NO_CONTENT)
def update_personalmemo(update_data: memo_schema.PersonalmemoUpdate,
                        db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    db_exist = memo_crud.get_personalmemo(user_id=current_user.id, db=db)
    if not db_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='사용자의 개인 메모가 존재하지 않습니다. 먼저 메모를 생성해주세요.')
    memo_crud.update_personalmemo(db=db, db_exist=db_exist, update_data=update_data)

@router.delete('/personal/delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_personalmemo(db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    db_exist = memo_crud.get_personalmemo(user_id=current_user.id, db=db)
    if not db_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='데이터가 존재하지 않습니다.')
    memo_crud.delete_personalmemo(db=db, db_exise=db_exist)

