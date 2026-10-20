from collections.abc import Sequence

from common.detection import Detection
from common.event import Event
from detection.base import DetectionRule


class DetectionEngine:
    def __init__(self, rules: Sequence[DetectionRule]) -> None:
        self._rules = rules

    def process(self, event: Event) -> list[Detection]:
        detections: list[Detection] = []

        for rule in self._rules:
            detection = rule.match(event)

            if detection is not None:
                detections.append(detection)

        return detections
