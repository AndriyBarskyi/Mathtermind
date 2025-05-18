from PyQt5 import QtWidgets, QtCore, QtGui
from main_page import Ui_MainWindow
from account_login import*
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QAction
import sys
import os

# Add the parent directory to the path so we can import the ui package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core import app_state

from ui_wrapper import *
from account_login import LoginPage
from register_page import RegisterPage


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mathtermind")
        self.resize(1400, 900)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.main_stack = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.main_stack)
        
        # Логін
        self.login_page = LoginPage()
        self.login_page.login_successful.connect(self.show_main_interface)
        self.login_page.goto_register.connect(self.show_register)
        self.main_stack.addWidget(self.login_page)

        # Реєстрація
        self.register_page = RegisterPage()
        self.register_page.back_to_login.connect(self.show_login)
        self.main_stack.addWidget(self.register_page)

        # Головна частина
        self.ui_wrapper = UiWrapper()
        self.ui_page = self.ui_wrapper.centralWidget()
        self.main_stack.addWidget(self.ui_page)

        self.main_stack.setCurrentWidget(self.login_page)
        self.ui_wrapper.ui.btn_user.clicked.connect(self.show_menu)

    def show_main_interface(self):
        self.main_stack.setCurrentWidget(self.ui_page)

    def show_register(self):
        self.main_stack.setCurrentWidget(self.register_page)

    def show_login(self):
        self.main_stack.setCurrentWidget(self.login_page)

    def show_menu(self):
        menu = QMenu(self)
        
        # Get current user data
        user_data = app_state.get_current_user()
        username = user_data.get("username", "Користувач") if user_data else "Користувач"
        
        # Add username as a disabled action (just for display)
        user_display = QAction(f"Вітаємо, {username}", self)
        user_display.setEnabled(False)
        menu.addAction(user_display)
        menu.addSeparator()
        
        action1 = QAction("Змінити користувача", self)
        action2 = QAction("Вихід", self)
        action1.triggered.connect(self.action1_triggered)
        action2.triggered.connect(self.action2_triggered)
        menu.addAction(action1)
        menu.addAction(action2)
        menu.exec_(self.ui_wrapper.ui.btn_user.mapToGlobal(self.ui_wrapper.ui.btn_user.rect().bottomLeft()))

    def action1_triggered(self):
        # Log out current user and show login page
        self.logout_user()
        
    def action2_triggered(self):
        # Log out and go to login page
        self.logout_user()
        
    def logout_user(self):
        """Log out the current user and return to login page"""
        # Call logout method on the login page to reset fields and clear app state
        self.login_page.logout()
        self.main_stack.setCurrentWidget(self.login_page)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Find the style.qss file relative to the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    style_path = os.path.join(current_dir, "style.qss")
    
    try:
        # Try to open the style file
        with open(style_path, "r") as file:
            style_sheet = file.read()
            app.setStyleSheet(style_sheet)
    except FileNotFoundError:
        print(f"Style file not found at: {style_path}")
   
    window = MainApp()
    window.show()
    sys.exit(app.exec_())