from __future__ import annotations

from dataclasses import dataclass

from application.dto.base import Response
from common.event import Event


@dataclass(slots=True)
class GetEventResponse(Response):
    """
    Response returned when retrieving an event.
    """

    event: Event
