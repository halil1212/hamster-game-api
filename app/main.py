from fastapi import FastAPI, HTTPException
from app.models import GameEvent
from app.database import get_connection, init_db
import json

app = FastAPI(title="Hamster Game API", version="1.0.0")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"status": "ok", "message": "Hamster Game API is running 🐹"}

@app.post("/webhook/event")
def receive_event(event: GameEvent):
    """Receives game events (same as n8n webhook trigger). Saves to Neon DB."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO events (event_type, user_id, payload, status) VALUES (%s, %s, %s, 'pending') RETURNING id;",
            (event.event_type, event.user_id, json.dumps(event.payload))
        )
        event_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "queued", "event_id": event_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/events")
def list_events(status: str = None):
    """List events, optionally filtered by status."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        if status:
            cur.execute("SELECT id, event_type, user_id, payload, status, created_at FROM events WHERE status = %s ORDER BY created_at DESC LIMIT 100;", (status,))
        else:
            cur.execute("SELECT id, event_type, user_id, payload, status, created_at FROM events ORDER BY created_at DESC LIMIT 100;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id": r[0], "event_type": r[1], "user_id": r[2], "payload": r[3], "status": r[4], "created_at": str(r[5])} for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
