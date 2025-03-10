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
        
        # Filter state
        self.filter_state = {
            "subjects": [],
            "levels": [],
            "year_range": (2013, 2020)
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
        subject_label = self._create_section_label("Предмет")
        layout.addWidget(subject_label)
        
        # Create checkboxes for subjects
        self.subject_checkboxes = {
            "info": self._create_checkbox("Інформатика", True),
            "math": self._create_checkbox("Математика", False)
        }
        
        for checkbox in self.subject_checkboxes.values():
            layout.addWidget(checkbox)
        
        # 3. Level section
        level_label = self._create_section_label("Рівень")
        layout.addWidget(level_label)
        
        # Create checkboxes for levels
        self.level_checkboxes = {
            "basic": self._create_checkbox("Базовий", True),
            "medium": self._create_checkbox("Середній", False),
            "advanced": self._create_checkbox("Просунутий", False)
        }
        
        for checkbox in self.level_checkboxes.values():
            layout.addWidget(checkbox)
        
        # 4. Updated period section with range slider
        updated_label = self._create_section_label("Оновлено")
        layout.addWidget(updated_label)
        
        self.range_slider = QRangeSlider()
        # Set range values directly instead of using setRange
        self.range_slider.min_value = 2013
        self.range_slider.max_value = 2020
        self.range_slider.current_min = 2013
        self.range_slider.current_max = 2020
        layout.addWidget(self.range_slider)
        
        # Date range labels
        date_range_layout = QHBoxLayout()
        self.start_year_label = QLabel("2013")
        self.end_year_label = QLabel("2020")
        
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
        
        # Connect signals
        self.range_slider.valueChanged.connect(self._on_range_changed)
    
    def _create_header(self):
        """Create the header with title and clear button"""
        header_layout = QHBoxLayout()
        
        filter_label = QLabel("Фільтри (4)")
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
        self.range_slider.current_min = 2013
        self.range_slider.current_max = 2020
        self.start_year_label.setText("2013")
        self.end_year_label.setText("2020")
        self.range_slider.update()  # Force redraw
        
        # Reset filter state
        self.filter_state = {
            "subjects": ["info"],
            "levels": ["basic"],
            "year_range": (2013, 2020)
        }
        
        # Emit signal
        self.filters_cleared.emit() 