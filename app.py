import sys
import logging
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer
from db.initdb import init_db, init_tasksdb
from ui.HomeUI import HomeUI
from ui.LoginUI import LoginUI
from ui.RegisterUI import RegisterUI
from ui.SettingsUI import SettingUI
from ui.RedirectUI import RedirectUI
from ui.MenuUI import MenuUI
from utils.config import AppSettings, APP_NAME, APP_VERSION, REDIRECT_TIMEOUT

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ApplicationManager:
    """
    Manages the application's UI flow and transitions between different screens.
    Centralizes UI management and provides cleaner organization.
    """
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName(APP_NAME)
        self.app.setApplicationVersion(APP_VERSION)
        
        self.settings = AppSettings()
        
        if not self._initialize_databases():
            sys.exit(1)
        
        self._initialize_ui_components()
        
        self._connect_signals()
    
    def _initialize_databases(self):
        """Initialize application databases with error handling."""
        try:
            if not init_db() or not init_tasksdb():
                self._show_error_message("Database Initialization Failed", 
                                        "Could not initialize one or more databases. Please check permissions and disk space.")
                return False
            logger.info("All databases initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            self._show_error_message("Database Error", 
                                    f"An error occurred during database initialization: {str(e)}")
            return False
    
    def _initialize_ui_components(self):
        """Initialize all UI components."""
        try:
            logger.info("Initializing UI components")
            self.home_ui = HomeUI()
            self.login_ui = LoginUI()
            self.register_ui = RegisterUI()
            self.menu_ui = MenuUI()
            self.redirect_ui = RedirectUI()
            self.settings_ui = SettingUI()
        except Exception as e:
            logger.error(f"UI initialization failed: {e}")
            self._show_error_message("UI Error", 
                                    f"An error occurred during UI initialization: {str(e)}")
            sys.exit(1)
    
    def _connect_signals(self):
        """Connect all UI signals to their respective handlers."""
        try:
            logger.info("Connecting UI signals")
            self.home_ui.login_signal.connect(
                lambda: self.switch_ui(self.home_ui, self.login_ui, None))
            self.home_ui.register_signal.connect(
                lambda: self.switch_ui(self.home_ui, self.register_ui, None))
            self.home_ui.setting_signal.connect(
                lambda: self.switch_ui(self.home_ui, self.settings_ui, None))
            self.login_ui.login_signal.connect(
                lambda: self.switch_ui(self.login_ui, self.menu_ui, self.redirect_ui))
            self.login_ui.back_home.connect(
                lambda: self.switch_ui(self.login_ui, self.home_ui, None))
            self.login_ui.register_signal.connect(
                lambda: self.switch_ui(self.login_ui, self.register_ui, self.redirect_ui))
            self.register_ui.register_signal.connect(
                lambda: self.switch_ui(self.register_ui, self.login_ui, self.redirect_ui))
            self.register_ui.back_home.connect(
                lambda: self.switch_ui(self.register_ui, self.home_ui, None))
            self.settings_ui.back_home.connect(
                lambda: self.switch_ui(self.settings_ui, self.home_ui, None))
            self.menu_ui.backtohome_signal.connect(
                lambda: self.switch_ui(self.menu_ui, self.home_ui, None))
        except Exception as e:
            logger.error(f"Signal connection failed: {e}")
            self._show_error_message("Application Error", 
                                    f"An error occurred during signal connection: {str(e)}")
            sys.exit(1)
    
    def switch_ui(self, current_ui, next_ui, redir):
        """
        Switches the current UI to the next UI with optional redirection.
        
        Args:
            current_ui: The current UI instance.
            next_ui: The next UI instance to switch to.
            redir: The redirecting UI instance to show briefly (or None for direct transition).
        """
        try:
            logger.info(f"Switching from {current_ui.__class__.__name__} to {next_ui.__class__.__name__}")
            
            if redir is None:
                next_ui.move(current_ui.pos())
                current_ui.hide()
                next_ui.show()
                return
                
            redir.move(current_ui.pos())
            next_ui.move(redir.pos())
            current_ui.hide()
            redir.show()
            QTimer.singleShot(REDIRECT_TIMEOUT, lambda: self._hide_redirect_and_show_next(redir, next_ui))
        except Exception as e:
            logger.error(f"Error during UI transition: {e}")
            self._show_error_message("UI Transition Error", 
                                   f"An error occurred during UI transition: {str(e)}")
    
    def _hide_redirect_and_show_next(self, redir, next_ui):
        """
        Hides the redirect UI and shows the next UI.
        
        Args:
            redir: The redirecting UI to hide.
            next_ui: The next UI to show.
        """
        try:
            redir.hide()
            next_ui.show()
        except Exception as e:
            logger.error(f"Error during redirect transition: {e}")
    
    def _show_error_message(self, title, message):
        """Display an error message box."""
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.exec_()
    
    def run(self):
        """Start the application and show the home screen."""
        try:
            logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
            self.home_ui.show()
            return self.app.exec_()
        except Exception as e:
            logger.critical(f"Application failed to start: {e}")
            self._show_error_message("Critical Error", 
                                   f"Application failed to start: {str(e)}")
            return 1

def main():
    """Application entry point."""
    try:
        app_manager = ApplicationManager()
        sys.exit(app_manager.run())
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    
