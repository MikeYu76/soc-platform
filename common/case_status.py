from enum import StrEnum


class CaseStatus(StrEnum):
    """
    Represents the lifecycle of a security investigation.
    """

    NEW = "NEW"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"