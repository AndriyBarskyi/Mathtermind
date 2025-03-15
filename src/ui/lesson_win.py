from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QScrollArea,
    QFrame,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from src.ui.widgets.lessons_grid import LessonsGrid
from src.ui.services.course_service import CourseService
from src.ui.services.lesson_service import LessonService
from src.ui.styles.constants import COLORS, FONTS
from src.ui.theme import ThemeManager

class CourseTab(QPushButton):
    """Custom tab button for course navigation"""
    def __init__(self, course, parent=None):
        super().__init__(parent)
        self.course = course
        self.setText(course.name)
        self.setCheckable(True)
        self.setFont(QFont("Inter", 12))
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumWidth(120)
        self.setFixedHeight(36)
        
        # Apply styles using ThemeManager
        self.setStyleSheet(f"""
            QPushButton {{
                border: none;
                border-bottom: 2px solid transparent;
                color: {ThemeManager.get_color('secondary_text')};
                padding: 0 16px;
            }}
            QPushButton:checked {{
                border-bottom: 2px solid {ThemeManager.get_color('accent_primary')};
                color: {ThemeManager.get_color('accent_primary')};
            }}
            QPushButton:hover:!checked {{
                color: {ThemeManager.get_color('primary_text')};
            }}
        """)
    
    def update_theme_styles(self):
        """Update styles when theme changes"""
        self.setStyleSheet(f"""
            QPushButton {{
                border: none;
                border-bottom: 2px solid transparent;
                color: {ThemeManager.get_color('secondary_text')};
                padding: 0 16px;
            }}
            QPushButton:checked {{
                border-bottom: 2px solid {ThemeManager.get_color('accent_primary')};
                color: {ThemeManager.get_color('accent_primary')};
            }}
            QPushButton:hover:!checked {{
                color: {ThemeManager.get_color('primary_text')};
            }}
        """)

class LessonDetailPage(QWidget):
    """
    Page displaying lessons for enrolled courses.
    Features:
    1. Course tabs at the top for quick navigation between enrolled courses
    2. Current course title and details button
    3. Grid of lesson cards sorted by lesson order
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize services
        self.course_service = CourseService()
        self.lesson_service = LessonService()
        
        # Initialize state
        self.current_course = None
        self.active_courses = []
        
        self._setup_ui()
        self._connect_signals()
        self._load_active_courses()
    
    def _setup_ui(self):
        """Set up the main UI layout"""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(16)
        
        # 1. Course tabs scroll area
        self.tabs_scroll = QScrollArea()
        self.tabs_scroll.setWidgetResizable(True)
        self.tabs_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tabs_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tabs_scroll.setMaximumHeight(50)
        self.tabs_scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        # Tabs container
        self.tabs_container = QWidget()
        self.tabs_layout = QHBoxLayout(self.tabs_container)
        self.tabs_layout.setSpacing(8)
        self.tabs_layout.setContentsMargins(0, 0, 0, 0)
        self.tabs_scroll.setWidget(self.tabs_container)
        
        # 2. Course header
        header_layout = QHBoxLayout()
        
        # Course title
        self.course_title = QLabel("Виберіть курс")
        self.course_title.setFont(FONTS.H1)
        
        # Use ThemeManager for title text color
        self.course_title.setStyleSheet(f"color: {ThemeManager.get_color('primary_text')};")
        
        # Course details button
        self.details_btn = QPushButton("Деталі курсу")
        self.details_btn.setFont(QFont("Inter", 13))
        self.details_btn.setCursor(Qt.PointingHandCursor)
        
        # Use ThemeManager for button styling
        self.details_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid {ThemeManager.get_color('accent_primary')};
                color: {ThemeManager.get_color('accent_primary')};
                border-radius: 25px;
                padding: 0 24px;
            }}
            QPushButton:hover {{
                background-color: {ThemeManager.get_color('accent_secondary')};
            }}
        """)
        
        self.details_btn.setFixedHeight(36)
        
        header_layout.addWidget(self.course_title)
        header_layout.addStretch()
        header_layout.addWidget(self.details_btn)
        
        # 3. Lessons grid
        self.lessons_grid = LessonsGrid()
        
        # Add all components to main layout
        self.main_layout.addWidget(self.tabs_scroll)
        self.main_layout.addLayout(header_layout)
        self.main_layout.addWidget(self.lessons_grid)
    
    def _connect_signals(self):
        """Connect all signals"""
        self.details_btn.clicked.connect(self._on_details_clicked)
        self.lessons_grid.lesson_started.connect(self._on_lesson_started)
    
    def _load_active_courses(self):
        """Load active courses for the current user"""
        # Get active courses from the service
        self.active_courses = self.course_service.get_active_courses()
        
        # Update the course tabs
        self.update_course_tabs(self.active_courses)
        
        # Load the first course if available
        if self.active_courses:
            self.load_course(self.active_courses[0].id)
    
    def _on_details_clicked(self):
        """Handle course details button click"""
        if self.current_course:
            # TODO: Show course details dialog or navigate to details page
            print(f"Showing details for course: {self.current_course.name}")
    
    def _on_course_tab_clicked(self):
        """Handle course tab selection"""
        tab = self.sender()
        if tab and isinstance(tab, CourseTab):
            self.load_course(tab.course.id)
    
    def _on_lesson_started(self, lesson_id):
        """Handle lesson started signal"""
        # TODO: Navigate to lesson content page
        print(f"Starting lesson: {lesson_id}")
    
    def load_course(self, course_id):
        """Load a course and its lessons"""
        # Get course data
        course = self.course_service.get_course_by_id(course_id)
        if not course:
            return
        
        self.current_course = course
        
        # Update UI
        self.course_title.setText(course.name)
        
        # Get and display lessons
        lessons = self.lesson_service.get_lessons_by_course_id(course_id)
        
        # Sort lessons by lesson_order
        sorted_lessons = sorted(lessons, key=lambda lesson: lesson.lesson_order)
        
        self.lessons_grid.set_lessons(sorted_lessons)
        
        # Update active tab
        for i in range(self.tabs_layout.count()):
            widget = self.tabs_layout.itemAt(i).widget()
            if isinstance(widget, CourseTab):
                widget.setChecked(widget.course.id == course_id)
    
    def update_course_tabs(self, active_courses):
        """Update the course tabs with active courses"""
        # Clear existing tabs
        while self.tabs_layout.count():
            item = self.tabs_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add new tabs
        for course in active_courses:
            tab = CourseTab(course)
            tab.clicked.connect(self._on_course_tab_clicked)
            self.tabs_layout.addWidget(tab)
        
        # Add stretch at the end
        self.tabs_layout.addStretch()
        
        # If we have a current course, make sure its tab is selected
        if self.current_course:
            for i in range(self.tabs_layout.count()):
                widget = self.tabs_layout.itemAt(i).widget()
                if isinstance(widget, CourseTab) and widget.course.id == self.current_course.id:
                    widget.setChecked(True)
    
    def update_theme_styles(self):
        """Update all component styles when theme changes"""
        # Update course title
        self.course_title.setStyleSheet(f"color: {ThemeManager.get_color('primary_text')};")
        
        # Update details button
        self.details_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid {ThemeManager.get_color('accent_primary')};
                color: {ThemeManager.get_color('accent_primary')};
                border-radius: 25px;
                padding: 0 24px;
            }}
            QPushButton:hover {{
                background-color: {ThemeManager.get_color('accent_secondary')};
            }}
        """)
        
        # Update course tabs
        for i in range(self.tabs_layout.count()):
            widget = self.tabs_layout.itemAt(i).widget()
            if isinstance(widget, CourseTab):
                widget.update_theme_styles()
        
        # Update lessons grid
        if hasattr(self.lessons_grid, 'update_theme_styles'):
            self.lessons_grid.update_theme_styles()
        
        # Update all lesson cards directly
        for card in self.lessons_grid.findChildren(QFrame):
            if hasattr(card, 'update_theme_styles'):
                card.update_theme_styles() 