from abc import ABC, abstractmethod
from typing import Any


class BaseIngestor(ABC):
    """Abstract base class for all ingestion sources."""

    @abstractmethod
    def read_logs(self) -> list[dict[str, Any]]:
        """
        Read raw logs from the ingestion source.

        Returns:
            A list of raw log dictionaries.
        """
        raise NotImplementedError