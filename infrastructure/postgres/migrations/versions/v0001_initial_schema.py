"""Initial schema matching the PostgreSQL schema before migration tracking."""

from __future__ import annotations

from infrastructure.postgres.migrations import Migration

MIGRATION = Migration(
    version="0001_initial_schema",
    statements=(
        """CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY, timestamp TEXT NOT NULL, log_source TEXT NOT NULL,
            event_type TEXT NOT NULL, hostname TEXT, username TEXT, source_ip TEXT,
            destination_ip TEXT, data TEXT NOT NULL
        )""",
        "CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp)",
        "CREATE INDEX IF NOT EXISTS idx_events_source ON events(log_source)",
        "CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type)",
        "CREATE INDEX IF NOT EXISTS idx_events_hostname ON events(hostname)",
        "CREATE INDEX IF NOT EXISTS idx_events_username ON events(username)",
        "CREATE INDEX IF NOT EXISTS idx_events_source_ip ON events(source_ip)",
        """CREATE INDEX IF NOT EXISTS idx_events_destination_ip
            ON events(destination_ip)""",
        """CREATE TABLE IF NOT EXISTS detections (
            id TEXT PRIMARY KEY, rule_id TEXT NOT NULL, severity TEXT NOT NULL,
            matched_at TEXT NOT NULL, data TEXT NOT NULL
        )""",
        "CREATE INDEX IF NOT EXISTS idx_detection_rule ON detections(rule_id)",
        "CREATE INDEX IF NOT EXISTS idx_detection_severity ON detections(severity)",
        "CREATE INDEX IF NOT EXISTS idx_detection_matched ON detections(matched_at)",
        """CREATE TABLE IF NOT EXISTS alerts (
            id TEXT PRIMARY KEY, status TEXT NOT NULL, severity TEXT NOT NULL,
            created_at TEXT NOT NULL, acknowledged_by TEXT, acknowledged_at TEXT,
            data TEXT NOT NULL
        )""",
        "CREATE INDEX IF NOT EXISTS idx_alert_status ON alerts(status)",
        "CREATE INDEX IF NOT EXISTS idx_alert_severity ON alerts(severity)",
        "CREATE INDEX IF NOT EXISTS idx_alert_created ON alerts(created_at)",
        """CREATE INDEX IF NOT EXISTS idx_alert_acknowledged_by
            ON alerts(acknowledged_by)""",
        """CREATE TABLE IF NOT EXISTS cases (
            id TEXT PRIMARY KEY, status TEXT NOT NULL, priority TEXT NOT NULL,
            assigned_to TEXT, created_at TEXT NOT NULL, closed_at TEXT,
            data TEXT NOT NULL
        )""",
        "CREATE INDEX IF NOT EXISTS idx_case_status ON cases(status)",
        "CREATE INDEX IF NOT EXISTS idx_case_priority ON cases(priority)",
        "CREATE INDEX IF NOT EXISTS idx_case_assigned ON cases(assigned_to)",
        "CREATE INDEX IF NOT EXISTS idx_case_created ON cases(created_at)",
        """CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY, username TEXT NOT NULL, role TEXT NOT NULL,
            is_active BOOLEAN NOT NULL, created_at TEXT NOT NULL, data TEXT NOT NULL
        )""",
        """CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username_ci
            ON users(LOWER(username))""",
        """CREATE TABLE IF NOT EXISTS event_index_outbox (
            event_id TEXT PRIMARY KEY, created_at TEXT NOT NULL,
            attempts INTEGER NOT NULL DEFAULT 0, next_attempt_at TEXT NOT NULL,
            last_error TEXT
        )""",
        """CREATE INDEX IF NOT EXISTS idx_event_index_outbox_due
            ON event_index_outbox(next_attempt_at, created_at)""",
    ),
)
