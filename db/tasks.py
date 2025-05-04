import sqlite3
from db.user import DB_PATH_TASKS
def add_task(username, task):
    """
    Adds a new task to the database.
    :param user_id: The ID of the user who owns the task.
    :param task: The task description.
    :return: None
    """
    conn = sqlite3.connect(DB_PATH_TASKS)
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (username, task) VALUES (?, ?)", (username, task))
    conn.commit()
    conn.close()

def delete_task_db(username, task):
    """
    Deletes a task from the database.
    :param user_id: The ID of the user who owns the task.
    :param task: The task description.
    :return: None
    """
    conn = sqlite3.connect(DB_PATH_TASKS)
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE username = ? AND task = ?", (username, task))
    conn.commit()
    conn.close()
    
