from datetime import datetime

from domain.post.post_schema import PostCreate, PostUpdate
from models import Post, Comment, User
from sqlalchemy.orm import Session
from sqlalchemy import and_

def get_post_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''):
    post_list = db.query(Post)
    if keyword:
        search = '%%{}%%'.format(keyword)
        sub_query = db.query(Comment.post_id, Comment.content, User.username)\
            .outerjoin(User, and_(Comment.user_id == User.id)).subquery()
        post_list = post_list \
            .outerjoin(User) \
            .outerjoin(sub_query, and_(sub_query.c.post_id == Post.id)) \
            .filter(Post.subject.ilike(search) |
                    Post.content.ilike(search) |
                    User.username.ilike(search) |
                    sub_query.c.content.ilike(search) |
                    sub_query.c.username.ilike(search)
                    )
    total = post_list.distinct().count()
    post_list = post_list.order_by(Post.occ_date.desc(), Post.create_date.desc())\
        .offset(skip).limit(limit).distinct().all()
    return total, post_list

def get_post(db: Session, post_id: int):
    post = db.query(Post).get(post_id)
    return post


def create_post(db:Session, post_create: PostCreate, user: User):
    db_post = Post(category=post_create.category,
                   subject=post_create.subject,
                       content=post_create.content,
                       person=post_create.person,
                       occ_date=post_create.occ_date,
                       create_date=datetime.now(),
                       user=user)
                       #content_info=post_create.content_info)
    db.add(db_post)
    db.commit()


def delete_post(db: Session, db_post: Post):
    db.delete(db_post)
    db.commit()


def update_post(db: Session, db_post: Post,
                  post_update: PostUpdate):
    db_post.subject = post_update.subject
    db_post.category = post_update.category
    db_post.content = post_update.content
    db_post.person = post_update.person
    db_post.occ_date = post_update.occ_date
    db_post.modify_date = datetime.now()
    #db_post.content_info = post_update.content_info
    db.add(db_post)
    db.commit()
