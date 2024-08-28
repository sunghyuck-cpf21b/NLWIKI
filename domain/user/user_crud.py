from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User

from passlib.context import CryptContext

import Levenshtein

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def create_user(db: Session, user_create: UserCreate):
    db_user = User(username=user_create.username,
                   password=pwd_context.hash(user_create.password1))
    db.add(db_user)
    db.commit()

def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter((User.username == user_create.username)).first()

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def user_info(db: Session, user_id: int):
    return db.query(User).get(user_id)



def search_user(db: Session, username: str, cutoff: float):
    user_dict = {
        f'{Levenshtein.ratio(username, user.username)}user.username': user
        for user
        in db.query(User).all()
        if Levenshtein.ratio(username.lower(), user.username.lower()) >= cutoff
    }
    print(username)
    print(user_dict)
    temp = dict(sorted(user_dict.items(), reverse=True))
    result = list(temp.values())
    return result

def get_user_id(db: Session ,username: str):
    return db.query(User.id).filter_by(username=username).scalar()