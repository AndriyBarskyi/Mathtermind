from PyQt5.QtWidgets import QWidget, QGridLayout,QVBoxLayout, QLabel,QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from main_page import *
from lesson_win import Lesson_page
from src.services.lesson_service import LessonService
from src.services.course_service import CourseService
from src.services.progress_service import ProgressService
import uuid


class Lessons_page(QWidget):    
    def __init__(self,stack=None, lesson_page=None):
        super().__init__()
        self.stack = None
        self.pg_lesson = None
        self.stack = stack
        self.pg_lesson = lesson_page
        
        # Set parent pages for lesson navigation
        if self.pg_lesson:
            self.pg_lesson.set_parent_pages(lessons_page=self, stack=stack)
        
        # Initialize services
        self.lesson_service = LessonService()
        self.course_service = CourseService()
        self.progress_service = ProgressService()
        
        # Store current course ID
        self.current_course_id = None

        self.pg_lessons = QtWidgets.QWidget()
        self.pg_lessons.setObjectName("pg_lessons")
        self.main_lessons_layout = QtWidgets.QGridLayout(self.pg_lessons)
        self.main_lessons_layout.setObjectName("main_lessons_layout")
        
        self.lb_lessons = QtWidgets.QLabel(self.pg_lessons)
        self.lb_lessons.setText("Уроки")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.lb_lessons.setSizePolicy(sizePolicy)
        self.lb_lessons.setMinimumSize(QtCore.QSize(0, 50))
        self.lb_lessons.setMaximumSize(QtCore.QSize(16777215, 50))
        self.lb_lessons.setProperty("type", "title")
        
        self.lb_lessons.setObjectName("lb_lessons")
        self.main_lessons_layout.addWidget(self.lb_lessons, 0, 0, 1, 1)
        self.lessons_tab_widget = QtWidgets.QTabWidget(self.pg_lessons)
        self.lessons_tab_widget.setMinimumSize(QtCore.QSize(660, 300))
        self.lessons_tab_widget.setObjectName("lessons_tab_widget")
        
        self.main_lessons_layout.addWidget(self.lessons_tab_widget, 2, 0, 1, 1)
        self.lb_choice = QtWidgets.QLabel(self.pg_lessons)
        self.lb_choice.setText("Виберіть курс:")
        self.lb_choice.setSizePolicy(sizePolicy)
        self.lb_choice.setMinimumSize(QtCore.QSize(0, 50))
        self.lb_choice.setMaximumSize(QtCore.QSize(16777215, 50))
        self.lb_choice.setProperty("type", "page_section")
        self.lb_choice.setObjectName("lb_choice")
        self.main_lessons_layout.addWidget(self.lb_choice, 1, 0, 1, 1)

        self.setLayout(self.main_lessons_layout)
        
        # Initialize with a message tab for when no course is selected
        self.add_no_course_selected_tab()

    def add_no_course_selected_tab(self):
        """Add a tab with a message when no course is selected"""
        # Clear existing tabs
        while self.lessons_tab_widget.count() > 0:
            self.lessons_tab_widget.removeTab(0)
            
        # Create a new tab with a message
        no_course_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(no_course_tab)
        
        message = QtWidgets.QLabel("Виберіть курс на сторінці Курси, щоб розпочати навчання")
        message.setAlignment(QtCore.Qt.AlignCenter)
        message.setProperty("type", "lb_description")
        message.setWordWrap(True)
        
        layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        layout.addWidget(message)
        layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        
        self.lessons_tab_widget.addTab(no_course_tab, "Оберіть курс")

    def load_course_lessons(self, course_id):
        """Load lessons for the specified course from the database"""
        try:
            # Store current course ID
            self.current_course_id = course_id
            
            # Get course details
            course = self.course_service.get_course_by_id(course_id)
            if not course:
                print(f"Курс не знайдено: {course_id}")
                self.add_no_course_selected_tab()
                return
                
            print(f"Завантаження уроків для курсу: {course.name} (ID: {course_id})")
            
            # Update course selection label
            self.lb_choice.setText(f"Курс: {course.name}")
            
            # Get all lessons for this course
            lessons = self.lesson_service.get_lessons_by_course_id(course_id)
            
            if not lessons or len(lessons) == 0:
                print(f"Для курсу немає уроків: {course.name}")
                
                # Create a tab with an explanation message
                no_lessons_tab = QtWidgets.QWidget()
                layout = QtWidgets.QVBoxLayout(no_lessons_tab)
                
                message = QtWidgets.QLabel("Для цього курсу ще немає уроків. Будь ласка, виберіть інший курс.")
                message.setAlignment(QtCore.Qt.AlignCenter)
                message.setProperty("type", "lb_description")
                message.setWordWrap(True)
                
                layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
                layout.addWidget(message)
                layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
                
                # Clear existing tabs
                while self.lessons_tab_widget.count() > 0:
                    self.lessons_tab_widget.removeTab(0)
                
                self.lessons_tab_widget.addTab(no_lessons_tab, course.name)
                return
            
            # Clear existing tabs
            while self.lessons_tab_widget.count() > 0:
                self.lessons_tab_widget.removeTab(0)
            
            # Organize lessons by section based on lesson_order
            section1_lessons = []
            section2_lessons = []
            
            for lesson in lessons:
                # Debug print to help troubleshoot
                print(f"Обробка уроку: {lesson.title}, ID: {lesson.id}, order: {lesson.lesson_order}")
                
                # Create data for the lesson card
                lesson_data = {
                    "title": lesson.title,
                    "labels": (
                        course.topic.value if hasattr(course, 'topic') and hasattr(course.topic, 'value') else "Загальне", 
                        self._get_difficulty_text(lesson)
                    ),
                    "description": f"Урок {lesson.lesson_order}: {lesson.title}",
                    "lesson_id": str(lesson.id),
                    "estimated_time": lesson.estimated_time
                }
                
                # Distribute lessons between sections based on order
                if lesson.lesson_order <= 3:
                    section1_lessons.append(lesson_data)
                else:
                    section2_lessons.append(lesson_data)
            
            # Create tab for the course
            sections_data = []
            
            # Only add sections if they have lessons
            if section1_lessons:
                sections_data.append(("Розділ 1: Основи", section1_lessons))
            if section2_lessons:
                sections_data.append(("Розділ 2: Практика", section2_lessons))
            
            # Add the tab with course data
            self.add_new_tab(course.name, sections_data)
            
        except Exception as e:
            print(f"Помилка завантаження уроків курсу: {str(e)}")
            import traceback
            traceback.print_exc()
            # If there's an error, show the no course selected tab
            self.add_no_course_selected_tab()

    def create_card(self, title_text="Назва", labels_text=("TextLabel1", "TextLabel2"), desc_text="Опис", lesson_id=None, estimated_time=30):
        card = QtWidgets.QWidget()
        card.setFixedSize(QtCore.QSize(320, 280))
        card.setProperty("type", "card")
        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setContentsMargins(10, 10, 10, 10)
        
        # Lesson title
        title = QtWidgets.QLabel(title_text)
        title.setProperty("type","lb_name_lesson")
        title.setStyleSheet("font-size: 14pt; font-weight: bold;")
        title.setWordWrap(True)
        title.setMaximumHeight(50)
        
        # Create a horizontal layout for tags directly in the card layout
        tags_layout = QtWidgets.QHBoxLayout()
        tags_layout.setSpacing(10)
        tags_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create styled tags for subject and difficulty level
        for i, text in enumerate(labels_text):
            tag_label = QtWidgets.QLabel(text)
            tag_label.setProperty("type", "tag")
            tag_label.setMaximumSize(QtCore.QSize(120, 25))
            tag_label.setMinimumSize(QtCore.QSize(70, 25))
            tag_label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            tag_label.setAlignment(QtCore.Qt.AlignCenter)
            
            # Different background colors for different tags
            bg_color = "#e6f2ff" if i == 0 else "#fff0e6"  # Blue for subject, Orange for difficulty
            
            tag_label.setStyleSheet(f"""
                background-color: {bg_color}; 
                border-radius: 12px; 
                padding: 3px;
                font-size: 9pt;
            """)
            
            tags_layout.addWidget(tag_label)
            
        tags_layout.addStretch()  # Push tags to the left
        
        # Description label
        lb_description = QtWidgets.QLabel(desc_text)
        lb_description.setProperty("type","lb_description")
        lb_description.setStyleSheet("background-color: transparent; border: none; padding: 0; font-size: 10pt;")
        lb_description.setWordWrap(True)
        lb_description.setMaximumHeight(50)
        
        # Add estimated time
        lb_time = QtWidgets.QLabel(f"Тривалість: {estimated_time} хв")
        lb_time.setProperty("type","lb_small")
        lb_time.setStyleSheet("font-size: 9pt;")
        
        stacked_widget = QtWidgets.QStackedWidget()
        stacked_widget.setMaximumSize(QtCore.QSize(16777215, 60))
        stacked_widget.setProperty("type","w_pg")

        page_start = QtWidgets.QWidget()
        page_start.setProperty("type","w_pg")
        layout_start = QtWidgets.QGridLayout(page_start)
        layout_start.setContentsMargins(0, 0, 0, 0)

        btn_start = QtWidgets.QPushButton("Почати урок")
        btn_start.setMinimumSize(QtCore.QSize(0, 35))
        btn_start.setMaximumSize(QtCore.QSize(16777215, 35))
        btn_start.setProperty("type","start_continue")
        btn_start.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                padding: 5px;
                font-size: 11pt;
            }
        """)
        
        layout_start.addWidget(btn_start, 0, 0, 1, 1)

        page_start.setLayout(layout_start)

        page_continue = QtWidgets.QWidget()
        layout_continue = QtWidgets.QGridLayout(page_continue)
        layout_continue.setContentsMargins(0, 0, 0, 0)

        btn_continue = QtWidgets.QPushButton("Продовжити")
        btn_continue.setMinimumSize(QtCore.QSize(0, 35))
        btn_continue.setMaximumSize(QtCore.QSize(16777215, 35))
        btn_continue.setProperty("type","start_continue")
        btn_continue.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                padding: 5px;
                font-size: 11pt;
            }
        """)

        progress_bar = QtWidgets.QProgressBar()
        progress_bar.setMinimumSize(QtCore.QSize(0, 15))
        progress_bar.setMaximumSize(QtCore.QSize(16777215, 15))
        progress_bar.setMaximum(100)
        progress_bar.setTextVisible(True)
        progress_bar.setFormat("%p%%")
        progress_bar.setStyleSheet("""
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
        
        # Check if lesson is completed by the current user
        progress_value = 0
        if lesson_id:
            try:
                from src.services.session_manager import SessionManager
                session_manager = SessionManager()
                user_data = session_manager.get_current_user_data()
                
                if user_data and 'id' in user_data:
                    user_id = user_data['id']
                    is_completed = self.progress_service.has_completed_lesson(user_id, lesson_id)
                    if is_completed:
                        progress_value = 100
                        btn_continue.setText("Пройдено ✓")
                        btn_continue.setStyleSheet("""
                            QPushButton {
                                background-color: #4CAF50;
                                color: white;
                                border-radius: 10px;
                                padding: 5px;
                                font-size: 11pt;
                            }
                        """)
            except Exception as e:
                print(f"Error checking lesson completion: {str(e)}")
        
        progress_bar.setValue(progress_value)
        
        layout_continue.setContentsMargins(0, 0, 0, 0)
        layout_continue.addWidget(btn_continue, 0, 0, 1, 1)
        layout_continue.addWidget(progress_bar, 1, 0, 1, 1)

        page_continue.setLayout(layout_continue)
        page_continue.setProperty("type","w_pg")

        stacked_widget.addWidget(page_start)
        stacked_widget.addWidget(page_continue)

        def switch_to_continue():
            stacked_widget.setCurrentWidget(page_continue)

        def open_lesson_page():
            if lesson_id:
                print(f"Відкриваємо урок: {title_text} (ID: {lesson_id})")
                self.pg_lesson.set_lesson_data(title_text, lesson_id)
            else:
                print(f"Відкриваємо урок: {title_text}")
                self.pg_lesson.set_lesson_data(title_text)
            self.stack.setCurrentWidget(self.pg_lesson)
        
        btn_start.clicked.connect(switch_to_continue)
        btn_continue.clicked.connect(open_lesson_page)

        card_layout.addWidget(title)
        card_layout.addLayout(tags_layout)
        card_layout.addWidget(lb_description)
        card_layout.addWidget(lb_time)
        card_layout.addWidget(stacked_widget)
        
        # Always show progress bar for better UI consistency
        if progress_value == 0:
            stacked_widget.setCurrentWidget(page_start)
        else:
            stacked_widget.setCurrentWidget(page_continue)
            
        return card

    def create_section(self, section_title="Розділ", cards_data=None):
        section_widget = QtWidgets.QWidget()
        section_layout = QtWidgets.QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 15)
        
        # Improved section title styling
        section_label = QtWidgets.QLabel(section_title)
        section_label.setProperty("type", "page_section")
        section_label.setStyleSheet("""
            font-size: 18pt;
            font-weight: bold;
            padding: 10px 0;
            border-bottom: 2px solid #e0e0e0;
            margin-bottom: 15px;
        """)
        section_layout.addWidget(section_label)

        # Create a scrollable area for cards to enable horizontal scrolling
        cards_scroll_area = QtWidgets.QScrollArea()
        cards_scroll_area.setWidgetResizable(True)
        cards_scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        cards_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        cards_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        cards_scroll_area.setMinimumHeight(300)

        cards_container = QtWidgets.QWidget()
        cards_layout = QtWidgets.QHBoxLayout(cards_container)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(20)  # Increase spacing between cards
        cards_layout.setAlignment(QtCore.Qt.AlignLeft) 

        if cards_data:
            for card_info in cards_data:
                title = card_info.get("title", "Назва")
                labels = card_info.get("labels", ("Label1", "Label2"))
                desc = card_info.get("description", "Опис")
                lesson_id = card_info.get("lesson_id", None)
                estimated_time = card_info.get("estimated_time", 30)
                card = self.create_card(title, labels, desc, lesson_id, estimated_time)
                cards_layout.addWidget(card)

        spacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        cards_layout.addItem(spacer)
        
        cards_scroll_area.setWidget(cards_container)
        section_layout.addWidget(cards_scroll_area)
        
        return section_widget

    def add_new_tab(self, name="Нова вкладка", sections_data=None):
        new_tab = QtWidgets.QWidget()
        new_tab.setObjectName(name)
        
        # Improved scroll area with better styling
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
        """)
        
        # Content widget with improved layout
        scroll_area_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_area_widget)
        scroll_layout.setContentsMargins(20, 20, 20, 20)  # Increased padding for better visual spacing
        scroll_layout.setSpacing(30)  # Increased spacing between sections
        
        # Add a welcoming header for the course
        if name:
            course_header = QtWidgets.QLabel(f"Курс: {name}")
            course_header.setProperty("type", "title")
            course_header.setStyleSheet("""
                font-size: 24pt;
                font-weight: bold;
                color: #333;
                margin-bottom: 20px;
            """)
            scroll_layout.addWidget(course_header)
            
            # Add a description label
            course_desc = QtWidgets.QLabel("Оберіть урок із запропонованих розділів нижче, щоб почати навчання.")
            course_desc.setProperty("type", "lb_description")
            course_desc.setWordWrap(True)
            scroll_layout.addWidget(course_desc)
            
            # Add separator
            separator = QtWidgets.QFrame()
            separator.setFrameShape(QtWidgets.QFrame.HLine)
            separator.setFrameShadow(QtWidgets.QFrame.Sunken)
            separator.setStyleSheet("background-color: #e0e0e0;")
            separator.setFixedHeight(2)
            scroll_layout.addWidget(separator)
        
        # Add section widgets
        if sections_data:
            for section_title, cards_data in sections_data:
                section_widget = self.create_section(section_title, cards_data)
                scroll_layout.addWidget(section_widget)
                
        # Add spacer at the bottom
        spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        scroll_layout.addItem(spacer)
                
        scroll_area.setWidget(scroll_area_widget)
        
        # Set up the tab layout
        tab_layout = QtWidgets.QVBoxLayout(new_tab)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll_area)
        
        # Add the tab to the tab widget
        self.lessons_tab_widget.addTab(new_tab, name)
    
    def set_lesson_tab_by_name(self, lesson_name):
        print(f"Пошук уроку у вкладках: {lesson_name}")
        tab_count = self.lessons_tab_widget.count()
        found_index = -1
        for i in range(tab_count):
            tab_label = self.lessons_tab_widget.tabText(i)
            if isinstance(tab_label, str):
                if tab_label.lower() == lesson_name.lower():
                    found_index = i
                    break
        if found_index != -1:
            self.lessons_tab_widget.setCurrentIndex(found_index)
        else:
            print("Вкладку не знайдено")

    def _get_difficulty_text(self, lesson):
        """Get a formatted difficulty text from a lesson object
        
        Args:
            lesson: The lesson object
            
        Returns:
            A string representing the difficulty level
        """
        if not hasattr(lesson, 'difficulty_level'):
            return "Базовий"  # Default
            
        difficulty = lesson.difficulty_level
        if difficulty is None:
            return "Базовий"
            
        # Handle if it's an enum
        if hasattr(difficulty, 'value'):
            return difficulty.value
            
        # Handle if it's a string
        return str(difficulty)

    def set_current_course_id(self, course_id):
        """Set the current course ID and load its lessons
        
        Args:
            course_id: The ID of the course to load
        """
        print(f"Setting current course ID: {course_id}")
        if course_id:
            self.current_course_id = course_id
            self.load_course_lessons(course_id)
        else:
            print("Warning: Tried to set current course ID to None")
            self.add_no_course_selected_tab()