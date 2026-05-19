from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from .env."""

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    APP_NAME: str = 'EquitySaaS'
    DEBUG: bool = False
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    GOOGLE_REDIRECT_URI: str | None = None
    ALLOWED_ORIGINS: list[str] = Field(default_factory=lambda: ['http://localhost:3000'])


settings = Settings()
