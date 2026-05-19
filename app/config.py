from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = 'EquitySaaS'
    DEBUG: bool = False
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    ALLOWED_ORIGINS: list[str] = ['http://localhost:3000']

    class Config:
        env_file = '.env'


settings = Settings()
