"""Versioned PostgreSQL schema migrations."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Migration:
    """One forward-only PostgreSQL schema change."""

    version: str
    statements: tuple[str, ...]
