from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.comment import comment_schema, comment_crud
from domain.nonlan import nonlan_crud

router = APIRouter(
    prefix="/api/comment"
)

@router.post("/create/{nonlan_id}", status_code=status.HTTP_204_NO_CONTENT)
def comment_create(nonlan_id: int,
                   _comment_create: comment_schema.CommentCreate,
                   db: Session = Depends(get_db)):
    nonlan = nonlan_crud.get_nonlan(db, nonlan_id=nonlan_id)
    if not nonlan:
        raise HTTPException(status_code=404, detail="논란을 찾을 수 없습니다.")
    comment_crud.create_comment(db, nonlan=nonlan, comment_create=_comment_create)


@router.get("/detail/{comment_id}", response_model=comment_schema.Comment)
def comment_detail(comment_id: int, db: Session = Depends(get_db)):
    comment = comment_crud.get_comment(db, comment_id=comment_id)
    return comment

