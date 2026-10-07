from enum import StrEnum


class EventType(StrEnum):
    AUTHENTICATION_SUCCESS = "authentication_success"
    AUTHENTICATION_FAILED = "authentication_failed"

    PROCESS_CREATED = "process_created"
    PROCESS_TERMINATED = "process_terminated"

    FILE_CREATED = "file_created"
    FILE_DELETED = "file_deleted"

    NETWORK_CONNECTION = "network_connection"
    DNS_QUERY = "dns_query"
    WEB_REQUEST = "web_request"
    FIREWALL_DENY = "firewall_deny"

    UNKNOWN = "unknown"