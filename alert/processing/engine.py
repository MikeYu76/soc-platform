from alert.models import Alert

from alert.processing.base import AlertProcessor


class AlertProcessingEngine:
    """
    Executes a sequence of AlertProcessors.

    The output of each processor becomes the input to the next,
    allowing alert processing policies to be composed into a
    configurable pipeline.
    """

    def __init__(
        self,
        processors: list[AlertProcessor],
    ) -> None:
        self._processors = processors

    def process(
        self,
        alerts: list[Alert],
    ) -> list[Alert]:
        """
        Execute all registered processors in order.
        """
        for processor in self._processors:
            alerts = processor.process(alerts)

        return alerts