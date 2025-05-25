from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from ui import*
from lesson_win import Lesson_page
from src.services import LessonService, ProgressService, SessionManager, CourseService
from itertools import groupby


class Lessons_page(QWidget):    
    def __init__(self, stack=None, lesson_page=None, course_id=None):
        super().__init__()
        self.stack = None
        self.pg_lesson = None
        self.stack = stack
        self.pg_lesson = lesson_page
        self.course_id = course_id
        
        # Initialize services
        self.lesson_service = LessonService()
        self.progress_service = ProgressService()
        self.course_service = CourseService()

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

        # If course_id is provided, load lessons for that course
        if self.course_id:
            self.load_course_lessons(self.course_id)
        else:
            # Otherwise, load sample data for demonstration
            self.add_new_tab("Перша вкладка", [
            ("Розділ 1", [
                {"title": "Вступ до Python", "labels": ("Math", "Beginner"), "description": "Опис уроку 1"},
                {"title": "Умовні оператори", "labels": ("IT", "Intermediate"), "description": "Опис уроку 2"},
                {"title": "Цикли for та while", "labels": ("Math", "Advanced"), "description": "Опис уроку 3"}
            ]),
            ("Python Basics", [
                {"title": "Функції", "labels": ("Math", "Beginner"), "description": "Опис уроку 4"},
                {"title": "Класи та обʼєкти", "labels": ("IT", "Advanced"), "description": "Опис уроку 5"}
            ])
        ])
            self.add_new_tab("Python Basics", [
            ("Розділ 1", [
                {"title": "Алгоритми сортування", "labels": ("Math", "Beginner"), "description": "Опис уроку 1"},
                {"title": "Рекурсія", "labels": ("IT", "Intermediate"), "description": "Опис уроку 2"},
                {"title": "Списки та словники", "labels": ("Math", "Advanced"), "description": "Опис уроку 3"}
            ]),
            ("Розділ 2", [
                {"title": "Модулі та пакети", "labels": ("Math", "Beginner"), "description": "Опис уроку 4"},
                {"title": "Урок 5", "labels": ("IT", "Advanced"), "description": "Опис уроку 5"}
            ])
        ])

        self.setLayout(self.main_lessons_layout)

    def set_course_id(self, course_id):
        """Set the course ID and load lessons for that course"""
        self.course_id = course_id
        if course_id:
            self.load_course_lessons(course_id)
    
    def load_course_lessons(self, course_id):
        """Load lessons for a specific course and organize them into sections"""
        # Clear existing tabs
        while self.lessons_tab_widget.count() > 0:
            self.lessons_tab_widget.removeTab(0)
        
        # Get lessons for the course
        lessons = self.lesson_service.get_lessons_by_course_id(course_id)
        if not lessons:
            # If no lessons, add an empty tab
            self.add_new_tab("Немає уроків", [])
            return
        
        # Get course details for the tab title and potentially for tags
        current_course = self.course_service.get_course_by_id(course_id)
        course_name_for_tab = current_course.name if current_course else "Курс"
        course_topic_for_tag = current_course.topic if current_course and hasattr(current_course, 'topic') and current_course.topic else "Загальне"
        
        # Group lessons by order (every 5 lessons is a new section)
        grouped_lessons = []
        for i, lesson in enumerate(sorted(lessons, key=lambda l: l.lesson_order)):
            section_index = i // 5
            section_name = f"Розділ {section_index + 1}"
            
            if len(grouped_lessons) <= section_index:
                grouped_lessons.append((section_name, []))
            
            # Get user's completion status for this lesson
            completed = False
            current_user = SessionManager.get_current_user()
            # SessionManager.get_current_user() returns a tuple or None
            if current_user and isinstance(current_user, tuple) and len(current_user) >= 3:
                # Extract user data from the tuple
                user_dict = current_user[2]
                if isinstance(user_dict, dict) and 'id' in user_dict:
                    user_id = user_dict['id']
                    completed = self.progress_service.has_completed_lesson(user_id, lesson.id)
            
            # Create card data
            lesson_difficulty = getattr(lesson, 'difficulty_level', "Початковий")
            if hasattr(lesson_difficulty, 'value'): # If it's an enum
                lesson_difficulty = lesson_difficulty.value

            card_data = {
                "title": lesson.title,
                "labels": (course_topic_for_tag, lesson_difficulty),
                "description": f"Урок {lesson.lesson_order}: {getattr(lesson, 'formatted_duration', '10 хв')}",
                "lesson_id": lesson.id,
                "completed": completed
            }
            
            grouped_lessons[section_index][1].append(card_data)
        
        # Add a tab for the course with all sections
        self.add_new_tab(course_name_for_tab, grouped_lessons)

    def create_card(self, title_text="Назва", labels_text=("TextLabel1", "TextLabel2"), desc_text="Опис", lesson_id=None, completed=False):
        card = QtWidgets.QWidget()
        card.setFixedSize(QtCore.QSize(360, 330))
        card.setProperty("type", "card")
        card_layout = QtWidgets.QVBoxLayout(card)
        title = QtWidgets.QLabel(title_text)
        title.setProperty("type","lb_name_lesson")
        # Мітки 
        labels = QtWidgets.QHBoxLayout()
        for text in labels_text:
            lb_subject = QtWidgets.QLabel(text)
            lb_subject.setProperty("type","lb_name_course")
            lb_subject.setMinimumSize(QtCore.QSize(165, 50))
            lb_subject.setMaximumSize(QtCore.QSize(165, 50))
            labels.addWidget(lb_subject)
        
        lb_description = QtWidgets.QLabel(desc_text)
        lb_description.setProperty("type","lb_description")
        
        stacked_widget = QtWidgets.QStackedWidget()
        stacked_widget.setMaximumSize(QtCore.QSize(16777215, 75))
        stacked_widget.setProperty("type","w_pg")

        page_start = QtWidgets.QWidget()
        page_start.setProperty("type","w_pg")
        layout_start = QtWidgets.QGridLayout(page_start)

        btn_start = QtWidgets.QPushButton("Почати урок")
        btn_start.setMinimumSize(QtCore.QSize(310, 50))
        btn_start.setProperty("type","start_continue")
        
        layout_start.addWidget(btn_start, 0, 0, 1, 1)

        page_start.setLayout(layout_start)

        page_continue = QtWidgets.QWidget()
        layout_continue = QtWidgets.QGridLayout(page_continue)

        # If lesson is completed, show "Completed" button, otherwise "Continue"
        btn_text = "Завершено" if completed else "Продовжити"
        btn_continue = QtWidgets.QPushButton(btn_text)
        btn_continue.setMinimumSize(QtCore.QSize(310, 50))
        btn_continue.setProperty("type","start_continue")

        progress_bar = QtWidgets.QProgressBar()
        progress_bar.setMinimumSize(QtCore.QSize(310, 20))
        progress_bar.setMaximum(100)
        progress_bar.setValue(100 if completed else 10)
        
        layout_continue.setContentsMargins(0, 0, 0, 0)
        layout_continue.addWidget(btn_continue, 0, 0, 1, 1)
        layout_continue.addWidget(progress_bar, 1, 0, 1, 1)

        page_continue.setLayout(layout_continue)
        page_continue.setProperty("type","w_pg")

        stacked_widget.addWidget(page_start)
        stacked_widget.addWidget(page_continue)

        # If already completed, show continue page by default
        if completed:
            stacked_widget.setCurrentWidget(page_continue)

        def switch_to_continue():
            stacked_widget.setCurrentWidget(page_continue)

        def open_lesson_page():
            # Store the lesson_id
            lesson_data = {"id": lesson_id, "title": title_text}
            
            if self.pg_lesson and self.stack:
                if hasattr(self.pg_lesson, 'set_lesson_data'):
                    self.pg_lesson.set_lesson_data(lesson_data)
                self.stack.setCurrentWidget(self.pg_lesson)
            else:
                # Create a new lesson page if needed
                lesson_page = Lesson_page(lesson_id=lesson_id)
                if self.stack:
                    self.stack.addWidget(lesson_page)
                    self.stack.setCurrentWidget(lesson_page)
        
        btn_start.clicked.connect(switch_to_continue)
        btn_continue.clicked.connect(open_lesson_page)

        card_layout.addWidget(title)
        card_layout.addLayout(labels)
        card_layout.addWidget(lb_description)
        card_layout.addWidget(stacked_widget)
        return card

    def create_section(self, section_title="Розділ", cards_data=None):
        section_widget = QtWidgets.QWidget()
        section_layout = QtWidgets.QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)
        
        section_label = QtWidgets.QLabel(section_title)
        section_label.setProperty("type", "card")
        section_layout.addWidget(section_label)

        cards_container = QtWidgets.QWidget()
        cards_layout = QtWidgets.QHBoxLayout(cards_container)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(10)  
        cards_layout.setAlignment(QtCore.Qt.AlignLeft) 

        if cards_data:
            for card_info in cards_data:
                title = card_info.get("title", "Назва")
                labels = card_info.get("labels", ("Label1", "Label2"))
                desc = card_info.get("description", "Опис")
                lesson_id = card_info.get("lesson_id")
                completed = card_info.get("completed", False)
                card = self.create_card(title, labels, desc, lesson_id, completed)
                cards_layout.addWidget(card)

        spacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        cards_layout.addItem(spacer)

        section_layout.addWidget(cards_container)
        return section_widget

    def add_new_tab(self, name="Нова вкладка", sections_data=None):
        new_tab = QtWidgets.QWidget()
        new_tab.setObjectName(name)
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_area_widget)
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        scroll_layout.setSpacing(15)
        if sections_data:
            for section_title, num_cards in sections_data:
                section_widget = self.create_section(section_title, num_cards)
                scroll_layout.addWidget(section_widget)
        scroll_area.setWidget(scroll_area_widget)
        tab_layout = QtWidgets.QVBoxLayout(new_tab)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll_area)
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