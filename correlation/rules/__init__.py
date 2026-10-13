from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """
    Application configuration.

    This class centralizes configuration used throughout the
    application. Infrastructure and composition components
    should obtain configuration from here rather than embedding
    hard-coded values.
    """

    database_path: Path = Path("soc.db")

    debug: bool = False

    application_name: str = "SOC Platform"

    environment: str = "development"