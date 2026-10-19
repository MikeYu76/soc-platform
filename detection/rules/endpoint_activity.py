from __future__ import annotations

from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType
from detection.base import DetectionRule


class ProcessIndicatorRule(DetectionRule):
    """Matches suspicious process activity against simple signatures."""

    rule_id = ""
    title = ""
    severity = Severity.HIGH
    signatures: tuple[tuple[str, ...], ...] = ()
    event_ids: tuple[int, ...] = ()

    def match(self, event: Event) -> Detection | None:
        event_id_matches = (
            event.event_id is not None
            and str(event.event_id)
            in {str(event_id) for event_id in self.event_ids}
        )
        if (
            event.event_type != EventType.PROCESS_CREATED
            and not event_id_matches
        ):
            return None

        searchable_text = " ".join(
            value
            for value in (
                event.process_name,
                event.command_line,
                event.message,
                event.raw_message,
            )
            if value
        ).casefold().replace("'", "").replace('"', "")

        for signature in self.signatures:
            if all(indicator in searchable_text for indicator in signature):
                return Detection(
                    rule_id=self.rule_id,
                    title=self.title,
                    severity=self.severity,
                    event=event,
                    metadata={"matched_indicators": list(signature)},
                )

        return None


class PowerShellAbuseRule(ProcessIndicatorRule):
    rule_id = "WIN-PS-001"
    title = "Suspicious PowerShell Execution"
    severity = Severity.HIGH
    event_ids = (4104,)
    signatures = (
        ("powershell", "-enc"),
        ("powershell", "-encodedcommand"),
        ("pwsh", "-enc"),
        ("downloadstring", "powershell"),
        ("invoke-expression", "powershell"),
    )


class ServiceCreationRule(ProcessIndicatorRule):
    rule_id = "WIN-SVC-001"
    title = "Suspicious Service Creation"
    severity = Severity.HIGH
    event_ids = (4697, 7045)
    signatures = (
        ("sc create",),
        ("sc.exe create",),
        ("new-service",),
        ("create service",),
        ("service was installed",),
        ("service installed",),
    )


class CredentialDumpingRule(ProcessIndicatorRule):
    rule_id = "WIN-CRED-001"
    title = "Credential Dumping Tool or Command Detected"
    severity = Severity.CRITICAL
    signatures = (
        ("mimikatz",),
        ("sekurlsa::logonpasswords",),
        ("lsadump::",),
        ("procdump", "lsass"),
        ("comsvcs.dll", "minidump"),
    )


class PassTheHashRule(ProcessIndicatorRule):
    rule_id = "WIN-CRED-002"
    title = "Pass-the-Hash Activity Detected"
    severity = Severity.CRITICAL
    signatures = (
        ("sekurlsa::pth",),
        ("pass-the-hash",),
        ("pass the hash",),
    )


class KerberoastingRule(ProcessIndicatorRule):
    rule_id = "WIN-CRED-003"
    title = "Kerberoasting Tool or Command Detected"
    severity = Severity.HIGH
    signatures = (
        ("kerberoast",),
        ("getuserspns",),
        ("tgsrepcrack",),
    )


class LSASSAccessRule(ProcessIndicatorRule):
    rule_id = "WIN-CRED-004"
    title = "Suspicious LSASS Process Access"
    severity = Severity.HIGH
    event_ids = (10,)
    signatures = (
        ("lsass.exe",),
        ("lsass", "process access"),
        ("handle.exe", "lsass"),
        ("openprocess", "lsass"),
    )


class ScheduledTaskPersistenceRule(ProcessIndicatorRule):
    rule_id = "WIN-PERSIST-001"
    title = "Scheduled Task Persistence Activity"
    severity = Severity.HIGH
    event_ids = (106, 4698)
    signatures = (
        ("schtasks", "/create"),
        ("register-scheduledtask",),
        ("new-scheduledtask",),
        ("scheduled task created",),
        ("scheduled task was created",),
    )


class WMIExecutionRule(ProcessIndicatorRule):
    rule_id = "WIN-EXEC-001"
    title = "Suspicious WMI Process Execution"
    severity = Severity.HIGH
    signatures = (
        ("wmic", "process call create"),
        ("invoke-wmimethod",),
        ("invoke-cimmethod", "win32_process"),
    )


class WindowsEventLogClearingRule(ProcessIndicatorRule):
    rule_id = "WIN-EVASION-001"
    title = "Windows Event Log Clearing Activity"
    severity = Severity.HIGH
    event_ids = (1102,)
    signatures = (
        ("wevtutil", " cl "),
        ("clear-eventlog",),
        ("event log cleared",),
        ("audit log was cleared",),
    )


class RemoteDesktopFailedLoginRule(DetectionRule):
    """Detects an individual failed RDP logon; burst logic stays correlated."""

    def match(self, event: Event) -> Detection | None:
        if event.event_type != EventType.AUTHENTICATION_FAILED:
            return None

        if event.event_id is None or str(event.event_id) != "4625":
            return None

        searchable_text = " ".join(
            value
            for value in (event.message, event.raw_message)
            if value
        ).casefold().replace("'", "").replace('"', "")
        rdp_indicators = (
            "logontype: 10",
            "logontype=10",
            "logon type 10",
            "remote desktop",
            "terminalservices",
            "remoteinteractive",
        )
        matched = [
            indicator
            for indicator in rdp_indicators
            if indicator in searchable_text
        ]
        if not matched:
            return None

        return Detection(
            rule_id="WIN-RDP-001",
            title="Remote Desktop Failed Logon",
            severity=Severity.MEDIUM,
            event=event,
            metadata={"matched_indicators": matched},
        )
