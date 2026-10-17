from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType
from detection.base import DetectionRule


class FailedLoginRule(DetectionRule):
    """
    Detects failed Windows authentication events.
    """

    def match(self, event: Event) -> Detection | None:
        """
        Return a Detection if the event represents
        a failed authentication attempt.
        """

        if event.event_type != EventType.AUTHENTICATION_FAILED:
            return None

        return Detection(
            rule_id="AUTH-001",
            title="Windows Failed Login",
            severity=Severity.MEDIUM,
            event=event,
        )
