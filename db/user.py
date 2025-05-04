import sqlite3
import bcrypt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
DB_PATH = os.path.abspath(os.path.join(DATA_DIR, "users.db"))
DB_PATH_TASKS = os.path.abspath(os.path.join(DATA_DIR, "tasks.db"))
def add_user(username, email, password):
    """
    Adds a new user to the database with a hashed password.
    :param username: The username of the new user.
    :param password: The password of the new user.
    :return: None
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if verify_user(username,email,password):
        conn.close()
        return False
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cur.execute("INSERT INTO users (username,email, password) VALUES (?,?,?)", (username,email,hashed_pw))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
    finally:
        conn.close()
    return True
def get_mail(username):
    """
    Retrieves the email address of a user from the database.
    :param username: The username of the user.
    :return: The email address of the user, or None if not found.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT email FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
def verify_user(username,email, password):
    """
    Verifies if the provided username and password match a user in the database.
    :param username: The username of the user to verify.
    :param password: The password of the user to verify.
    :return: True if the user exists and the password matches, False otherwise.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()

    if row:
        stored_hashed_pw = row[0]
        return bcrypt.checkpw(password.encode('utf-8'), stored_hashed_pw)
    return False
