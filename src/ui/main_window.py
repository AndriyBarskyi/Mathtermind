# src/ui/main_window.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Main Window Placeholder"))

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)