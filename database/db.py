import sqlite3
from datetime import datetime
import pytz


# -----------------------------
# DATABASE CONNECTION
# -----------------------------
connection = sqlite3.connect(
    "database/soc_memory.db",
    check_same_thread=False
)

cursor = connection.cursor()


# -----------------------------
# CREATE TABLE
# -----------------------------
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_address TEXT,
        event_type TEXT,
        threat_type TEXT,
        severity TEXT,
        timestamp TEXT
    )
"""
)

connection.commit()


# -----------------------------
# INDIA TIMEZONE
# -----------------------------
india = pytz.timezone("Asia/Kolkata")


# -----------------------------
# SAVE INCIDENT FUNCTION
# -----------------------------
def save_incident(
    ip_address,
    event_type,
    threat_type,
    severity
):

    current_time = datetime.now(india).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT INTO incidents (
            ip_address,
            event_type,
            threat_type,
            severity,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            ip_address,
            event_type,
            threat_type,
            severity,
            current_time
        )
    )

    connection.commit()


# -----------------------------
# FETCH INCIDENTS
# -----------------------------
def fetch_incidents():

    cursor.execute(
        """
        SELECT *
        FROM incidents
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    return rows