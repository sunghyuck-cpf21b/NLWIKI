from database import SessionLocal
from models import Nonlan

db = SessionLocal()
id_list = db.query(Nonlan.id).all()
print(id_list)
print(id_list[-1][0])
print(type(id_list[-1][0]))
id = db.query(Nonlan.id).order_by(Nonlan.id.desc()).all()[0][0]
print(id)