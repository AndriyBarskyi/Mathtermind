# src/ui/settings.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class Settings(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Settings Placeholder"))

        self.setLayout(layout)