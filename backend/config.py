import os
from dotenv import load_dotenv

from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    DATABASE_URL = os.getenv('DB_LITE')
    DATABASE_URL_FOR_ALEMBIC = os.getenv('DB_LITE_FOR_ALEMBIC')
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHM = os.getenv('ALGORITHM')

    LOGIN = os.getenv('LOGIN')
    PASSWORD = os.getenv('PASSWORD')


settings = Settings()


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}