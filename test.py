from database import SessionLocal
from models import *

from passlib.context import CryptContext

db = SessionLocal()

ps = db.query(Post).filter_by(id=79).first()


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

hash_text = pwd_context.hash('123')
print(hash_text)
print(ps.user.password)
dehash1 = pwd_context.verify('123', hash_text)
dehash2 = pwd_context.verify('123', ps.user.password)

print(dehash1)
print(dehash2)
