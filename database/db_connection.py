"""Optional MySQL connection helper. Database use is not required by the app.

Configure DB_HOST, DB_PORT, DB_USER, DB_PASSWORD and DB_NAME in .env only if
using MySQL. Credentials are never hard-coded here.
"""
from __future__ import annotations
import os


def get_connection():
    """Create and return a MySQL connection; raises a clear error if unconfigured."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    required = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise RuntimeError("MySQL is optional and is not configured. Missing: " + ", ".join(missing))
    try:
        import mysql.connector
    except ImportError as exc:
        raise RuntimeError("Install mysql-connector-python to enable MySQL: pip install mysql-connector-python") from exc
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"), port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"), connection_timeout=5,
    )


def test_connection() -> bool:
    """Return True when configured MySQL is reachable; always closes connection."""
    connection = get_connection()
    try:
        return bool(connection.is_connected())
    finally:
        connection.close()
