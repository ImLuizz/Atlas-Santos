from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable overrides."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # General
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    APP_NAME: str = Field(default="Atlas Santos API")
    APP_VERSION: str = Field(default="0.1.0")
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)

    # Security
    SECRET_KEY: SecretStr | None = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=1440)
    COOKIE_SECURE: bool = Field(default=True)
    COOKIE_SAMESITE: str = Field(default="lax")

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/atlas_santos"
    )
    DATABASE_ECHO: bool = Field(default=False)
    DATABASE_POOL_SIZE: int = Field(default=10)
    DATABASE_MAX_OVERFLOW: int = Field(default=20)

    # CORS
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000"]
    )

    # Storage (Railway Buckets / S3)
    STORAGE_BUCKET_NAME: str = Field(default="atlas-santos-media-dev")
    STORAGE_ENDPOINT_URL: str | None = None
    STORAGE_ACCESS_KEY_ID: SecretStr | None = None
    STORAGE_SECRET_ACCESS_KEY: SecretStr | None = None
    STORAGE_REGION: str | None = None

    # Operational Parameters (Configurable proposals)
    DEFAULT_PHOTO_QUOTA: int = Field(default=20)
    MAX_UPLOAD_SIZE_MB: int = Field(default=15)
    RESERVATION_TTL_MINUTES: int = Field(default=30)
    PRESIGNED_UPLOAD_TTL_MINUTES: int = Field(default=10)
    PRESIGNED_DOWNLOAD_TTL_MINUTES: int = Field(default=5)
    JOB_TIMEOUT_SECONDS: int = Field(default=300, gt=0)

    @field_validator("DATABASE_URL")
    @classmethod
    def normalize_database_driver(cls, value: str) -> str:
        scheme, separator, address = value.partition("://")
        if scheme in {"postgres", "postgresql"} and separator:
            return f"postgresql+psycopg://{address}"
        if scheme == "sqlite" and separator:
            return f"sqlite+aiosqlite://{address}"
        return value


settings = Settings()
