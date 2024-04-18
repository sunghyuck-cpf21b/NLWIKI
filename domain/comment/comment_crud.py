from datetime import datetime

from sqlalchemy.orm import Session

from domain.comment.comment_schema import CommentCreate, CommentUpdate
from models import Nonlan, Comment, User


def create_comment(db: Session, nonlan: Nonlan, comment_create: CommentCreate, user: User):
    db_comment = Comment(nonlan=nonlan,
                         content=comment_create.content,
                         create_date=datetime.now(),
                         user=user)
    db.add(db_comment)
    db.commit()

def get_comment(db: Session, comment_id: int):
    return db.query(Comment).get(comment_id)

def delete_comment(db: Session, db_comment: Comment):
    db.delete(db_comment)
    db.commit()

