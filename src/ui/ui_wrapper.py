from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from ui import Ui_MainWindow

class UiWrapper(QMainWindow):
    def __init__(self):
        super().__init__()

        
        self.setMinimumSize(1700, 865)  
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
