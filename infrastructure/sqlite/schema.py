from __future__ import annotations

import sqlite3


def initialize_schema(connection: sqlite3.Connection) -> None:
    """
    Create all SQLite tables and indexes.
    """

    connection.executescript(
        """
        PRAGMA foreign_keys = ON;

        --------------------------------------------------------------------
        -- Events
        --------------------------------------------------------------------

        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            log_source TEXT NOT NULL,
            event_type TEXT NOT NULL,

            hostname TEXT,
            username TEXT,
            source_ip TEXT,
            destination_ip TEXT,

            data TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_events_timestamp
            ON events(timestamp);

        CREATE INDEX IF NOT EXISTS idx_events_source
            ON events(log_source);

        CREATE INDEX IF NOT EXISTS idx_events_type
            ON events(event_type);

        CREATE INDEX IF NOT EXISTS idx_events_hostname
            ON events(hostname);

        CREATE INDEX IF NOT EXISTS idx_events_username
            ON events(username);

        CREATE INDEX IF NOT EXISTS idx_events_source_ip
            ON events(source_ip);

        CREATE INDEX IF NOT EXISTS idx_events_destination_ip
            ON events(destination_ip);

        --------------------------------------------------------------------
        -- Detections
        --------------------------------------------------------------------

        CREATE TABLE IF NOT EXISTS detections (
            id TEXT PRIMARY KEY,
            rule_id TEXT NOT NULL,
            severity TEXT NOT NULL,
            matched_at TEXT NOT NULL,
            data TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_detection_rule
            ON detections(rule_id);

        CREATE INDEX IF NOT EXISTS idx_detection_severity
            ON detections(severity);

        CREATE INDEX IF NOT EXISTS idx_detection_matched
            ON detections(matched_at);

        --------------------------------------------------------------------
        -- Alerts
        --------------------------------------------------------------------

        CREATE TABLE IF NOT EXISTS alerts (
            id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            severity TEXT NOT NULL,
            created_at TEXT NOT NULL,
            acknowledged_by TEXT,
            acknowledged_at TEXT,
            data TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_alert_status
            ON alerts(status);

        CREATE INDEX IF NOT EXISTS idx_alert_severity
            ON alerts(severity);

        CREATE INDEX IF NOT EXISTS idx_alert_created
            ON alerts(created_at);

        CREATE INDEX IF NOT EXISTS idx_alert_acknowledged_by
            ON alerts(acknowledged_by);

        --------------------------------------------------------------------
        -- Cases
        --------------------------------------------------------------------

        CREATE TABLE IF NOT EXISTS cases (
            id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            priority TEXT NOT NULL,
            assigned_to TEXT,
            created_at TEXT NOT NULL,
            closed_at TEXT,
            data TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_case_status
            ON cases(status);

        CREATE INDEX IF NOT EXISTS idx_case_priority
            ON cases(priority);

        CREATE INDEX IF NOT EXISTS idx_case_assigned
            ON cases(assigned_to);

        CREATE INDEX IF NOT EXISTS idx_case_created
            ON cases(created_at);
        """
    )

    connection.commit()