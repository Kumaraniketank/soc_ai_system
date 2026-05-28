import time
import random


logs = [
    "Failed SSH login attempt from 45.33.21.9",
    "Encoded PowerShell command detected",
    "Ransomware signature detected",
    "Multiple failed admin logins",
    "Suspicious outbound connection detected",
    "Credential dumping attempt detected",
]


while True:

    log = random.choice(logs)

    with open("live_logs.txt", "a") as f:
        f.write(log + "\\n")

    print(f"Generated Log: {log}")

    time.sleep(5)