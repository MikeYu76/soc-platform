from __future__ import annotations

import logging
from collections.abc import Callable

from alert.engine import AlertEngine
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
from repositories.event_indexer import EventIndexer
from repositories.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)


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
        alert_engine: AlertEngine,
        alert_processing_engine: AlertProcessingEngine,
        case_factory: CaseFactory,
        case_processing_engine: CaseProcessingEngine,
        event_indexer: EventIndexer | None = None,
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory
        self._detection_engine = detection_engine
        self._enrichment_engine = enrichment_engine
        self._correlation_engine = correlation_engine
        self._alert_engine = alert_engine
        self._alert_processing_engine = alert_processing_engine
        self._case_factory = case_factory
        self._case_processing_engine = case_processing_engine
        self._event_indexer = event_indexer

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

            # Alert generation
            alerts = self._alert_engine.generate(
                detections=detections,
                correlations=correlations,
            )

            # Alert processing
            alerts = self._alert_processing_engine.process(
                alerts,
            )

            uow.alerts.save_all(alerts)

            # Case creation
            cases = [self._case_factory.create(alert) for alert in alerts]

            # Case processing
            cases = self._case_processing_engine.process(
                cases,
            )

            uow.cases.save_all(cases)

            uow.commit()

        # The relational database remains the source of truth. OpenSearch is
        # an auxiliary search index, so an indexing outage must not undo a
        # successfully committed event-processing result.
        if self._event_indexer is not None:
            try:
                self._event_indexer.index(request.event)
            except Exception:
                logger.exception(
                    "Could not index processed event in OpenSearch",
                    extra={"event_id": request.event.id},
                )

        return ProcessSecurityEventResponse(
            event=request.event,
            detections=detections,
            enriched_detections=enriched_detections,
            correlations=correlations,
            alerts=alerts,
            cases=cases,
        )
