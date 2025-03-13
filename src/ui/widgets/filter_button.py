from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon, QFont

from src.ui.styles.constants import FONTS, STYLES, COLORS

class FilterButton(QPushButton):
    """
    Widget representing the filter button in the courses page.
    Provides filter functionality with a clear visual separation from search.
    """
    # Signals
    filter_button_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__("Фільтри", parent)
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the filter button UI"""
        self.setObjectName("filterButton")
        self.setIcon(QIcon("src/ui/assets/icons/filter.svg"))
        self.setFixedHeight(40)
        self.setFont(FONTS.TAB)
        self.setStyleSheet(STYLES.FILTER_BUTTON)
        
        # Connect filter button to signal
        self.clicked.connect(self.filter_button_clicked.emit)
    
    def update_state(self, is_active):
        """Update the filter button state to indicate if filters are visible"""
        if is_active:
            self.setStyleSheet(f"""
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
            self.setStyleSheet(STYLES.FILTER_BUTTON) 