import logging
from typing import Callable

import boto3
import sib_api_v3_sdk
from fastapi import FastAPI
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker


from utils.misc import TokenBackend

logger = logging.getLogger(__name__)


async def _startup(app: FastAPI) -> None:
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = app.config.SENDINBLUE_API_KEY

    engine = create_engine(
        URL.create(
            drivername="postgresql+psycopg2",
            username=app.config.POSTGRES_USER,
            password=app.config.POSTGRES_PASSWORD,
            host=app.config.POSTGRES_HOST,
            port=5432,
            database=app.config.POSTGRES_DB,
        ).render_as_string(hide_password=False),
        pool_size=app.config.DB_POOL_SIZE,  # Database connections in the pool.
        max_overflow=app.config.DB_MAX_OVERFLOW,  # Additional connections beyond the pool size.
    )
    app.db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    app.token_backend = TokenBackend("HS256", app.config.SECRET_KEY, "", None, None, None, 0, None)
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
