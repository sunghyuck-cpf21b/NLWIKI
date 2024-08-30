from database import SessionLocal
from models import Nonlan, User, ProgramDate
from sqlalchemy import and_

db = SessionLocal()



data_list = db.query(ProgramDate).filter(ProgramDate.user_id == 3).all()
print(data_list)