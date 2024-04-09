from datetime import datetime

from sqlalchemy.orm import Session

from domain.comment.comment_schema import CommentCreate, CommentUpdate
from models import Nonlan, Comment


def create_comment(db: Session, nonlan: Nonlan, comment_create: CommentCreate):
    db_comment = Comment(nonlan=nonlan,
                         content=comment_create.content,
                         create_date=datetime.now())
    db.add(db_comment)
    db.commit()

def get_comment(db: Session, comment_id: int):
    return db.query(Comment).get(comment_id)

def comment_delete(db: Session, db_comment: Comment):
    db.delete(db_comment)
    db.commit()

