from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db import get_db
from models import User
from schemas.users import UserInDB, UserInResponse
from oauth2 import get_current_user
from routers.auth import hash
from exception import NewHTTPException

user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.post('/', response_model=UserInResponse)
async def create_user(user: UserInDB, db: Session = Depends(get_db)):
    if db.query(User).filter(User.name == user.name).first():
        raise NewHTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                               detail='Username already registered')

    new_user = User(username=user.username,
                    password=hash(password=user.password),
                    name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@user_router.get('/', response_model=UserInResponse)
async def get_user(current_user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    return UserInResponse.model_validate(current_user)


@user_router.put('/', response_model=UserInResponse)
async def update_user(user: UserInDB,
                      current_user: User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user.password != '':
        current_user.password = hash(password=user.password)
    current_user.name = user.name
    db.commit()
    db.refresh(current_user)
    return UserInResponse.model_validate(current_user)


@user_router.delete('/')
async def delete_user(current_user: User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    db.delete(current_user)
    db.commit()
    return None
