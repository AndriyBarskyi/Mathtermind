from PyQt5.QtWidgets import (
    QScrollArea, QWidget, QGridLayout, QFrame, QVBoxLayout,
    QSizePolicy, QLabel
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QTimer

from src.ui.widgets.lesson_card import LessonCard
from src.ui.theme import ThemeManager

class LessonsGrid(QScrollArea):
    """
    Grid layout for displaying lesson cards.
    Automatically adjusts the number of columns based on available width.
    """
    # Signal emitted when a lesson is started
    lesson_started = pyqtSignal(str)  # Emits lesson ID
    
    # Grid configuration
    GRID_SPACING = 24
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._lessons = []
        
        # Add resize timer to prevent excessive refreshes
        self._resize_timer = QTimer(self)
        self._resize_timer.setSingleShot(True)
        self._resize_timer.timeout.connect(self._delayed_refresh)
        
    def _setup_ui(self):
        """Set up the grid layout"""
        # Configure scroll area
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setFrameShape(QFrame.NoFrame)
        
        # Use ThemeManager for scroll area styling
        self.setStyleSheet(f"""
            QScrollArea {{
                background-color: transparent;
                border: none;
            }}
            QScrollBar:vertical {{
                background: {ThemeManager.get_color('input_background')};
                width: 8px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {ThemeManager.get_color('button_background')};
                min-height: 20px;
                border-radius: 4px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        # Create container widget
        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.container.setStyleSheet(f"background-color: {ThemeManager.get_color('app_background')};")
        
        # Create grid layout
        self.grid = QGridLayout(self.container)
        self.grid.setSpacing(self.GRID_SPACING)
        self.grid.setContentsMargins(0, 0, 0, 16)
        
        # Set container as scroll area widget
        self.setWidget(self.container)
    
    def set_lessons(self, lessons):
        """Update the grid with new lessons"""
        # Clear existing lessons
        self._lessons = lessons
        self._refresh_grid()
    
    def _refresh_grid(self):
        """Refresh the grid with current lessons"""
        # Clear existing lessons
        self._clear_grid()
        
        if not self._lessons:
            return
        
        # Calculate number of columns
        columns = self._calculate_columns()
        
        # Add new lesson cards
        for i, lesson in enumerate(self._lessons):
            # Calculate row and column
            row = i // columns
            col = i % columns
            
            # Create and add lesson card
            card = LessonCard(lesson)
            
            # Set a maximum size to prevent cards from becoming too large
            card.setMaximumWidth(int(LessonCard.MIN_CARD_WIDTH * 1.5))
            card.setMaximumHeight(int(LessonCard.MIN_CARD_HEIGHT * 1.5))
            
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
        card_width = LessonCard.MIN_CARD_WIDTH + self.GRID_SPACING
        columns = max(1, width // card_width)
        return columns
    
    def _delayed_refresh(self):
        """Delayed refresh to prevent excessive updates during resize"""
        self._refresh_grid()
    
    def resizeEvent(self, event):
        """Handle resize events to reflow the grid"""
        super().resizeEvent(event)
        
        # Cancel any pending timer and start a new one
        self._resize_timer.stop()
        self._resize_timer.start(150)  # 150ms delay before refresh
        
    def update_theme_styles(self):
        """Update all component styles when theme changes"""
        # Update scroll area styling
        self.setStyleSheet(f"""
            QScrollArea {{
                background-color: transparent;
                border: none;
            }}
            QScrollBar:vertical {{
                background: {ThemeManager.get_color('input_background')};
                width: 8px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {ThemeManager.get_color('button_background')};
                min-height: 20px;
                border-radius: 4px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        # Update container background
        self.container.setStyleSheet(f"background-color: {ThemeManager.get_color('app_background')};")
        
        # Update all lesson cards
        for i in range(self.grid.count()):
            item = self.grid.itemAt(i)
            if item and item.widget() and hasattr(item.widget(), 'update_theme_styles'):
                item.widget().update_theme_styles() 