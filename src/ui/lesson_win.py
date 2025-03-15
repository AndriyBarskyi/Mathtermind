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
import logging

from src.ui.widgets.lessons_grid import LessonsGrid
from src.services.course_service import CourseService, Course
from src.services.lesson_service import LessonService, Lesson
from src.ui.styles.constants import COLORS, FONTS

logger = logging.getLogger(__name__)

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
        
        # Apply styles
        self.setStyleSheet("""
            QPushButton {
                border: none;
                border-bottom: 2px solid transparent;
                color: #666666;
                padding: 0 16px;
            }
            QPushButton:checked {
                border-bottom: 2px solid #2196F3;
                color: #2196F3;
            }
            QPushButton:hover:!checked {
                color: #333333;
            }
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
        
        # Set object name for finding this widget
        self.setObjectName("lessonDetailPage")
        
        # Initialize services
        self.course_service = CourseService()
        self.lesson_service = LessonService()
        
        # Initialize state
        self.current_course = None
        self.active_courses = []
        self.current_user_id = None
        
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Set up the main UI layout"""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(16)
        
        # Create the navigation bar - SIMPLE IMPLEMENTATION FROM test_nav_bar.py
        nav_bar = QScrollArea()
        nav_bar.setWidgetResizable(True)
        nav_bar.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        nav_bar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        nav_bar.setMaximumHeight(50)
        nav_bar.setStyleSheet("""
            QScrollArea {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 20px;
                margin: 0;
                padding: 0;
            }
        """)
        
        # Container for buttons
        container = QWidget()
        container.setStyleSheet("background-color: white;")
        buttons_layout = QHBoxLayout(container)
        buttons_layout.setSpacing(8)
        buttons_layout.setContentsMargins(8, 4, 8, 4)
        
        # Add course buttons
        course_names = [
            "Working with AI", 
            "Business Analytics", 
            "Google AI Essentials", 
            "IBM Data Analyst", 
            "Business Analytics with Excel: Elementary to Advanced",
            "Cloud Computing"
        ]
        
        for i, name in enumerate(course_names):
            button = self._create_simple_button(name, i == 0)  # First button is selected
            buttons_layout.addWidget(button)
        
        # Add stretch at the end
        buttons_layout.addStretch()
        
        # Set the container as the widget for the scroll area
        nav_bar.setWidget(container)
        
        # Add to main layout
        self.main_layout.addWidget(nav_bar)
        
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
        
        # Course details button
        self.details_btn = QPushButton("Деталі курсу")
        self.details_btn.setFont(QFont("Inter", 13))
        self.details_btn.setCursor(Qt.PointingHandCursor)
        self.details_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid {COLORS.PRIMARY};
                color: {COLORS.PRIMARY};
                border-radius: 18px;
                padding: 0 24px;
            }}
            QPushButton:hover {{
                background-color: {COLORS.PRIMARY_LIGHT};
            }}
        """)
        self.details_btn.setFixedHeight(36)
        
        header_layout.addWidget(self.course_title)
        header_layout.addStretch()
        header_layout.addWidget(self.details_btn)
        
        # 4. Lessons grid
        self.lessons_grid = LessonsGrid()
        
        # Add all components to main layout
        self.main_layout.addWidget(self.tabs_scroll)
        self.main_layout.addLayout(header_layout)
        self.main_layout.addWidget(self.lessons_grid)
    
    def _connect_signals(self):
        """Connect all signals"""
        self.details_btn.clicked.connect(self._on_details_clicked)
        self.lessons_grid.lesson_started.connect(self._on_lesson_started)
    
    def set_current_user(self, user_id):
        """Set the current user ID and load active courses"""
        self.current_user_id = user_id
        self._load_active_courses()
    
    def _load_active_courses(self):
        """Load active courses for the current user"""
        if not self.current_user_id:
            logger.info("No current user ID, skipping active courses loading")
            return
        
        try:
            logger.info(f"Loading active courses for user ID: {self.current_user_id}")
            active_courses = self.course_service.get_active_courses(self.current_user_id)
            logger.info(f"Found {len(active_courses)} active courses")
            
            # If no active courses, load all available courses instead
            if not active_courses:
                logger.info("No active courses found, loading all available courses")
                active_courses = self.course_service.get_all_courses()
                logger.info(f"Loaded {len(active_courses)} available courses")
            
            self.active_courses = active_courses
            
            # Update course tabs
            self.update_course_tabs(active_courses)
            
            # If there are active courses, load the first one
            if active_courses:
                logger.info(f"Loading first course: {active_courses[0].name}")
                self.load_course(active_courses[0].id)
            else:
                logger.info("No courses available, showing no courses message")
                self._show_no_courses_message()
        except Exception as e:
            logger.error(f"Error loading active courses: {str(e)}")
            logger.exception(e)
    
    def _show_no_courses_message(self):
        """Show a message when no courses are available"""
        # Clear any existing lessons
        self.lessons_grid.set_lessons([])
        
        # Update course title
        self.course_title.setText("Немає активних курсів")
        
        # Create a placeholder message in the main layout
        # We'll use a frame with a message instead of trying to add to the lessons grid
        if hasattr(self, 'no_courses_frame'):
            self.no_courses_frame.setVisible(True)
            return
            
        self.no_courses_frame = QFrame()
        self.no_courses_frame.setFrameShape(QFrame.StyledPanel)
        self.no_courses_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
            }
        """)
        
        message_layout = QVBoxLayout(self.no_courses_frame)
        message_layout.setContentsMargins(20, 40, 20, 40)
        
        message_label = QLabel("У вас немає активних курсів. Будь ласка, перейдіть на сторінку курсів, щоб записатися на курс.")
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setFont(QFont("Inter", 14))
        message_label.setStyleSheet("color: #666666;")
        message_label.setWordWrap(True)
        
        message_layout.addWidget(message_label)
        
        # Replace the lessons grid with our message frame
        self.main_layout.replaceWidget(self.lessons_grid, self.no_courses_frame)
        self.lessons_grid.setVisible(False)
        self.no_courses_frame.setVisible(True)
    
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
    
    def _restore_lessons_grid(self):
        """Restore the lessons grid if it was replaced with a no courses message"""
        if hasattr(self, 'no_courses_frame') and self.no_courses_frame.isVisible():
            self.main_layout.replaceWidget(self.no_courses_frame, self.lessons_grid)
            self.no_courses_frame.setVisible(False)
            self.lessons_grid.setVisible(True)

    def load_course(self, course_id):
        """Load a course and its lessons"""
        try:
            # Get course details
            course = self.course_service.get_course_by_id(course_id)
            self.current_course = course
            
            # Update UI
            self.course_title.setText(course.name)
            
            # Highlight active course in tabs
            self._highlight_active_course(course_id)
            
            # Load lessons for this course
            lessons = self.lesson_service.get_lessons_by_course_id(course_id)
            
            # Sort lessons by lesson_order
            sorted_lessons = sorted(lessons, key=lambda lesson: lesson.lesson_order)
            
            self.lessons_grid.set_lessons(sorted_lessons)
            
        except Exception as e:
            logger.error(f"Error loading course: {str(e)}")
    
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
    
    def _highlight_active_course(self, course_id):
        """Highlight the selected course in the active courses list"""
        for i in range(self.tabs_layout.count()):
            item = self.tabs_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, QPushButton):
                    widget.setChecked(widget.objectName() == f"course_button_{course_id}")
    
    def _create_simple_button(self, name, is_selected=False):
        """Create a button for the navigation bar - SIMPLE IMPLEMENTATION FROM test_nav_bar.py"""
        button = QPushButton(name)
        button.setCursor(Qt.PointingHandCursor)
        button.setFont(QFont("Inter", 11))
        button.setCheckable(True)
        button.setChecked(is_selected)
        button.setMinimumWidth(120)
        button.setFixedHeight(32)
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-radius: 16px;
                padding: 4px 16px;
                color: #666666;
                font-weight: normal;
                border: none;
                text-align: center;
            }
            QPushButton:hover:!checked {
                background-color: #F5F5F5;
                color: #333333;
            }
            QPushButton:checked {
                background-color: #E6F2FF;
                color: #2196F3;
                font-weight: bold;
            }
        """)
        
        return button 