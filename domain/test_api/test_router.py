from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db


router = APIRouter(
    prefix='/api/test'
)

@router.get('/just_test', status_code=status.HTTP_200_OK)
def just_test(db: Session = Depends(get_db)):
    return 'it is just test'