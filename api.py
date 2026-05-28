from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from kafka import KafkaProducer
from websocket_manager import manager

import json
import sqlite3
from datetime import datetime


# =========================================
# FASTAPI APP
# =========================================

app = FastAPI(
    title="AI SOC Platform",
    description="Enterprise AI SOC Backend",
    version="1.0.0"
)


# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================
# KAFKA PRODUCER
# =========================================

try:

    producer = KafkaProducer(
        bootstrap_servers=['127.0.0.1:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    print("Kafka Connected Successfully")

except Exception as e:

    print("Kafka Connection Failed:", e)

    producer = None


# =========================================
# DATABASE CONNECTION
# =========================================

connection = sqlite3.connect(
    "database/soc_memory.db",
    check_same_thread=False
)

cursor = connection.cursor()


# =========================================
# REQUEST MODELS
# =========================================

class LogRequest(BaseModel):

    log: str


class AlertRequest(BaseModel):

    report: str


# =========================================
# HOME
# =========================================

@app.get("/")

def home():

    return {
        "message": "AI SOC Platform Running",
        "status": "active",
        "timestamp": str(datetime.now())
    }


# =========================================
# HEALTH CHECK
# =========================================

@app.get("/health")

def health_check():

    return {
        "status": "healthy",
        "kafka": "connected" if producer else "disconnected",
        "database": "connected"
    }


# =========================================
# SEND LOG TO KAFKA
# =========================================

@app.post("/log")

def send_log(data: LogRequest):

    try:

        if producer is None:

            raise HTTPException(
                status_code=500,
                detail="Kafka not available"
            )

        producer.send(
            "soc_logs",
            {
                "source": "api",
                "log": data.log
            }
        )

        producer.flush()

        print("Log Sent:", data.log)

        return {
            "status": "success",
            "message": "Log sent successfully",
            "log": data.log
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Kafka Error: {str(e)}"
        )


# =========================================
# GET INCIDENTS
# =========================================

@app.get("/incidents")

def get_incidents(limit: int = 20):

    try:

        cursor.execute(
            """
            SELECT *
            FROM incidents
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()

        incidents = []

        for row in rows:

            incidents.append({
                "id": row[0],
                "ip_address": row[1],
                "event_type": row[2],
                "threat_type": row[3],
                "severity": row[4],
                "timestamp": row[5]
            })

        return {
            "count": len(incidents),
            "incidents": incidents
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================
# FILTER INCIDENTS BY SEVERITY
# =========================================

@app.get("/incidents/severity/{severity}")

def get_incidents_by_severity(severity: str):

    try:

        cursor.execute(
            """
            SELECT *
            FROM incidents
            WHERE LOWER(severity)=LOWER(?)
            ORDER BY id DESC
            """,
            (severity,)
        )

        rows = cursor.fetchall()

        incidents = []

        for row in rows:

            incidents.append({
                "id": row[0],
                "ip_address": row[1],
                "event_type": row[2],
                "threat_type": row[3],
                "severity": row[4],
                "timestamp": row[5]
            })

        return {
            "severity": severity,
            "count": len(incidents),
            "incidents": incidents
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================
# SOC STATISTICS
# =========================================

@app.get("/stats")

def get_statistics():

    try:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM incidents
            """
        )

        total_incidents = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT severity, COUNT(*)
            FROM incidents
            GROUP BY severity
            """
        )

        severity_stats = cursor.fetchall()

        severity_data = {}

        for severity, count in severity_stats:

            severity_data[severity] = count

        return {
            "total_incidents": total_incidents,
            "severity_distribution": severity_data
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================
# WEBSOCKET ENDPOINT
# =========================================

@app.websocket("/ws")

async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    try:

        while True:

            await websocket.receive_text()

    except Exception as e:

        print("WebSocket Error:", e)

        manager.disconnect(websocket)


# =========================================
# LIVE ALERT BROADCAST
# =========================================

@app.post("/live-alert")

async def live_alert(data: AlertRequest):

    try:

        print("Received Alert:", data.report)

        await manager.broadcast({
            "report": data.report
        })

        return {
            "status": "broadcasted"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )