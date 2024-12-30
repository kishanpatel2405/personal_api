from pydantic_settings import BaseSettings


class Config(BaseSettings):
    CELERY_BROKER_URL: str = "amqp://user:root@localhost:5672"
    CELERY_RESULT_BACKEND: str = "rpc://"


config = Config()
