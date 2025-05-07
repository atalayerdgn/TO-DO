"""
Database utility module.
Provides a centralized database connection and operation interface.
"""
import sqlite3
import logging
from utils.config import USER_DB_PATH, TASKS_DB_PATH

logger = logging.getLogger(__name__)

class Database:
    """Database connection and operation class."""
    
    def __init__(self, db_path):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """
        Establish database connection.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            return True
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    def execute(self, query, params=None):
        """
        Execute a database query.
        
        Args:
            query: SQL query string
            params: Parameters for the query (optional)
            
        Returns:
            cursor: Database cursor for fetching results
        """
        try:
            if not self.connection:
                self.connect()
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
                
            return self.cursor
        except sqlite3.Error as e:
            logger.error(f"Query execution error: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            raise
    
    def commit(self):
        """Commit current transaction."""
        if self.connection:
            self.connection.commit()
    
    def rollback(self):
        """Rollback current transaction."""
        if self.connection:
            self.connection.rollback()
    
    def fetch_one(self, query, params=None):
        """
        Execute query and fetch one result.
        
        Args:
            query: SQL query string
            params: Parameters for the query (optional)
            
        Returns:
            row: Single database row or None
        """
        cursor = self.execute(query, params)
        return cursor.fetchone()
    
    def fetch_all(self, query, params=None):
        """
        Execute query and fetch all results.
        
        Args:
            query: SQL query string
            params: Parameters for the query (optional)
            
        Returns:
            rows: List of database rows
        """
        cursor = self.execute(query, params)
        return cursor.fetchall()
    
    def execute_transaction(self, queries_and_params):
        """
        Execute multiple queries as a transaction.
        
        Args:
            queries_and_params: List of (query, params) tuples
            
        Returns:
            bool: True if transaction successful, False otherwise
        """
        if not self.connection:
            self.connect()
            
        try:
            for query, params in queries_and_params:
                self.execute(query, params)
            self.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Transaction execution error: {e}")
            self.rollback()
            return False


class UserDatabase(Database):
    """User database operations."""
    
    def __init__(self):
        """Initialize user database connection."""
        super().__init__(USER_DB_PATH)
    
    def get_user(self, username):
        """
        Get user by username.
        
        Args:
            username: Username to lookup
            
        Returns:
            user: User data or None if not found
        """
        return self.fetch_one(
            "SELECT id, username, email, password FROM users WHERE username = ?",
            (username,)
        )
    
    def add_user(self, username, email, password):
        """
        Add a new user.
        
        Args:
            username: Username
            email: Email address
            password: Hashed password
            
        Returns:
            bool: True if user added successfully, False otherwise
        """
        try:
            self.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )
            self.commit()
            return True
        except sqlite3.IntegrityError:
            logger.warning(f"Attempted to add duplicate user: {username}")
            return False
        except Exception as e:
            logger.error(f"Error adding user: {e}")
            return False
    
    def update_last_login(self, username):
        """
        Update user's last login timestamp.
        
        Args:
            username: Username
            
        Returns:
            bool: True if updated successfully
        """
        try:
            self.execute(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE username = ?",
                (username,)
            )
            self.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating last login: {e}")
            return False


class TasksDatabase(Database):
    """Tasks database operations."""
    
    def __init__(self):
        """Initialize tasks database connection."""
        super().__init__(TASKS_DB_PATH)
    
    def get_user_tasks(self, username):
        """
        Get all tasks for a user.
        
        Args:
            username: Username
            
        Returns:
            tasks: List of task data
        """
        return self.fetch_all(
            """SELECT id, task, status, priority, created_at, due_date, completed_at 
               FROM tasks 
               WHERE username = ? 
               ORDER BY priority DESC, created_at DESC""",
            (username,)
        )
    
    def add_task(self, username, task, priority=0, due_date=None):
        """
        Add a new task for a user.
        
        Args:
            username: Username
            task: Task description
            priority: Task priority (0-5)
            due_date: Task due date (optional)
            
        Returns:
            bool: True if task added successfully
        """
        try:
            self.execute(
                """INSERT INTO tasks (username, task, priority, due_date) 
                   VALUES (?, ?, ?, ?)""",
                (username, task, priority, due_date)
            )
            self.commit()
            return True
        except Exception as e:
            logger.error(f"Error adding task: {e}")
            return False
    
    def update_task_status(self, task_id, status):
        """
        Update task status.
        
        Args:
            task_id: Task ID
            status: New status ('pending', 'in_progress', 'completed')
            
        Returns:
            bool: True if updated successfully
        """
        try:
            completed_at = None
            if status == 'completed':
                self.execute(
                    """UPDATE tasks 
                       SET status = ?, completed_at = CURRENT_TIMESTAMP 
                       WHERE id = ?""",
                    (status, task_id)
                )
            else:
                self.execute(
                    """UPDATE tasks 
                       SET status = ?, completed_at = NULL 
                       WHERE id = ?""",
                    (status, task_id)
                )
            self.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating task status: {e}")
            return False
    
    def delete_task(self, task_id):
        """
        Delete a task.
        
        Args:
            task_id: Task ID
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            self.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting task: {e}")
            return False 
