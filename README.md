# 🐹 hamster-game-api

Python event-driven API for Hamster Game — Task 1 & 2.

## Structure

- `app/main.py` — FastAPI webhook, receives events and saves to DB
- `app/database.py` — Neon connection + table setup
- `worker/worker.py` — Polls DB and processes pending events
- `worker/dispatcher.py` — Routes event_type to correct handler
- `worker/handlers.py` — One function per event type (like n8n nodes)

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

## Run

**Task 1 — Start API:**
```bash
uvicorn app.main:app --reload
```

**Task 2 — Start Worker:**
```bash
python -m worker.worker
```

## Test

```bash
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{"event_type": "tap", "user_id": "user_1", "payload": {"tap_power": 3}}'
```
