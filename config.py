import secrets

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    API_PREFIX: str = "/api/"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    PROJECT_NAME: str

    DB_POOL_SIZE: int
    DB_MAX_OVERFLOW: int

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    APP_HOST: str
    APP_PORT: int

    class Config:
        env_file = ".env"
        case_sensitive = True


config = Config()



