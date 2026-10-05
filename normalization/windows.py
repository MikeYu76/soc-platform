from datetime import datetime
from typing import Any

from common import event_types
from common.event import Event
from normalization.base import BaseParser

EVENT_ID_MAP = {
    4624: event_types.AUTHENTICATION_SUCCESS,
    4625: event_types.AUTHENTICATION_FAILED,
    4688: event_types.PROCESS_CREATED,
}

FIELD_MAP = {
    "Computer": "hostname",
    "TargetUserName": "username",
    "IpAddress": "source_ip",
    "ProcessName": "process_name",
    "CommandLine": "command_line",
}

class WindowsParser(BaseParser):
    """
    Parser for normalized Windows event logs.
    """

    def _get_event_type(self, event_id: int | None) -> str:
        """
        Map a Windows Event ID to a canonical event type.
        """
        if event_id is None:
            return event_types.UNKNOWN

        return EVENT_ID_MAP.get(event_id, event_types.UNKNOWN)

    def parse(self, raw_log: Any) -> Event:
        """
        Convert a Windows log into the canonical Event model.
        """
        if not isinstance(raw_log, dict):
            raise TypeError("WindowsParser expects a dictionary.")

        event_id = raw_log.get("EventID")

        event_data = {}

        for windows_field, event_field in FIELD_MAP.items():
            event_data[event_field] = raw_log.get(windows_field)

        return Event(
            timestamp=datetime.fromisoformat(raw_log["TimeCreated"]),
            log_source="windows",
            event_type=self._get_event_type(event_id),
            message=raw_log.get("Message", ""),
            raw_message=str(raw_log),
            event_id=event_id,
            **event_data,
        )