from PyQt5.QtWidgets import QWidget, QGridLayout,QVBoxLayout, QLabel,QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from slider import RangeSlider
from lessons_list_win import Lessons_page
from src.services.course_service import CourseService
from src.services.progress_service import ProgressService
from src.db.models.enums import Topic, DifficultyLevel


class Course_page(QWidget):
    def __init__(self,stack=None, lessons_page=None):
        super().__init__()
        self.stack = None
        self.pg_lessons = None
        self.stack = stack
        self.pg_lessons = lessons_page
        
        # Initialize services
        self.course_service = CourseService()
        self.progress_service = ProgressService()

        # Store actual course data for re-layout
        self._all_loaded_courses_data = [] 
        self._current_display_courses_data = []
        self._current_num_columns = -1 # Initialize to an invalid number

        self.pg_courses = QtWidgets.QWidget()
        self.pg_courses.setObjectName("pg_courses")
        self.main_courses_layout = QtWidgets.QGridLayout(self.pg_courses)
        self.main_courses_layout.setObjectName("main_courses_layout")
        self.filter_buttons_widget = QtWidgets.QWidget(self.pg_courses)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.filter_buttons_widget.setSizePolicy(sizePolicy)
        self.filter_buttons_widget.setMinimumSize(QtCore.QSize(1020, 50))
        self.filter_buttons_widget.setMaximumSize(QtCore.QSize(1600000, 50))
        self.filter_buttons_widget.setProperty("type", "transparent_widget")
        self.filter_buttons_widget.setObjectName("filter_buttons_widget")
        self.filter_buttons_layout = QtWidgets.QHBoxLayout(self.filter_buttons_widget)
        self.filter_buttons_layout.setContentsMargins(-1, 0, -1, -1)
        self.filter_buttons_layout.setObjectName("filter_buttons_layout")
        
        self.course_filter_button_group = QtWidgets.QButtonGroup(self.filter_buttons_widget)
        self.course_filter_button_group.setExclusive(True)
        
        self.btn_all = QtWidgets.QPushButton(self.filter_buttons_widget)
        self.btn_all.setText("Всі курси")        
        self.btn_all.setSizePolicy(sizePolicy)        
        self.btn_all.setProperty("type", "start_continue_complete")
        self.btn_all.setObjectName("btn_all")
        self.btn_all.setCheckable(True)
        self.btn_all.setChecked(True) # Default to all courses
        self.course_filter_button_group.addButton(self.btn_all)
        self.filter_buttons_layout.addWidget(self.btn_all)
        
        self.btn_started_all = QtWidgets.QPushButton(self.filter_buttons_widget)
        self.btn_started_all.setText("Розпочаті")
        self.btn_started_all.setSizePolicy(sizePolicy)
        self.btn_started_all.setProperty("type", "start_continue_complete")
        self.btn_started_all.setObjectName("btn_started_all")
        self.btn_started_all.setCheckable(True)
        self.course_filter_button_group.addButton(self.btn_started_all)
        self.filter_buttons_layout.addWidget(self.btn_started_all)
        
        self.btn_completed = QtWidgets.QPushButton(self.filter_buttons_widget)
        self.btn_completed.setText("Завершені")     
        self.btn_completed.setSizePolicy(sizePolicy)
        self.btn_completed.setProperty("type", "start_continue_complete")
        self.btn_completed.setObjectName("btn_completed")
        self.btn_completed.setCheckable(True)
        self.course_filter_button_group.addButton(self.btn_completed)
        self.filter_buttons_layout.addWidget(self.btn_completed)
        self.main_courses_layout.addWidget(self.filter_buttons_widget, 1, 0, 1, 1)

        self.left_filter_section = QtWidgets.QWidget(self.pg_courses)
        self.left_filter_section.setMinimumSize(QtCore.QSize(240, 0))
        self.left_filter_section.setMaximumSize(QtCore.QSize(240, 16777215))
        self.left_filter_section.setProperty("type", "w_pg") 
        self.left_filter_section.setObjectName("left_filter_section")
        self.left_filter_layout = QtWidgets.QGridLayout(self.left_filter_section)
        self.left_filter_layout.setContentsMargins(-1, 0, -1, 0)
        self.left_filter_layout.setSpacing(0)
        self.left_filter_layout.setObjectName("left_filter_layout")
        
        self.subject_filter_widget = QtWidgets.QWidget(self.left_filter_section)
        self.subject_filter_widget.setMinimumSize(QtCore.QSize(0, 100))
        self.subject_filter_widget.setMaximumSize(QtCore.QSize(16777215, 200))
        self.subject_filter_widget.setProperty("type", "w_pg")
        self.subject_filter_widget.setObjectName("subject_filter_widget")
        self.subject_filter_layout = QtWidgets.QGridLayout(self.subject_filter_widget)
        self.subject_filter_layout.setContentsMargins(-1, 0, -1, 0)
        self.subject_filter_layout.setHorizontalSpacing(7)
        self.subject_filter_layout.setVerticalSpacing(0)
        self.subject_filter_layout.setObjectName("subject_filter_layout")
        
        self.lb_subject = QtWidgets.QLabel(self.subject_filter_widget)
        self.lb_subject.setText("Предмет")
        self.lb_subject.setProperty("type", "lb_description")
        self.lb_subject.setSizePolicy(sizePolicy)
        self.lb_subject.setMaximumSize(QtCore.QSize(16777215, 50))
        self.lb_subject.setObjectName("lb_subject")
        self.subject_filter_layout.addWidget(self.lb_subject, 0, 0, 1, 1)
        
        self.cb_subject1 = QtWidgets.QCheckBox(self.subject_filter_widget)
        self.cb_subject1.setText("Математика")
        self.cb_subject1.setObjectName("cb_subject1")
        self.subject_filter_layout.addWidget(self.cb_subject1, 1, 0, 1, 1)
        
        self.cb_subject2 = QtWidgets.QCheckBox(self.subject_filter_widget)
        self.cb_subject2.setText("Інформатика")
        self.cb_subject2.setObjectName("cb_subject2")
        self.subject_filter_layout.addWidget(self.cb_subject2, 2, 0, 1, 1)
        self.left_filter_layout.addWidget(self.subject_filter_widget, 1, 0, 1, 1)
        
        self.level_filter_widget = QtWidgets.QWidget(self.left_filter_section)
        self.level_filter_widget.setMinimumSize(QtCore.QSize(0, 50))
        self.level_filter_widget.setMaximumSize(QtCore.QSize(16777215, 300))
        self.level_filter_widget.setProperty("type", "w_pg")
        self.level_filter_widget.setObjectName("level_filter_widget")
        self.level_filter_layout = QtWidgets.QGridLayout(self.level_filter_widget)
        self.level_filter_layout.setContentsMargins(11, 0, -1, 0)
        self.level_filter_layout.setObjectName("level_filter_layout")

        self.range_label = QtWidgets.QLabel(self.level_filter_widget)
        self.range_label.setText("Тривалість")
        self.range_label.setProperty("type", "lb_description")
        self.range_label.setMaximumSize(QtCore.QSize(16777215, 50))
        self.range_label.setObjectName("lb_range")
        self.subject_filter_layout.addWidget(self.range_label, 3, 0, 1, 1)

        self.range_slider = RangeSlider(min_value=0, max_value=500, start_min=50, start_max=250)
        self.subject_filter_layout.addWidget(self.range_slider, 4, 0, 1, 1)

        self.lb_level = QtWidgets.QLabel(self.level_filter_widget)
        self.lb_level.setText("Рівень")
        self.lb_level.setProperty("type", "lb_description")
        self.lb_level.setMaximumSize(QtCore.QSize(16777215, 50))
        self.lb_level.setObjectName("lb_level")
        self.level_filter_layout.addWidget(self.lb_level, 0, 0, 1, 1)
        
        self.rb_level1 = QtWidgets.QRadioButton(self.level_filter_widget)
        self.rb_level1.setText("Базовий")
        self.rb_level1.setObjectName("rb_level1")
        self.level_filter_layout.addWidget(self.rb_level1, 1, 0, 1, 1)
        
        self.rb_level2 = QtWidgets.QRadioButton(self.level_filter_widget)
        self.rb_level2.setText("Середній")
        self.rb_level2.setObjectName("rb_level2")
        self.level_filter_layout.addWidget(self.rb_level2, 2, 0, 1, 1)
        
        self.rb_level3 = QtWidgets.QRadioButton(self.level_filter_widget)
        self.rb_level3.setText("Високий")
        self.rb_level3.setObjectName("rb_level3")
        self.level_filter_layout.addWidget(self.rb_level3, 3, 0, 1, 1)
        
        spacerItem = QtWidgets.QSpacerItem(20, 200, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.level_filter_layout.addItem(spacerItem)
        self.left_filter_layout.addWidget(self.level_filter_widget, 2, 0, 1, 1)
        
        self.btn_clear = QtWidgets.QPushButton(self.left_filter_section)
        self.btn_clear.setText("Очистити все")
        self.btn_clear.setSizePolicy(sizePolicy)
        self.btn_clear.setMinimumSize(QtCore.QSize(0, 50))
        self.btn_clear.setMaximumSize(QtCore.QSize(16777215, 50))
        self.btn_clear.setObjectName("btn_clear")
        self.btn_clear.setProperty("type", "register")
        self.left_filter_layout.addWidget(self.btn_clear, 0, 1, 1, 1)
        
        self.btn_apply = QtWidgets.QPushButton(self.left_filter_section)
        self.btn_apply.setText("Застосувати")
        self.btn_apply.setMinimumSize(QtCore.QSize(0, 35))
        self.btn_apply.setMaximumSize(QtCore.QSize(16777215, 35))
        self.btn_apply.setProperty("type","start_continue")
        self.btn_apply.setObjectName("btn_apply")
        self.left_filter_layout.addWidget(self.btn_apply, 3, 0, 1, 2)
        self.main_courses_layout.addWidget(self.left_filter_section, 2, 1, 4, 1)

        self.courses_scroll_area = QtWidgets.QScrollArea(self.pg_courses)
        self.courses_scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.courses_scroll_area.setWidgetResizable(True)
        self.courses_scroll_area.setObjectName("courses_scroll_area")
        
        self.scroll_area_content = QtWidgets.QWidget()
        self.scroll_area_content.setGeometry(QtCore.QRect(-111, -476, 1110, 1066))
        self.scroll_area_content.setObjectName("scroll_area_content")
        
        # Use a grid layout with proper spacing and set column count
        self.course_cards_layout = QtWidgets.QGridLayout(self.scroll_area_content)
        self.course_cards_layout.setObjectName("course_cards_layout")
        self.course_cards_layout.setSpacing(6)  # Minimal spacing between cards
        self.course_cards_layout.setContentsMargins(4, 4, 4, 4)  # Minimal margins
        self.course_cards_layout.setColumnStretch(0, 1)
        self.course_cards_layout.setColumnStretch(1, 1)
        self.course_cards_layout.setColumnStretch(2, 1)

        self.courses_scroll_area.setWidget(self.scroll_area_content)
        self.main_courses_layout.addWidget(self.courses_scroll_area, 2, 0, 1, 1)
        self.courses_filter_layout = QtWidgets.QHBoxLayout()
        self.courses_filter_layout.setObjectName("courses_filter_layout")
        self.main_courses_layout.addLayout(self.courses_filter_layout, 3, 0, 1, 1)
        self.lb_courses = QtWidgets.QLabel(self.pg_courses)
        self.lb_courses.setProperty("type", "title")
        self.lb_courses.setObjectName("lb_courses")
        self.lb_courses.setText("Курси")
        self.main_courses_layout.addWidget(self.lb_courses, 0, 0, 1, 1)
        self.setLayout(self.main_courses_layout)
        
        # Load courses from database
        # self.course_widgets_complete = [] # This will be managed by _current_display_courses_data
        self.load_courses_from_db()
        
        self.btn_completed.clicked.connect(self.show_completed_courses)
        self.btn_all.clicked.connect(self.show_all_courses)
        self.btn_started_all.clicked.connect(self.show_started_courses)
        self.btn_apply.clicked.connect(self.apply_filters)
        self.btn_clear.clicked.connect(self.clear_filters)

        # Modify main layout to give more space to the courses section 
        self.main_courses_layout.setColumnStretch(0, 3) # Give more space to the courses column
        self.main_courses_layout.setColumnStretch(1, 1) # Give less space to the filter column

    def load_courses_from_db(self):
        """Load courses from the database and store their data"""
        try:
            courses = self.course_service.get_all_courses()
            self._all_loaded_courses_data = [] # Clear previous full list
            for course in courses:
                difficulty_text = "Базовий"
                if course.difficulty_level == DifficultyLevel.INTERMEDIATE:
                    difficulty_text = "Середній"
                elif course.difficulty_level == DifficultyLevel.ADVANCED:
                    difficulty_text = "Високий"
                
                subject_text = "Математика" if course.topic == Topic.MATHEMATICS else "Інформатика"
                num_lessons = len(course.lessons) if hasattr(course, 'lessons') and course.lessons else 5
                
                # Store course data instead of directly adding widget
                self._all_loaded_courses_data.append({
                    'name': course.name, 
                    'description': course.description, 
                    'subject': subject_text, 
                    'level': difficulty_text, 
                    'lessons': num_lessons,
                    'completed_lessons': 0, # Placeholder
                    'course_id': course.id
                })
            
            self._current_display_courses_data = list(self._all_loaded_courses_data) # Initially display all
            self.update_course_display() # New method to handle layout
            
        except Exception as e:
            print(f"Error loading courses: {str(e)}")

    def clear_courses_layout(self):
        """Clear only the widgets from the course cards layout"""
        while self.course_cards_layout.count():
            item = self.course_cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def update_course_display(self, num_columns=None):
        """Re-populate the course_cards_layout with current course data and columns"""
        self.clear_courses_layout()

        if num_columns is None:
            num_columns = self._calculate_num_columns()

        # Reset all previous column stretches
        if self._current_num_columns != -1: 
            for i in range(self._current_num_columns):
                self.course_cards_layout.setColumnStretch(i, 0)
        
        self._current_num_columns = num_columns
        
        # Set equal stretch for all columns
        for i in range(num_columns):
            self.course_cards_layout.setColumnStretch(i, 1)

        # Add course cards to the layout
        for idx, course_data in enumerate(self._current_display_courses_data):
            row = idx // num_columns
            col = idx % num_columns
            course_card_widget = self._create_course_card_widget(course_data)
            # Set alignment to center and no stretch to ensure equal sizes
            self.course_cards_layout.addWidget(course_card_widget, row, col, 1, 1, Qt.AlignCenter)
        
        # Add extra empty row with stretch to push content to the top
        empty_row = len(self._current_display_courses_data) // num_columns + 1
        if empty_row > 0 and self.course_cards_layout.rowCount() <= empty_row:
            self.course_cards_layout.setRowStretch(empty_row, 1)
        
        # Ensure the scroll area updates its layout
        self.scroll_area_content.adjustSize()
        self.courses_scroll_area.updateGeometry()

    def _create_course_card_widget(self, course_data):
        # This is basically the content of the old add_course_widget,
        # but takes course_data dict and returns the widget
        course_card_widget = QtWidgets.QWidget(self.scroll_area_content)
        # Use fixed size for consistent card width
        course_card_widget.setFixedSize(QtCore.QSize(310, 280))
        course_card_widget.setProperty("type", "card")
        
        if course_data['course_id']:
            course_card_widget.setProperty("course_id", course_data['course_id'])
        
        card_layout = QtWidgets.QVBoxLayout(course_card_widget)
        card_layout.setContentsMargins(10, 10, 10, 10)
        
        title = QtWidgets.QLabel(course_data['name'])
        title.setProperty("type", "lb_name_lesson")
        title.setStyleSheet("font-size: 14pt; font-weight: bold;")
        title.setWordWrap(True)
        title.setMaximumHeight(50)
        
        tags_layout = QtWidgets.QHBoxLayout()
        tags_layout.setSpacing(10)
        tags_layout.setContentsMargins(0, 0, 0, 0)
        
        lb_subject = QtWidgets.QLabel(course_data['subject'])
        lb_subject.setProperty("type", "tag")
        lb_subject.setMaximumSize(QtCore.QSize(120, 25))
        lb_subject.setMinimumSize(QtCore.QSize(70, 25))
        lb_subject.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        lb_subject.setAlignment(QtCore.Qt.AlignCenter)
        lb_subject.setStyleSheet('''
            background-color: #e6f2ff; 
            border-radius: 12px; 
            padding: 3px;
            font-size: 9pt;
        ''')
        tags_layout.addWidget(lb_subject)
        
        lb_level = QtWidgets.QLabel(course_data['level'])
        lb_level.setProperty("type", "tag")
        lb_level.setMaximumSize(QtCore.QSize(120, 25))
        lb_level.setMinimumSize(QtCore.QSize(70, 25))
        lb_level.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        lb_level.setAlignment(QtCore.Qt.AlignCenter)
        lb_level.setStyleSheet('''
            background-color: #fff0e6; 
            border-radius: 12px; 
            padding: 3px;
            font-size: 9pt;
        ''')
        tags_layout.addWidget(lb_level)
        
        tags_layout.addStretch()
        
        description_widget = QtWidgets.QLabel(course_data['description'])
        description_widget.setProperty("type", "lb_description")
        description_widget.setStyleSheet("background-color: transparent; border: none; padding: 0; font-size: 10pt;")
        description_widget.setWordWrap(True)
        description_widget.setMaximumHeight(50)
        
        course_info = QtWidgets.QLabel(f"Уроків: {course_data['lessons']}")
        course_info.setProperty("type", "lb_small")
        course_info.setStyleSheet("font-size: 9pt;")
        
        stacked_widget = QtWidgets.QStackedWidget()
        stacked_widget.setMaximumSize(QtCore.QSize(16777215, 60))
        stacked_widget.setProperty("type", "w_pg")
        
        page_start = QtWidgets.QWidget()
        page_start.setProperty("type", "w_pg")
        layout_start = QtWidgets.QGridLayout(page_start)
        layout_start.setContentsMargins(0, 0, 0, 0)
        
        btn_start = QtWidgets.QPushButton("Розпочати")
        btn_start.setMinimumSize(QtCore.QSize(0, 35))
        btn_start.setMaximumSize(QtCore.QSize(16777215, 35))
        btn_start.setProperty("type", "start_continue")
        btn_start.setStyleSheet('''
            QPushButton {
                padding: 5px;
                font-size: 11pt;
                font-weight: normal;
            }
        ''')
        
        layout_start.addWidget(btn_start, 0, 0, 1, 1)
        page_start.setLayout(layout_start)
        
        page_continue = QtWidgets.QWidget()
        page_continue.setProperty("type", "w_pg")
        layout_continue = QtWidgets.QGridLayout(page_continue)
        layout_continue.setContentsMargins(0, 0, 0, 0)
        
        btn_continue = QtWidgets.QPushButton("Continue") # Needs translation if still here
        btn_continue.setMinimumSize(QtCore.QSize(0, 35))
        btn_continue.setMaximumSize(QtCore.QSize(16777215, 35))
        btn_continue.setProperty("type", "start_continue")
        btn_continue.setStyleSheet('''
            QPushButton {
                padding: 5px;
                font-size: 11pt;
                font-weight: normal;
            }
        ''')
        
        course_progress_bar = QtWidgets.QProgressBar()
        course_progress_bar.setMinimumSize(QtCore.QSize(0, 15))
        course_progress_bar.setMaximumSize(QtCore.QSize(16777215, 15))
        course_progress_bar.setMaximum(100)
        course_progress_bar.setTextVisible(True)
        course_progress_bar.setFormat("%p%%")
        course_progress_bar.setStyleSheet('''
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 5px;
                text-align: center;
                margin-top: 3px;
                font-size: 8pt;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 5px;
                margin: 0.5px;
            }
        ''')
        
        course_progress_percentage = 0
        if course_data['lessons'] > 0 and course_data['completed_lessons'] > 0:
            course_progress_percentage = min(int((course_data['completed_lessons'] / course_data['lessons']) * 100), 100)
        
        course_progress_bar.setValue(int(course_progress_percentage))
        
        layout_continue.addWidget(btn_continue, 0, 0, 1, 1)
        layout_continue.addWidget(course_progress_bar, 1, 0, 1, 1)
        
        page_continue.setLayout(layout_continue)
        
        stacked_widget.addWidget(page_start)
        stacked_widget.addWidget(page_continue)
        
        card_layout.addWidget(title)
        card_layout.addLayout(tags_layout)
        card_layout.addWidget(description_widget)
        card_layout.addWidget(course_info)
        card_layout.addWidget(stacked_widget)
        
        if course_data['completed_lessons'] > 0: # or some other logic for active courses
            stacked_widget.setCurrentWidget(page_continue)
        else:
            stacked_widget.setCurrentWidget(page_start)
            
        if course_data['course_id']:
            btn_start.setProperty("course_id", course_data['course_id'])
            btn_continue.setProperty("course_id", course_data['course_id'])
        
        # Simplified connect, actual logic might need self as well
        btn_start.clicked.connect(lambda: self._handle_start_course(course_data['course_id'], stacked_widget, page_continue))
        btn_continue.clicked.connect(lambda: self._handle_open_lessons(course_data['course_id']))
        
        return course_card_widget

    def _handle_start_course(self, course_id, stacked_widget, page_continue):
        # Placeholder for original switch_to_continue logic
        print(f"Starting course: {course_id}")
        # Actual logic from original switch_to_continue
        try:
            if course_id:
                from src.services.session_manager import SessionManager
                session_manager = SessionManager()
                user_data = session_manager.get_current_user_data()
                if user_data and 'id' in user_data:
                    user_id = user_data['id']
                    progress = self.progress_service.get_course_progress(user_id, str(course_id))
                    if not progress:
                        self.progress_service.create_course_progress(user_id, str(course_id))
                stacked_widget.setCurrentWidget(page_continue)
                self._handle_open_lessons(course_id) # Also open lessons page
        except Exception as e:
            print(f"Error in _handle_start_course: {e}")

    def _handle_open_lessons(self, course_id):
        # Placeholder for original open_lessons_page logic
        print(f"Opening lessons for course: {course_id}")
        try:
            if course_id and self.stack and self.pg_lessons:
                self.pg_lessons.set_current_course_id(course_id) # Ensure this method exists and works
                self.stack.setCurrentWidget(self.pg_lessons)
        except Exception as e:
            print(f"Error in _handle_open_lessons: {e}")

    def _calculate_num_columns(self):
        viewport_width = self.courses_scroll_area.viewport().width()
        card_width = 310  # Fixed card width
        spacing = self.course_cards_layout.spacing()
        
        # Calculate how many cards can fit based on available width
        available_width = viewport_width - (self.course_cards_layout.contentsMargins().left() + 
                                           self.course_cards_layout.contentsMargins().right())
        num_columns = max(1, int(available_width / (card_width + spacing)))
        
        # Ensure we have at least 3 columns on wider screens
        if viewport_width >= 960 and num_columns < 3:
            num_columns = 3
            
        # For very large screens, allow more columns
        if viewport_width >= 1350 and num_columns < 4:
            num_columns = 4
        elif viewport_width >= 1750 and num_columns < 5:
            num_columns = 5
            
        # Clamp number of columns
        return min(max(num_columns, 1), 5)

    def resizeEvent(self, event: QtGui.QResizeEvent):
        super().resizeEvent(event)
        # Use a timer to avoid too frequent updates during resize drag
        if hasattr(self, '_resize_timer'):
            self._resize_timer.stop()
        
        self._resize_timer = QtCore.QTimer()
        self._resize_timer.setSingleShot(True)
        self._resize_timer.timeout.connect(self._perform_resize_layout)
        self._resize_timer.start(100) # Adjust delay as needed

    def _perform_resize_layout(self):
        new_num_columns = self._calculate_num_columns()
        if new_num_columns != self._current_num_columns :
            self.update_course_display(num_columns=new_num_columns)
        # If only width changed but num_columns is same, QGridLayout with stretch factors should handle it.

    def show_completed_courses(self):
        """Show only completed courses"""
        try:
            from src.services.session_manager import SessionManager
            session_manager = SessionManager()
            user_data = session_manager.get_current_user_data()
            
            if not (user_data and 'id' in user_data):
                print("No user data for completed courses")
                self._current_display_courses_data = []
                self.update_course_display()
                return

            user_id = user_data['id']
            completed_courses_data = []
            for course_data_item in self._all_loaded_courses_data:
                progress = self.progress_service.get_course_progress(user_id, str(course_data_item['course_id']))
                if progress and progress.is_completed:
                    # Update completed_lessons if needed for display, or rely on service
                    # For simplicity, keeping the stored 'completed_lessons' which is 0
                    completed_courses_data.append(course_data_item)
            
            self._current_display_courses_data = completed_courses_data
            self.update_course_display()
            if not completed_courses_data:
                print("No completed courses found")

        except Exception as e:
            print(f"Error filtering completed courses: {str(e)}")
            self._current_display_courses_data = list(self._all_loaded_courses_data) # Fallback
            self.update_course_display()

    def show_all_courses(self):
        """Show all courses regardless of progress"""
        self._current_display_courses_data = list(self._all_loaded_courses_data)
        self.update_course_display()

    def show_started_courses(self):
        """Show only courses that have been started but not yet completed"""
        try:
            from src.services.session_manager import SessionManager
            session_manager = SessionManager()
            user_data = session_manager.get_current_user_data()

            if not (user_data and 'id' in user_data):
                print("No user data for started courses")
                self._current_display_courses_data = []
                self.update_course_display()
                return

            user_id = user_data['id']
            started_courses_data = []
            for course_data_item in self._all_loaded_courses_data:
                progress = self.progress_service.get_course_progress(user_id, str(course_data_item['course_id']))
                # Consider started if progress exists and not fully completed
                # (assuming is_completed on progress means 100%)
                if progress and not progress.is_completed: 
                    updated_item = course_data_item.copy()
                    # Ensure lessons key exists and progress percentage is valid before calculation
                    lessons_count = updated_item.get('lessons', 0)
                    percentage = progress.progress_percentage
                    if lessons_count > 0 and percentage is not None:
                        completed_count = int((float(percentage) / 100.0) * float(lessons_count))
                        updated_item['completed_lessons'] = completed_count
                    # If not, completed_lessons might remain as it was in course_data_item (likely 0 or undefined)
                    # or we could set it to 0 explicitly if it wasn't set in .copy()
                    elif 'completed_lessons' not in updated_item: # Ensure it has a default
                        updated_item['completed_lessons'] = 0
                        
                    started_courses_data.append(updated_item)
            
            self._current_display_courses_data = started_courses_data
            self.update_course_display()
            if not started_courses_data:
                 # Create a message to show in the UI if layout is empty
                if self.course_cards_layout.count() == 0:
                    message_widget = QtWidgets.QLabel("No courses in progress")
                    message_widget.setAlignment(Qt.AlignCenter)
                    message_widget.setStyleSheet("font-size: 18px; color: #888;")
                    self.course_cards_layout.addWidget(message_widget, 0, 0, 1, self._current_num_columns if self._current_num_columns > 0 else 1)


        except Exception as e:
            print(f"Error filtering started courses: {str(e)}")
            import traceback
            traceback.print_exc()
            self._current_display_courses_data = list(self._all_loaded_courses_data) # Fallback
            self.update_course_display()

    def apply_filters(self):
        """Apply selected filters to the course list"""
        filters = {}
        selected_subjects_names = []
        if self.cb_subject1.isChecked():
            selected_subjects_names.append("Математика")
        if self.cb_subject2.isChecked():
            selected_subjects_names.append("Інформатика")
        
        selected_difficulty_name = None
        if self.rb_level1.isChecked():
            selected_difficulty_name = "Базовий"
        elif self.rb_level2.isChecked():
            selected_difficulty_name = "Середній"
        elif self.rb_level3.isChecked():
            selected_difficulty_name = "Високий"

        # Duration filter (assuming range_slider.get_range() exists and returns min_val, max_val)
        # min_duration, max_duration = self.range_slider.get_range()
        # For now, duration filter is not applied on the pre-loaded data,
        # as course data doesn't have explicit duration.
        # This would require CourseService.filter_courses to be called if we want server-side filtering
        # or having duration in the loaded course data.

        temp_filtered_data = []
        for course_item_data in self._all_loaded_courses_data:
            match = True
            if selected_subjects_names:
                if course_item_data['subject'] not in selected_subjects_names:
                    match = False
            
            if selected_difficulty_name:
                if course_item_data['level'] != selected_difficulty_name:
                    match = False
            
            # Add duration filter here if data is available
            # if min_duration > 0 or max_duration < MAX_COURSE_DURATION: # (pseudo-code for duration)
            #    if not (min_duration <= course_item_data['duration'] <= max_duration):
            #        match = False

            if match:
                temp_filtered_data.append(course_item_data)
        
        self._current_display_courses_data = temp_filtered_data
        self.update_course_display()

    def clear_filters(self):
        # Uncheck all checkboxes and radio buttons
        self.cb_subject1.setChecked(False)
        self.cb_subject2.setChecked(False)
        self.rb_level1.setChecked(False) 
        self.rb_level2.setChecked(False)
        self.rb_level3.setChecked(False)
        # Reset slider if you have one, e.g., self.range_slider.reset_values()

        # Load all courses
        self.show_all_courses() # This will set _current_display_courses_data and update display



    