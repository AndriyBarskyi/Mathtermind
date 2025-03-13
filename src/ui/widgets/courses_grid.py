from PyQt5.QtWidgets import (
    QScrollArea, QWidget, QGridLayout, QFrame, QVBoxLayout,
    QSizePolicy, QLabel
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QTimer
from typing import List

from src.ui.models.course import Course
from src.ui.widgets.course_card import CourseCard
from src.ui.widgets.flow_layout import FlowLayout

class CoursesGrid(QScrollArea):
    """
    Widget representing the grid of course cards.
    Displays a collection of courses in a grid layout.
    """
    # Signal emitted when a course is started
    course_started = pyqtSignal(str)  # Emits course ID
    
    # Grid configuration
    GRID_SPACING = 24
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.courses = []
        self.current_filter_state = {}
        self.refresh_timer = QTimer()
        self.refresh_timer.setSingleShot(True)
        self.refresh_timer.timeout.connect(self._refresh_grid)
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the grid UI"""
        # Make the scroll area take up all available space
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setFrameShape(QFrame.NoFrame)
        
        # Create a container widget for the grid
        self.container = QWidget()
        self.setWidget(self.container)
        
        # Create a main layout for the container
        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create a flow layout for the course cards
        self.flow_layout = FlowLayout()
        self.flow_layout.setSpacing(self.GRID_SPACING)
        
        # Create a label for no results message
        self.no_results_label = QLabel("Немає результатів")
        self.no_results_label.setAlignment(Qt.AlignCenter)
        self.no_results_label.setStyleSheet("""
            font-size: 18px;
            color: #858A94;
            margin: 40px 0;
        """)
        self.no_results_label.hide()
        
        # Add layouts to main layout
        self.main_layout.addLayout(self.flow_layout)
        self.main_layout.addWidget(self.no_results_label)
        self.main_layout.addStretch()
        
        # Set background color
        self.setStyleSheet("background-color: #F7F8FA;")
    
    def set_courses(self, courses: List[Course]):
        """Set the courses to display in the grid"""
        self.courses = courses
        self._delayed_refresh()
    
    def _refresh_grid(self):
        """Refresh the grid with current courses"""
        # Clear existing courses
        self._clear_grid()
        
        if not self.courses:
            self.show_no_results_message()
            return
        
        # Calculate number of columns
        columns = self._calculate_columns()
        
        # Add new course cards
        for i, course in enumerate(self.courses):
            # Calculate row and column
            row = i // columns
            col = i % columns
            
            # Create and add course card
            card = CourseCard(course)
            card.course_started.connect(self.course_started.emit)
            
            # Set a maximum size to prevent cards from becoming too large
            card.setMaximumWidth(int(CourseCard.MIN_CARD_WIDTH * 1.5))
            card.setMaximumHeight(int(CourseCard.MIN_CARD_HEIGHT * 1.5))
            
            self.flow_layout.addWidget(card)
    
    def _clear_grid(self):
        """Remove all course cards from the grid"""
        self.flow_layout.clear()
    
    def _calculate_columns(self):
        """Calculate number of columns based on container width"""
        width = self.viewport().width()
        card_width = CourseCard.MIN_CARD_WIDTH + self.GRID_SPACING
        columns = max(1, width // card_width)
        return columns
    
    def _delayed_refresh(self):
        """Delayed refresh to prevent excessive updates during resize"""
        self._refresh_grid()
    
    def resizeEvent(self, event):
        """Handle resize events to reflow the grid"""
        super().resizeEvent(event)
        
        # Cancel any pending timer and start a new one
        self.refresh_timer.stop()
        self.refresh_timer.start(150)  # 150ms delay before refresh
    
    def filter_courses(self, filter_state: dict):
        """Apply filters to the courses"""
        # This would be implemented to filter courses based on filter_state
        # For now, just refresh the grid
        self._refresh_grid()
    
    def show_no_results_message(self, message: str = "Немає результатів"):
        """Show a message when no results are found"""
        self.no_results_label.setText(message)
        self.no_results_label.show()
    
    def hide_no_results_message(self):
        """Hide the no results message"""
        self.no_results_label.hide() 