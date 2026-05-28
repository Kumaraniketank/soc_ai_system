from dotenv import load_dotenv

from graphs.workflow import workflow


load_dotenv()


sample_log = "Failed login attempt detected from 192.168.1.5"

initial_state = {
    "raw_log": sample_log,
    "parsed_log": {},
    "threat_type": None,
    "severity": None,
    "recommendation": None,
    "report": None,
}

result = workflow.invoke(initial_state)
print(result["report"])