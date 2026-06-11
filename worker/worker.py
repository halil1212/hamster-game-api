"""
Event Worker — veritabanındaki 'pending' olayları okur,
dispatcher üzerinden işler ve 'processed' olarak işaretler.
"""
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import get_connection, init_db
from worker.dispatcher import dispatch

POLL_INTERVAL_SECONDS = 3


def fetch_pending_events(conn, batch_size: int = 10) -> list:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, event_type, user_id, payload
        FROM events
        WHERE status = 'pending'
        ORDER BY created_at ASC
        LIMIT %s
        FOR UPDATE SKIP LOCKED
        """,
        (batch_size,)
    )
    rows = cur.fetchall()
    cur.close()
    return [dict(r) for r in rows]


def mark_processed(conn, event_id: int):
    cur = conn.cursor()
    cur.execute(
        "UPDATE events SET status='processed', processed_at=NOW() WHERE id=%s",
        (event_id,)
    )
    cur.close()


def mark_failed(conn, event_id: int):
    cur = conn.cursor()
    cur.execute(
        "UPDATE events SET status='failed' WHERE id=%s",
        (event_id,)
    )
    cur.close()


def run_worker():
    print("🐹 Hamster Event Worker started — polling every "
          f"{POLL_INTERVAL_SECONDS}s...\n")
    init_db()

    while True:
        try:
            conn = get_connection()
            events = fetch_pending_events(conn)

            if not events:
                conn.close()
                time.sleep(POLL_INTERVAL_SECONDS)
                continue

            print(f"📥 {len(events)} pending event(s) found")

            for event in events:
                eid     = event["id"]
                etype   = event["event_type"]
                uid     = event["user_id"]
                payload = event["payload"] or {}

                try:
                    result = dispatch(etype, uid, payload)
                    mark_processed(conn, eid)
                    print(f"  ✅ event #{eid} processed → {result}")
                except Exception as e:
                    mark_failed(conn, eid)
                    print(f"  ❌ event #{eid} FAILED → {e}")

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"⚠️  Worker error: {e}")

        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    run_worker()
