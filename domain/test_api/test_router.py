from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse
from typing import Optional, List
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
    filename = str_date + file.filename
    print(filename)
    print('=============================================================================')
    with open(f'C:/NLWIKI_proj/myapi/frontend/media-server/public/{filename}', 'wb') as f:
        f.write(content)
    image_url = f'http://localhost:4000/{filename}'
    return image_url


@router.get('/html/{test}', status_code=status.HTTP_200_OK)
def test_page(test: str):
    return f'<h1>this is your text : {test}</h1>'