from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
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