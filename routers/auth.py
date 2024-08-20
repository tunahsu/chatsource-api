from fastapi import APIRouter, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from db import get_db
from models import User
from oauth2 import access_security, get_current_user, refresh_tokens, refresh_security
from schemas.users import Token, UserInResponse
from exception import NewHTTPException

auth_router = APIRouter(prefix='/auth', tags=['Auth'])
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash(password):
    return pwd_context.hash(secret=password)


def verify(password, hashed_password):
    return pwd_context.verify(secret=password, hash=hashed_password)


@auth_router.post('/login', response_model=Token)
def login(
        user_credentials: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.username == user_credentials.username).first()
    if not user:
        raise NewHTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid credentials')
    if not verify(user_credentials.password, user.password):
        raise NewHTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid Credentials')
    # create token
    payload_data = {'id': user.id}
    access_token = access_security.create_access_token(subject=payload_data)
    refresh_token = refresh_security.create_refresh_token(subject=payload_data)
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'refresh_token': refresh_token,
    }


@auth_router.get('/current', response_model=UserInResponse)
def get_curr_user(current_user: User = Depends(get_current_user)):
    return current_user


@auth_router.post('/refresh', response_model=Token)
def refresh(tokens: Token = Depends(refresh_tokens)):
    return tokens
