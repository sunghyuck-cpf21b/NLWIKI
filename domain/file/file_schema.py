import datetime

from pydantic import BaseModel, field_validator

class CreateFile(BaseModel):
    filename: str
    fileurl: str



class FileTemp_s(BaseModel):
    id: int
    filename: str
    fileurl: str

class File_s(BaseModel):
    id: int
    filename: str
    fileurl: str
    nonlan_id: int



class UpdateFile(CreateFile):        # 이미지를 임시 폴더에서 최종 폴더로 옮길 때 사용
    file_id: int

class DeleteFile(BaseModel):        # 논란 작성 시 임시저장된 이미지 삭제(db에서도 삭제해야 하기 때문에) 또는 논란 삭제 시에 모두 사용
    filename: str


