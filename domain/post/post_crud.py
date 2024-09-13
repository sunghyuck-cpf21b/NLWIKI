from datetime import datetime

from domain.post.post_schema import PostCreate, PostUpdate
from models import Post, Comment, User, categories
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc

from domain.post.data_maker import data_maker


def get_post_list(db: Session, category: str, user: User,
                  category_list: list = categories[:],
                  skip: int = 0, limit: int = 15, keyword: str = ''):
    if not user.set_nonlan_user: # 논란 열람 가능한 사용자인지 판단
        category_list.remove('논란')
    if category != categories[0]: # 선택한 카테고리가 '전체' 가 아니라면 카테고리 리스트를 축소(선택한 카테고리 하나만 남도록) => 판별을 category_list로만 할거기때문
        category_list = [category]
    post_list = db.query(Post).filter(Post.category.in_(category_list)).order_by(desc(Post.id))

    if keyword: # 검색기능
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
    post_list = post_list.offset(skip).limit(limit).distinct().all()
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
