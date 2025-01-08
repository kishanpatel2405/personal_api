import secrets
from typing import List, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings

from utils.enums import Environment


class Config(BaseSettings):
    ENVIRONMENT: Environment
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
        extra = "allow"
        case_sensitive = True

config = Config()
