import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from starlette import status

from typing import List, Dict

from database import get_db
from domain.Sep_Program import sep_program_schema, sep_program_crud
from domain.Sep_Program.analysis import data_maker
from domain.user.user_router import get_current_user
from domain.user import user_crud
from models import ProgramDate, Exercise, Volume, User

router = APIRouter(
    prefix='/api/sep_program'
)

''' get list '''
@router.get('/list/program_date', response_model=list[sep_program_schema.ProgramDate])
def get_program_date_list(db: Session = Depends(get_db)):
    list = sep_program_crud.get_program_date_list(db=db)
    return list

@router.get('/list/exercise', response_model=list[sep_program_schema.Exercise])
def get_exercise_list(db: Session = Depends(get_db)):
    list = sep_program_crud.get_exercise_list(db=db)
    return list

@router.get('/list/volume', response_model=list[sep_program_schema.Volume])
def get_volume_list(db: Session = Depends(get_db)):
    list = sep_program_crud.get_volume_list(db=db)
    return list


''' get '''
@router.get('/program_date', response_model=sep_program_schema.ProgramDate)
def get_program_date(program_date: datetime.date, db: Session = Depends(get_db)):
    program_date = sep_program_crud.get_program_date(db=db, program_date=program_date)
    return program_date

@router.get('/exercise', response_model=sep_program_schema.Exercise)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = sep_program_crud.get_exercise(db=db, exercise_id=exercise_id)
    return exercise

@router.get('/volume', response_model=sep_program_schema.Volume)
def get_volume(volume_id: int, db: Session = Depends(get_db)):
    volume = sep_program_crud.get_volume(db=db, volume_id=volume_id)
    return volume

@router.get('/program/{program_date}', status_code=status.HTTP_200_OK)
def get_program(program_date: datetime.date, db: Session = Depends(get_db)):
    exercises, volumes = sep_program_crud.get_program(db=db, program_date=program_date)
    return {'exercises':exercises, 'volumes': volumes}

@router.get('/month_data', status_code=status.HTTP_200_OK)
def get_month_data(year: int, month: int, db: Session = Depends(get_db)):
    data = sep_program_crud.get_month_data(db=db, year=year, month=month)
    return data

@router.get('/month_data_2', response_model=list[sep_program_schema.ProgramDate])
def get_month_data_2(start_date: datetime.date,
                     end_date: datetime.date,
                     username: str,
                     db: Session = Depends(get_db)):
    user_id = user_crud.get_user_id(db=db, username=username)
    '''
    if not user_id:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail='해당 사용자가 존재하지 않습니다.')
    '''
    data = sep_program_crud.get_month_data_2(db=db, start_date=start_date,
                                             end_date=end_date, user_id=user_id)
    return data

@router.get('/all_ex', status_code=status.HTTP_200_OK)
def get_all_ex(db: Session = Depends(get_db)):
    data = sep_program_crud.get_all_ex(db=db)
    return data

@router.get('/overload_data', status_code=status.HTTP_200_OK)
def get_overload_data(
        username: str,
        date_limit: List[datetime.date] = Query(None),
        weight_limit: List[float] = Query(None),
        wk_list: List[str] = Query(None),
        name_list: List[str] = Query(...),
        db: Session = Depends(get_db)):
    print(username, date_limit, weight_limit, name_list)
    user_id = user_crud.get_user_id(db=db, username=username)
    labels, data, weight_range = data_maker.overload_data(name_list=name_list, date_limit=date_limit,
                                            weight_limit=weight_limit, wk_list=wk_list, user_id=user_id,
                                            MD=Exercise, db=db)
    return {'labels': labels, 'data': data, 'weight_range': weight_range}


''' create '''
@router.post('/create/program_date', status_code=status.HTTP_200_OK)
def create_program_date(program_date_create: sep_program_schema.ProgramDateCreate,
                        db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    pd_data_exist = sep_program_crud.get_program_date(db=db, program_date=program_date_create.date)
    if pd_data_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='해당 날짜에 이미 데이터가 존재합니다.')
    pd_data = sep_program_crud.create_program_date(db=db,
                                                   program_date_create=program_date_create,
                                                   user=current_user)

    ex_info = sep_program_schema.ExerciseCreate(date=program_date_create.date, exercise='', order=0)
    ex_data = sep_program_crud.create_exercise(db=db, program_date=pd_data,
                                               exercise_create=ex_info, user=current_user)

    vo_info = sep_program_schema.VolumeCreate(exercise_id=ex_data.id, set='', rep='', weight='', weight_kind='kg')
    sep_program_crud.create_volume(db=db, exercise=ex_data,
                                   volume_create=vo_info, user=current_user)



@router.post('/create/exercise', status_code=status.HTTP_200_OK)
def create_exercise(exercise_create: sep_program_schema.ExerciseCreate,
                    db: Session = Depends(get_db),
                    current_user: User =Depends(get_current_user)):
    program_date = sep_program_crud.get_program_date(db=db,program_date=exercise_create.date)
    if not program_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='날짜 데이터를 찾을 수 없습니다.')
    ex_info = sep_program_schema.ExerciseCreate(exercise='', date=exercise_create.date, order=exercise_create.order)
    ex_data = sep_program_crud.create_exercise(db=db, program_date=program_date,
                                               exercise_create=ex_info, user=current_user)

    vo_info = sep_program_schema.VolumeCreate(exercise_id=ex_data.id, set='', rep='', weight='', weight_kind='kg')
    sep_program_crud.create_volume(db=db, exercise=ex_data,
                                   volume_create=vo_info, user=current_user)

@router.post('/create/volume', status_code=status.HTTP_200_OK)
def create_volume(volume_create: sep_program_schema.VolumeCreate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    ex_data = sep_program_crud.get_exercise(db=db, exercise_id=volume_create.exercise_id)
    if not ex_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='종목 데이터를 찾을 수 없습니다.')

    vo_info = sep_program_schema.VolumeCreate(exercise_id=volume_create.exercise_id, set='', rep='', weight='', weight_kind='kg')
    sep_program_crud.create_volume(db=db, exercise=ex_data,
                                   volume_create=vo_info, user=current_user)


''' update '''
@router.put('/update/exercise', status_code=status.HTTP_204_NO_CONTENT)
def update_exercise(update_data: sep_program_crud.ExerciseUpdate, db: Session = Depends(get_db)):
    db_exercise = sep_program_crud.get_exercise(db=db, exercise_id=update_data.id)
    if not db_exercise:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='없는 데이터 입니다.')
    sep_program_crud.update_exercise(db=db, db_exercise=db_exercise, update_data=update_data)

@router.put('/update/volume', status_code=status.HTTP_204_NO_CONTENT)
def update_volume(update_data: sep_program_schema.VolumeUpdate, db: Session = Depends(get_db)):
    db_volume = sep_program_crud.get_volume(db=db, volume_id=update_data.id)
    if not db_volume:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='없는 데이터 입니다.')
    sep_program_crud.update_volume(db=db, db_volume=db_volume, update_data=update_data)

''' delete '''
@router.delete('/delete/program_date', status_code=status.HTTP_204_NO_CONTENT)
def delete_program_date(info: sep_program_crud.ProgramDateDelete, db: Session = Depends(get_db)):
    data = sep_program_crud.get_program_date(db=db, program_date=info.date)
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='program_date 데이터가 존재하지 않습니다')
    sep_program_crud.delete_program_date(db=db, data=data)

@router.delete('/delete/exercise', status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(info: sep_program_crud.ExerciseDelete, db: Session = Depends(get_db)):
    data = sep_program_crud.get_exercise(db=db, exercise_id=info.exercise_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='exercise 데이터가 존재하지 않습니다')
    sep_program_crud.delete_exercise(db=db, data=data)

@router.delete('/delete/volume', status_code=status.HTTP_204_NO_CONTENT)
def delete_volume(info: sep_program_crud.VolumeDelete, db: Session = Depends(get_db)):
    data = sep_program_crud.get_volume(db=db, volume_id=info.volume_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='volume 데이터가 존재하지 않습니다')
    sep_program_crud.delete_volume(db=db, data=data)


''' others '''
