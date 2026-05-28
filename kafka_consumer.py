from kafka import KafkaConsumer
import json
import requests
from graphs.workflow import workflow

from datetime import datetime
import pytz

india = pytz.timezone("Asia/Kolkata")

consumer = KafkaConsumer(
    "soc_logs",
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("SOC AI Kafka Consumer Started...")


for message in consumer:

    try:

        data = message.value

        log = data.get("log", "No Log")

        current_time = datetime.now(india).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        print(f"\n[{current_time}] Received Log: {log}")

        initial_state = {
            "raw_log": log,
            "parsed_log": {},
            "threat_type": None,
            "severity": None,
            "recommendation": None,
            "report": None,
            "threat_intelligence": "",
            "previous_incidents": 0,
            "timestamp": current_time
        }

        try:

            result = workflow.invoke(initial_state)

            final_report = result["report"]

        except Exception as llm_error:

            print("Threat Agent Error:", llm_error)

            final_report = f"""
================ INCIDENT REPORT ================

Timestamp:
{current_time}

Raw Log:
{log}

Threat Analysis:
LLM unavailable due to rate limit.

Severity:
MEDIUM

Recommendation:
Check Groq API quota or switch model.

=================================================
"""

        print(final_report)

        # Broadcast to dashboard
        try:

            response = requests.post(
                "http://127.0.0.1:8000/live-alert",
                json={
                    "report": final_report
                }
            )

            print("Broadcast Status:", response.status_code)

        except Exception as ws_error:

            print("WebSocket Broadcast Error:", ws_error)

    except Exception as consumer_error:

        print("Consumer Error:", consumer_error)