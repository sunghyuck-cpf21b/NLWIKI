from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.comment import comment_schema, comment_crud
from domain.user.user_router import get_current_user
from domain.nonlan import nonlan_crud
from models import User

router = APIRouter(
    prefix="/api/comment"
)

@router.post("/create/{nonlan_id}", status_code=status.HTTP_204_NO_CONTENT)
def comment_create(nonlan_id: int,
                   _comment_create: comment_schema.CommentCreate,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    nonlan = nonlan_crud.get_nonlan(db, nonlan_id=nonlan_id)
    if not nonlan:
        raise HTTPException(status_code=404, detail="논란을 찾을 수 없습니다.")
    comment_crud.create_comment(db, nonlan=nonlan, comment_create=_comment_create, user=current_user)


@router.get("/detail/{comment_id}", response_model=comment_schema.Comment)
def comment_detail(comment_id: int, db: Session = Depends(get_db)):
    comment = comment_crud.get_comment(db, comment_id=comment_id)
    return comment

@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
def comment_delete(_comment_delete: comment_schema.CommentDelete,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    db_comment = comment_crud.get_comment(db, comment_id=_comment_delete.comment_id)
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if (current_user.id != db_comment.user.id) and (current_user.set_admin == False):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='삭제 권한이 없습니다.')
    comment_crud.delete_comment(db=db, db_comment=db_comment)