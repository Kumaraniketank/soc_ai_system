import time

from graphs.workflow import workflow


processed_logs = set()


while True:

    with open("live_logs.txt", "r") as f:
        logs = f.readlines()

    for log in logs:

        if log not in processed_logs:

            processed_logs.add(log)

            initial_state = {
                "raw_log": log.strip(),
                "parsed_log": {},
                "threat_type": None,
                "severity": None,
                "recommendation": None,
                "report": None,
                "threat_intelligence": "",
                "previous_incidents": 0
            }

            result = workflow.invoke(initial_state)

            print(result["report"])

    time.sleep(2)