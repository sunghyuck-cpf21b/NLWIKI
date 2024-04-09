from database import SessionLocal
from models import Nonlan
from datetime import datetime
import ast

db = SessionLocal()

''' 임시로 move 파일에 있습니다. 파일을 실행할 때에는 main.py 와 같은 위치로 '''

'''
with open('move/total.txt', 'r') as f:
    nonlan_list = ast.literal_eval(f.read())
    for data in nonlan_list:
        N = Nonlan(occ_date=data[0], person=data[1], subject=data[2], content=data[3])
        db.add(N)
    db.commit()
'''


'''
with open('move/total.txt', 'r', encoding='utf-8') as f:
    print(f.read())
'''
split_code = 'split_subuncream_point'
# 입력 정보 : id
# 조건문_1 : id에 해당하는 db의 내용이 존재한다면 Update(혹은 total.txt 파일에서 비교한 후, 다른 내용이 있다면 Update)
# 조건문_2 : id에 해당하는 db의 내용이 없다면 Create
with open('move/total.txt', 'r', encoding='utf-8') as f:
    lines = [i.split(split_code) for i in f.readlines()]

    for i in lines:
        nonlan_id = int(i[0])
        nonlan_occ_date = datetime.strptime(i[1], "%Y-%m-%d %H:%M:%S")
        nonlan_person = ast.literal_eval(i[2])[0]
        nonlan_subject = ast.literal_eval(i[3])[0]
        nonlan_content = '\n'.join(ast.literal_eval(i[4]))
        user_id = 1


        data = db.get(Nonlan, nonlan_id)  # filter_by(id=nonl an_id)

        if data:
            data.occ_date = nonlan_occ_date
            data.person = nonlan_person
            data.subject = nonlan_subject
            data.content = nonlan_content
            data.user_id = user_id
            db.add(data)
            db.commit()
        if not data:
            N = Nonlan(id=nonlan_id ,occ_date=nonlan_occ_date, person=nonlan_person, subject=nonlan_subject, content=nonlan_content, create_date=datetime.now(), user_id=user_id)
            db.add(N)
            db.commit()




'''
for data in nonlan_result:
    N = Nonlan(occ_date=data[0], person=data[1], subject=data[2], content=data[3], create_date=datetime.now())
    db.add(N)
db.commit()
'''