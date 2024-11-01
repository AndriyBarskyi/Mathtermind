# src/ui/user_dashboard.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class UserDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Dashboard")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("User Dashboard Placeholder"))

        self.setLayout(layout)