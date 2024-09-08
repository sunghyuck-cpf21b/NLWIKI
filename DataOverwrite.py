from database import SessionLocal
from models import User, ProgramDate, Post
from sqlalchemy import and_
import datetime
db = SessionLocal()

split_code = '***subunchockchock***'

with open('backups/users.txt', 'r', encoding='utf-8') as f:
    info = f.read()



'''
for i in range(int(main_count)):
    cd = datetime.datetime.strptime(pp[i*8+4], '%Y-%m-%d %H:%M:%S.%f')
    od = datetime.datetime.strptime(pp[i * 8 + 6], '%Y-%m-%d %H:%M:%S')
    p = Post(id=pp[i*8], category=pp[i*8+1], subject=pp[i*8+2], content=pp[i*8+3], create_date=cd,
             person=pp[i*8+5], occ_date=od, user_id=pp[i*8+7])
    db.add(p)
    db.commit()
'''

'''
작성 잘못해서 splitcode로만 나눠야함
8개 단위로 게시물이 바뀜
0: id
1: 카테고리
2: 제목
3: 내용
4: 작성날짜
5: 인물
6: 발생일자
7: 작성자 id
8: 작성자 이름
9: 작성자 비밀번호

현재 nonlan, comment(기존) 테이블 주석처리 하고 새롭게
post, comment(새로운) 테이블 generate 해놨음

backups에서 문서 가져와서 데이터베이스에 넣어주면 됨

이 파일에 기능 만들고
git add 해서 서버 데이터도 복구해주기

+ 백업 데이터베이스 만들기
백엔드 파일을 변경하기 전에 백업 진행하고 백엔드 업데이트 하기

'''


