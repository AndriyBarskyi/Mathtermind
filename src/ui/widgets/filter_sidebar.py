import datetime
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QCheckBox, QScrollArea, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from src.ui.widgets.range_slider import QRangeSlider
from src.ui.styles.constants import COLORS, FONTS, STYLES

class FilterSidebar(QFrame):
    """
    Widget representing the filter sidebar in the courses page.
    Provides filtering options for courses.
    """
    # Signals for filter changes
    filters_applied = pyqtSignal(dict)  # Emits filter settings
    filters_cleared = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        
        # Define constants
        self.MIN_YEAR = 2013
        self.MAX_YEAR = datetime.datetime.now().year
        
        # Initialize default filter state
        self.filter_state = {
            "subjects": ["info"],  # Default to "info" selected
            "levels": ["basic"],   # Default to "basic" selected
            "year_range": (self.MIN_YEAR, self.MAX_YEAR)
        }
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the sidebar UI"""
        # Create a scroll area for the sidebar content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        # Create the content widget for the scroll area
        sidebar_content = QWidget()
        layout = QVBoxLayout(sidebar_content)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # 1. Header with title and clear button
        header_layout = self._create_header()
        layout.addLayout(header_layout)
        
        # 2. Subject section
        layout.addWidget(self._create_section_label("Предмет"))
        
        # Create checkboxes for subjects
        self.subject_checkboxes = {
            "info": self._create_checkbox("Інформатика", True),
            "math": self._create_checkbox("Математика", False)
        }
        
        for checkbox in self.subject_checkboxes.values():
            layout.addWidget(checkbox)
        
        # 3. Level section
        layout.addWidget(self._create_section_label("Рівень"))
        
        # Create checkboxes for levels
        self.level_checkboxes = {
            "basic": self._create_checkbox("Базовий", True),
            "medium": self._create_checkbox("Середній", False),
            "advanced": self._create_checkbox("Просунутий", False)
        }
        
        for checkbox in self.level_checkboxes.values():
            layout.addWidget(checkbox)
        
        # 4. Updated period section with range slider
        layout.addWidget(self._create_section_label("Оновлено"))
        
        # Setup range slider with consistent values
        self.range_slider = QRangeSlider()
        self.range_slider.min_value = self.MIN_YEAR
        self.range_slider.max_value = self.MAX_YEAR
        self.range_slider.current_min = self.MIN_YEAR
        self.range_slider.current_max = self.MAX_YEAR
        self.range_slider.valueChanged.connect(self._on_range_changed)
        layout.addWidget(self.range_slider)
        
        # Date range labels
        date_range_layout = QHBoxLayout()
        self.start_year_label = QLabel(str(self.MIN_YEAR))
        self.end_year_label = QLabel(str(self.MAX_YEAR))
        
        for label in [self.start_year_label, self.end_year_label]:
            label.setFont(FONTS.BODY_SMALL)
            label.setStyleSheet(f"color: {COLORS.TEXT_PRIMARY};")
        
        date_range_layout.addWidget(self.start_year_label)
        date_range_layout.addStretch()
        date_range_layout.addWidget(self.end_year_label)
        layout.addLayout(date_range_layout)
        
        # 5. Apply button
        self.apply_btn = QPushButton("Застосувати")
        self.apply_btn.setFont(FONTS.BUTTON)
        self.apply_btn.setFixedHeight(36)
        self.apply_btn.setStyleSheet(STYLES.PRIMARY_BUTTON)
        self.apply_btn.clicked.connect(self._on_apply_filters)
        layout.addWidget(self.apply_btn)
        
        layout.addStretch()
        
        # Set the content widget to the scroll area
        scroll_area.setWidget(sidebar_content)
        
        # Add the scroll area to the sidebar
        sidebar_layout = QVBoxLayout(self)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.addWidget(scroll_area)
    
    def _create_header(self):
        """Create the header with title and clear button"""
        header_layout = QHBoxLayout()
        
        filter_label = QLabel("Фільтри")
        filter_label.setFont(FONTS.SUBTITLE)
        filter_label.setStyleSheet(f"color: {COLORS.TEXT_PRIMARY};")
        
        clear_btn = QPushButton("Очистити")
        clear_btn.setFont(FONTS.TAB)
        clear_btn.setStyleSheet(f"background-color: transparent; color: {COLORS.PRIMARY}; border: none;")
        clear_btn.clicked.connect(self._on_clear_filters)
        
        header_layout.addWidget(filter_label)
        header_layout.addStretch()
        header_layout.addWidget(clear_btn)
        
        return header_layout
    
    def _create_section_label(self, text):
        """Create a section label for the filter sidebar"""
        label = QLabel(text)
        label.setFont(FONTS.SUBTITLE)
        label.setStyleSheet(f"color: {COLORS.TEXT_PRIMARY};")
        return label
    
    def _create_checkbox(self, text, checked=False):
        """Create a styled checkbox"""
        checkbox = QCheckBox(text)
        checkbox.setFont(FONTS.TAB)
        checkbox.setChecked(checked)
        checkbox.setStyleSheet(STYLES.CHECKBOX)
        checkbox.stateChanged.connect(self._on_checkbox_changed)
        return checkbox
    
    def _on_checkbox_changed(self):
        """Handle checkbox state changes"""
        # Update filter state based on checkbox changes
        self.filter_state["subjects"] = [
            key for key, checkbox in self.subject_checkboxes.items() 
            if checkbox.isChecked()
        ]
        
        self.filter_state["levels"] = [
            key for key, checkbox in self.level_checkboxes.items() 
            if checkbox.isChecked()
        ]
        
        # Update the filter count in the header
        self._update_filter_count()
    
    def _on_range_changed(self, min_val, max_val):
        """Handle range slider changes"""
        self.filter_state["year_range"] = (min_val, max_val)
        self.start_year_label.setText(str(min_val))
        self.end_year_label.setText(str(max_val))
    
    def _on_apply_filters(self):
        """Apply the current filters"""
        self.filters_applied.emit(self.filter_state)
    
    def _on_clear_filters(self):
        """Clear all filters"""
        # Reset checkboxes
        for checkbox in self.subject_checkboxes.values():
            checkbox.setChecked(False)
        self.subject_checkboxes["info"].setChecked(True)
        
        for checkbox in self.level_checkboxes.values():
            checkbox.setChecked(False)
        self.level_checkboxes["basic"].setChecked(True)
        
        # Reset range slider
        self.range_slider.current_min = self.MIN_YEAR
        self.range_slider.current_max = self.MAX_YEAR
        self.start_year_label.setText(str(self.MIN_YEAR))
        self.end_year_label.setText(str(self.MAX_YEAR))
        self.range_slider.update()  # Force redraw
        
        # Reset filter state
        self.filter_state = {
            "subjects": ["info"],
            "levels": ["basic"],
            "year_range": (self.MIN_YEAR, self.MAX_YEAR)
        }
        
        # Update the filter count
        self._update_filter_count()
        
        # Emit signal
        self.filters_cleared.emit()
    
    def _update_filter_count(self):
        """Update the filter count in the header"""
        # Count active filters (excluding default ones)
        count = 0
        
        # Count selected subjects (excluding the default "info")
        subject_count = len(self.filter_state["subjects"])
        if subject_count > 0 and not (subject_count == 1 and "info" in self.filter_state["subjects"]):
            count += 1
            
        # Count selected levels (excluding the default "basic")
        level_count = len(self.filter_state["levels"])
        if level_count > 0 and not (level_count == 1 and "basic" in self.filter_state["levels"]):
            count += 1
            
        # Check if year range is different from default
        if self.filter_state["year_range"] != (self.MIN_YEAR, self.MAX_YEAR):
            count += 1
            
        # Update the filter label
        filter_text = f"Фільтри{f' ({count})' if count > 0 else ''}"
        self.findChild(QLabel, "", Qt.FindChildOption.FindDirectChildrenOnly).setText(filter_text) 