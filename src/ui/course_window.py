# src/ui/course_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class CourseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Course Window")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Course Window Placeholder"))

        self.setLayout(layout)