import os
import re


def response_agent(state):

    log = state.get(
        "raw_log",
        ""
    ).lower()

    severity = str(
        state.get("severity", "")
    ).lower()

    actions = []

    blocked_ip = None


    # =====================================
    # EXTRACT IP ADDRESS
    # =====================================

    ip_match = re.search(
        r"(?:\d{1,3}\.){3}\d{1,3}",
        log
    )

    if ip_match:

        blocked_ip = ip_match.group()


    # =====================================
    # POWERSHELL ATTACK RESPONSE
    # =====================================

    if "powershell" in log:

        try:

            os.system(
                "taskkill /F /IM powershell.exe"
            )

            actions.append(
                "Killed suspicious PowerShell process"
            )

        except Exception as e:

            actions.append(
                f"Failed to kill PowerShell: {e}"
            )


    # =====================================
    # BRUTE FORCE RESPONSE
    # =====================================

    if (
        "bruteforce" in log
        or "failed login" in log
        or "multiple login attempts" in log
    ):

        if blocked_ip:

            try:

                command = (
                    'netsh advfirewall firewall add rule '
                    f'name="BLOCK_{blocked_ip}" '
                    'dir=in action=block '
                    f'remoteip={blocked_ip}'
                )

                os.system(command)

                actions.append(
                    f"Blocked attacker IP: {blocked_ip}"
                )

            except Exception as e:

                actions.append(
                    f"Failed to block IP: {e}"
                )


    # =====================================
    # RANSOMWARE RESPONSE
    # =====================================

    if "ransomware" in log:

        try:

            os.system(
                'netsh interface set interface "Wi-Fi" admin=disable'
            )

            actions.append(
                "Machine isolated from network"
            )

        except Exception as e:

            actions.append(
                f"Isolation failed: {e}"
            )


    # =====================================
    # MALWARE RESPONSE
    # =====================================

    if (
        "mimikatz" in log
        or "credential dumping" in log
        or "malware" in log
    ):

        try:

            os.system(
                "taskkill /F /IM cmd.exe"
            )

            actions.append(
                "Terminated suspicious command shell"
            )

        except Exception as e:

            actions.append(
                f"Failed malware response: {e}"
            )


    # =====================================
    # CRITICAL INCIDENT RESPONSE
    # =====================================

    if severity == "critical":

        try:

            os.system(
                'netsh interface set interface "Wi-Fi" admin=disable'
            )

            actions.append(
                "Critical isolation executed"
            )

        except Exception as e:

            actions.append(
                f"Critical isolation failed: {e}"
            )


    # =====================================
    # NO ACTION
    # =====================================

    if len(actions) == 0:

        actions.append(
            "No autonomous action required"
        )


    # =====================================
    # SAVE ACTIONS
    # =====================================

    state["autonomous_actions"] = actions

    return state