"""Application settings loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_env: str = "development"
    debug: bool = False

    database_url: str = "postgresql+asyncpg://mhs:mhs@localhost:5432/mhs"
    database_url_sync: str = "postgresql://mhs:mhs@localhost:5432/mhs"

    redis_url: str = "redis://localhost:6379/0"

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    cors_origins: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
