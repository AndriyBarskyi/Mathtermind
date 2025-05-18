#!/usr/bin/env python3
"""
Mathtermind - A self-paced learning platform for mathematics and informatics

This is the main entry point for the Mathtermind application.
"""

import sys
from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMenu, QAction
from sqlalchemy import text

# Add project root to path if needed
project_root = Path(__file__).parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import our new core framework
from src.core import initialize, get_logger, debug_mode
from src.core.error_handling import (
    handle_ui_errors,
    with_error_boundary,
    DatabaseConnectionError,
    UIError,
    create_error_boundary
)

# Initialize core framework
initialize("development")

# Import application initialization
from src.app_init import init_app

# Get a logger for this module
logger = get_logger(__name__)

# Import application modules
from ui.main_page import MainWindowUI
from src.db import get_db
from src.config import DATABASE_URL, DEBUG_MODE


class MathtermindApp(QtWidgets.QMainWindow):
    """Main application window for Mathtermind."""
    
    def __init__(self):
        """Initialize the application window and UI components."""
        super().__init__()
        
        logger.info("Starting Mathtermind application")
        
        # Set up the UI
        with create_error_boundary("ui_setup"):
            self.ui = MainWindowUI()
            self.ui.setupUi(self)
            self.setWindowTitle("Mathtermind")
            
            # Connect signals to slots
            self._connect_signals()
        
        # Verify database connection
        with create_error_boundary("database_connection_check"):
            self._check_database_connection()
        
        logger.info("Application initialized successfully")
    
    def _connect_signals(self):
        """Connect UI signals to their respective slots."""
        logger.debug("Connecting UI signals to slots")
        self.ui.userButton.clicked.connect(self.show_user_menu)
    
    def _check_database_connection(self):
        """Check database connection and log status."""
        logger.info("Checking database connection")
        
        try:
            db = next(get_db())
            # Check if we can query the database
            course_count = db.execute(text("SELECT COUNT(*) FROM courses")).scalar()
            logger.info(f"Database connection successful. Found {course_count} courses.")
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            error_message = ("Database connection error. Please run 'python db_manage.py init' and "
                           "'python db_manage.py seed' to set up the database.")
            
            # Show error message to user
            QtWidgets.QMessageBox.critical(self, "Database Error", error_message)
            
            # Raise a proper exception
            raise DatabaseConnectionError(
                message="Failed to connect to the database",
                details={"error": str(e), "database_url": DATABASE_URL}
            ) from e

    @handle_ui_errors(component="user_menu")
    def show_user_menu(self):
        """Display the user menu when the user button is clicked."""
        logger.debug("Showing user menu")
        
        menu = QMenu(self)
        
        # Create menu actions
        change_user_action = QAction("Змінити користувача", self)
        exit_action = QAction("Вихід", self)
        
        # Connect actions to slots
        change_user_action.triggered.connect(self.on_change_user)
        exit_action.triggered.connect(self.on_exit)
        
        # Add actions to menu
        menu.addAction(change_user_action)
        menu.addAction(exit_action)
        
        # Show menu at the appropriate position
        menu.exec_(self.ui.userButton.mapToGlobal(self.ui.userButton.rect().bottomLeft()))

    @handle_ui_errors(component="change_user")
    def on_change_user(self):
        """Handle the change user action."""
        logger.info("Change user action triggered")
        print("Вибрана дія: Змінити користувача")
        
    @handle_ui_errors(component="exit")
    def on_exit(self):
        """Handle the exit action."""
        logger.info("Exit action triggered")
        QApplication.quit()


@with_error_boundary(name="load_stylesheet")
def load_stylesheet():
    """Load the application stylesheet."""
    logger.debug("Loading application stylesheet")
    
    try:
        stylesheet_path = Path("src/ui/style.qss")
        with open(stylesheet_path, "r") as file:
            stylesheet = file.read()
            logger.debug("Stylesheet loaded successfully")
            return stylesheet
    except FileNotFoundError:
        logger.warning("Style file not found: src/ui/style.qss")
        return ""
    except Exception as e:
        logger.error(f"Error loading stylesheet: {str(e)}")
        raise UIError(
            message="Failed to load application stylesheet",
            details={"error": str(e), "path": "src/ui/style.qss"}
        ) from e


def main():
    """Main entry point for the application."""
    try:
        # Initialize the application
        init_app()
        
        # Enable debug mode in debug mode
        if DEBUG_MODE:
            debug_mode()
            logger.info("Debug mode enabled")
        
        # Create the application
        app = QApplication(sys.argv)
        
        # Set application stylesheet
        stylesheet = load_stylesheet()
        if stylesheet:
            app.setStyleSheet(stylesheet)
        
        # Create and show the main window
        window = MathtermindApp()
        window.show()
        
        # Start the event loop
        return app.exec_()
    except Exception as e:
        logger.critical(f"Application failed to start: {str(e)}")
        
        # Show error dialog to user
        if QtWidgets.QApplication.instance():
            QtWidgets.QMessageBox.critical(
                None, 
                "Application Error",
                f"The application failed to start: {str(e)}"
            )
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
