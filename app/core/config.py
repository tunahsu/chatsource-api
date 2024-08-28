from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    PORT: int = 8000
    RELOAD: bool = False
    OPENAPI_URL: Optional[str] = None
    DB_URL: str = 'sqlite:///./sqlite.db'
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    model_config = SettingsConfigDict(env_file='.env', case_sensitive=True)


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
