from __future__ import annotations

from dataclasses import dataclass

from application.dto.base import Request
from common.event import Event


@dataclass(slots=True)
class IngestEventRequest(Request):
    """
    Request for ingesting a normalized security event.
    """

    event: Event