from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Request:
    """
    Base class for application service requests.

    Shared application-level metadata (such as correlation IDs,
    tenant IDs, user context, or tracing information) belongs
    here rather than in domain models.
    """


@dataclass(slots=True)
class Response:
    """
    Base class for application service responses.
    """