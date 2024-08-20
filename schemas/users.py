from typing import Optional
from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    id: int

    class Config:
        from_attributes = True
        from_orm = True


class BaseInDBModel(BaseModel):

    class Config:
        from_attributes = True


class UserInDB(BaseInDBModel):
    username: str
    password: str
    name: str


class UserInResponse(BaseResponseModel):
    username: str
    name: str


class UserInLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class TokenPayload(BaseModel):
    id: Optional[int]

    class Config:
        from_attributes = True
