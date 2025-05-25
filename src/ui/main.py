import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from ui import Ui_MainWindow
from account_login import*
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QAction
from ui_wrapper import *
from account_login import LoginPage
from register_page import RegisterPage
from src.services import SessionManager

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mathtermind")
        self.resize(1400, 900)

        icon = QtGui.QIcon()
        icon_path = os.path.join(SCRIPT_DIR, "icon/logo.png")
        icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        self.ui_wrapper.update_user_display()
        self.ui_wrapper.refresh_main_page_data()

    def show_register(self):
        self.main_stack.setCurrentWidget(self.register_page)

    def show_login(self):
        self.main_stack.setCurrentWidget(self.login_page)

    def show_menu(self):
        menu = QMenu(self)
        action1 = QAction("Змінити користувача", self)
        action2 = QAction("Вихід", self)
        action1.triggered.connect(self.action1_triggered)
        action2.triggered.connect(self.action2_triggered)
        menu.addAction(action1)
        menu.addAction(action2)
        menu.exec_(self.ui_wrapper.ui.btn_user.mapToGlobal(self.ui_wrapper.ui.btn_user.rect().bottomLeft()))

    def action1_triggered(self):
        SessionManager.set_current_user(None)
        self.main_stack.setCurrentWidget(self.login_page)
        
    def action2_triggered(self):
        self.main_stack.setCurrentWidget(self.login_page)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    style_file_path = os.path.join(SCRIPT_DIR, "style.qss")
    try:
        with open(style_file_path, "r") as file:
            style_sheet = file.read()
        app.setStyleSheet(style_sheet)
    except FileNotFoundError:
        print(f"Warning: Could not find style.qss at {style_file_path}. Application will run without custom styles from this file.")
    except Exception as e:
        print(f"Warning: Error loading style.qss: {e}. Application will run without custom styles from this file.")
   
    window = MainApp()
    window.show()
    sys.exit(app.exec_())