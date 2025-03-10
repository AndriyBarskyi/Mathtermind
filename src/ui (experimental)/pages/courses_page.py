from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QFrame,
    QLabel,
    QGridLayout,
    QCheckBox,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QSize, QMargins, pyqtSlot
from PyQt6.QtGui import QIcon, QFont
from src.ui.widgets.range_slider import QRangeSlider
from src.ui.widgets.filter_tabs import FilterTabs
from src.ui.widgets.search_bar import SearchBar
from src.ui.widgets.courses_grid import CoursesGrid
from src.ui.widgets.filter_sidebar import FilterSidebar
from src.ui.services.course_service import CourseService
from src.ui.services.lesson_service import LessonService

class CoursePage(QWidget):
    """
    Course page displaying available courses with filtering options.
    The page is divided into several components:
    1. Filter tabs (All courses, Active, Completed)
    2. Search bar with filter button
    3. Course cards grid
    4. Filter sidebar
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize services
        self.course_service = CourseService()
        self.lesson_service = LessonService()
        
        # Initialize state
        self.current_tab = "all"
        self.search_text = ""
        self.filter_state = {
            "subjects": ["info", "math"],  # Include both subjects
            "levels": ["basic", "intermediate", "advanced"],  # Include all levels
            "year_range": (2010, 2030)  # Wider year range
        }
        
        self._setup_ui()
        self._connect_signals()
        self._load_initial_data()

    def _setup_ui(self):
        """Setup the main UI layout"""
        # Main layout with content area and sidebar
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(16)

        # Create content area (left side)
        self.content_area = self._create_content_area()
        
        # Create filter sidebar (right side)
        self.filter_sidebar = FilterSidebar()
        # Set minimum and maximum width for the filter sidebar
        self.filter_sidebar.setMinimumWidth(280)
        self.filter_sidebar.setMaximumWidth(320)
        
        # Initially hide the filter sidebar
        self.filter_sidebar.hide()
        self.filter_sidebar_visible = False
        
        # Add both main components to the layout
        self.main_layout.addWidget(self.content_area, 9)  # Increased ratio for content
        self.main_layout.addWidget(self.filter_sidebar, 0)  # Initially collapsed

    def _create_content_area(self):
        """Create the main content area with filter tabs, search, and course grid"""
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(16)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # 1. Create filter tabs
        self.filter_tabs = FilterTabs()
        
        # 2. Create search bar
        self.search_bar = SearchBar()
        
        # Combine filter tabs and search in one row
        filter_section = QHBoxLayout()
        filter_section.setSpacing(16)
        filter_section.addWidget(self.filter_tabs)
        filter_section.addStretch()
        filter_section.addWidget(self.search_bar)
        
        content_layout.addLayout(filter_section)
        
        # 3. Create courses grid
        self.courses_grid = CoursesGrid()
        content_layout.addWidget(self.courses_grid)
        
        return content_widget

    def _connect_signals(self):
        """Connect all signals"""
        # Connect filter tabs signals
        self.filter_tabs.tab_changed.connect(self._on_tab_changed)
        
        # Connect search bar signals
        self.search_bar.search_changed.connect(self._on_search_text_changed)
        self.search_bar.filter_button_clicked.connect(self._on_filter_button_clicked)
        
        # Connect filter sidebar signals
        self.filter_sidebar.filters_applied.connect(self._on_filters_applied)
        self.filter_sidebar.filters_cleared.connect(self._on_filters_cleared)
        
        # Connect courses grid signals
        self.courses_grid.course_started.connect(self._on_course_started)
    
    def _load_initial_data(self):
        """Load initial courses data"""
        courses = self.course_service.get_all_courses()
        self.courses_grid.set_courses(courses)
    
    @pyqtSlot(str)
    def _on_tab_changed(self, tab):
        """Handle tab change"""
        self.current_tab = tab
        self._refresh_courses()
    
    @pyqtSlot(str)
    def _on_search_text_changed(self, text):
        """Handle search text change"""
        self.search_text = text
        self._refresh_courses()
    
    def _on_filter_button_clicked(self):
        """Handle filter button click"""
        # Toggle the filter sidebar visibility
        if self.filter_sidebar_visible:
            self.filter_sidebar.hide()
            self.main_layout.setStretch(0, 9)  # Content area
            self.main_layout.setStretch(1, 0)  # Filter sidebar
            self.filter_sidebar_visible = False
            # Update filter button state
            self.search_bar.update_filter_button_state(False)
        else:
            self.filter_sidebar.show()
            self.main_layout.setStretch(0, 7)  # Content area
            self.main_layout.setStretch(1, 3)  # Filter sidebar
            self.filter_sidebar_visible = True
            # Update filter button state
            self.search_bar.update_filter_button_state(True)
    
    @pyqtSlot(dict)
    def _on_filters_applied(self, filter_state):
        """Handle filters applied from sidebar"""
        self.filter_state = filter_state
        self._refresh_courses()
    
    @pyqtSlot()
    def _on_filters_cleared(self):
        """Handle filters cleared from sidebar"""
        self.filter_state = {
            "subjects": ["info", "math"],  # Include both subjects
            "levels": ["basic", "intermediate", "advanced"],  # Include all levels
            "year_range": (2010, 2030)  # Wider year range
        }
        self._refresh_courses()
    
    @pyqtSlot(str)
    def _on_course_started(self, course_id):
        """Handle course started"""
        # Get the first lesson for this course
        lessons = self.lesson_service.get_lessons_by_course_id(course_id)
        if not lessons:
            print("No lessons found for this course")
            return
        
        # Get the first lesson
        first_lesson = lessons[0]
        
        # Get the parent window
        parent = self.parent()
        while parent and not isinstance(parent, QStackedWidget):
            parent = parent.parent()
        
        if parent:
            # Get the lessons page
            lessons_page = None
            for i in range(parent.count()):
                widget = parent.widget(i)
                if isinstance(widget, LessonPage):
                    lessons_page = widget
                    break
            
            if lessons_page:
                # Load the lesson content
                lessons_page.load_lesson(first_lesson.id)
                # Switch to the lessons page
                parent.setCurrentWidget(lessons_page)
            else:
                print("Lessons page not found")
        else:
            print("Parent stacked widget not found")
    
    def _refresh_courses(self):
        """Refresh the courses grid based on current filters"""
        if self.current_tab == "all" and not self.search_text and self.filter_state == {
            "subjects": ["info", "math"],
            "levels": ["basic", "intermediate", "advanced"],
            "year_range": (2010, 2030)
        }:
            # If no filters are applied, just get all courses
            courses = self.course_service.get_all_courses()
        else:
            # Otherwise, apply filters
            courses = self.course_service.filter_courses(
                status=self.current_tab,
                search_text=self.search_text,
                subjects=self.filter_state["subjects"],
                levels=self.filter_state["levels"],
                year_range=self.filter_state["year_range"]
            )
        
        self.courses_grid.set_courses(courses) 