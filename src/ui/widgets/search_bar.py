from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QPushButton, QLabel
)
from PyQt6.QtCore import pyqtSignal, QTimer, Qt
from PyQt6.QtGui import QIcon, QFont

from src.ui.styles.constants import FONTS, STYLES, COLORS

class SearchBar(QWidget):
    """
    Widget representing the search bar in the courses page.
    Provides search functionality with a clear visual separation from filtering.
    """
    # Signals
    search_changed = pyqtSignal(str)  # Emits search text
    
    # Delay in milliseconds before emitting search signal
    SEARCH_DELAY = 300
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        
        # Setup search delay timer
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self._emit_search_text)
    
    def _setup_ui(self):
        """Set up the search bar UI"""
        search_layout = QHBoxLayout(self)
        search_layout.setSpacing(8)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введіть текст для пошуку")
        self.search_input.setFixedWidth(300)
        self.search_input.setFixedHeight(40)
        self.search_input.setFont(FONTS.TAB)
        
        # Add clear button to search input
        self.search_input.setClearButtonEnabled(True)
        
        # Connect search input to delayed signal
        self.search_input.textChanged.connect(self._on_text_changed)
        
        # Add to layout
        search_layout.addWidget(self.search_input)
    
    def _on_text_changed(self, text):
        """Handle text changes with a delay to avoid excessive filtering"""
        # Reset the timer on each text change
        self.search_timer.stop()
        
        # If text is empty, emit immediately to show all courses
        if not text.strip():
            self.search_changed.emit("")
        else:
            # Otherwise, start the timer for delayed search
            self.search_timer.start(self.SEARCH_DELAY)
    
    def _emit_search_text(self):
        """Emit the search text after the delay"""
        text = self.search_input.text().strip()
        self.search_changed.emit(text)
    
    def get_search_text(self):
        """Get the current search text"""
        return self.search_input.text().strip()
    
    def clear_search(self):
        """Clear the search input"""
        self.search_input.clear()
        # Emit empty search immediately
        self.search_changed.emit("")
    
    def set_search_text(self, text):
        """Set the search text programmatically"""
        self.search_input.setText(text)
        # The textChanged signal will handle the rest 