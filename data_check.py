from database import SessionLocal, engine
from models import Nonlan, Comment, User
from sqlalchemy import inspect

db = SessionLocal()

n = db.query(Comment)
n_id = [i[0] for i in db.query(Comment.id).all()]

ins = inspect(engine)
cols = ins.get_columns('comment')

list = []
for i in n_id:
    temp = []
    for c in cols:
        temp.append(db.query(getattr(Comment, c['name'])).filter_by(id=i).first()[0])
    list.append(temp)
for i in list:
    print(i)
for i in cols:
    print(i['name'])