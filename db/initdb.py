import sqlite3
from db.user import DB_PATH, DB_PATH_TASKS

def init_db():
    """Initialize the database and create the users table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def init_tasksdb():
    """Initialize the tasks database and create the tasks table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH_TASKS)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            username TEXT NOT NULL,
            task TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
