from enum import StrEnum


class CasePriority(StrEnum):
    """
    Represents the operational priority of a case.
    """

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"