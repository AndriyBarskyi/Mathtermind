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

        self.pg_courses = QtWidgets.QWidget()
        self.pg_courses.setObjectName("pg_courses")
        self.main_courses_layout = QtWidgets.QGridLayout(self.pg_courses)
        self.main_courses_layout.setObjectName("main_courses_layout")
        self.filter_buttons_widget = QtWidgets.QWidget(self.pg_courses)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.filter_buttons_widget.setSizePolicy(sizePolicy)
        self.filter_buttons_widget.setMinimumSize(QtCore.QSize(1020, 50))
        self.filter_buttons_widget.setMaximumSize(QtCore.QSize(1600000, 50))
        self.filter_buttons_widget.setProperty("type", "w_pg") 
        self.filter_buttons_widget.setObjectName("filter_buttons_widget")
        self.filter_buttons_layout = QtWidgets.QHBoxLayout(self.filter_buttons_widget)
        self.filter_buttons_layout.setContentsMargins(-1, 0, -1, -1)
        self.filter_buttons_layout.setObjectName("filter_buttons_layout")
        
        self.btn_all = QtWidgets.QPushButton(self.filter_buttons_widget)
        self.btn_all.setText("Всі курси")        
        self.btn_all.setSizePolicy(sizePolicy)        
        self.btn_all.setProperty("type", "start_continue_complete")
        self.btn_all.setObjectName("btn_all")
        self.filter_buttons_layout.addWidget(self.btn_all)
        self.btn_started_all = QtWidgets.QPushButton(self.filter_buttons_widget)
        self.btn_started_all.setText("Розпочаті")
        
        
        self.btn_started_all.setSizePolicy(sizePolicy)
        self.btn_started_all.setProperty("type", "start_continue_complete")
        self.btn_started_all.setObjectName("btn_started_all")
        self.filter_buttons_layout.addWidget(self.btn_started_all)
        self.btn_completed = QtWidgets.QPushButton(self.filter_buttons_widget)
        self.btn_completed.setText("Завершені")     
        self.btn_completed.setSizePolicy(sizePolicy)
        self.btn_completed.setProperty("type", "start_continue_complete")
        self.btn_completed.setObjectName("btn_completed")
        self.filter_buttons_layout.addWidget(self.btn_completed)
        self.main_courses_layout.addWidget(self.filter_buttons_widget, 1, 0, 1, 1)

        self.left_filter_section = QtWidgets.QWidget(self.pg_courses)
        self.left_filter_section.setMinimumSize(QtCore.QSize(300, 0))
        self.left_filter_section.setMaximumSize(QtCore.QSize(300, 16777215))
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
        self.range_label.setText("Оновлення")
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
        self.btn_apply.setMinimumSize(QtCore.QSize(0, 50))
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
        self.course_cards_layout.setSpacing(8)  # Reduced spacing between cards
        self.course_cards_layout.setContentsMargins(5, 5, 5, 5)  # Reduced margins
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
        self.course_widgets_complete = []  # список для збереження карток
        self.load_courses_from_db()
        
        self.btn_completed.clicked.connect(self.show_completed_courses)
        self.btn_all.clicked.connect(self.show_all_courses)
        self.btn_started_all.clicked.connect(self.show_started_courses)
        self.btn_apply.clicked.connect(self.apply_filters)
        self.btn_clear.clicked.connect(self.clear_filters)

    def load_courses_from_db(self):
        """Load courses from the database and display them"""
        try:
            # Clear existing courses
            self.clear_courses()
            
            # Get all courses from the database
            courses = self.course_service.get_all_courses()
            
            # Display each course
            for course in courses:
                # Map difficulty level to UI text
                difficulty_text = "Базовий"
                if course.difficulty_level == DifficultyLevel.INTERMEDIATE:
                    difficulty_text = "Середній"
                elif course.difficulty_level == DifficultyLevel.ADVANCED:
                    difficulty_text = "Високий"
                
                # Map topic to UI text
                subject_text = "Математика" if course.topic == Topic.MATHEMATICS else "Інформатика"
                
                # Get number of lessons (placeholder)
                num_lessons = len(course.lessons) if hasattr(course, 'lessons') and course.lessons else 5
                
                # Add course widget
                self.add_course_widget(
                    course.name, 
                    course.description, 
                    subject_text, 
                    difficulty_text, 
                    num_lessons,
                    0,  # For now, set completed_lessons to 0
                    course.id  # Pass the course ID
                )
        except Exception as e:
            print(f"Error loading courses: {str(e)}")

    def clear_courses(self):
        """Clear all course widgets from the layout"""
        # Remove all widgets from the course cards layout
        while self.course_cards_layout.count():
            item = self.course_cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # Clear the list of course widgets
        self.course_widgets_complete = []
        
    def add_course_widget(self, name, description, subject, level, lessons, complete_lessons=0, course_id=None):
        course_card_widget = QtWidgets.QWidget(self.scroll_area_content)
        course_card_widget.setFixedSize(QtCore.QSize(320, 280))
        course_card_widget.setProperty("type", "card")
        
        # Store course_id as a property on the widget
        if course_id:
            course_card_widget.setProperty("course_id", course_id)
        
        card_layout = QtWidgets.QVBoxLayout(course_card_widget)
        card_layout.setContentsMargins(10, 10, 10, 10)
        
        # Course title
        title = QtWidgets.QLabel(name)
        title.setProperty("type", "lb_name_lesson")
        title.setStyleSheet("font-size: 14pt; font-weight: bold;")
        title.setWordWrap(True)
        title.setMaximumHeight(50)
        
        # Create a horizontal layout for tags directly in the card layout
        tags_layout = QtWidgets.QHBoxLayout()
        tags_layout.setSpacing(10)
        tags_layout.setContentsMargins(0, 0, 0, 0)
        
        # Subject tag with color
        lb_subject = QtWidgets.QLabel(subject)
        lb_subject.setProperty("type", "tag")
        lb_subject.setMaximumSize(QtCore.QSize(120, 25))
        lb_subject.setMinimumSize(QtCore.QSize(70, 25))
        lb_subject.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        lb_subject.setAlignment(QtCore.Qt.AlignCenter)
        lb_subject.setStyleSheet("""
            background-color: #e6f2ff; 
            border-radius: 12px; 
            padding: 3px;
            font-size: 9pt;
        """)
        tags_layout.addWidget(lb_subject)
        
        # Level tag with color
        lb_level = QtWidgets.QLabel(level)
        lb_level.setProperty("type", "tag")
        lb_level.setMaximumSize(QtCore.QSize(120, 25))
        lb_level.setMinimumSize(QtCore.QSize(70, 25))
        lb_level.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        lb_level.setAlignment(QtCore.Qt.AlignCenter)
        lb_level.setStyleSheet("""
            background-color: #fff0e6; 
            border-radius: 12px; 
            padding: 3px;
            font-size: 9pt;
        """)
        tags_layout.addWidget(lb_level)
        
        tags_layout.addStretch()  # Push tags to the left
        
        # Description label
        description_widget = QtWidgets.QLabel(description)
        description_widget.setProperty("type", "lb_description")
        description_widget.setStyleSheet("background-color: transparent; border: none; padding: 0; font-size: 10pt;")
        description_widget.setWordWrap(True)
        description_widget.setMaximumHeight(50)
        
        # Add course info
        course_info = QtWidgets.QLabel(f"Уроків: {lessons}")
        course_info.setProperty("type", "lb_small")
        course_info.setStyleSheet("font-size: 9pt;")
        
        # Stacked widget for buttons
        stacked_widget = QtWidgets.QStackedWidget()
        stacked_widget.setMaximumSize(QtCore.QSize(16777215, 60))
        stacked_widget.setProperty("type", "w_pg")
        
        # Start button page
        page_start = QtWidgets.QWidget()
        page_start.setProperty("type", "w_pg")
        layout_start = QtWidgets.QGridLayout(page_start)
        layout_start.setContentsMargins(0, 0, 0, 0)
        
        btn_start = QtWidgets.QPushButton("Розпочати")
        btn_start.setMinimumSize(QtCore.QSize(0, 35))
        btn_start.setMaximumSize(QtCore.QSize(16777215, 35))
        btn_start.setProperty("type", "start_continue")
        btn_start.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                padding: 5px;
                font-size: 11pt;
            }
        """)
        
        layout_start.addWidget(btn_start, 0, 0, 1, 1)
        page_start.setLayout(layout_start)
        
        # Continue button page
        page_continue = QtWidgets.QWidget()
        layout_continue = QtWidgets.QGridLayout(page_continue)
        layout_continue.setContentsMargins(0, 0, 0, 0)
        
        btn_continue = QtWidgets.QPushButton("Continue")
        btn_continue.setMinimumSize(QtCore.QSize(0, 35))
        btn_continue.setMaximumSize(QtCore.QSize(16777215, 35))
        btn_continue.setProperty("type", "start_continue")
        btn_continue.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                padding: 5px;
                font-size: 11pt;
            }
        """)
        
        # Progress bar for courses
        course_progress_bar = QtWidgets.QProgressBar()
        course_progress_bar.setMinimumSize(QtCore.QSize(0, 15))
        course_progress_bar.setMaximumSize(QtCore.QSize(16777215, 15))
        course_progress_bar.setMaximum(100)
        course_progress_bar.setTextVisible(True)
        course_progress_bar.setFormat("%p%%")
        course_progress_bar.setStyleSheet("""
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
        """)
        
        # Calculate progress
        course_progress_percentage = 0
        if lessons > 0 and complete_lessons > 0:
            course_progress_percentage = min(int((complete_lessons / lessons) * 100), 100)
        
        course_progress_bar.setValue(int(course_progress_percentage))
        
        layout_continue.addWidget(btn_continue, 0, 0, 1, 1)
        layout_continue.addWidget(course_progress_bar, 1, 0, 1, 1)
        
        page_continue.setLayout(layout_continue)
        page_continue.setProperty("type", "w_pg")
        
        stacked_widget.addWidget(page_start)
        stacked_widget.addWidget(page_continue)
        
        # Add everything to the card layout
        card_layout.addWidget(title)
        card_layout.addLayout(tags_layout)
        card_layout.addWidget(description_widget)
        card_layout.addWidget(course_info)
        card_layout.addWidget(stacked_widget)
        
        # Show the appropriate button based on course status
        if complete_lessons > 0:
            stacked_widget.setCurrentWidget(page_continue)
        else:
            stacked_widget.setCurrentWidget(page_start)
            
        # Store the course_id on the buttons for reference
        if course_id:
            btn_start.setProperty("course_id", course_id)
            btn_continue.setProperty("course_id", course_id)
        
        # Connect button signals
        def switch_to_continue():
            try:
                # Get the course_id from the button
                sender = self.sender()
                course_id = sender.property("course_id")
                
                if course_id:
                    # Get user data
                    from src.services.session_manager import SessionManager
                    session_manager = SessionManager()
                    user_data = session_manager.get_current_user_data()
                    
                    if user_data and 'id' in user_data:
                        user_id = user_data['id']
                        
                        # Create or update progress for this course
                        progress = self.progress_service.get_course_progress(user_id, str(course_id))
                        if not progress:
                            # Create new progress
                            progress = self.progress_service.create_course_progress(user_id, str(course_id))
                            print(f"Created new progress for course {course_id}")
                        
                        # Switch to continue button
                        stacked_widget.setCurrentWidget(page_continue)
                        
                        # Open lessons page
                        open_lessons_page()
            except Exception as e:
                print(f"Error starting course: {str(e)}")
        
        def open_lessons_page():
            try:
                # Get the course_id from the sender
                sender = self.sender()
                course_id = sender.property("course_id")
                
                if course_id and self.stack and self.pg_lessons:
                    # Set the course ID in lessons page and switch to it
                    self.pg_lessons.set_current_course_id(course_id)
                    self.stack.setCurrentWidget(self.pg_lessons)
            except Exception as e:
                print(f"Error opening lessons page: {str(e)}")
        
        # Connect signals
        btn_start.clicked.connect(switch_to_continue)
        btn_continue.clicked.connect(open_lessons_page)
        
        # Add to layout with proper grid positioning
        # Find the next available position in the grid
        count = self.course_cards_layout.count()
        row = count // 3  # Max 3 cards per row
        col = count % 3
        self.course_cards_layout.addWidget(course_card_widget, row, col, 1, 1)
        self.course_widgets_complete.append(course_card_widget)
        
        return course_card_widget

    def show_completed_courses(self):
        """Show only completed courses"""
        # Clear existing courses
        self.clear_courses()
        
        # Get all courses and filter for completed ones
        courses = self.course_service.get_all_courses()
        completed_courses = []
        
        try:
            # Get user data
            from src.services.session_manager import SessionManager
            session_manager = SessionManager()
            user_data = session_manager.get_current_user_data()
            
            if user_data and 'id' in user_data:
                user_id = user_data['id']
                
                # Display each completed course
                for course in courses:
                    # Check if course is completed
                    course_id = str(course.id)
                    progress = self.progress_service.get_course_progress(user_id, course_id)
                    
                    if progress and progress.is_completed:
                        completed_courses.append(course)
                
                # If no completed courses, show a message
                if not completed_courses:
                    print("No completed courses found")
                    # You could add a label to the UI here to show "No completed courses found"
                
                # Display completed courses
                for course in completed_courses:
                    # Map difficulty level to UI text
                    difficulty_text = "Базовий"
                    if course.difficulty_level == DifficultyLevel.INTERMEDIATE:
                        difficulty_text = "Середній"
                    elif course.difficulty_level == DifficultyLevel.ADVANCED:
                        difficulty_text = "Високий"
                    
                    # Map topic to UI text
                    subject_text = "Математика" if course.topic == Topic.MATHEMATICS else "Інформатика"
                    
                    # Get number of lessons
                    num_lessons = len(course.lessons) if hasattr(course, 'lessons') and course.lessons else 5
                    
                    # Add course widget
                    self.add_course_widget(
                        course.name, 
                        course.description, 
                        subject_text, 
                        difficulty_text, 
                        num_lessons,
                        0,  # For now, set completed_lessons to 0
                        course.id  # Pass the course ID
                    )
            else:
                print("No user data available")
                self.load_courses_from_db()  # Fallback to showing all courses
        except Exception as e:
            print(f"Error filtering completed courses: {str(e)}")
            self.load_courses_from_db()  # Fallback to showing all courses

    def show_all_courses(self):
        """Show all courses regardless of progress"""
        # Reload all courses from the database
        self.load_courses_from_db()

    def show_started_courses(self):
        """Show only courses that have been started but not yet completed"""
        # Clear existing courses
        self.clear_courses()
        
        # Get all courses and filter for started ones
        courses = self.course_service.get_all_courses()
        started_courses = []
        
        try:
            # Get user data
            from src.services.session_manager import SessionManager
            session_manager = SessionManager()
            user_data = session_manager.get_current_user_data()
            
            print(f"User data in show_started_courses: {user_data}")
            
            if user_data and 'id' in user_data:
                user_id = user_data['id']
                
                # Display each started but not completed course
                for course in courses:
                    # Check if course is started but not completed
                    course_id = str(course.id)
                    progress = self.progress_service.get_course_progress(user_id, course_id)
                    
                    print(f"Course {course.name} (ID: {course_id}) progress: {progress}")
                    
                    # Consider a course started if it has any progress at all
                    if progress:
                        started_courses.append((course, progress.progress_percentage))
                
                # If no started courses, show a message
                if not started_courses:
                    print("No started courses found")
                    # Create a message to show in the UI
                    message_widget = QtWidgets.QLabel("No courses in progress")
                    message_widget.setAlignment(Qt.AlignCenter)
                    message_widget.setStyleSheet("font-size: 18px; color: #888;")
                    self.course_cards_layout.addWidget(message_widget, 0, 0, 1, 1)
                else:
                    print(f"Found {len(started_courses)} started courses")
                    
                    # Display started courses
                    for course, percentage in started_courses:
                        # Map difficulty level to UI text
                        difficulty_text = "Базовий"
                        if course.difficulty_level == DifficultyLevel.INTERMEDIATE:
                            difficulty_text = "Середній"
                        elif course.difficulty_level == DifficultyLevel.ADVANCED:
                            difficulty_text = "Високий"
                        
                        # Map topic to UI text
                        subject_text = "Математика" if course.topic == Topic.MATHEMATICS else "Інформатика"
                        
                        # Get number of lessons
                        num_lessons = len(course.lessons) if hasattr(course, 'lessons') and course.lessons else 5
                        
                        # Calculate completed lessons based on percentage
                        completed_lessons = int((percentage / 100) * num_lessons)
                        
                        # Add course widget - the layout is handled in add_course_widget
                        self.add_course_widget(
                            course.name, 
                            course.description, 
                            subject_text, 
                            difficulty_text, 
                            num_lessons,
                            completed_lessons,  # Show actual completed lessons
                            course.id  # Pass the course ID
                        )
                        
            else:
                print("No user data available")
                self.load_courses_from_db()  # Fallback to showing all courses
        except Exception as e:
            print(f"Error filtering started courses: {str(e)}")
            import traceback
            traceback.print_exc()
            self.load_courses_from_db()  # Fallback to showing all courses

    def apply_filters(self):
        try:
            # Clear existing courses
            self.clear_courses()
            
            # Build filter criteria
            filters = {}
            
            # Topic/subject filters
            topics = []
            if self.cb_subject1.isChecked():  # Математика
                topics.append(Topic.MATHEMATICS)
            if self.cb_subject2.isChecked():  # Інформатика
                topics.append(Topic.INFORMATICS)
            
            if topics:
                filters["topics"] = topics
            
            # Difficulty level filter
            if self.rb_level1.isChecked():  # Базовий
                filters["difficulty_level"] = DifficultyLevel.BEGINNER
            elif self.rb_level2.isChecked():  # Середній
                filters["difficulty_level"] = DifficultyLevel.INTERMEDIATE
            elif self.rb_level3.isChecked():  # Високий
                filters["difficulty_level"] = DifficultyLevel.ADVANCED
            
            # Get filtered courses
            filtered_courses = self.course_service.filter_courses(filters)
            
            # Display filtered courses
            for course in filtered_courses:
                # Map difficulty level to UI text
                difficulty_text = "Базовий"
                if course.difficulty_level == DifficultyLevel.INTERMEDIATE:
                    difficulty_text = "Середній"
                elif course.difficulty_level == DifficultyLevel.ADVANCED:
                    difficulty_text = "Високий"
                
                # Map topic to UI text
                subject_text = "Математика" if course.topic == Topic.MATHEMATICS else "Інформатика"
                
                # Get number of lessons
                num_lessons = len(course.lessons) if hasattr(course, 'lessons') and course.lessons else 5
                
                # Add course widget
                self.add_course_widget(
                    course.name, 
                    course.description, 
                    subject_text, 
                    difficulty_text, 
                    num_lessons,
                    0,  # For now, set completed_lessons to 0
                    course.id  # Pass the course ID
                )
                
        except Exception as e:
            print(f"Error applying filters: {str(e)}")

    def clear_filters(self):
        # Uncheck all checkboxes and radio buttons
        self.cb_subject1.setChecked(False)
        self.cb_subject2.setChecked(False)
        self.rb_level1.setChecked(False)
        self.rb_level2.setChecked(False)
        self.rb_level3.setChecked(False)
        
        # Reset slider
        self.range_slider.setLowerValue(50)
        self.range_slider.setUpperValue(250)
        
        # Load all courses
        self.load_courses_from_db()



    