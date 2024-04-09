from datetime import datetime

from domain.file.file_schema import CreateFile, UpdateFile
from models import Nonlan, File_M, FileTemp_M
from sqlalchemy.orm import Session


def create_temp_file(db: Session, temp_file_create: CreateFile):
    db_temp_file = FileTemp_M(filename=temp_file_create.filename,
                              fileurl=temp_file_create.fileurl)
    db.add(db_temp_file)
    db.commit()

def create_file(db: Session, file_create: CreateFile):
    db_file = File_M(filename=file_create.filename,
                     fileurl=file_create.fileurl)
    db.add(db_file)
    db.commit()

def get_temp_file_info(db: Session, filename: str):
    return db.query(FileTemp_M).get(filename)

def get_file_info(db: Session, filename: str):
    return db.query(File_M).get(filename)



# 위키독스에서 댓글 수정 기능 참고하기

# 게시글을 수정할 때, 이미지를 추가하거나 삭제할 수 있기 때문에
# 게시글을 수정할 때 이미지도 수정 => 은 맞지 않는 것 같다
# 이미지 '수정' 이 아닌 '교체'
# update 기능은 임시 파일 -> 최종 파일 변경 시에만 적용
def create_file(db: Session, file_create: CreateFile, nonlan: Nonlan):
    db_file = File_M(nonlan=nonlan,
                     filename=file_create.filename,
                     fileurl=file_create.fileurl)


def delete_file(db: Session, db_file: FileTemp_M):
    db.delete(db_file)
    db.commit()

