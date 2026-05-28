from typing import TypedDict, List


class SOCState(TypedDict):

    raw_log: str

    parsed_log: dict

    threat_type: str

    severity: str

    recommendation: str

    report: str

    threat_intelligence: str

    previous_incidents: int

    timestamp: str

    autonomous_actions: List[str]

    mitre: dict