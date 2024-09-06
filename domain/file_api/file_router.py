from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from starlette import status
import datetime

from PIL import Image
from io import BytesIO

import os

from database import get_db

router = APIRouter(
    prefix='/api/file'
)

here_abs_path = os.path.dirname(os.path.abspath(__file__))
media_public = os.path.join(here_abs_path, '..', '..', 'frontend', 'media-server', 'public')
print(media_public)
@router.post('/img', status_code=status.HTTP_200_OK)
async def upload_image(file: UploadFile = File(None)):
    img_data = await file.read()
    date = datetime.datetime.now()
    str_date = date.strftime('%Y%m%d%H%M%S') + f'{date.microsecond // 1000:03d}'
    filename = str_date + file.filename
    with open(media_public+'/'+filename, 'wb') as f:
        f.write(img_data)

    img_data_for_size = Image.open(BytesIO(img_data))
    width, height = img_data_for_size.size
    print(width, height)
    ''' 위 코드는 배포용, 아래 코드는 개발용 '''
    image_url = f'https://nlwk.nlwiki.com/media/{filename}'
    # image_url = f'http://localhost:4000/{filename}'
    return {'image_url': image_url, 'width': width, 'height': height}

