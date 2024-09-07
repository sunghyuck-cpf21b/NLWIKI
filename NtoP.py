from database import SessionLocal
from models import *

db = SessionLocal()


ps = db.query(Post).all()

for p in ps:
    