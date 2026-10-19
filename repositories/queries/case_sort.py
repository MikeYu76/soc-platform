from enum import StrEnum


class CaseSort(StrEnum):
    """
    Fields that cases can be sorted by.
    """

    CREATED_AT = "created_at"
    PRIORITY = "priority"
    STATUS = "status"
    ASSIGNED_TO = "assigned_to"
