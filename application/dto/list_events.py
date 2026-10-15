from __future__ import annotations

from dataclasses import dataclass

from application.dto.base import (
    Request,
    Response,
)

from common.event import Event


@dataclass(slots=True)
class ListEventsRequest(Request):
    """
    Request to retrieve all persisted events.
    """


@dataclass(slots=True)
class ListEventsResponse(Response):
    """
    Response containing persisted events.
    """

    events: list[Event]