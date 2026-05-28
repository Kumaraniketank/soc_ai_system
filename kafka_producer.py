from kafka import KafkaProducer
import json
import time
import random


producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


logs = [
    "Failed SSH login attempt from 45.33.21.9",
    "Encoded PowerShell command detected",
    "Ransomware signature detected",
    "Credential dumping attempt detected",
    "Suspicious outbound connection detected"
]


while True:

    log = random.choice(logs)

    event = {
        
    "source": "fake",
    "log": log

    }

    producer.send(
        "soc_logs",
        event
    )

    print(f"Sent Log: {log}")

    time.sleep(5)