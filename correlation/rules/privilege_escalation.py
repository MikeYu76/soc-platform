from datetime import UTC, datetime, timedelta
from uuid import uuid4

from common.detection import Severity
from common.event_types import EventType
from correlation.base import CorrelationRule
from correlation.models import CorrelationResult
from enrichment.models import EnrichedDetection


class PrivilegeEscalationRule(CorrelationRule):
    """
    Detect a possible privilege escalation by correlating a
    successful authentication followed by execution of a
    privilege-related process on the same host within a
    configurable time window.
    """

    PRIVILEGE_INDICATORS = (
        "runas",
        "sudo",
        "su",
        "psexec",
        "administrator",
        "admin",
        "elevated",
        "privilege",
    )

    def __init__(
        self,
        window_minutes: int = 10,
    ) -> None:
        if window_minutes < 1:
            raise ValueError("window_minutes must be at least 1")

        self.window = timedelta(
            minutes=window_minutes,
        )

    def correlate(
        self,
        detections: list[EnrichedDetection],
    ) -> list[CorrelationResult]:

        relevant_detections = [
            detection
            for detection in detections
            if (
                detection.detection.event.username is not None
                and detection.detection.event.hostname is not None
                and detection.detection.event.event_type
                in (
                    EventType.AUTHENTICATION_SUCCESS,
                    EventType.PROCESS_CREATED,
                )
            )
        ]

        detections_by_user: dict[
            str,
            list[EnrichedDetection],
        ] = {}

        for detection in relevant_detections:
            username = detection.detection.event.username
            if username is None:
                continue
            detections_by_user.setdefault(
                username,
                [],
            ).append(detection)

        results: list[CorrelationResult] = []

        for username, user_detections in detections_by_user.items():

            user_detections.sort(
                key=lambda detection: (detection.detection.event.timestamp)
            )

            for login_detection in user_detections:

                login_event = login_detection.detection.event

                if login_event.event_type != EventType.AUTHENTICATION_SUCCESS:
                    continue

                for process_detection in user_detections:

                    process_event = process_detection.detection.event

                    if process_event.event_type != EventType.PROCESS_CREATED:
                        continue

                    if process_event.timestamp <= login_event.timestamp:
                        continue

                    if (
                        process_event.timestamp - login_event.timestamp
                        > self.window
                    ):
                        continue

                    if process_event.hostname != login_event.hostname:
                        continue

                    searchable_text = " ".join(
                        filter(
                            None,
                            [
                                process_event.process_name,
                                process_event.command_line,
                                process_event.message,
                            ],
                        )
                    ).lower()

                    if not any(
                        indicator in searchable_text
                        for indicator in self.PRIVILEGE_INDICATORS
                    ):
                        continue

                    results.append(
                        CorrelationResult(
                            correlation_id=str(uuid4()),
                            rule_id="CORR-PRIV-001",
                            title="Possible Privilege Escalation",
                            severity=Severity.HIGH,
                            matched_at=datetime.now(UTC),
                            detections=[
                                login_detection,
                                process_detection,
                            ],
                            metadata={
                                "username": username,
                                "hostname": login_event.hostname,
                                "process": process_event.process_name,
                                "command_line": process_event.command_line,
                                "window_minutes": (
                                    self.window.total_seconds() / 60
                                ),
                            },
                        )
                    )

                    # One correlation per login sequence.
                    break

        return results
