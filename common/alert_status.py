from enum import StrEnum


class AlertStatus(StrEnum):
    """
    Represents the current workflow state of an alert.

    Alert status is independent of severity.
    A CRITICAL alert may still be NEW, ACKNOWLEDGED,
    IN_PROGRESS, or CLOSED.
    """

    NEW = "NEW"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"
