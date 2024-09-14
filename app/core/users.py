import uuid
from typing import Optional

from fastapi import Depends, Response, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_mail import MessageSchema, MessageType
from httpx_oauth.clients.google import GoogleOAuth2
from starlette.responses import JSONResponse, RedirectResponse

from app.core.db import User, get_user_db
from app.core.config import settings
from app.core.mailer import EmailSchema, fm, forgot_passwor_template

SECRET = settings.APP_SECRET

google_oauth_client = GoogleOAuth2(
    settings.OAUTH_GOOGLE_CLIENT_ID,
    settings.OAUTH_GOOGLE_CLIENT_SECRET,
)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self,
                                user: User,
                                request: Optional[Request] = None):
        print(f'User {user.id} has registered.')

    async def on_after_forgot_password(self,
                                       user: User,
                                       token: str,
                                       request: Optional[Request] = None):

        message = MessageSchema(subject='Forgot Password',
                                recipients=[user.email],
                                body=forgot_passwor_template.format(
                                    settings.APP_FRONTEND_URL, token),
                                subtype=MessageType.html)
        await fm.send_message(message)
        return JSONResponse(status_code=200,
                            content={'message': 'Email has been sent'})

    async def on_after_request_verify(self,
                                      user: User,
                                      token: str,
                                      request: Optional[Request] = None):
        print(
            f'Verification requested for user {user.id}. Verification token: {token}'
        )


async def get_user_manager(
        user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


cookie_transport = CookieTransport(cookie_max_age=3600, cookie_samesite='none')
auth_backend = AuthenticationBackend(
    name='cookie',
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)
