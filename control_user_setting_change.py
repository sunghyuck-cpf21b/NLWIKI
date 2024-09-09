from database import SessionLocal
from models import User

db = SessionLocal()


user_list = ['subuncream', '영주꼬추', '여대장', 'godyeongju98', '이승준', '토모', '토모토모', '복희', '승준']


# 작업
# set_nonlan_user 권한 True로 할 사용자들

for u in user_list:
    data = db.query(User).filter(User.username == u).first()
    data.set_nonlan_user = True
    db.add(data)
    db.commit()


# admin 설정할 유저
user = db.query(User).filter(User.username == 'subuncream').first()
user.set_admin = True
db.add(user)
db.commit()