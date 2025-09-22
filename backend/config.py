import os
from dotenv import load_dotenv

from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    # SQLITE #
    # DATABASE_URL = os.getenv('DB_LITE')
    # DATABASE_URL_FOR_ALEMBIC = os.getenv('DB_LITE_FOR_ALEMBIC')

    # PostgreSQL #
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DATABASE_URL_POSTGRE = os.getenv('ASYNC_DATABASE_URL_POSTGRE')
    DATABASE_URL_FOR_ALEMBIC_POSTGRE = os.getenv('DATABASE_URL_POSTGRE')

    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHM = os.getenv('ALGORITHM')

    LOGIN = os.getenv('LOGIN')
    PASSWORD = os.getenv('PASSWORD')


settings = Settings()


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}