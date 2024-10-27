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
    summary: str = ("A comprehensive API for user referral management, "
                    "enabling unique referral codes, and tracking.")
    description: str = (
        "The Referral API is designed to manage user referral systems, "
        "offering features for creating, validating, and managing unique "
        "referral codes. This API allows users to generate referral links, "
        "and track successful referrals. Key features include:\n\n"
        "- **User Registration & Authentication**: Secure user authentication "
        "with JWT tokens.\n"
        "- **Referral Code Generation**: Create unique codes for users to "
        "share with others.\n"
        "- **Referral Tracking**: Track successful referrals and manage "
        "reward distribution.\n"
        "Ideal for applications that aim to incentivize user growth through "
        "a referral system."
    )
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
