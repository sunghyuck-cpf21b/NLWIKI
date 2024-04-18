from database import SessionLocal
from models import Nonlan, Comment, User

db = SessionLocal()

u = db.query(User.username).all()
print(u)

ad = db.query(User).filter_by(username='subuncream').first()
