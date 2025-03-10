from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class PlaceholderPage(QWidget):
    """
    A simple placeholder page to display when a feature is not yet implemented.
    """
    def __init__(self, page_name, parent=None):
        super().__init__(parent)
        self.page_name = page_name
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the UI components."""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create a label with the placeholder message
        message = QLabel(f"Сторінка '{self.page_name}' знаходиться в розробці.")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setStyleSheet("""
            font-size: 18px;
            color: #566CD2;
            margin: 20px;
        """)
        
        # Add a secondary message
        secondary_message = QLabel("Ця функціональність буде доступна в наступних версіях.")
        secondary_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        secondary_message.setStyleSheet("""
            font-size: 14px;
            color: #858A94;
            margin: 10px;
        """)
        
        layout.addWidget(message)
        layout.addWidget(secondary_message) 