from database import SessionLocal
from models import Nonlan, User, ProgramDate, Post, CommentTemp, Comment
from sqlalchemy import and_

db = SessionLocal()

ns = db.query(Nonlan).all()
cs = db.query(Comment).all()
split_code = '*ssubun11111*'




