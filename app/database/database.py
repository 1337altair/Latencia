import os
import sqlite3
from datetime import datetime
from pathlib import Path


def db_path():
    if os.name == "nt":
        base = Path(os.getenv("LOCALAPPDATA", Path.home())) / "Latencia"
    else:
        base = Path.home() / ".latencia"
    base.mkdir(parents=True, exist_ok=True)
    return base / "latencia.db"


def connect():
    conn = sqlite3.connect(db_path())
    conn.row_factory = sqlite3.Row
    return conn


def setup():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                download REAL NOT NULL,
                upload REAL NOT NULL,
                ping REAL NOT NULL,
                jitter REAL NOT NULL,
                packet_loss REAL NOT NULL,
                score INTEGER NOT NULL,
                local_ip TEXT NOT NULL,
                adapter TEXT NOT NULL
            )
        """)


def save_test(row):
    setup()
    with connect() as conn:
        conn.execute("""
            INSERT INTO tests (
                created_at, download, upload, ping, jitter,
                packet_loss, score, local_ip, adapter
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            row["download"], row["upload"], row["ping"], row["jitter"],
            row["packet_loss"], row["score"], row["local_ip"], row["adapter"]
        ))


def recent(limit=100):
    setup()
    with connect() as conn:
        rows = conn.execute("SELECT * FROM tests ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [dict(row) for row in rows]
