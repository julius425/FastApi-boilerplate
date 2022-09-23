import os
from typing import List

from fastapi_jwt_auth import AuthJWT
from fastapi_mail import ConnectionConfig
from pydantic import BaseSettings
from pydantic.networks import AnyHttpUrl


class Settings(BaseSettings):
    SECRET_KEY: str = 'somekey'
    ROOT_DIR: str = os.path.dirname(os.path.abspath('app'))
    MEDIA_PATH: str = 'media/'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    POSTGRES_HOST: str = 'localhost'
    POSTGRES_USER: str = ''
    POSTGRES_PASSWORD: str = ''
    POSTGRES_DB: str = ''

    MAIL_USERNAME: str = ''
    MAIL_PASSWORD: str = ''
    MAIL_FROM: str = ''
    MAIL_PORT: int = 587
    MAIL_SERVER: str = 'smtp.gmail.com'
    MAIL_FROM_NAME: str = 'TestName'
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    authjwt_secret_key: str = 'secretkey'

    @property
    def TORTOISE_MODELS(self):
        from app.core.utils.core import get_models_files
        return get_models_files()

    @property
    def DATABASE_URL(self):
        return f'postgres://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}' f'@db:5432/{self.POSTGRES_DB}'

    class Config:
        env_file = ".env"


settings = Settings()


mail_conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_TLS=settings.MAIL_TLS,
    MAIL_SSL=settings.MAIL_SSL,
    USE_CREDENTIALS=True
)


@AuthJWT.load_config
def get_config():
    return settings
