from __future__ import annotations

from opensearchpy import OpenSearch

from common.event import Event


class OpenSearchEventIndexer:
    """Indexes normalized security events in an OpenSearch index."""

    def __init__(self, client: OpenSearch, index_name: str) -> None:
        self._client = client
        self._index_name = index_name

    def index(self, event: Event) -> None:
        """Index or replace one event using its stable event ID."""
        if not self._client.indices.exists(index=self._index_name):
            self._client.indices.create(
                index=self._index_name,
                body={
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0,
                    },
                    "mappings": {
                        "properties": {
                            "id": {"type": "keyword"},
                            "timestamp": {"type": "date"},
                            "log_source": {"type": "keyword"},
                            "event_type": {"type": "keyword"},
                            "message": {"type": "text"},
                            "raw_message": {"type": "text"},
                            "hostname": {"type": "keyword"},
                            "username": {"type": "keyword"},
                            "source_ip": {"type": "ip"},
                            "destination_ip": {"type": "ip"},
                            "event_id": {"type": "keyword"},
                            "process_name": {"type": "keyword"},
                            "command_line": {"type": "text"},
                        }
                    },
                },
            )

        document = event.model_dump(mode="json")
        if document["event_id"] is not None:
            document["event_id"] = str(document["event_id"])

        self._client.index(
            index=self._index_name,
            id=event.id,
            body=document,
        )
