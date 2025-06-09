"""Application configuration using environment variables."""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    # Required fields - MUST be in .env file
    OLLAMA_BASE_URL: str
    SECRET_KEY: str

    # Optional fields with sensible defaults
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False

    # Ollama settings with defaults
    OLLAMA_DEFAULT_MODEL: str = "llama3"
    OLLAMA_TIMEOUT: int = 30
    OLLAMA_MAX_RETRIES: int = 3

    # Other optional settings
    ALLOWED_HOSTS: str = "*"
    MODEL_PATH: str = "./models"
    MAX_BATCH_SIZE: int = 32
    UPLOAD_DIR: str = "./uploads"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI FastAPI Project"
    VERSION: str = "0.1.0"
    MAX_PROMPT_LENGTH: int = 2000
    DEFAULT_TEMPERATURE: float = 0.7


# Create global settings instance
settings = Settings()
