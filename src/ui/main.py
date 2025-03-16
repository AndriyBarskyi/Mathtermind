from PyQt5 import QtWidgets, QtCore, QtGui
from ui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QAction
import sys
#from listw import *
class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Mathtermind")
        self.ui.btn_user.clicked.connect(self.show_menu)





        

    def show_menu(self):
        menu = QMenu(self)

        action1 = QAction("Змінити користувача", self)
        action2 = QAction("Вихід", self)

        action1.triggered.connect(self.action1_triggered)
        action2.triggered.connect(self.action2_triggered)
        menu.addAction(action1)
        menu.addAction(action2)

        menu.exec_(self.ui.btn_user.mapToGlobal(self.ui.btn_user.rect().bottomLeft()))

    def action1_triggered(self):
        print("Вибрана дія 1")
        
    def action2_triggered(self):
        sys.exit(app.exec_())
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    with open("style.qss", "r") as file:
        style_sheet = file.read()
        

    app.setStyleSheet(style_sheet)
   
    

    window = MainApp()
    window.show()
    sys.exit(app.exec_())
