from __future__ import annotations

from dataclasses import dataclass

from alert.models import Alert
from application.dto.base import Request, Response
from case.models import Case
from common.detection import Detection
from common.event import Event
from correlation.models import CorrelationResult
from enrichment.models import EnrichedDetection


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
