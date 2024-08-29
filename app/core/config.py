from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    APP_PORT: int = 8000
    APP_RELOAD: bool = False
    APP_OPENAPI_URL: Optional[str] = None
    APP_DB_URL: str = 'sqlite:///./sqlite.db'
    APP_SECRET: str
    
    OAUTH_GOOGLE_CLIENT_ID: str
    OAUTH_GOOGLE_CLIENT_SECRET: str
    OAUTH_GOOGLE_REDIRECT_URI: str
    
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 465
    MAIL_SERVER: str = 'smtp.gmail.com'
    MAIL_FROM_NAME: str = 'Chatsource'
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    
    model_config = SettingsConfigDict(env_file='.env', case_sensitive=True)


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
