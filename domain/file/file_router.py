from hashlib import sha256
import os

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile

from database import get_db
from domain.file import file_schema, file_crud

from starlette import status

from models import FileTemp_M, File_M, Nonlan


router = APIRouter(
    prefix="/api/file",
)


# params에는 db: Session 을 제외한 다른 매개변수에 해당하는 값들이 들어간다고 생각하면 될 듯 하다.

# <db에서 파일에 대한 데이터(이름, url) 가져오기 시작>
@router.get("/temp_info/{filename}", response_model=file_schema.File_S)
def get_temp_file(filename: str, db: Session = Depends(get_db)):
    _file = file_crud.get_temp_file_info(db, filename=filename)
    return _file

@router.get("/info/{filename}", response_model=file_schema.File_s)
def get_file(filename: str, db: Session = Depends(get_db)):
    _file = file_crud.get_file_info(db, filename=filename)
# <끝>


# <파일 임시 및 최종 업로드 시작>
@router.post("/temp_upload")
def temp_file_upload(db: Session = Depends(get_db), file: UploadFile = File(...)):
    file_data = file.read()
    filename_by_hash = sha256(file_data).hexdigest()
    temp_file_path = f'C:/NLWIKI_proj/myapi/file_db/temp/{filename_by_hash}'

    file_list = [name for name in db.execute(select(FileTemp_M.filename))]
    if filename_by_hash not in file_list:
        with open(temp_file_path, 'wb') as f:
            f.write(file_data)
        db_temp_file = FileTemp_M(filename=filename_by_hash, fileurl=temp_file_path)
        db.add(db_temp_file)
        db.commit()
    return {'filename': filename_by_hash, 'fileurl': temp_file_path}
'''
'사진' 을 클릭하면 새 창을 열고, 이미지 선택 후 '확인'을 누르면 임시 업로드
그리고 
'''

@router.post("/upload")
def file_upload(filename_by_hash: str, db: Session = Depends(get_db)):
    temp_file_path = f'C:/NLWIKI_proj/myapi/file_db/temp/{filename_by_hash}'
    file_path = f'C:/NLWIKI_proj/myapi/file_db/temp/{filename_by_hash}'

    temp_file_list = [name for name in db.execute(select(FileTemp_M.filename))]
    file_list = [name for name in db.execute(select(File_M.filename))]
    if ((filename_by_hash in temp_file_list)) and (filename_by_hash not in file_list):
        with open(temp_file_path, 'rb') as f_temp:
            file_content = f_temp.read()
        with open(file_path, 'wb') as f:
            f.write(file_content)
    elif filename_by_hash not in temp_file_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="업로드되지 않은 이미지입니다.")

    db_file = File_M(filename=filename_by_hash, fileurl=file_path)
    db.add(db_file)
    db.commit()
    os.remove(temp_file_path)
# <끝>

'''
from hashlib import sha256

def generate_filename(file_contents):
    # 파일 내용의 해시값 계산
    file_hash = sha256(file_contents).hexdigest()
    # 일부분을 파일 이름으로 사용
    filename = f"{file_hash[:10]}_{file_hash[-10:]}.jpg"  # 예시: 앞뒤로 10자리씩 사용
    return filename


파일의 내용에 따라 이름을 만들어주는 기능


중복검사를 하여 파일 내용이 동일하다면 또 업로드되지 않도록 방지해주는 코드를 작성할것
예 : 
2020년 2월 3일에 A 이미지파일 업로드
2024년 3월 1일에 A 이미지파일이 다른 게시글에서 업로드됨
=> 이미지가 중복되어 올라가지 않게 하고, 2020년2월3일에 이미 업로드된 A 이미지파일을 다시 불러와 
2024년3월1일에 작성된 게시글에 표시될 수 있도록 하기

=> 디렉토리 관리에 더 좋은 방법
'''