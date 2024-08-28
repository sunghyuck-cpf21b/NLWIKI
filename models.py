from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Date, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base


class Nonlan(Base):
    __tablename__ = "nonlan"

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    #content_info = Column(Text, nullable=False)
    person = Column(String,nullable=False)
    occ_date = Column(DateTime, nullable=False)
    create_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='nonlan_users')




class FileTemp_M(Base):
    __tablename__ = "file_temp"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    fileurl = Column(String, nullable=False)

class File_M(Base):      # 이미지 선택 창을 따로 띄워 임시 저장한 후 글 작성이 완료되면 최종 저장
    __tablename__ = "file"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    fileurl = Column(String, nullable=False)




class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    nonlan_id = Column(Integer, ForeignKey("nonlan.id"))
    nonlan = relationship("Nonlan", backref="comments")
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='comment_users')


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    set_admin = Column(Boolean, default=False, nullable=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

'''
관리자 로그인
id : 관리자
password : 123454321
'''

'''
관리자 id
1958273
'''

''' 운동 모델 '''
class ProgramDate(Base):
    __tablename__ = "program_date"
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)

    user = relationship("User", back_populates='program_dates')

class Exercise(Base):
    __tablename__ = "exercise"
    id = Column(Integer, primary_key=True)
    exercise = Column(String, nullable=True)
    order = Column(Integer, nullable=False)
    __table_args__ = (UniqueConstraint('date', 'order', name='date_order_unique'),) # date 별로 order에 unique 속성 부여
    date = Column(Date, ForeignKey("program_date.date", ondelete='CASCADE'), nullable=False)  # create 때에는 필요하지 않음
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)

    program_date = relationship("ProgramDate", back_populates='exercises')
    user = relationship("User", back_populates='exercises')

class Volume(Base):
    __tablename__ = "volume"
    id = Column(Integer, primary_key=True)
    set = Column(String, nullable=True)
    rep = Column(String, nullable=True)
    weight = Column(String, nullable=True)
    weight_kind = Column(String, nullable=False)
    isit_float = Column(Boolean, nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercise.id", ondelete='CASCADE'), nullable=False) # create 때에는 필요하지 않음
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)

    exercise = relationship("Exercise", back_populates='volumes')
    user = relationship("User", back_populates='volumes')

class Weeklymemo(Base):
    __tablename__ = "weeklymemo"
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    sunday_date = Column(Date, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates='weeklymemos')



ProgramDate.exercises = relationship("Exercise", order_by=Exercise.order, back_populates='program_date', cascade='all, delete-orphan')
Exercise.volumes = relationship('Volume', order_by=Volume.id, back_populates='exercise', cascade='all, delete-orphan')
# 각 부모자식 테이블의 관계 지정, order_by에 의해 어떤 column을 기준으로 정렬할건지 정할 수 있음
# delete-orphan은 부모 데이터가 삭제될 때 자식 데이터도 같이 삭제되도록 만들어줌
User.program_dates = relationship('ProgramDate', back_populates='user')
User.exercises = relationship("Exercise", back_populates='user')
User.volumes = relationship("Volume", back_populates='user')
User.weeklymemos = relationship("Weeklymemo", back_populates='user')