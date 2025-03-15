import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from src.ui.ui import MainWindowUI
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QAction
from src.db import get_db, init_db
from src.db.seed_courses import seed_courses
from src.ui.theme import ThemeManager
from src.config import (
    DATABASE_URL,
    DEBUG_MODE,
)


class MathtermindApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainWindowUI()
        self.ui.setupUi(self)
        self.setWindowTitle("Mathtermind")
        
        # Connect button signals
        self.ui.userButton.clicked.connect(self.show_user_menu)
        
        # Connect theme toggle in settings if it exists
        if hasattr(self.ui, 'pg_settings') and hasattr(self.ui.pg_settings, 'themeToggle'):
            self.ui.pg_settings.themeToggle.toggled.connect(self.toggle_theme)
        
        # Test Database Interaction
        self.initialize_sample_data()

    def show_user_menu(self):
        menu = QMenu(self)

        change_user_action = QAction("Змінити користувача", self)
        exit_action = QAction("Вихід", self)

        change_user_action.triggered.connect(self.on_change_user)
        exit_action.triggered.connect(self.on_exit)
        menu.addAction(change_user_action)
        menu.addAction(exit_action)

        menu.exec_(self.ui.userButton.mapToGlobal(self.ui.userButton.rect().bottomLeft()))

    def on_change_user(self):
        print("Вибрана дія: Змінити користувача")
        
    def on_exit(self):
        sys.exit(app.exec_())
    
    def toggle_theme(self, checked):
        """Toggle between light and dark themes."""
        theme = ThemeManager.DARK_THEME if checked else ThemeManager.LIGHT_THEME
        ThemeManager.set_theme(theme)
        self.apply_theme()
    
    def apply_theme(self):
        """Apply the current theme to the application."""
        # Apply global stylesheet
        app.setStyleSheet(ThemeManager.get_theme_stylesheet())
        
        # Update UI components that need specific styling
        self.ui.update_theme_styles()
        
        # Update individual pages
        if hasattr(self.ui, 'pg_settings') and hasattr(self.ui.pg_settings, 'update_theme_styles'):
            self.ui.pg_settings.update_theme_styles()
            
        # Update other pages if they have theme update methods
        for page_name in ['pg_main', 'pg_courses', 'pg_lessons', 'pg_progress']:
            if hasattr(self.ui, page_name):
                page = getattr(self.ui, page_name)
                if hasattr(page, 'update_theme_styles'):
                    page.update_theme_styles()
        
    def initialize_sample_data(self):
        """Insert a test user into the database."""
        db = next(get_db())
        # Add your database operations here
        print("Test user created successfully!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Initialize database
    init_db.init_db()
    
    # Seed courses and lessons
    seed_courses()
    
    # Apply theme from ThemeManager
    app.setStyleSheet(ThemeManager.get_theme_stylesheet())

    window = MathtermindApp()
    window.show()
    sys.exit(app.exec_())
