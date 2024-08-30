from fastapi import APIRouter

from app.schemas.users import UserCreate, UserRead, UserUpdate
from app.core.users import (
    SECRET,
    auth_backend,
    fastapi_users,
    google_oauth_client,
)
from app.core.config import settings

user_router = APIRouter(prefix='/users')

user_router.include_router(fastapi_users.get_users_router(
    UserRead, UserUpdate),
                           tags=['Users'])
user_router.include_router(fastapi_users.get_register_router(
    UserRead, UserCreate),
                           tags=['Users'])
user_router.include_router(fastapi_users.get_reset_password_router(),
                           tags=['Users'])

user_router.include_router(fastapi_users.get_verify_router(UserRead),
                           prefix='/auth',
                           tags=['Auth'])
user_router.include_router(fastapi_users.get_auth_router(auth_backend),
                           prefix='/auth/jwt',
                           tags=['Auth'])
user_router.include_router(fastapi_users.get_oauth_router(
    google_oauth_client,
    auth_backend,
    SECRET,
    settings.OAUTH_GOOGLE_BACKEND_REDIRECT_URI,
    associate_by_email=True,
    is_verified_by_default=True),
                           prefix='/auth/google',
                           tags=['Auth'])
user_router.include_router(
    fastapi_users.get_oauth_associate_router(google_oauth_client, UserRead,
                                             SECRET),
    prefix="/auth/associate/google",
    tags=['Auth'],
)
