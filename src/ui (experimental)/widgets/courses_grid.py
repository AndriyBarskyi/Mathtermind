from PyQt6.QtWidgets import (
    QScrollArea, QWidget, QGridLayout, QFrame, QVBoxLayout,
    QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from typing import List

from src.ui.models.course import Course
from src.ui.widgets.course_card import CourseCard

class CoursesGrid(QScrollArea):
    """
    Widget representing the grid of course cards.
    Displays a collection of courses in a grid layout.
    """
    # Signal emitted when a course is started
    course_started = pyqtSignal(str)  # Emits course ID
    
    # Grid configuration
    GRID_SPACING = 24
    # No longer using fixed CARDS_PER_ROW
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.courses = []
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the grid UI"""
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setFrameShape(QFrame.Shape.NoFrame)
        
        # Create container widget
        self.container = QWidget()
        self.container.setObjectName("coursesContainer")
        
        # Create main layout
        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create grid layout
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(self.GRID_SPACING)
        self.grid_layout.setContentsMargins(0, 0, 0, self.GRID_SPACING)
        
        # Set alignment to ensure cards are properly aligned
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        # Add grid layout to main layout
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addStretch()
        
        self.setWidget(self.container)
        
        # Set size policy to allow the grid to expand
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    
    def set_courses(self, courses: List[Course]):
        """Set the courses to display in the grid"""
        self.courses = courses
        self._refresh_grid()
    
    def _refresh_grid(self):
        """Refresh the grid with current courses"""
        # Clear existing widgets
        self._clear_grid()
        
        # Calculate cards per row based on available width
        available_width = self.viewport().width()
        min_card_width = CourseCard.MIN_CARD_WIDTH + self.GRID_SPACING
        cards_per_row = max(1, available_width // min_card_width)
        
        # Add course cards to the grid
        for i, course in enumerate(self.courses):
            card = CourseCard(course)
            # Connect the card's signal to our signal
            card.course_started.connect(self.course_started.emit)
            
            # Add cards with proper spacing
            row = i // cards_per_row
            col = i % cards_per_row
            self.grid_layout.addWidget(card, row, col, Qt.AlignmentFlag.AlignCenter)
    
    def _clear_grid(self):
        """Clear all widgets from the grid"""
        # Remove all widgets from the grid
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def resizeEvent(self, event):
        """Handle resize events to adjust the grid layout"""
        super().resizeEvent(event)
        # Refresh the grid when the widget is resized
        if hasattr(self, 'courses') and self.courses:
            self._refresh_grid()
    
    def filter_courses(self, filter_state: dict):
        """Filter courses based on filter state"""
        # This would be implemented to filter the courses based on the filter state
        # For now, we'll just refresh the grid
        self._refresh_grid() 