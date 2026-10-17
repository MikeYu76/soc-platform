import json
from pathlib import Path
from typing import Any

from ingestion.base import BaseIngestor
from ingestion.exceptions import FileReadError, InvalidLogFormatError


class FileIngestor(BaseIngestor):
    """Reads raw logs from a JSON file."""

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)

    def read_logs(self) -> list[dict[str, Any]]:
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                logs = json.load(file)
        except OSError as exc:
            raise FileReadError(
                f"Unable to read file: {self.file_path}"
            ) from exc
        except json.JSONDecodeError as exc:
            raise InvalidLogFormatError(
                f"Invalid JSON in file: {self.file_path}"
            ) from exc

        if not isinstance(logs, list):
            raise InvalidLogFormatError(
                "Expected the JSON root to be a list of log objects."
            )

        if not all(isinstance(log, dict) for log in logs):
            raise InvalidLogFormatError(
                "Each log entry must be a JSON object."
            )

        return logs
