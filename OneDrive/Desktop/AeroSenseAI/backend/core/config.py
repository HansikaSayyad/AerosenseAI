# backend/core/config.py

from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List
import os


class Settings(BaseSettings):
    """
    Central configuration class.
    Automatically loads values from .env file.
    All settings are validated by Pydantic.
    """

    # ─────────────────────────────────────────
    # APP SETTINGS
    # ─────────────────────────────────────────
    APP_NAME: str = "AirGuard AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # ─────────────────────────────────────────
    # DATABASE SETTINGS
    # ─────────────────────────────────────────
    DATABASE_URL: str

    # ─────────────────────────────────────────
    # JWT SECURITY SETTINGS
    # ─────────────────────────────────────────
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ─────────────────────────────────────────
    # AQI API SETTINGS
    # ─────────────────────────────────────────
    AQI_API_KEY: str
    AQI_BASE_URL: str = "https://api.waqi.info"

    # ─────────────────────────────────────────
    # CORS SETTINGS
    # ─────────────────────────────────────────
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v):
        """
        Allows ALLOWED_ORIGINS to be either:
        - A list: ["http://localhost:3000"]
        - A string: "http://localhost:3000"
        """
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# ─────────────────────────────────────────
# Create a single instance to use everywhere
# ─────────────────────────────────────────
settings = Settings()