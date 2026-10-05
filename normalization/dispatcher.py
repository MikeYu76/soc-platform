from typing import Any

from common.event import Event
from normalization.registry import ParserRegistry


class Dispatcher:
    """
    Dispatches raw logs to the appropriate parser.
    """

    def __init__(self, registry: ParserRegistry) -> None:
        self._registry = registry

    def dispatch(
        self,
        log_source: str,
        raw_log: Any,
    ) -> Event:
        """
        Dispatch a raw log to the appropriate parser.
        """
        parser = self._registry.create(log_source)

        return parser.parse(raw_log)