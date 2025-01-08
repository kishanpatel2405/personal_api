import logging
from typing import Callable

import sib_api_v3_sdk
from fastapi import FastAPI
from pydantic_settings import BaseSettings
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    DB_POOL_SIZE: int
    DB_MAX_OVERFLOW: int

    # SECRET_KEY: str

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()


async def _startup(app: FastAPI) -> None:
    configuration = sib_api_v3_sdk.Configuration()

    engine = create_engine(
        URL.create(
            drivername="postgresql+psycopg2",
            username=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=5432,
            database=settings.POSTGRES_DB,
        ).render_as_string(hide_password=False),
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
    )
    app.db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    app.sendinblue_api_client = sib_api_v3_sdk.ApiClient(configuration)


def _shutdown(app: FastAPI) -> None:
    if hasattr(app, "db_session"):
        app.db_session.close_all()


def start_app_handler(app: FastAPI) -> Callable:
    async def startup() -> None:
        logger.info("Running app start handler.")
        await _startup(app)

    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info("Running app shutdown handler.")
        _shutdown(app)

    return shutdown
