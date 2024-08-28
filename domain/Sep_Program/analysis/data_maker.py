from models import ProgramDate, Exercise, Volume
from database import SessionLocal_read, Base
from domain.Sep_Program import sep_program_schema

import pandas as pd

from sqlalchemy.orm import Session, subqueryload
from sqlalchemy import and_, select, func
import datetime

db = SessionLocal_read()

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

'''
작성순서
SELECT - FROM - WHERE - GROUP By - HAVING - ORDER BY - LIMIT
실행 순서
FROM - WHERE - GROUP BY - HAVING - SELECT - ORDER BY - LIMIT
'''

''' 추후에는 기본 중량 설정(kg or lbs)에 따라 데이터 변경하는 기능도 만들어야함 '''
def weight_range_maker(name_list: list, data: list):
    result_dict = {name:[2000, 0] for name in name_list}

    for d in data:
        weight = float(d.Volume.weight)
        weight = weight if d.Volume.weight_kind=='kg' else weight*0.453592
        if weight < result_dict[d.Exercise.exercise][0]:
            result_dict[d.Exercise.exercise][0] = weight
        if result_dict[d.Exercise.exercise][1] < weight:
            result_dict[d.Exercise.exercise][1] = weight

    for name in name_list:
        if result_dict[name][1] == result_dict[name][0]:
            # 중량 범위가 0 일 경우 (하한과 상한이 동일할 경우) 색상을 중앙으로 설정하기 위한 조건문
            result_dict[name][0] = result_dict[name][0]-1
            result_dict[name].append(2)
        else:
            result_dict[name].append(result_dict[name][1]-result_dict[name][0])
    return result_dict



def overload_data(name_list: list, date_limit: list, weight_limit: list, wk_list: list,
                  user_id: int ,MD: Base, db: Session):
    '''
    상한, 하한 리스트는 name_list 인덱스의 2배, 2배+1 위치에 있음
    isit_float 은 set, rep, weight 가 모두 숫자형으로 변경 가능할 때 True임
    '''

    wk_mag = {'kg': 1, 'lbs': 0.453592} # magnification ratio
    temp_data = (
        db.query(Exercise, Volume)
        .join(Volume, Exercise.id==Volume.exercise_id, isouter=False)
        .filter(and_(Exercise.exercise.in_(name_list),
                     Volume.isit_float,
                     user_id==user_id))
        .order_by(Exercise.date, Exercise.order)
        .all()
    )

    weight_range = {name:[10000, 0] for name in name_list}
    labels = []
    data_list = []

    for td in temp_data:
        name = td.Exercise.exercise
        name_index = name_list.index(name)
        date = td.Exercise.date
        if not (date_limit[2*name_index] <= date <= date_limit[2*name_index+1]):
            continue
        weight = float(td.Volume.weight)
        weight_kind = td.Volume.weight_kind
        weight_lower = weight_limit[2*name_index] * wk_mag[wk_list[2*name_index]]
        weight_upper = weight_limit[2*name_index+1] * wk_mag[wk_list[2*name_index+1]]
        if not (weight_lower <= weight*wk_mag[weight_kind] <= weight_upper):
            continue

        if weight*wk_mag[weight_kind] < weight_range[name][0]:
            weight_range[name][0] = weight*wk_mag[weight_kind]
        if weight_range[name][1] < weight*wk_mag[weight_kind]:
            weight_range[name][1] = weight * wk_mag[weight_kind]

        set = int(td.Volume.set)
        rep = int(td.Volume.rep)
        data_dict = {
            'x': date,
            'y': set*rep*weight*wk_mag[weight_kind],
            'color': weight*wk_mag[weight_kind],
            'tooltip': [name, f'{set} x {rep} x {weight} {weight_kind}', f'volume = {round(set*rep*weight*wk_mag[weight_kind])}']
        }
        if date not in labels:
            labels.append(date)
        data_list.append(data_dict)
        print(date, name, td.Exercise.order)
    return labels, data_list, weight_range




'''
name_list = ['백스쿼트', '정지 프론트 스쿼트']

overload_dict(name_list=name_list, MD=Exercise, db=db)
'''
