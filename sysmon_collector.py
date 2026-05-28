import win32evtlog
import json
from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers='127.0.0.1:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


server = 'localhost'

log_type = 'Microsoft-Windows-Sysmon/Operational'


hand = win32evtlog.OpenEventLog(server, log_type)

flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ


print("Listening to Sysmon logs...")


while True:

    events = win32evtlog.ReadEventLog(
        hand,
        flags,
        0
    )

    if events:

        for event in events:

            try:

                message = str(event.StringInserts)

                log_data = {
    "source": "sysmon",
    "log": message
}

                producer.send(
                    "soc_logs",
                    log_data
                )

                print("\nSent Sysmon Event To Kafka")
                print(message)

            except Exception as e:

                print("Error:", e)