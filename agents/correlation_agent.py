from collections import deque
from datetime import datetime


# Memory of recent attacks
attack_memory = deque(maxlen=20)


def correlation_agent(state):

    threat = state.get(
        "threat_type",
        ""
    ).lower()

    raw_log = state.get(
        "raw_log",
        ""
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Store event
    attack_memory.append({
        "time": timestamp,
        "threat": threat,
        "log": raw_log
    })

    recent_attacks = " ".join([
        attack["threat"]
        for attack in attack_memory
    ])


    # -------------------------
    # Correlation Rules
    # -------------------------

    correlation_result = (
        "No major correlated attack detected."
    )


    # Brute Force → PowerShell
    if (
        "brute force" in recent_attacks
        and "powershell" in recent_attacks
    ):

        correlation_result = """
        Correlated Attack Detected:

        Possible successful brute-force attack
        followed by malicious PowerShell execution.

        Potential lateral movement or malware execution.
        """


    # Credential Dumping + Outbound Connection
    elif (
        "credential" in recent_attacks
        and "outbound" in recent_attacks
    ):

        correlation_result = """
        Correlated Attack Detected:

        Credential dumping activity followed by
        suspicious outbound communication.

        Possible data exfiltration or C2 beaconing.
        """


    # Ransomware Indicators
    elif (
        "powershell" in recent_attacks
        and "outbound" in recent_attacks
        and "credential" in recent_attacks
    ):

        correlation_result = """
        Multi-Stage Attack Chain Detected:

        - PowerShell activity
        - Credential access
        - Outbound communication

        High likelihood of ransomware intrusion.
        """


    # Store result
    state["correlated_attack"] = (
        correlation_result
    )

    return state