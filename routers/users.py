from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db import get_db
from models import User
from schemas.users import UserCreate, UserUpdate, UserResponse
from oauth2 import get_current_user
from routers.auth import hash, verify
from exception import NewHTTPException

user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.post('/', response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise NewHTTPException(status_code=status.HTTP_409_CONFLICT,
                               detail='Username already registered')
    new_user = User(username=user.username,
                    password=hash(password=user.password),
                    name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@user_router.get('/', response_model=UserResponse)
async def get_user(current_user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    return UserResponse.model_validate(current_user)


@user_router.put('/', response_model=UserResponse)
async def update_user(user: UserUpdate,
                      current_user: User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user.name:
        current_user.name = user.name
    if user.new_password:
        if not verify(user.current_password, current_user.password):
            raise NewHTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                   detail='Incorrect password')
        current_user.password = hash(user.new_password)
    db.commit()
    db.refresh(current_user)
    return UserResponse.model_validate(current_user)


@user_router.delete('/')
async def delete_user(current_user: User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    db.delete(current_user)
    db.commit()
    return None
