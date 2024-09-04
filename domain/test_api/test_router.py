from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import Optional
from sqlalchemy.orm import Session
from starlette import status
import datetime

from database import get_db


router = APIRouter(
    prefix='/api/test'
)

@router.get('/just_test', status_code=status.HTTP_200_OK)
def just_test(db: Session = Depends(get_db)):
    return 'it is just test'

@router.post('/img_test', status_code=status.HTTP_200_OK)
async def img_test(file: UploadFile = File(None)):
    print('=============================================================================')
    print(file)
    content = await file.read()
    date = datetime.datetime.now()
    str_date = date.strftime('%Y%m%d%H%M%S') + f'{date.microsecond // 1000:03d}'
    print(str_date)

    filename = str_date + file.filename
    print('=============================================================================')
    with open(f'C:/NLWIKI_proj/myapi/domain/test_api/file_storage/{filename}', 'wb') as f:
        f.write(content)
    return file