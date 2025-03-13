from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class ContentArea(QWidget):
    """A dynamic content area for displaying different pages."""

    def __init__(self):
        super().__init__()
        # Use a clearer variable name to avoid conflicts
        self.content_layout = QVBoxLayout(self)

        # Main label for content display
        self.content_label = QLabel("Welcome to the Learning Platform!")
        self.content_label.setAlignment(Qt.AlignCenter)

        # Add label to layout
        self.content_layout.addWidget(self.content_label)

    def update_content(self, page_name: str):
        """Update the content label to reflect the current page."""
        self.content_label.setText(f"Currently Viewing: {page_name}")
