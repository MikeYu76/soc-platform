from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApplicationSettings:
    """
    Application configuration.

    This object centralizes application configuration so the
    composition root can construct infrastructure and services
    without scattering configuration throughout the codebase.
    """

    database_path: str = "soc.db"