import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from src.ui.ui import MainWindowUI
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QAction
from src.db import get_db, init_db
from src.db.seed_courses import seed_courses
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
    
    # Load stylesheet
    try:
        with open("src/ui/style.qss", "r") as file:
            style_sheet = file.read()
            app.setStyleSheet(style_sheet)
    except FileNotFoundError:
        print("Warning: style.qss file not found.")

    window = MathtermindApp()
    window.show()
    sys.exit(app.exec_())
