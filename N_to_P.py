from database import SessionLocal
from models import *

db = SessionLocal()
split_code = '***subunchockchock***'




ps = db.query(Post).all()
for i, p in enumerate(ps):
    how = 'w' if i == 0 else 'a'
    with open('backups/posts.txt', how, encoding='utf-8') as f:
        f.write(str(p.id))
        f.write(split_code)
        f.write(str(p.category))
        f.write(split_code)
        f.write(str(p.subject))
        f.write(split_code)
        f.write(str(p.content))
        f.write(split_code)
        f.write(str(p.create_date))
        f.write(split_code)
        f.write(str(p.person))
        f.write(split_code)
        f.write(str(p.occ_date))
        f.write(split_code)
        f.write(str(p.user_id))
        f.write(split_code)
        f.write(str(p.user.username))
        f.write(split_code)
        f.write(str(p.user.password))
        f.write(split_code)
        f.write('\n')


cs = db.query(Comment).all()
for i, c in enumerate(cs):
    how = 'w' if i == 0 else 'a'
    with open('backups/comments.txt', how, encoding='utf-8') as f:
        f.write(str(c.id))
        f.write(split_code)
        f.write(str(c.content))
        f.write(split_code)
        f.write(str(c.create_date))
        f.write(split_code)
        f.write(str(c.post_id))
        f.write(split_code)
        f.write(str(c.user_id))
        f.write(split_code)
        f.write(str(c.user.username))
        f.write(split_code)
        f.write(str(c.user.password))
        f.write(split_code)
        f.write('\n')

us = db.query(User).all()
for i, e in enumerate(us):
    how = 'w' if i == 0 else 'a'
    with open('backups/users.txt', how, encoding='utf-8') as f:
        f.write(str(e.id))
        f.write(split_code)
        f.write(str(e.username))
        f.write(split_code)
        f.write(str(e.password))
        f.write(split_code)
        f.write('\n')
