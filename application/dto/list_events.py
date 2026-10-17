from __future__ import annotations

from dataclasses import dataclass, field

from application.dto.base import Request, Response
from common.event import Event
from repositories.queries.event_query import EventQuery


@dataclass(slots=True)
class ListEventsRequest(Request):
    """
    Request to retrieve persisted events.
    """

    query: EventQuery = field(
        default_factory=EventQuery,
    )


@dataclass(slots=True)
class ListEventsResponse(Response):
    """
    Response containing persisted events.
    """

    events: list[Event]
