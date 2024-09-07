from database import SessionLocal
from models import *

db = SessionLocal()


ns = db.query(Nonlan).all()

for n in ns:
    p = Post(id=n.id, category='논란', subject=n.subject, content=n.content, create_date=n.create_date,
             person=n.person, occ_date=n.occ_date, user_id=n.user_id)
    db.add(p)
    db.commit()