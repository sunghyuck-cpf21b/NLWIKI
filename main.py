from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from domain.nonlan import nonlan_router
from domain.comment import comment_router
from domain.user import user_router
from domain.Sep_Program import sep_program_router
from domain.weeklymemo import weeklymemo_router
# from domain.image import image_router

app = FastAPI()

origins = [
    'http://http://127.0.0.1:8000',
]
#
#
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 라우터 객체 등록
app.include_router(nonlan_router.router)
app.include_router(comment_router.router)
app.include_router(user_router.router)
app.include_router(sep_program_router.router)
app.include_router(weeklymemo_router.router)
# app.include_router(image_router.router)


# 여기부터
app.mount('/assets', StaticFiles(directory='frontend/dist/assets'))
# index.html에서 참조하는 js, css파일의 경로가 /assets로 시작하는 경로로 참조하므로
# directory 경로를 /assets로 매핑한다.




@app.get('/')
def index():
    return FileResponse('frontend/dist/index.html')
# 여기까지
'''
프론트엔드 서버 없이도 사이트를 작동시키기 위한 단계이다
1. 프론트엔드 서버에서 npm run build 입력
2. dist 폴더 및 하위 파일(html, css, js)생성 확인
3. 백엔드 서버에서 참조할 정적 파일 경로를 위 함수에 대입
4. 이제 프론트엔드 서버 없이 백엔드 서버 만으로 사이트 동작 가능
http://127.0.0.1:8000/docs => 백엔드 api 체크
http://127.0.0.1:8000/ => 사이트
'''



'''
1. 프로그램 변경 작업하기
2. git add <파일명> 또는 git add * 명령 수행하기
3. git commit -m "커밋 코멘트" 명령 수행하기
4. git push 명령 수행하기
'''





