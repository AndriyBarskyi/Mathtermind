from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from src.ui.styles.constants import FONTS, STYLES

class FilterTabs(QWidget):
    """
    Widget representing the filter tabs at the top of the courses page.
    Provides tabs for filtering courses by status.
    """
    # Signal emitted when a tab is selected
    tab_changed = pyqtSignal(str)  # Emits tab ID
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_tab = "all"
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the tabs UI"""
        tabs_layout = QHBoxLayout(self)
        tabs_layout.setSpacing(8)
        tabs_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create tab buttons
        self.tabs = {
            "all": self._create_tab_button("Всі курси"),
            "active": self._create_tab_button("Активні (12)"),
            "completed": self._create_tab_button("Пройдені (2)")
        }
        
        # Add tabs to layout
        for tab_id, button in self.tabs.items():
            tabs_layout.addWidget(button)
        
        # Set default selected tab
        self.tabs["all"].setChecked(True)
    
    def _create_tab_button(self, text):
        """Create a tab button with proper styling"""
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setFont(FONTS.TAB)
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn.setStyleSheet(STYLES.TAB_BUTTON)
        btn.clicked.connect(lambda checked, b=btn: self._on_tab_clicked(b))
        return btn
    
    def _on_tab_clicked(self, button):
        """Handle tab button clicks"""
        # Uncheck all other tabs
        for tab_id, tab_button in self.tabs.items():
            if tab_button != button:
                tab_button.setChecked(False)
            else:
                # Make sure the clicked button is checked
                button.setChecked(True)
                self.active_tab = tab_id
        
        # Emit signal with the selected tab ID
        self.tab_changed.emit(self.active_tab)
    
    def update_counts(self, active_count, completed_count):
        """Update the counts displayed in the tabs"""
        self.tabs["active"].setText(f"Активні ({active_count})")
        self.tabs["completed"].setText(f"Пройдені ({completed_count})") 