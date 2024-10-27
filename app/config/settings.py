from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS512"
    SECONDS_TO_EXPIRE: int = 604800
    REFERRAL_CODE_DAYS: int = 30

    title: str = "Referral API"
    summary: str = "Soon..."
    description: str = "Soon..."
    version: str = "1.0.0"
    contact: dict = {
        "name": "Selivanov Nikita",
        "email": "niki_landgelo@outlook.com",
        "url": "https://t.me/niki_landgelo",
    }

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
