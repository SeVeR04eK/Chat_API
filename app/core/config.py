from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timedelta
from pydantic import ValidationError

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    access_token_expire_minutes: timedelta = timedelta(minutes=15)
    refresh_token_expire_days: timedelta = timedelta(days=7)
    algorithm: str = 'HS256'

    model_config = SettingsConfigDict(env_file=str(BASE_DIR / ".env"), env_file_encoding="utf-8")


try:
    settings = Settings()
except ValidationError as e:
    raise ValueError(f"Missing required environment variables: {e}")
