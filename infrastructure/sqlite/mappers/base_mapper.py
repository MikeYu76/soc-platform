from __future__ import annotations

import sqlite3
from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseMapper:
    """
    Shared mapping utilities for SQLite persistence.
    """

    @staticmethod
    def serialize(model: BaseModel) -> str:
        """
        Serialize a Pydantic model to JSON.
        """
        return model.model_dump_json()

    @staticmethod
    def deserialize(
        model_type: type[T],
        payload: str,
    ) -> T:
        """
        Deserialize a Pydantic model from JSON.
        """
        return model_type.model_validate_json(payload)

    @staticmethod
    def row_to_record(
        row: sqlite3.Row,
    ) -> dict[str, Any]:
        """
        Convert a sqlite3.Row into a plain dictionary.
        """
        return dict(row)

    @staticmethod
    def as_record(
        record: Mapping[str, Any],
    ) -> dict[str, Any]:
        """
        Return a mutable dictionary copy of a mapping.
        """
        return dict(record)
