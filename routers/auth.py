import requests

from fastapi import APIRouter, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from db import get_db
from models import User
from oauth2 import access_security, refresh_tokens, refresh_security
from config import settings
from schemas.users import Token
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


@auth_router.post('/refresh', response_model=Token)
def refresh(tokens: Token = Depends(refresh_tokens)):
    return tokens


@auth_router.get('/google/login')
async def login_google():
    return {
        'url':
        f'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline'
    }


@auth_router.get('/google')
async def auth_google(code: str, db: Session = Depends(get_db)):
    token_url = 'https://accounts.google.com/o/oauth2/token'
    data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get('access_token')
    user_info = requests.get('https://www.googleapis.com/oauth2/v1/userinfo',
                             headers={
                                 'Authorization': f'Bearer {access_token}'
                             }).json()
    user = db.query(User).filter(User.username == user_info['email']).first()
    if not user:
        user = User(username=user_info['email'],
                    password=hash(user_info['email']),
                    name=user_info['name'])
        db.add(user)
        db.commit()
        db.refresh(user)
    # create token
    payload_data = {'id': user.id}
    access_token = access_security.create_access_token(subject=payload_data)
    refresh_token = refresh_security.create_refresh_token(subject=payload_data)
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'refresh_token': refresh_token
    }
