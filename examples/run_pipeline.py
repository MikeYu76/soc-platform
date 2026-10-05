from ingestion import FileIngestor
from normalization.dispatcher import Dispatcher
from normalization.registry import ParserRegistry
from normalization.windows import WindowsParser


def main() -> None:
    # Create and configure the parser registry.
    registry = ParserRegistry()
    registry.register("windows", WindowsParser)

    # Create the dispatcher.
    dispatcher = Dispatcher(registry)

    # Read sample logs.
    ingestor = FileIngestor("sample_logs/windows_failed_login.json")
    raw_logs = ingestor.read_logs()

    # Normalize each raw log.
    for raw_log in raw_logs:
        event = dispatcher.dispatch("windows", raw_log)
        print(event)


if __name__ == "__main__":
    main()