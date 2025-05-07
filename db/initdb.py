"""
Database initialization module.
Handles the creation and initialization of database tables.
"""
import os
import sqlite3
import logging
from utils.config import USER_DB_PATH, TASKS_DB_PATH

logger = logging.getLogger(__name__)

def init_db():
    """
    Initialize the users database and create the users table if it doesn't exist.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(USER_DB_PATH), exist_ok=True)
        
        conn = sqlite3.connect(USER_DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
        logger.info("Users database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing users database: {e}")
        return False


def init_tasksdb():
    """
    Initialize the tasks database and create the tasks table if it doesn't exist.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(TASKS_DB_PATH), exist_ok=True)
        
        conn = sqlite3.connect(TASKS_DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                task TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                priority INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TIMESTAMP,
                completed_at TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
        logger.info("Tasks database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing tasks database: {e}")
        return False
