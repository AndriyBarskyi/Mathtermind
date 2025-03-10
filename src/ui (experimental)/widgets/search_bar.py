from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QPushButton
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon, QFont

from src.ui.styles.constants import FONTS, STYLES, COLORS

class SearchBar(QWidget):
    """
    Widget representing the search bar in the courses page.
    Provides search functionality and filter button.
    """
    # Signals
    search_changed = pyqtSignal(str)  # Emits search text
    filter_button_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the search bar UI"""
        search_layout = QHBoxLayout(self)
        search_layout.setSpacing(8)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Пошук")
        self.search_input.setFixedWidth(300)
        self.search_input.setFixedHeight(40)
        self.search_input.setFont(FONTS.TAB)
        
        # Connect search input to signal
        self.search_input.textChanged.connect(self.search_changed.emit)
        
        # Create filter button
        self.filter_btn = QPushButton("Фільтри")
        self.filter_btn.setObjectName("filterButton")
        self.filter_btn.setIcon(QIcon("src/ui/assets/icons/filter.svg"))
        self.filter_btn.setFixedHeight(40)
        self.filter_btn.setFont(FONTS.TAB)
        self.filter_btn.setStyleSheet(STYLES.FILTER_BUTTON)
        
        # Connect filter button to signal
        self.filter_btn.clicked.connect(self.filter_button_clicked.emit)
        
        # Add to layout
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.filter_btn)
    
    def get_search_text(self):
        """Get the current search text"""
        return self.search_input.text()
    
    def clear_search(self):
        """Clear the search input"""
        self.search_input.clear()
        
    def update_filter_button_state(self, is_active):
        """Update the filter button state to indicate if filters are visible"""
        if is_active:
            self.filter_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS.PRIMARY_LIGHT};
                    color: {COLORS.PRIMARY};
                    border: 1px solid {COLORS.PRIMARY};
                    border-radius: 20px;
                    padding: 8px 16px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background-color: {COLORS.PRIMARY_LIGHT};
                    border-color: {COLORS.PRIMARY};
                }}
            """)
        else:
            self.filter_btn.setStyleSheet(STYLES.FILTER_BUTTON) 