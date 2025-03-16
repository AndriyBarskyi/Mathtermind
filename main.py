#!/usr/bin/env python3
"""
Mathtermind - A self-paced learning platform for mathematics and informatics

This is the main entry point for the Mathtermind application.
"""

import sys
import logging
from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMenu, QAction
from sqlalchemy import text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add project root to path if needed
project_root = Path(__file__).parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import application modules
from src.ui.ui import MainWindowUI
from src.db import get_db
from src.config import DATABASE_URL, DEBUG_MODE


class MathtermindApp(QtWidgets.QMainWindow):
    """Main application window for Mathtermind."""
    
    def __init__(self):
        """Initialize the application window and UI components."""
        super().__init__()
        
        # Set up the UI
        self.ui = MainWindowUI()
        self.ui.setupUi(self)
        self.setWindowTitle("Mathtermind")
        
        # Connect signals to slots
        self._connect_signals()
        
        # Verify database connection
        self._check_database_connection()
        
        logger.info("Application initialized successfully")
    
    def _connect_signals(self):
        """Connect UI signals to their respective slots."""
        self.ui.userButton.clicked.connect(self.show_user_menu)
    
    def _check_database_connection(self):
        """Check database connection and log status."""
        try:
            db = next(get_db())
            # Check if we can query the database
            course_count = db.execute(text("SELECT COUNT(*) FROM courses")).scalar()
            logger.info(f"Database connection successful. Found {course_count} courses.")
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            print("Database connection error. Please run 'python db_manage.py init' and "
                  "'python db_manage.py seed' to set up the database.")

    def show_user_menu(self):
        """Display the user menu when the user button is clicked."""
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

    def on_change_user(self):
        """Handle the change user action."""
        logger.info("Change user action triggered")
        print("Вибрана дія: Змінити користувача")
        
    def on_exit(self):
        """Handle the exit action."""
        logger.info("Exit action triggered")
        QApplication.quit()


def load_stylesheet():
    """Load the application stylesheet."""
    try:
        stylesheet_path = Path("src/ui/style.qss")
        with open(stylesheet_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        logger.warning("Style file not found: src/ui/style.qss")
        return ""


def main():
    """Main entry point for the application."""
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


if __name__ == "__main__":
    sys.exit(main())
