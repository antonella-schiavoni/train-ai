"""Application configuration using environment variables."""

import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    # Server Configuration
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALLOWED_HOSTS: List[str] = ["*"]

    # AI/ML Configuration
    MODEL_PATH: str = "./models"
    MAX_BATCH_SIZE: int = 32
    UPLOAD_DIR: str = "./uploads"

    # Logging
    LOG_LEVEL: str = "INFO"

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI FastAPI Project"
    VERSION: str = "0.1.0"


# Create global settings instance
settings = Settings()
