from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """
    Application configuration.

    Values may be overridden using environment variables.
    """

    model_config = SettingsConfigDict(
        env_prefix="SOC_",
        extra="ignore",
    )

    database_path: str = Field(
        default="soc_platform.db",
    )

    api_host: str = Field(
        default="127.0.0.1",
    )

    api_port: int = Field(
        default=8000,
    )

    debug: bool = Field(
        default=False,
    )

    opensearch_host: str = Field(
        default="localhost",
    )

    opensearch_port: int = Field(
        default=9200,
    )

    opensearch_use_ssl: bool = Field(
        default=False,
    )

    opensearch_index: str = Field(
        default="security-events",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns the application settings singleton.
    """
    return Settings()
