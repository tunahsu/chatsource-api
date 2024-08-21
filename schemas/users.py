from typing import Optional
from pydantic import BaseModel


class BaseDBModel(BaseModel):

    class Config:
        from_attributes = True


class BaseResponseModel(BaseModel):
    id: int

    class Config:
        from_attributes = True
        from_orm = True


class UserCreate(BaseDBModel):
    username: str
    password: str
    name: str


class UserUpdate(BaseDBModel):
    password: str
    name: str


class UserResponse(BaseResponseModel):
    username: str
    name: str


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class TokenPayload(BaseModel):
    id: Optional[int]

    class Config:
        from_attributes = True
