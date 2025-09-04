from pathlib import Path

from pydantic_settings import BaseSettings

from config.gunicorn import GunicornSettings
from config.postgres import PostgresSettings

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    postgres: PostgresSettings
    gunicorn: GunicornSettings

    class Config:
        env_file = BASE_DIR / ".env"
        case_sensitive = False
        env_nested_delimiter = "__"


settings = Settings()
