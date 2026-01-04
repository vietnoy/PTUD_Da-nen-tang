"""Application settings loaded from environment variables."""

from functools import lru_cache
from typing import Any, Dict, List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "Di Cho Tien Loi API"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "change-me"
    access_token_expires_minutes: int = 150
    refresh_token_expires_minutes: int = 60 * 24 * 7
    backend_cors_origins: str = "*"

    @property
    def cors_origins(self) -> List[str]:
        if self.backend_cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.backend_cors_origins.split(",")]

    database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/di_cho"
    redis_url: str = "redis://redis:6379/0"
    minio_endpoint: str = "minio:9000"
    minio_public_url: str = "http://localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "di-cho-media"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings instance."""
    return Settings()


settings = get_settings()


def settings_summary() -> Dict[str, Any]:
    """Expose safe subset of settings for diagnostics and docs."""
    return {
        "project_name": settings.project_name,
        "api_v1_prefix": settings.api_v1_prefix,
        "database_url": settings.database_url,
        "redis_url": settings.redis_url,
        "minio_endpoint": settings.minio_endpoint,
    }
