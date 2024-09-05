from database import SessionLocal
from models import Nonlan, User, ProgramDate, Post, CommentTemp
from sqlalchemy import and_

db = SessionLocal()



import os

dir = os.path.dirname(os.path.abspath(__file__))

print(dir)

fp = os.path.join(dir, '../../a.txt')

print(fp)