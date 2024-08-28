from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import InvalidRequestError
from starlette.config import Config

config = Config('.env')
SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)   # 커넥션 풀
'''
1. 연결 재사용: 커넥션 풀은 데이터베이스에 연결된 커넥션을 미리 만들어두고 이를 재사용함으로써 연결 속도를 향상시킵니다. 이렇게 함으로써 매번 연결을 맺고 끊는 데 드는 오버헤드를 줄일 수 있습니다.
2. 동시성 제어: 커넥션 풀은 동시에 여러 요청이 들어왔을 때 각각의 요청이 별도의 커넥션을 사용하도록 보장하여 데이터베이스의 동시성을 관리합니다. 이를 통해 데이터베이스의 부하를 분산시키고 성능을 최적화할 수 있습니다.
3. 자원 관리:션 풀은 데이터베이스 연결을 효율적으로 관리하여 자원을 절약합니다. 연결이 더 이상 필요하지 않을 때는 커넥션을 닫고 재활용하거나 반환하여 데이터베이스 자원을 최적화합니다.
'''

class ReadOnly(Session):
    def commit(self):
        raise InvalidRequestError("읽기 전용 파일입니다.")
    def flush(self, *args, **kwargs):
        raise InvalidRequestError("읽기 전용 파일입니다.")


SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind = engine)
SessionLocal_read = sessionmaker(autocommit = False, autoflush = False, bind = engine, class_=ReadOnly)

'''
autoflush : 세션 객체가 변경 사항이 발생할 때 마다 데이터베이스에 자동으로 반영된다. 변경 사항이 발생하는 시점에는 세션이 데이터베이스에 대한 쿼리를 실행하여 변경 사항을 반영한다.
비활성화 시에는 명시적으로 commit() 메소드를 호출하여 변경 사항을 데이터베이스에 반영해야 한다.

bind : 데이터베이스와의 세션을 설정할 때 사용된다. 세션을 특정 데이터베이스와 연결할 수 있다.
bind 옵션에 전달할 수 있는 값들
- 엔진 객체 : 엔진 객체를 전달하여 세션을 특정 데이터베이스와 연결할 수 있다.(engine)
- 연결 문자열 : 데이터베이스에 연결하기 위한 연결 문자열을 전달할 수 있다. sqlalchemy는 연결 문자열을 사용하여 엔진 객체를 생성하고 세션을 해당 엔진과 연결한다.(SQLALCHEMY_DATABASE_URL)
'''

Base = declarative_base()
# 객체 관계 매핑(ORM)을 사용하여 데이터베이스 모델을 정의할 떄 사용되는 중요한 기능이다.
# ORM을 통해 데이터베이스 테이블을 정의하는데 도움이 된다.
'''
1. 테이블 정의: SQLAlchemy의 클래스를 사용하여 데이터베이스 테이블을 정의할 수 있습니다. 클래스의 각 속성은 데이터베이스의 열을 나타내며, 클래스는 테이블의 이름과 매핑됩니다.
2. ORM 매핑: declarative_base()로 생성된 클래스는 데이터베이스 테이블과 객체를 매핑하여 데이터베이스 레코드를 객체로 쉽게 다룰 수 있도록 합니다. 이를 통해 개발자는 SQL 쿼리 대신 Python 객체를 사용하여 데이터베이스와 상호작용할 수 있습니다.
3. 상속 관계 지원: declarative_base()로 생성된 클래스는 상속을 지원하므로 객체 지향 프로그래밍의 기능을 활용하여 데이터베이스 모델을 정의할 수 있습니다.
'''


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata = MetaData(naming_convention=naming_convention)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def read_only_db():
    db = SessionLocal_read()
    try:
        yield db
    finally:
        db.close()