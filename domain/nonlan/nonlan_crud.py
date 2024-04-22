from datetime import datetime

from domain.nonlan.nonlan_schema import NonlanCreate, NonlanUpdate
from models import Nonlan, Comment, User
from sqlalchemy.orm import Session
from sqlalchemy import and_

def get_nonlan_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''):
    nonlan_list = db.query(Nonlan)
    if keyword:
        search = '%%{}%%'.format(keyword)
        sub_query = db.query(Comment.nonlan_id, Comment.content, User.username)\
            .outerjoin(User, and_(Comment.user_id == User.id)).subquery()
        nonlan_list = nonlan_list \
            .outerjoin(User) \
            .outerjoin(sub_query, and_(sub_query.c.nonlan_id == Nonlan.id)) \
            .filter(Nonlan.subject.ilike(search) |
                    Nonlan.content.ilike(search) |
                    User.username.ilike(search) |
                    sub_query.c.content.ilike(search) |
                    sub_query.c.username.ilike(search)
                    )
    total = nonlan_list.distinct().count()
    nonlan_list = nonlan_list.order_by(Nonlan.occ_date.desc(), Nonlan.create_date.desc())\
        .offset(skip).limit(limit).distinct().all()
    return total, nonlan_list

def get_nonlan(db: Session, nonlan_id: int):
    nonlan = db.query(Nonlan).get(nonlan_id)
    return nonlan


def create_nonlan(db:Session, nonlan_create: NonlanCreate, user: User):
    db_nonlan = Nonlan(subject=nonlan_create.subject,
                       content=nonlan_create.content,
                       person=nonlan_create.person,
                       occ_date=nonlan_create.occ_date,
                       create_date=datetime.now(),
                       user=user)
                       #content_info=nonlan_create.content_info)
    db.add(db_nonlan)
    db.commit()


def delete_nonlan(db: Session, db_nonlan: Nonlan):
    db.delete(db_nonlan)
    db.commit()


def update_nonlan(db: Session, db_nonlan: Nonlan,
                  nonlan_update: NonlanUpdate):
    db_nonlan.subject = nonlan_update.subject
    db_nonlan.content = nonlan_update.content
    db_nonlan.person = nonlan_update.person
    db_nonlan.occ_date = nonlan_update.occ_date
    db_nonlan.modify_date = datetime.now()
    #db_nonlan.content_info = nonlan_update.content_info
    db.add(db_nonlan)
    db.commit()
