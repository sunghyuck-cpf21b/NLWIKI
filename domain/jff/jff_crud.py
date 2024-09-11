import datetime

from domain.jff.jff_schema import DPCreate
from domain.jff.DP import pixel_editor as pe
from models import User, DotPaint
from sqlalchemy.orm import Session
from sqlalchemy import and_


''' DP (dot paint) '''
x_limit = 100
y_limit = 100
def get_dotpaint(db: Session, x: int, y: int):
    data = db.query(DotPaint).filter(and_(DotPaint.x==x, DotPaint.y==y)).first()
    return data

def get_dotpaint_list(db: Session):
    data = db.query(DotPaint).all()
    return data


def create_dotpaint(db: Session, create_data: DPCreate, name: str, user: User):
    pe.image_editor(x=create_data.x, y=create_data.y, color=create_data.color, name=name)
    data = DotPaint(x=create_data.x, y=create_data.y, color=create_data.color, create_date=datetime.datetime.now(), user=user)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data