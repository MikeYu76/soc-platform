from enum import StrEnum


class UserRole(StrEnum):
    ANALYST = "Analyst"
    SENIOR_ANALYST = "Senior Analyst"
    INCIDENT_RESPONDER = "Incident Responder"
    SOC_MANAGER = "SOC Manager"
    ADMINISTRATOR = "Administrator"
