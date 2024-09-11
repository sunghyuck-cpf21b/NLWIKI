from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import base64

from database import get_db
from domain.jff import jff_schema, jff_crud
from domain.user.user_router import get_current_user
from models import User

from starlette import status

router = APIRouter(
    prefix='/api/jff'
)


@router.get('/dot', response_model=jff_schema.DP)
def get_dotpaint(x: int, y: int,
                 db: Session = Depends(get_db)):
    data = jff_crud.get_dotpaint(db=db, x=x, y=y)
    return data

import os
here_abs_path = os.path.dirname(os.path.abspath(__file__))
DP_img_path = os.path.join(here_abs_path, 'DP', 'now_image.png')
@router.get('/dp_image', status_code=status.HTTP_200_OK)
def get_dp_image(current_user: User = Depends(get_current_user)):
    with open(DP_img_path, 'rb') as img:
        encoded_string = base64.b64encode(img.read()).decode('utf-8')
    return JSONResponse(content={'image_data': encoded_string, 'x_limit': jff_crud.x_limit, 'y_limit': jff_crud.y_limit})
    # return FileResponse(DP_img_path, media_type='image/png')


@router.post('/create_dot', status_code=status.HTTP_200_OK)
def create_dot(create_data: jff_schema.DPCreate,
               db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    print(create_data)
    if (create_data.x < 0) or (create_data.y < 0) or (jff_crud.x_limit < create_data.x) or (jff_crud.y_limit < create_data.y):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='픽셀 범위를 벗어났습니다.')
    data = jff_crud.create_dotpaint(db=db, create_data=create_data, name=DP_img_path, user=current_user)
    return data

