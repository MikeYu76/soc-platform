class IngestionError(Exception):
    """Base exception for ingestion-related errors."""


class FileReadError(IngestionError):
    """Raised when an ingestion source cannot be read."""


class InvalidLogFormatError(IngestionError):
    """Raised when log data is malformed or unsupported."""