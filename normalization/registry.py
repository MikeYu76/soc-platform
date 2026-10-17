from collections.abc import Callable

from normalization.base import BaseParser
from normalization.exceptions import DuplicateParserError, ParserNotFoundError


class ParserRegistry:
    """
    Registry for parser factories.
    """

    def __init__(self) -> None:
        self._factories: dict[str, Callable[[], BaseParser]] = {}

    def register(
        self,
        log_source: str,
        factory: Callable[[], BaseParser],
    ) -> None:
        """
        Register a parser factory for a log source.
        """
        if log_source in self._factories:
            raise DuplicateParserError(
                f"Parser already registered for '{log_source}'."
            )

        self._factories[log_source] = factory

    def create(self, log_source: str) -> BaseParser:
        """
        Create a parser for the requested log source.
        """
        try:
            factory = self._factories[log_source]
        except KeyError as exc:
            raise ParserNotFoundError(
                f"No parser registered for '{log_source}'."
            ) from exc

        return factory()
