# src/ui/course_selection.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class CourseSelection(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Course Selection")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Course Selection Placeholder"))

        self.setLayout(layout)