from dataclasses import dataclass

from application.dto.base import Request


@dataclass(slots=True)
class IdentifierRequest(Request):
    """
    Request containing a resource identifier.
    """

    id: str
