from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class UserCreate(BaseModel):
    username: str
    password1: str
    password2: str

    @field_validator('username', 'password1', 'password2')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('값을 입력해주세요')
        return v

    @field_validator('password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다.')
        return v

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str


class User(BaseModel):
    id: int
    username: str
    set_admin: bool | None

