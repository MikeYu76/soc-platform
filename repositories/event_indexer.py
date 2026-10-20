from __future__ import annotations

from typing import Protocol

from common.event import Event


class EventIndexer(Protocol):
    """Port for indexing normalized events in a search engine."""

    def index(self, event: Event) -> None:
        """Make an event searchable by its stable internal identifier."""
        ...
