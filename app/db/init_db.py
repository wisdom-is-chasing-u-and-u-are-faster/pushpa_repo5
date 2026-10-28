# Database initialization module
import sqlite3
import os

DB_PATH = os.getenv("SQLITE_DB_PATH", "smart_study.db")


def get_db_connection():
    """Returns a connection to the SQLite database with dictionary-like row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database(db_path: str = DB_PATH):
    """Initializes schema and seed data for the application."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    schema_file = os.path.join(os.path.dirname(__file__), "..", "..", "db", "schema.sql")
    seed_file = os.path.join(os.path.dirname(__file__), "..", "..", "db", "seed.sql")

    if os.path.exists(schema_file):
        with open(schema_file, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())

    if os.path.exists(seed_file):
        with open(seed_file, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_database()
    print("Database initialized successfully.")
