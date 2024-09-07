from database import SessionLocal
from models import *

db = SessionLocal()


cs = db.query(Comment).all()

for c in cs:
    ct = CommentTemp(id=c.id, content=c.content, create_date=c.create_date, post_id=c.nonlan_id, user_id=c.user_id)
    db.add(ct)
    db.commit()