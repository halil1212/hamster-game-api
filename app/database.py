import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def init_db():
    """Create the events table if it doesn't exist."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id          SERIAL PRIMARY KEY,
            event_type  VARCHAR(100) NOT NULL,
            user_id     VARCHAR(100),
            payload     JSONB,
            status      VARCHAR(20) DEFAULT 'pending',
            created_at  TIMESTAMP DEFAULT NOW(),
            processed_at TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Database initialized.")
