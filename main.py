from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from api.v1.router import api_router as api_v1_router
from celery_utils import create_celery
from config import config
from core.error_handlers import api_exception_handler
from core.event_handlers import start_app_handler, stop_app_handler
from utils.enums import Environment
from utils.errors import ApiException
from utils.misc import get_project_meta
import logging

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Function to initialize the app
def get_app() -> FastAPI:
    """Creates and configures the FastAPI application."""

    pkg_meta = get_project_meta("pyproject.toml")

    # Setup dynamic docs URL based on environment
    docs_url = None if config.ENVIRONMENT == Environment.PRODUCTION else "/docs"

    # Initialize FastAPI app with dynamic settings
    fast_app = FastAPI(
        title=config.PROJECT_NAME,
        version=pkg_meta["version"],
        debug=config.ENVIRONMENT != Environment.PRODUCTION,
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
        docs_url=docs_url,
    )

    # Add pagination support globally
    add_pagination(fast_app)

    # CORS Middleware to allow frontend to interact
    if config.BACKEND_CORS_ORIGINS:
        fast_app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in config.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Include API v1 router for versioned endpoints
    fast_app.include_router(api_v1_router, prefix="/api/v1")

    # Exception Handling
    fast_app.add_exception_handler(ApiException, api_exception_handler)

    # Start and stop app event handlers (startup/shutdown)
    fast_app.add_event_handler("startup", start_app_handler(fast_app))
    fast_app.add_event_handler("shutdown", stop_app_handler(fast_app))

    # Attach configuration and Celery instance to the app
    fast_app.config = config
    fast_app.celery_app = create_celery()

    logger.info(f"{config.PROJECT_NAME} version {pkg_meta['version']} is starting...")

    return fast_app


# Create the FastAPI app instance
app = get_app()

# Celery instance for background tasks
celery = app.celery_app