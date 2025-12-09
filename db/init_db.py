import sqlite3
import os

# Ścieżka do folderu db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "air.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

def init_db():
    conn = sqlite3.connect(DB_PATH)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()

    print("Baza danych została utworzona:", DB_PATH)

if __name__ == "__main__":
    init_db()
