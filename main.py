import logging

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from api.v1.router import api_router as api_v1_router
from celery_utils import create_celery
from config import config
from core.event_handlers import start_app_handler, stop_app_handler
from utils.enums import Environment

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_app() -> FastAPI:
    docs_url = None if config.ENVIRONMENT == Environment.DEVELOPMENT else "/docs"

    fast_app = FastAPI(
        title=config.PROJECT_NAME,
        debug=config.ENVIRONMENT != Environment.DEVELOPMENT,
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

    return fast_app


app = get_app()

celery = app.celery_app
