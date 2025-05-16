from PyQt5 import QtWidgets, QtCore, QtGui
from ui import Ui_MainWindow
from account_login import*
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QAction
import sys
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
        action1 = QAction("Змінити користувача", self)
        action2 = QAction("Вихід", self)
        action1.triggered.connect(self.action1_triggered)
        action2.triggered.connect(self.action2_triggered)
        menu.addAction(action1)
        menu.addAction(action2)
        menu.exec_(self.ui_wrapper.ui.btn_user.mapToGlobal(self.ui_wrapper.ui.btn_user.rect().bottomLeft()))

    def action1_triggered(self):
        print("Вибрана дія 1")
        
    def action2_triggered(self):
        self.main_stack.setCurrentWidget(self.login_page)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    with open("style.qss", "r") as file:
        style_sheet = file.read()
    app.setStyleSheet(style_sheet)
   
    window = MainApp()
    window.show()
    sys.exit(app.exec_())