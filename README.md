# AI SOC Platform

Enterprise AI-powered SIEM + SOAR platform using:

- FastAPI
- Kafka
- LangGraph
- Groq LLM
- React Dashboard
- WebSockets
- MITRE ATT&CK Mapping
- Autonomous SOAR Actions

## Features

- Real-time log ingestion
- AI threat analysis
- Correlation engine
- Live SOC dashboard
- Autonomous response system
- Kafka streaming
- Threat intelligence
- Incident reporting

## Run Backend

```bash
uvicorn api:app --reload
cd soc_dashboard
npm install
npm run dev
