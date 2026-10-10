from case.models import Case

from case.processing.base import CaseProcessor


class CaseProcessingEngine:
    """
    Executes a sequence of CaseProcessors.
    """

    def __init__(
        self,
        processors: list[CaseProcessor],
    ) -> None:
        self._processors = processors

    def process(
        self,
        cases: list[Case],
    ) -> list[Case]:
        for processor in self._processors:
            cases = processor.process(cases)

        return cases