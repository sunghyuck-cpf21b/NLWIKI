import datetime

from sqlalchemy.orm import Session

from domain.comment.comment_schema import CommentCreate, CommentUpdate, SubCommentCreate, SubCommentUpdate
from models import Post, Comment, User, SubComment


def create_comment(db: Session, post: Post, comment_create: CommentCreate, user: User):
    db_comment = Comment(post=post,
                         content=comment_create.content,
                         create_date=datetime.datetime.now(),
                         user=user)
    db.add(db_comment)
    db.commit()

def get_comment(db: Session, comment_id: int):
    return db.query(Comment).get(comment_id)

def update_comment(db: Session, db_data: Comment,update_data: CommentUpdate):
    db_data.comment = update_data.content
    db.add(db_data)
    db.commit()

def delete_comment(db: Session, db_comment: Comment):
    db.delete(db_comment)
    db.commit()


''' 대댓글 '''
def creat_subcomment(db: Session, comment: Comment, subcomment_create: SubCommentCreate, user: User):
    db_subcomment = SubComment(content=subcomment_create.content,
                               create_date=datetime.datetime.now(),
                               comment=comment,
                               user=user)
    db.add(db_subcomment)
    db.commit()

def get_subcomment(db: Session, subcomment_id: int):
    return db.query(SubComment).filter_by(id=subcomment_id).first()

def update_subcomment(db: Session, db_data: SubComment, update_data: SubCommentUpdate):
    db_data.content = update_data.content
    db.add(db_data)
    db.commit()

def delete_subcomment(db: Session, data: SubComment):
    db.delete(data)
    db.commit()
