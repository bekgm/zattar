"""
Application configuration management
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings with environment variables"""

    # App
    APP_NAME: str = "Zattar"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/zattar"
    DATABASE_ECHO: bool = False

    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_CACHE_EXPIRE: int = 3600  # 1 hour

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # S3
    S3_BUCKET_NAME: str = "zattar-images"
    S3_REGION: str = "us-east-1"
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_ENDPOINT_URL: Optional[str] = None

    # Security
    ALLOWED_ORIGINS: list = ["http://localhost:9000", "http://localhost:3000"]
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 15

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # File Upload
    MAX_IMAGE_SIZE_MB: int = 10
    ALLOWED_IMAGE_EXTENSIONS: list = ["jpg", "jpeg", "png", "webp"]
    MAX_IMAGES_PER_LISTING: int = 10

    # Email
    RESEND_API_KEY: str = "re_4cYcE7DH_PE6cZxk1bt1hGD16xwA3uvZw"
    FROM_EMAIL: str = "noreply@zattar.com"
    APP_URL: str = "http://localhost:9000"

    # Verification
        env_file = ".env"
        case_sensitive = True


settings = Settings()
