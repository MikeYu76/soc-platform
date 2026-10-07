from ingestion import FileIngestor

from normalization.dispatcher import Dispatcher
from normalization.registry import ParserRegistry
from normalization.windows import WindowsParser

from detection.engine import DetectionEngine
from detection.rules.failed_login import FailedLoginRule


def main() -> None:
    """
    Demonstrate the complete SOC processing pipeline.

    Pipeline:
        File -> Normalization -> Detection
    """

    # -----------------------------
    # Configure the parser registry.
    # -----------------------------
    registry = ParserRegistry()
    registry.register("windows", WindowsParser)

    # -----------------------------
    # Create the dispatcher.
    # -----------------------------
    dispatcher = Dispatcher(registry)

    # -----------------------------
    # Configure detection rules.
    # -----------------------------
    rules = [
        FailedLoginRule(),
    ]

    # -----------------------------
    # Create the detection engine.
    # -----------------------------
    engine = DetectionEngine(rules)

    # -----------------------------
    # Read sample logs.
    # -----------------------------
    ingestor = FileIngestor("sample_logs/windows_failed_login.json")
    raw_logs = ingestor.read_logs()

    # -----------------------------
    # Process each log.
    # -----------------------------
    for raw_log in raw_logs:

        # Normalize the raw log.
        event = dispatcher.dispatch("windows", raw_log)

        print("\n=== Normalized Event ===")
        print(event)

        # Run detection rules.
        detections = engine.detect(event)

        print("\n=== Detections ===")

        if not detections:
            print("No detections generated.")

        for detection in detections:
            print(detection)


if __name__ == "__main__":
    main()