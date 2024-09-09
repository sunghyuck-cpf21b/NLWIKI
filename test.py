from database import SessionLocal
from models import *

from passlib.context import CryptContext

db = SessionLocal()

u = db.query(User).all()
