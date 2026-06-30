import sqlite3
from ..config import settings

def connect() -> sqlite3.Connection:
    """Connects to the SQLite database and returns a Connection object."""
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
