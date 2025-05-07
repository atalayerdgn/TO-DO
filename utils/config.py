"""
Configuration module for the To-Do application.
Centralizes application settings and constants.
"""
import os
import json
from PyQt5.QtCore import QSettings

APP_NAME = "To-Do Application"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Atalay Erdogan"
GITHUB_URL = "https://github.com/atalayerdgn"

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DB_DIR, exist_ok=True)
USER_DB_PATH = os.path.join(DB_DIR, "users.db")
TASKS_DB_PATH = os.path.join(DB_DIR, "tasks.db")

DEFAULT_WINDOW_WIDTH = 1200
DEFAULT_WINDOW_HEIGHT = 800
REDIRECT_TIMEOUT = 1000

DEFAULT_FONT = "Arial"

class AppSettings:
    """Manages application settings using QSettings."""
    
    def __init__(self):
        self.settings = QSettings("AtolayErdogan", "ToDoApp")
    
    def get(self, key, default=None):
        """Get a setting value."""
        value = self.settings.value(key)
        return value if value is not None else default
    
    def set(self, key, value):
        """Set a setting value."""
        self.settings.setValue(key, value)
        self.settings.sync()
    
    def get_theme(self):
        """Get the current UI theme."""
        return self.get("theme", "light")
    
    def set_theme(self, theme):
        """Set the UI theme (light/dark)."""
        self.set("theme", theme)
    
    def get_user_preferences(self):
        """Get the user preferences."""
        prefs_json = self.get("user_preferences", "{}")
        try:
            return json.loads(prefs_json)
        except json.JSONDecodeError:
            return {}
    
    def set_user_preferences(self, preferences):
        """Set the user preferences."""
        self.set("user_preferences", json.dumps(preferences))
    
    def clear(self):
        """Clear all settings."""
        self.settings.clear() 
