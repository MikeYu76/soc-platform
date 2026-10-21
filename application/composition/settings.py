from functools import lru_cache
from typing import Literal

from dotenv import load_dotenv
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """Application configuration from defaults and SOC_ environment variables."""

    model_config = SettingsConfigDict(env_prefix="SOC_", extra="ignore")

    database_backend: Literal["sqlite", "postgresql"] = "sqlite"
    database_path: str = Field(default="soc_platform.db")
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_database: str = "soc_platform"
    postgres_user: str = "soc_platform"
    postgres_password: SecretStr = SecretStr("")
    api_host: str = Field(default="127.0.0.1")
    api_port: int = Field(default=8000)
    debug: bool = Field(default=False)
    opensearch_host: str = Field(default="localhost")
    opensearch_port: int = Field(default=9200)
    opensearch_use_ssl: bool = Field(default=False)
    opensearch_index: str = Field(default="security-events")
    opensearch_enabled: bool = False
    opensearch_username: str = "admin"
    opensearch_password: SecretStr = SecretStr("")
    opensearch_verify_certs: bool = True
    opensearch_outbox_alert_pending_threshold: int = Field(default=100, gt=0)
    opensearch_outbox_alert_sustained_seconds: int = Field(default=300, gt=0)
    jwt_secret: SecretStr = Field(default=SecretStr(""))
    access_token_expire_minutes: int = Field(default=30, gt=0)
    bootstrap_admin_username: str | None = None
    bootstrap_admin_password: SecretStr | None = None


@lru_cache
def get_settings() -> Settings:
    """Returns the application settings singleton."""
    return Settings()
