from datetime import datetime
import pytz


india = pytz.timezone("Asia/Kolkata")


def report_agent(state):

    parsed = state.get("parsed_log", {})

    current_time = datetime.now(
        india
    ).strftime("%Y-%m-%d %H:%M:%S")

    mitre = state.get(
        "mitre",
        {
            "technique": "Unknown",
            "tactic": "Unknown",
            "description": "Unknown"
        }
    )

    autonomous_actions = state.get(
        "autonomous_actions",
        ["No autonomous action executed"]
    )

    report = f"""
================ INCIDENT REPORT ================

Timestamp:
{current_time}

IP Address:
{parsed.get('ip_address', 'Unknown')}

Event Type:
{parsed.get('event', 'Unknown')}

Previous Incidents:
{state.get('previous_incidents', 0)}

-------------------------------------------------

Threat Analysis:
{state.get('threat_type', 'Unknown Threat')}

-------------------------------------------------

Correlated Attack Analysis:
{state.get(
    'correlated_attack',
    'No correlation available'
)}

-------------------------------------------------

MITRE ATT&CK Mapping:

Technique:
{mitre.get('technique', 'Unknown')}

Tactic:
{mitre.get('tactic', 'Unknown')}

Description:
{mitre.get('description', 'Unknown')}

-------------------------------------------------

Severity:
{state.get('severity', 'Unknown')}

-------------------------------------------------

Recommended Actions:
{state.get(
    'recommendation',
    'No recommendation available'
)}

-------------------------------------------------

SOAR Autonomous Response Actions:

{chr(10).join(
    f"- {action}"
    for action in autonomous_actions
)}

=================================================
"""

    state["report"] = report

    return state