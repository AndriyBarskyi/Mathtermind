from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class ContentArea(QWidget):
    """A dynamic content area for displaying different pages."""

    def __init__(self):
        super().__init__()
        # Use a clearer variable name to avoid conflicts
        self.main_layout = QVBoxLayout(self)

        # Main label for content display
        self.label = QLabel("Welcome to the Learning Platform!")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add label to layout
        self.main_layout.addWidget(self.label)

    def update_content(self, page_name: str):
        """Update the content label to reflect the current page."""
        self.label.setText(f"Currently Viewing: {page_name}")
