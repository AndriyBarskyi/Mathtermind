from PyQt6.QtWidgets import QScrollArea, QWidget, QGridLayout, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal

from src.ui.widgets.lesson_card import LessonCard

class LessonsGrid(QScrollArea):
    """
    Grid layout for displaying lesson cards.
    Automatically adjusts the number of columns based on available width.
    """
    # Signal emitted when a lesson is started
    lesson_started = pyqtSignal(str)  # Emits lesson ID
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._lessons = []
        
    def _setup_ui(self):
        """Set up the grid layout"""
        # Configure scroll area
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create container widget
        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Create grid layout
        self.grid = QGridLayout(self.container)
        self.grid.setSpacing(16)
        self.grid.setContentsMargins(0, 0, 0, 0)
        
        # Set container as scroll area widget
        self.setWidget(self.container)
    
    def set_lessons(self, lessons):
        """Update the grid with new lessons"""
        # Clear existing lessons
        self._clear_grid()
        self._lessons = lessons
        
        # Add new lesson cards
        for i, lesson in enumerate(lessons):
            # Calculate row and column
            row = i // self._calculate_columns()
            col = i % self._calculate_columns()
            
            # Create and add lesson card
            card = LessonCard(lesson)
            card.lesson_started.connect(self.lesson_started.emit)
            self.grid.addWidget(card, row, col)
    
    def _clear_grid(self):
        """Remove all lesson cards from the grid"""
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def _calculate_columns(self):
        """Calculate number of columns based on container width"""
        width = self.viewport().width()
        min_card_width = LessonCard.MIN_CARD_WIDTH + self.grid.spacing()
        columns = max(1, width // min_card_width)
        return columns
    
    def resizeEvent(self, event):
        """Handle resize events to reflow the grid"""
        super().resizeEvent(event)
        if self._lessons:
            self.set_lessons(self._lessons) 