from __future__ import annotations

from dataclasses import dataclass

from application.dto.base import Request, Response

from common.event import Event
from common.detection import Detection

from enrichment.models import EnrichedDetection
from correlation.models import CorrelationResult

from alert.models import Alert
from case.models import Case


@dataclass(slots=True)
class ProcessSecurityEventRequest(Request):
    """
    Request to process a security event through the SOC pipeline.
    """

    event: Event


@dataclass(slots=True)
class ProcessSecurityEventResponse(Response):
    """
    Result of processing a security event.
    """

    event: Event

    detections: list[Detection]

    enriched_detections: list[EnrichedDetection]

    correlations: list[CorrelationResult]

    alerts: list[Alert]

    cases: list[Case]