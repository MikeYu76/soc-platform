from __future__ import annotations

from collections.abc import Callable

from alert.factory import AlertFactory
from alert.processing.engine import AlertProcessingEngine

from application.dto.process_security_event import (
    ProcessSecurityEventRequest,
    ProcessSecurityEventResponse,
)
from application.services.base import ApplicationService

from case.factory import CaseFactory
from case.processing.engine import CaseProcessingEngine

from correlation.engine import CorrelationEngine

from detection.engine import DetectionEngine

from enrichment.engine import EnrichmentEngine

from repositories.unit_of_work import UnitOfWork


class ProcessSecurityEventService(
    ApplicationService[
        ProcessSecurityEventRequest,
        ProcessSecurityEventResponse,
    ],
):
    """
    Coordinates the complete security event processing pipeline.
    """

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
        detection_engine: DetectionEngine,
        enrichment_engine: EnrichmentEngine,
        correlation_engine: CorrelationEngine,
        alert_factory: AlertFactory,
        alert_processing_engine: AlertProcessingEngine,
        case_factory: CaseFactory,
        case_processing_engine: CaseProcessingEngine,
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory
        self._detection_engine = detection_engine
        self._enrichment_engine = enrichment_engine
        self._correlation_engine = correlation_engine
        self._alert_factory = alert_factory
        self._alert_processing_engine = alert_processing_engine
        self._case_factory = case_factory
        self._case_processing_engine = case_processing_engine

    def execute(
        self,
        request: ProcessSecurityEventRequest,
    ) -> ProcessSecurityEventResponse:

        with self._unit_of_work_factory() as uow:
            # Persist event
            uow.events.save(request.event)

            # Detection
            detections = self._detection_engine.process(
                request.event,
            )

            uow.detections.save_all(detections)

            # Enrichment
            enriched_detections = [
                self._enrichment_engine.process(detection)
                for detection in detections
            ]

            # Correlation
            correlations = self._correlation_engine.correlate(
                enriched_detections,
            )

            # Alert creation
            alerts = [
                self._alert_factory.create(correlation)
                for correlation in correlations
            ]

            # Alert processing
            alerts = self._alert_processing_engine.process(
                alerts,
            )

            uow.alerts.save_all(alerts)

            # Case creation
            cases = [
                self._case_factory.create(alert)
                for alert in alerts
            ]

            # Case processing
            cases = self._case_processing_engine.process(
                cases,
            )

            uow.cases.save_all(cases)

            uow.commit()

        return ProcessSecurityEventResponse(
            event=request.event,
            detections=detections,
            enriched_detections=enriched_detections,
            correlations=correlations,
            alerts=alerts,
            cases=cases,
        )