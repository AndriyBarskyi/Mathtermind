from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QScrollArea, QTabWidget
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from datetime import datetime

from src.services import LessonService, ProgressService, SessionManager, CourseService
from src.models.progress import Progress
from lesson_win import Lesson_page


class Lessons_page(QWidget):
    def __init__(self, stack=None, lesson_page=None):
        super().__init__()
        
        self.stack = stack
        self.pg_lesson = lesson_page
        
        self.lesson_service = LessonService()
        self.progress_service = ProgressService()
        self.course_service = CourseService()
        self.session_manager = SessionManager()
        
        self.recent_courses = []
        self.active_course_button = None
        self.course_buttons = []
        
        self.pg_lessons = QtWidgets.QWidget()
        self.pg_lessons.setObjectName("pg_lessons")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.pg_lessons)
        self.gridLayout_9.setObjectName("gridLayout_9")
        
        self.lb_lessons = QtWidgets.QLabel(self.pg_lessons)
        self.lb_lessons.setText("Уроки")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_lessons.sizePolicy().hasHeightForWidth())
        self.lb_lessons.setSizePolicy(sizePolicy)
        self.lb_lessons.setMinimumSize(QtCore.QSize(0, 50))
        self.lb_lessons.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lb_lessons.setFont(font)
        self.lb_lessons.setObjectName("lb_lessons")
        self.gridLayout_9.addWidget(self.lb_lessons, 0, 0, 1, 1)
        
        self.lb_choice = QtWidgets.QLabel(self.pg_lessons)
        self.lb_choice.setText("Виберіть курс:")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_choice.sizePolicy().hasHeightForWidth())
        self.lb_choice.setSizePolicy(sizePolicy)
        self.lb_choice.setMinimumSize(QtCore.QSize(0, 50))
        self.lb_choice.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lb_choice.setFont(font)
        self.lb_choice.setObjectName("lb_choice")
        self.gridLayout_9.addWidget(self.lb_choice, 1, 0, 1, 1)
        
        self.course_buttons_widget = QWidget()
        self.course_buttons_layout = QHBoxLayout(self.course_buttons_widget)
        self.course_buttons_layout.setSpacing(10)
        self.course_buttons_layout.setContentsMargins(0, 0, 0, 10)
        self.gridLayout_9.addWidget(self.course_buttons_widget, 2, 0, 1, 1)
        
        self.tabWidget_3 = QtWidgets.QTabWidget(self.pg_lessons)
        self.tabWidget_3.setMinimumSize(QtCore.QSize(660, 300))
        self.tabWidget_3.setObjectName("tabWidget_3")
        self.tabWidget_3.tabBar().setVisible(False)
        self.gridLayout_9.addWidget(self.tabWidget_3, 3, 0, 1, 1)
        
        self.setLayout(self.gridLayout_9)
        
        self._load_recent_courses()
    
    def _load_recent_courses(self):
        """
        Load the user's recent courses where they've made progress.
        If no user is logged in, display all available courses.
        """
        self._clear_course_buttons()
        self.recent_courses = []
        
        current_user = self.session_manager.get_current_user()
        user_id = None
        
        if current_user and isinstance(current_user, tuple) and len(current_user) >= 3:
            user_dict = current_user[2]
            if isinstance(user_dict, dict) and 'id' in user_dict:
                user_id = user_dict['id']
        
        if user_id:
            progress_records = self.progress_service.get_user_progress(user_id)
            
            progress_records = [p for p in progress_records if p.progress_percentage > 0]
            
            progress_records.sort(key=lambda p: p.last_accessed if p.last_accessed else datetime.min, reverse=True)
            
            recent_progress = progress_records[:5]
            
            if recent_progress:
                for progress in recent_progress:
                    course = self.course_service.get_course_by_id(progress.course_id)
                    if course:
                        self._add_course_button(course.name, course.id)
                        self.recent_courses.append(course)
                
                if self.recent_courses:
                    self._load_course_lessons(self.recent_courses[0].id)
                    return
        
        all_courses = self.course_service.get_all_courses()
        for i, course in enumerate(all_courses[:5]):
            self._add_course_button(course.name, course.id)
            self.recent_courses.append(course)
        
        if self.recent_courses:
            self._load_course_lessons(self.recent_courses[0].id)
        else:
            self._show_no_courses_message()
    
    def _clear_course_buttons(self):
        """Clear all course buttons from the container"""
        for button in self.course_buttons:
            self.course_buttons_layout.removeWidget(button)
            button.deleteLater()
        self.course_buttons = []
        self.active_course_button = None
    
    def _add_course_button(self, course_name, course_id):
        """Add a button for a course"""
        button = QPushButton(course_name)
        button.setMinimumSize(QtCore.QSize(180, 50))
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.setProperty("type", "lb_name_course")
        button.setProperty("active", "false")
        
        button.clicked.connect(lambda checked, cid=course_id, btn=button: self._on_course_button_clicked(cid, btn))
        
        self.course_buttons_layout.addWidget(button)
        self.course_buttons.append(button)
        
        if not self.active_course_button:
            self.active_course_button = button
            button.setProperty("active", "true")
    
    def _on_course_button_clicked(self, course_id, button):
        """Handle course button click"""
        # Update button styles for all course buttons
        for btn in self.course_buttons:
            btn.setProperty("active", "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        button.setProperty("active", "true")
        button.style().unpolish(button)
        button.style().polish(button)
        self.active_course_button = button
        self._load_course_lessons(course_id)
    
    def _load_course_lessons(self, course_id):
        """Load lessons for a course and display them"""
        while self.tabWidget_3.count() > 0:
            self.tabWidget_3.removeTab(0)
        
        lessons = self.lesson_service.get_lessons_by_course_id(course_id)
        if not lessons:
            tab = QWidget()
            layout = QVBoxLayout(tab)
            label = QLabel("Немає уроків для цього курсу")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
            self.tabWidget_3.addTab(tab, "Немає уроків")
            return
        
        current_course = self.course_service.get_course_by_id(course_id)
        course_name = current_course.name if current_course else "Курс"
        course_topic = current_course.topic if current_course else "Загальне"
        
        grouped_lessons = []
        for i, lesson in enumerate(sorted(lessons, key=lambda l: l.lesson_order)):
            section_index = i // 5
            section_name = f"Розділ {section_index + 1}"
            
            if len(grouped_lessons) <= section_index:
                grouped_lessons.append((section_name, []))
            
            completed = False
            current_user = self.session_manager.get_current_user()
            if current_user and isinstance(current_user, tuple) and len(current_user) >= 3:
                user_dict = current_user[2]
                if isinstance(user_dict, dict) and 'id' in user_dict:
                    user_id = user_dict['id']
                    completed = self.progress_service.has_completed_lesson(user_id, lesson.id)
            
            lesson_difficulty = getattr(lesson, 'difficulty_level', "Початковий")
            if hasattr(lesson_difficulty, 'value'):
                lesson_difficulty = lesson_difficulty.value
            
            card_data = {
                "title": lesson.title,
                "labels": (course_topic, lesson_difficulty),
                "description": f"Урок {lesson.lesson_order}: {getattr(lesson, 'formatted_duration', '10 хв')}",
                "lesson_id": lesson.id,
                "completed": completed
            }
            
            grouped_lessons[section_index][1].append(card_data)
        
        self._add_tabs_with_lessons(course_name, grouped_lessons)
    
    def _add_tabs_with_lessons(self, tab_name, sections_data):
        """Add tabs with lessons grouped by sections"""
        tab = QWidget()
        tab.setObjectName(tab_name)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        scroll_layout.setSpacing(15)
        
        for section_title, lessons_data in sections_data:
            section = self._create_section(section_title, lessons_data)
            scroll_layout.addWidget(section)
        
        scroll_area.setWidget(scroll_widget)
        
        tab_layout = QVBoxLayout(tab)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll_area)
        
        self.tabWidget_3.addTab(tab, tab_name)
    
    def _create_section(self, section_title="Розділ", cards_data=None):
        """Create a section with lesson cards"""
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)
        
        section_label = QLabel(section_title)
        section_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        section_layout.addWidget(section_label)
        
        cards_container = QWidget()
        cards_layout = QHBoxLayout(cards_container)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(10)
        cards_layout.setAlignment(Qt.AlignLeft)
        
        if cards_data:
            for card_info in cards_data:
                card = self._create_card(
                    title_text=card_info["title"],
                    labels_text=card_info["labels"],
                    desc_text=card_info["description"],
                    lesson_id=card_info["lesson_id"],
                    completed=card_info.get("completed", False)
                )
                cards_layout.addWidget(card)
        
        # Додаємо проміжок для розміщення останньої картки
        spacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        cards_layout.addItem(spacer)
        
        section_layout.addWidget(cards_container)
        return section_widget
    
    def _create_card(self, title_text="Назва", labels_text=("TextLabel1", "TextLabel2"), desc_text="Опис", lesson_id=None, completed=False):
        """Create a lesson card widget"""
        card = QtWidgets.QWidget()
        card.setMinimumSize(QtCore.QSize(360, 330))
        card.setMaximumSize(QtCore.QSize(360, 330))
        card.setStyleSheet("QWidget { border-radius: 25px; border: 2px solid #e6e6e6; background-color: rgb(255, 255, 255); }")
        card_layout = QtWidgets.QVBoxLayout(card)
    
        title = QtWidgets.QLabel(title_text)
        title.setStyleSheet("font: 75 14pt 'MS Shell Dlg 2';border-color: rgb(255, 255, 255);")
        # Мітки 
        labels = QtWidgets.QHBoxLayout()
        for text in labels_text:
            lb_subject = QtWidgets.QLabel(text)
            lb_subject.setStyleSheet("border-radius: 25px; background-color: #bbebee; border: 2px solid #bbebee;")
            lb_subject.setMinimumSize(QtCore.QSize(165, 50))
            lb_subject.setMaximumSize(QtCore.QSize(165, 50))
            labels.addWidget(lb_subject)
        
        lb_description = QtWidgets.QLabel(desc_text)
        lb_description.setStyleSheet("font: 75 10pt 'MS Shell Dlg 2';border-color: rgb(255, 255, 255);")
        
        stacked_widget = QtWidgets.QStackedWidget()
        stacked_widget.setMaximumSize(QtCore.QSize(16777215, 75))
        stacked_widget.setStyleSheet("border-color: rgb(255, 255, 255);")

        # Сторінка для нових уроків
        page_start = QtWidgets.QWidget()
        layout_start = QtWidgets.QGridLayout(page_start)

        btn_start = QtWidgets.QPushButton("Почати урок")
        btn_start.setMinimumSize(QtCore.QSize(310, 50))
        btn_start.setStyleSheet("border-radius:25px; background: #516ed9; font: 75 15pt 'Bahnschrift'; color: white;")
        
        layout_start.addWidget(btn_start, 0, 0, 1, 1)
        page_start.setLayout(layout_start)

        page_continue = QtWidgets.QWidget()
        layout_continue = QtWidgets.QGridLayout(page_continue)

        # Якщо урок завершено, показуємо кнопку "Завершено", інакше "Продовжити"
        btn_text = "Завершено" if completed else "Продовжити"
        btn_continue = QtWidgets.QPushButton(btn_text)
        btn_continue.setMinimumSize(QtCore.QSize(310, 50))
        btn_continue.setStyleSheet("border-radius:25px; background: #516ed9; font: 75 15pt 'Bahnschrift'; color: white;")

        progress_bar = QtWidgets.QProgressBar()
        progress_bar.setMinimumSize(QtCore.QSize(310, 20))
        progress_bar.setStyleSheet("QProgressBar {border-radius: 8px;background-color: #f3f3f3;}")
        progress_bar.setMaximum(100)
        progress_bar.setValue(100 if completed else 10)
        
        layout_continue.setContentsMargins(0, 0, 0, 0)
        layout_continue.addWidget(btn_continue, 0, 0, 1, 1)
        layout_continue.addWidget(progress_bar, 1, 0, 1, 1)
        page_continue.setLayout(layout_continue)

        stacked_widget.addWidget(page_start)
        stacked_widget.addWidget(page_continue)

        # Якщо урок вже завершено, показуємо сторінку продовження за замовчуванням
        if completed:
            stacked_widget.setCurrentWidget(page_continue)

        # Підключаємо дії кнопок
        def switch_to_continue():
                stacked_widget.setCurrentWidget(page_continue)

        def open_lesson_page():
            # Зберігаємо lesson_id
            lesson_data = {"id": lesson_id, "title": title_text}
            
            if self.pg_lesson and self.stack:
                if hasattr(self.pg_lesson, 'set_lesson_data'):
                    self.pg_lesson.set_lesson_data(lesson_data)
                self.stack.setCurrentWidget(self.pg_lesson)
            else:
                # Створюємо нову сторінку уроку, якщо потрібно
                lesson_page = Lesson_page(lesson_id=lesson_id)
                if self.stack:
                    self.stack.addWidget(lesson_page)
                    self.stack.setCurrentWidget(lesson_page)

        # Підключаємо кнопки
        btn_start.clicked.connect(switch_to_continue)
        btn_start.clicked.connect(open_lesson_page)
        btn_continue.clicked.connect(open_lesson_page)

        card_layout.addWidget(title)
        card_layout.addLayout(labels)
        card_layout.addWidget(lb_description)
        card_layout.addWidget(stacked_widget)
        
        return card

    def _show_not_logged_in_message(self):
        """Show a message when user is not logged in"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        label = QLabel("Будь ласка, увійдіть в систему, щоб побачити свої уроки")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.tabWidget_3.addTab(tab, "Вхід не виконано")
    
    def _show_no_courses_message(self):
        """Show a message when there are no courses"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        label = QLabel("Немає доступних курсів")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.tabWidget_3.addTab(tab, "Немає курсів")
    
    def refresh_content(self):
        """Refresh the page content"""
        self._load_recent_courses()