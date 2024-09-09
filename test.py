from database import SessionLocal
from models import *

from passlib.context import CryptContext

db = SessionLocal()

m = db.query(PersonalMemo).filter(PersonalMemo.user_id == 1).first()
print(m)