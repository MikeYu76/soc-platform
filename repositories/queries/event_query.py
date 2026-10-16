from __future__ import annotations

from pydantic import Field, IPvAnyAddress

from common.event_types import EventType

from repositories.queries.base import Query
from repositories.queries.event_sort import EventSort
from repositories.queries.sort_order import SortOrder


class EventQuery(Query):
    """
    Search criteria for event repositories.
    """

    event_type: EventType | None = None
    hostname: str | None = None
    username: str | None = None

    source_ip: IPvAnyAddress | None = None
    destination_ip: IPvAnyAddress | None = None

    log_source: str | None = None

    sort_by: EventSort = EventSort.TIMESTAMP
    order: SortOrder = SortOrder.DESC

    