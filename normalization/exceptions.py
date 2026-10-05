"""
Custom exceptions for the normalization package.
"""


class NormalizationError(Exception):
    """Base exception for all normalization errors."""


class ParserNotFoundError(NormalizationError):
    """Raised when no parser is registered for a log source."""


class DuplicateParserError(NormalizationError):
    """Raised when attempting to register a parser more than once."""