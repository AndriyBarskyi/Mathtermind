from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class ContentArea(QWidget):
    """A content area for displaying dynamic content."""

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Welcome to the Learning Platform!")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

    def update_content(self, page_name):
        """Update the content area dynamically."""
        self.label.setText(f"Currently Viewing: {page_name}")
