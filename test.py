from database import SessionLocal
from models import Nonlan, User, ProgramDate, Post, CommentTemp
from sqlalchemy import and_

db = SessionLocal()


n = db.query(Nonlan).filter(Nonlan.id == 77).first()

import base64


ll = n.content.split('"')
'''

data = base64.b64decode(ll[1])
print(data)
'''
data64 = ll[1]
length = len(data64)
mp = length % 4
if mp != 0:
    data64 += '=' * (4-mp)

data = base64.b64decode(data64)

with open('test_img.png', 'wb') as f:
    f.write(data)