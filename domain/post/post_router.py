from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from domain.post import post_schema, post_crud
from domain.user.user_router import get_current_user
from models import User

from starlette import status

router = APIRouter(
    prefix="/api/post",
)

# response_model : API 엔드포인트에서 반환하는 응답의 형식을 지정하는데 사용된다. FastAPI에서자동 생성되는 API 문서 및 데이터 유효성 검사를 위해 중요한 역할을 한다.
# 엔드포인트 : url 경로(여기서는 "/list")
# response_model에 값으로 입력된 모델을 사용하여 응답의 형식을 정의 및 검사한다. 그리고 API 문서에 해당 형식이 표시된다.
@router.get("/list", response_model=post_schema.PostList)
def post_list(db: Session = Depends(get_db), page: int = 0, size: int = 10, keyword: str = ''):     # db 객체에 get_db 제네레이터에 의해 생성된 세션 객체 주입
    total, _post_list = post_crud.get_post_list(
        db, skip=page*size, limit=size, keyword=keyword
    )
    return {'total': total, 'post_list': _post_list}
    # return 값은 dictionary 형식으로
    # API에서 받는 형식이 dictionart 이기 때문
'''
기존 라우터에서는 with 방식을 사용하여 열고 닫았는데, post_crud에서 가져온 get_post_list 함수에는 with 문이 없다
이유가 뭘까?
'''

# params는 db 매개변수 이외의 것들을 생각하면 될 듯 하다.

# get의 프론트엔드 동작
# fastapi = (operation, url, params, success_callback, failure_callback)
# operation : get / url : "/detail/{post_id}" / params : 단순 read 이므로 별도의 매개변수 없음(post_id를 입력해야 하지만 router.get 특성으로 인해 생략)
# s_callback : 응답 내용으로 response_model의 schema에 따라 내용 전달, 응답을 받는 프론트엔드 측 에서는 딕셔너리 형태로 받아올 데이터를 지정한다
# => let post = {comments:[], content: '', person: '', occ_date: '', image: ''} => schema의 내용에 맞게 key를 구성한다
# url에 작성된 post_id 값이 router.get 메소트의 특성으로 인해 post_detail 함수의 post_detail 매개변수에 자동적으로 매칭된다.
@router.get("/detail/{post_id}", response_model=post_schema.Post)
def post_detail(post_id: int, db: Session = Depends(get_db)):
    post = post_crud.get_post(db, post_id=post_id)
    print(post)
    return post
'''
파일을 가져오기 위해 입력해야 할 매개변수는 
'''

# post의 프론트엔드 동작
# fastapi = (operation, url, params, success_callback, failure_callback)
# operation : post / url : "/create" / params : _post_create에 매칭된 스키마에 따른 데이터들
# s_callback : status_code를 응답으로 전달
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def post_create(_post_create: post_schema.PostCreate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    post_crud.create_post(db=db, post_create=_post_create,
                              user=current_user)



@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def post_delete(_post_delete: post_schema.PostDelete,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_post = post_crud.get_post(db, post_id=_post_delete.post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="해당 논란을 찾을 수 없습니다.")
    if (current_user.id != db_post.user.id) and (current_user.set_admin == False):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='삭제 권한이 없습니다.')
    post_crud.delete_post(db=db, db_post=db_post)
'''
논란 삭제 스키마의 id 값을 이용해 삭제할 논란의 내용을 get_post 함수로 찾아줌
해당 내용이 데이터베이스에 있는지 확인하고
최종적으로 데이터베이스에서 논란을 삭제
'''

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def post_update(_post_update: post_schema.PostUpdate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_post = post_crud.get_post(db, post_id=_post_update.post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    elif (current_user.id != db_post.user.id) and (current_user.set_admin == False):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='수정 권한이 없습니다.')
    post_crud.update_post(db=db, db_post=db_post, post_update=_post_update)