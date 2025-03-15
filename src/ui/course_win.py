from PyQt5.QtWidgets import (
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
    QStackedWidget,
)
from PyQt5.QtCore import Qt, QSize, QMargins, pyqtSlot
from PyQt5.QtGui import QIcon, QFont
from src.ui.widgets.range_slider import QRangeSlider
from src.ui.widgets.filter_tabs import FilterTabs
from src.ui.widgets.search_bar import SearchBar
from src.ui.widgets.filter_button import FilterButton
from src.ui.widgets.courses_grid import CoursesGrid
from src.ui.widgets.filter_sidebar import FilterSidebar
from src.ui.services.course_service import CourseService
from src.ui.services.lesson_service import LessonService
from src.ui.lesson_win import LessonDetailPage
from src.ui.theme import ThemeManager

class CoursesPage(QWidget):
    """
    Course page displaying available courses with filtering options.
    The page is divided into several components:
    1. Filter tabs (All courses, Active, Completed)
    2. Search bar (independent from filters)
    3. Filter button (independent from search)
    4. Course cards grid
    5. Filter sidebar
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
        
        # 2. Create top controls section with search and filter
        top_controls = QHBoxLayout()
        top_controls.setSpacing(16)
        
        # Add filter tabs to the left
        top_controls.addWidget(self.filter_tabs)
        top_controls.addStretch()
        
        # Create search bar
        self.search_bar = SearchBar()
        top_controls.addWidget(self.search_bar)
        
        # Create filter button (separate from search)
        self.filter_button = FilterButton()
        top_controls.addWidget(self.filter_button)
        
        content_layout.addLayout(top_controls)
        
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
        
        # Connect filter button signals
        self.filter_button.filter_button_clicked.connect(self._on_filter_button_clicked)
        
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
        
        # Update UI to show search status
        if text.strip():
            self.search_bar.setToolTip(f"Пошук: {text}")
        else:
            self.search_bar.setToolTip("")
            
    def _on_filter_button_clicked(self):
        """Handle filter button click"""
        # Toggle the filter sidebar visibility
        if self.filter_sidebar_visible:
            self.filter_sidebar.hide()
            self.main_layout.setStretch(0, 9)  # Content area
            self.main_layout.setStretch(1, 0)  # Filter sidebar
            self.filter_sidebar_visible = False
            # Update filter button state
            self.filter_button.update_state(False)
        else:
            self.filter_sidebar.show()
            self.main_layout.setStretch(0, 7)  # Content area
            self.main_layout.setStretch(1, 3)  # Filter sidebar
            self.filter_sidebar_visible = True
            # Update filter button state
            self.filter_button.update_state(True)
    
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
        """Handle course started signal"""
        # Get the course
        course = self.course_service.get_course_by_id(course_id)
        if not course:
            return
        
        # Get the parent window
        parent = self.parent()
        while parent and not isinstance(parent, QStackedWidget):
            parent = parent.parent()
        
        if parent:
            # Get the lessons page
            lessons_page = None
            for i in range(parent.count()):
                widget = parent.widget(i)
                if isinstance(widget, LessonDetailPage):
                    lessons_page = widget
                    break
            
            if lessons_page:
                # Load the course
                lessons_page.load_course(course_id)
                
                # Switch to the lessons page
                parent.setCurrentWidget(lessons_page)
            else:
                print("Lessons page not found")
        else:
            print("Parent QStackedWidget not found")
    
    def _refresh_courses(self):
        """Refresh the courses grid based on current filters"""
        # Log the current filter state
        print(f"Refreshing courses with search text: '{self.search_text}'")
        print(f"Current tab: {self.current_tab}")
        print(f"Filter state: {self.filter_state}")
        
        # First, get the base list of courses based on tab
        if self.current_tab == "active":
            base_courses = self.course_service.get_active_courses()
        elif self.current_tab == "completed":
            base_courses = self.course_service.get_completed_courses()
        else:  # "all" tab
            base_courses = self.course_service.get_all_courses()
            
        print(f"Base courses from tab '{self.current_tab}': {len(base_courses)}")
        
        # Apply search text filter separately
        if self.search_text and self.search_text.strip():
            search_text = self.search_text.strip().lower()
            print(f"Applying search filter: '{search_text}'")
            
            # Split search text into words for more flexible matching
            search_words = search_text.split()
            
            filtered_courses = []
            for course in base_courses:
                # Check if any search word is in the course name or description
                course_text = (course.name + " " + course.description).lower()
                if any(word in course_text for word in search_words):
                    filtered_courses.append(course)
            
            base_courses = filtered_courses
            print(f"Courses after search filter: {len(base_courses)}")
        
        # Apply subject filter
        if self.filter_state["subjects"]:
            filtered_courses = []
            for course in base_courses:
                if course.topic.lower() in self.filter_state["subjects"]:
                    filtered_courses.append(course)
            
            base_courses = filtered_courses
            print(f"Courses after subject filter: {len(base_courses)}")
        
        # Apply level filter
        if self.filter_state["levels"]:
            filtered_courses = []
            for course in base_courses:
                if course.difficulty_level.lower() in self.filter_state["levels"]:
                    filtered_courses.append(course)
            
            base_courses = filtered_courses
            print(f"Courses after level filter: {len(base_courses)}")
        
        # Apply year range filter
        if self.filter_state["year_range"]:
            min_year, max_year = self.filter_state["year_range"]
            filtered_courses = []
            for course in base_courses:
                # Extract year from course.created_at (format: "2023-01-15")
                try:
                    year = int(course.created_at.split("-")[0])
                    if min_year <= year <= max_year:
                        filtered_courses.append(course)
                except (ValueError, AttributeError, IndexError):
                    # If we can't parse the year, include the course anyway
                    filtered_courses.append(course)
            
            base_courses = filtered_courses
            print(f"Courses after year filter: {len(base_courses)}")
        
        # Update the courses grid with filtered courses
        self.courses_grid.set_courses(base_courses)
        
        # Show appropriate message if no courses found
        if not base_courses:
            if self.search_text.strip():
                self.courses_grid.show_no_results_message(f"Немає курсів, що відповідають пошуку: '{self.search_text}'")
            elif self.current_tab != "all" or self.filter_state != {
                "subjects": ["info", "math"],
                "levels": ["basic", "intermediate", "advanced"],
                "year_range": (2010, 2030)
            }:
                self.courses_grid.show_no_results_message("Немає курсів, що відповідають вибраним фільтрам")
            else:
                self.courses_grid.show_no_results_message("Немає доступних курсів")
        else:
            self.courses_grid.hide_no_results_message()
    
    def update_theme_styles(self):
        """Update all component styles when theme changes"""
        # Update filter tabs
        if hasattr(self.filter_tabs, 'update_theme_styles'):
            self.filter_tabs.update_theme_styles()
        
        # Update search bar
        if hasattr(self.search_bar, 'update_theme_styles'):
            self.search_bar.update_theme_styles()
        
        # Update filter button
        if hasattr(self.filter_button, 'update_theme_styles'):
            self.filter_button.update_theme_styles()
        
        # Update filter sidebar
        if hasattr(self.filter_sidebar, 'update_theme_styles'):
            self.filter_sidebar.update_theme_styles()
        
        # Update courses grid - this is the most important part
        if hasattr(self.courses_grid, 'update_theme_styles'):
            self.courses_grid.update_theme_styles()
        
        # Update all course cards directly
        for card in self.courses_grid.findChildren(QFrame):
            if hasattr(card, 'update_theme_styles'):
                card.update_theme_styles() 