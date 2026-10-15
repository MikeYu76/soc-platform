
from common.detection import Detection, Severity
from risk.models import RiskAssessment


class RiskEngine:
    """Calculate a baseline risk score for a detection."""

    SEVERITY_SCORES = {
        Severity.LOW: 25,
        Severity.MEDIUM: 50,
        Severity.HIGH: 75,
        Severity.CRITICAL: 100,
    }

    def assess(self, detection: Detection) -> RiskAssessment:
        score = self.SEVERITY_SCORES[detection.severity]

        return RiskAssessment(
            id=detection.id,
            score=score,
            severity=detection.severity.value,
            reasoning=(
                f"Base risk score of {score} assigned "
                f"for {detection.severity.value} severity."
            ),
        )