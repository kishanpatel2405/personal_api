import logging

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from api.v1.router import api_router as api_v1_router
from celery_utils import create_celery
from config import config
from core.event_handlers import start_app_handler, stop_app_handler
from utils.enums import Environment
from utils.errors import ApiException
from utils.misc import get_project_meta

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_app() -> FastAPI:
    """Creates and configures the FastAPI application."""

    pkg_meta = get_project_meta("pyproject.toml")

    docs_url = None if config.ENVIRONMENT == Environment.PRODUCTION else "/docs"

    fast_app = FastAPI(
        title=config.PROJECT_NAME,
        version=pkg_meta["version"],
        debug=config.ENVIRONMENT != Environment.PRODUCTION,
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
        docs_url=docs_url,
    )

    add_pagination(fast_app)

    if config.BACKEND_CORS_ORIGINS:
        fast_app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in config.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    fast_app.include_router(api_v1_router, prefix="/api/v1")

    # fast_app.add_exception_handler(ApiException, api_exception_handler)

    fast_app.add_event_handler("startup", start_app_handler(fast_app))
    fast_app.add_event_handler("shutdown", stop_app_handler(fast_app))

    fast_app.config = config
    fast_app.celery_app = create_celery()

    logger.info(f"{config.PROJECT_NAME} version {pkg_meta['version']} is starting...")

    return fast_app


app = get_app()

celery = app.celery_app
