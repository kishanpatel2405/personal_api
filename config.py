import secrets
from typing import List, Union

from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings

from utils.enums import Environment


class AirlineLogoConfig(BaseModel):
    url: str = "https://imgak.mmtcdn.com/flights/assets/media/dt/common/icons/"
    format: str = "png"


class Config(BaseSettings):
    ENVIRONMENT: Environment
    API_PREFIX: str = "/api/"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    APP_HOST: str
    APP_PORT: int

    JSON_LOGS: bool
    GUNICORN_WORKERS: int

    SENDINBLUE_API_KEY: str

    USER_EMAIL_VERIFICATION_TOKEN_EXPIRATION_TIME_IN_HOURS: int

    TEMPLATE_ID_OF_EMAIL_STRUCTURE_FOR_USER_EMAIL_VERIFICATION: int

    TEMPLATE_ID_OF_EMAIL_STRUCTURE_FOR_FORGOT_PASSWORD_EMAIL_VERIFICATION: int

    USER_FORGOT_PASSWORD_TOKEN_EXPIRATION_TIME_IN_HOURS: int
    TEMPLATE_ID_OF_E_TICKET_EMAIL_TEMPLATE: int
    TEMPLATE_ID_OF_E_TICKET_CANCELLATION_EMAIL_TEMPLATE: int

    GST_PERCENTAGE_ON_SERVICE_CHARGE: float
    NORMAL_USER_CANCELLATION_CHARGES: float
    ENTERPRISE_USER_CANCELLATION_CHARGES: float

    # FRONTEND_URL: str

    class Config:
        case_sensitive = True


config = Config()
