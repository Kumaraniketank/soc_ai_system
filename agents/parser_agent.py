import re


def parser_agent(state):

    raw_log = state["raw_log"]

    parsed = {}

    if "powershell.exe" in raw_log.lower():
        parsed["process"] = "powershell.exe"

    if "-enc" in raw_log.lower():
        parsed["encoded"] = True

    ip_match = re.search(
        r'(\d+\.\d+\.\d+\.\d+)',
        raw_log
    )

    if ip_match:
        parsed["ip"] = ip_match.group(1)

    state["parsed_log"] = parsed

    return state