from PyQt5.QtWidgets import QWidget, QScrollArea,QGridLayout,QVBoxLayout, QLabel,QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QDrag,QPixmap,QIcon
from graphs import *
from tasks import *
import os

class LessonItem(QWidget):
    def __init__(self, title, duration, status="incomplete"):
        super().__init__()
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("background-color: transparent; font: normal 11pt \"MS Shell Dlg 2\";")
        duration_label = QLabel(duration)
        duration_label.setStyleSheet("color: gray; background-color: transparent; font: normal 10pt \"MS Shell Dlg 2\";")
        text_layout = QVBoxLayout()
        text_layout.addWidget(self.title_label)
        text_layout.addWidget(duration_label)
        check_label = QLabel()
        check_label.setFixedWidth(30)
        check_label.setAlignment(Qt.AlignCenter)
        check_label.setStyleSheet("background-color: transparent;")

        if status == "done":
            check_label.setFixedSize(30, 30)
            check_label.setPixmap(QPixmap("blue_icon/check_mark.PNG").scaled(check_label.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation))
        else:
            check_label.setText("")

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(text_layout)
        main_layout.addStretch()
        main_layout.addWidget(check_label)
        main_layout.setContentsMargins(10, 5, 10, 5)

        self.setLayout(main_layout)

        # Залежний від статусу фон
        bg_color = {
            "done": "#e0ffe0",     
            "active": "#e6f0ff",    
            "incomplete": "#ffffff" 
        }.get(status, "#ffffff")

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                padding: 6px;
                border-radius: 8px;
            }}
            QLabel {{
                background-color: transparent;
            }}
            QWidget:hover {{
                background-color: #dcdcdc;
            }}
        """)

class Lesson_page(QWidget):
    def __init__(self):
        super().__init__()
        
        # Store the current lesson ID and data
        self.current_lesson_id = None
        self.parent_lessons_page = None
        self.parent_stack = None
        
        # Initialize services
        from src.services.lesson_service import LessonService
        from src.services.progress_service import ProgressService
        self.lesson_service = LessonService()
        self.progress_service = ProgressService()
        
        # Create main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.main_layout)
        
        # Continue with the rest of the UI
        self.pg_lesson = QtWidgets.QWidget()
        self.pg_lesson.setObjectName("pg_lesson")
        
        self.main_grid_layout = QtWidgets.QGridLayout(self.pg_lesson)
        self.main_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.main_grid_layout.setObjectName("main_grid_layout")
        
        # Add the lesson page to the main layout
        self.main_layout.addWidget(self.pg_lesson)
        
        self.main_scroll_area = QtWidgets.QScrollArea(self.pg_lesson)
        self.main_scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.main_scroll_area.setWidgetResizable(True)
        self.main_scroll_area.setObjectName("main_scroll_area")
        self.main_scroll_content = QtWidgets.QWidget()

        self.main_scroll_content.setMinimumSize(QtCore.QSize(1399, 746))
        self.main_scroll_content.setMaximumSize(QtCore.QSize(2000, 2000))

        self.main_scroll_content.setObjectName("main_scroll_content")
        self.main_content_layout = QtWidgets.QGridLayout(self.main_scroll_content)
        self.main_content_layout.setObjectName("main_content_layout")
        
        self.main_content_layout.setColumnStretch(0, 3)
        
        self.progress_section_widget = QtWidgets.QWidget(self.main_scroll_content)
        self.progress_section_widget.setMaximumSize(QtCore.QSize(400, 200))
        self.progress_section_widget.setProperty("type","w_pg")
        self.progress_section_widget.setObjectName("progress_section_widget")
        self.progress_layout = QtWidgets.QGridLayout(self.progress_section_widget)
        self.progress_layout.setContentsMargins(-1, 25, -1, 25)
        self.progress_layout.setObjectName("progress_layout")
        
        self.course_title_lb = QtWidgets.QLabel(self.progress_section_widget)
        self.course_title_lb.setObjectName("course_title_lb")
        self.course_title_lb.setProperty("type","page_section")
        self.progress_layout.addWidget(self.course_title_lb, 0, 0, 1, 1)
        
        self.lesson_progress_bar = QtWidgets.QProgressBar(self.progress_section_widget)
        self.lesson_progress_bar.setMinimumSize(QtCore.QSize(0, 25))
        self.lesson_progress_bar.setProperty("value", 24)
        self.lesson_progress_bar.setObjectName("lesson_progress_bar")
        self.progress_layout.addWidget(self.lesson_progress_bar, 1, 0, 1, 1)
        self.main_content_layout.addWidget(self.progress_section_widget, 1, 1, 1, 1)
        
        self.lesson_title_lb = QtWidgets.QLabel(self.main_scroll_content)
        self.lesson_title_lb.setProperty("type", "title")
        self.lesson_title_lb.setMinimumSize(QtCore.QSize(1000, 50))
        self.lesson_title_lb.setMaximumSize(QtCore.QSize(16777215, 100))
        self.lesson_title_lb.setObjectName("lesson_title_lb")
        self.main_content_layout.addWidget(self.lesson_title_lb, 1, 0, 2, 1)
        
        self.lessons_list_scroll_area = QtWidgets.QScrollArea(self.main_scroll_content)
        self.lessons_list_scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lessons_list_scroll_area.setWidgetResizable(True)
        self.lessons_list_scroll_area.setObjectName("lessons_list_scroll_area")
        
        self.lessons_list_scroll_content = QtWidgets.QWidget()
        self.lessons_list_scroll_content.setMaximumSize(QtCore.QSize(400, 16777215))
        self.lessons_list_scroll_content.setGeometry(QtCore.QRect(0, 0, 570, 498))
        self.lessons_list_scroll_content.setObjectName("lessons_list_scroll_content")

        self.lessons_list_scroll_layout = QtWidgets.QGridLayout(self.lessons_list_scroll_content)
        self.lessons_list_scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.lessons_list_scroll_content.setMaximumSize(QtCore.QSize(400, 16777215))
        self.lessons_list_scroll_layout.setObjectName("lessons_list_scroll_layout")

        self.lessons_list_container = QtWidgets.QWidget(self.lessons_list_scroll_content)
        self.lessons_list_container.setProperty("type","w_pg")
        self.lessons_list_container.setObjectName("lessons_list_container")
        
        self.lessons_list_layout = QtWidgets.QGridLayout(self.lessons_list_container)
        self.lessons_list_layout.setContentsMargins(11, -1, -1, -1)
        self.lessons_list_layout.setObjectName("lessons_list_layout")
        
        self.list_widget = QtWidgets.QListWidget()
        self.lessons_list_layout.addWidget(self.list_widget, 0, 0, 1, 1)
        
        self.lessons_list_scroll_layout.addWidget(self.lessons_list_container, 0, 0, 1, 1)
        self.lessons_list_scroll_area.setWidget(self.lessons_list_scroll_content)
        self.main_content_layout.addWidget(self.lessons_list_scroll_area, 2, 1, 3, 1)
        
        self.task_section_scroll_area = QtWidgets.QScrollArea(self.main_scroll_content)
        self.task_section_scroll_area.setMinimumSize(QtCore.QSize(1000, 0))
        self.task_section_scroll_area.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.task_section_scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.task_section_scroll_area.setWidgetResizable(True)
        self.task_section_scroll_area.setObjectName("task_section_scroll_area")
        
        self.scroll_task_section_content = QtWidgets.QWidget()
        self.scroll_task_section_content.setGeometry(QtCore.QRect(0, 0, 800, 290))
        self.scroll_task_section_content.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scroll_task_section_content.setMinimumSize(QtCore.QSize(1000, 0))
        self.scroll_task_section_content.setObjectName("scroll_task_section_content")
        
        self.task_scroll_layout = QtWidgets.QGridLayout(self.scroll_task_section_content)
        self.task_scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.task_scroll_layout.setObjectName("task_scroll_layout")
        
        self.tab_container_widget = QtWidgets.QWidget()
        self.tab_container_widget.setMinimumSize(QtCore.QSize(1000, 290))
        self.tab_container_widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tab_container_widget.setProperty("type","w_pg")
        self.tab_container_widget.setObjectName("tab_container_widget")
        
        self.task_tabs_layout = QtWidgets.QGridLayout(self.tab_container_widget)
        self.task_tabs_layout.setObjectName("task_tabs_layout")
        
        self.task_tabs = QtWidgets.QTabWidget(self.tab_container_widget)
        self.task_tabs.setMinimumSize(QtCore.QSize(1000, 290))
        self.task_tabs.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.task_tabs.setObjectName("task_tabs")
        
        # Create tabs for different content types
        self.theory_tab = QtWidgets.QWidget()
        self.theory_tab.setObjectName("theory_tab")
        self.theory_layout = QtWidgets.QVBoxLayout(self.theory_tab)
        self.lesson_text = QtWidgets.QTextBrowser()
        self.lesson_text.setOpenExternalLinks(True)
        self.theory_layout.addWidget(self.lesson_text)
        
        # Create exercises tab
        self.exercises_tab = QtWidgets.QWidget()
        self.exercises_tab.setObjectName("exercises_tab")
        self.exercises_layout = QtWidgets.QVBoxLayout(self.exercises_tab)
        self.exercises_container = QtWidgets.QWidget()
        self.exercises_container_layout = QtWidgets.QVBoxLayout(self.exercises_container)
        self.exercises_layout.addWidget(self.exercises_container)
        
        # Create practice tab
        self.practice_tab = QtWidgets.QWidget()
        self.practice_tab.setObjectName("practice_tab")
        self.practice_layout = QtWidgets.QVBoxLayout(self.practice_tab)
        
        # Add tabs to the tab widget
        self.task_tabs.addTab(self.theory_tab, "Теорія")
        self.task_tabs.addTab(self.exercises_tab, "Вправи")
        self.task_tabs.addTab(self.practice_tab, "Практика")
        
        self.task_tabs_layout.addWidget(self.task_tabs, 0, 0, 1, 1)
        self.task_scroll_layout.addWidget(self.tab_container_widget, 0, 0, 1, 1)
        self.task_section_scroll_area.setWidget(self.scroll_task_section_content)
        self.main_content_layout.addWidget(self.task_section_scroll_area, 3, 0, 1, 1)
        
        # Add tools and navigation widget
        self.backButton = QtWidgets.QPushButton("Назад до уроків")
        self.backButton.setProperty("type", "start_continue")
        self.backButton.setFixedWidth(150)
        self.backButton.setMinimumHeight(40)
        self.backButton.setStyleSheet("""
            QPushButton {
                border-radius: 20px !important;
                border: none;
            }
        """)
        self.backButton.clicked.connect(self.go_back_to_lessons)
        
        # Create tools widget
        self.tools_widget = QtWidgets.QWidget()
        tools_layout = QtWidgets.QHBoxLayout(self.tools_widget)
        tools_layout.addWidget(self.backButton)
        
        # Progress widget instead of complete button
        self.progress_widget = QtWidgets.QWidget()
        self.progress_widget.setProperty("type", "w_pg")
        progress_layout = QtWidgets.QVBoxLayout(self.progress_widget)
        
        # Progress labels
        self.progress_status = QtWidgets.QLabel("Прогрес: 0%")
        self.progress_status.setProperty("type", "lb_description")
        progress_layout.addWidget(self.progress_status)
        
        # Progress bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        
        # Complete Lesson button
        self.complete_button = QtWidgets.QPushButton("Завершити урок")
        self.complete_button.setProperty("type", "start_continue")
        self.complete_button.setMinimumHeight(40)
        self.complete_button.setStyleSheet("""
            QPushButton {
                border-radius: 20px !important;
                border: none;
            }
        """)
        self.complete_button.clicked.connect(self.manual_complete_lesson)
        progress_layout.addWidget(self.complete_button)
        
        # Info container
        info_container = QtWidgets.QWidget()
        info_layout = QtWidgets.QHBoxLayout(info_container)
        info_layout.setContentsMargins(0, 0, 0, 0)
        
        # Lesson metadata
        self.lb_difficulty = QtWidgets.QLabel("Складність: Базовий")
        self.lb_difficulty.setProperty("type", "lb_description")
        info_layout.addWidget(self.lb_difficulty)
        
        self.lb_time = QtWidgets.QLabel("Час: ~30 хв")
        self.lb_time.setProperty("type", "lb_description")
        info_layout.addWidget(self.lb_time)
        
        progress_layout.addWidget(info_container)
        
        # Create a header container for tools
        self.header_container = QtWidgets.QWidget(self.main_scroll_content)
        self.header_container.setMaximumHeight(100)
        self.header_container.setMinimumHeight(80)
        header_layout = QtWidgets.QHBoxLayout(self.header_container)
        header_layout.setContentsMargins(10, 10, 10, 10)
        header_layout.addWidget(self.tools_widget)
        header_layout.setAlignment(self.tools_widget, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        # Add the header container
        self.main_content_layout.addWidget(self.header_container, 0, 0, 1, 2)
        self.main_content_layout.addWidget(self.progress_widget, 4, 0, 1, 1)
        
        self.main_scroll_area.setWidget(self.main_scroll_content)
        
        self.main_grid_layout.addWidget(self.main_scroll_area, 0, 0, 1, 1)
        
        # Connect signals
        self.task_tabs.currentChanged.connect(self.update_progress)
        
        # Exercise completion counter
        self.completed_exercises = 0
        self.total_exercises = 0

    def createScrollableTab(self, inner_widget):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(inner_widget)
        inner_widget.setProperty("type", "w_pg")
        return scroll_area

    def set_lesson_data(self, title, lesson_id=None):
        """Set the lesson data based on the lesson ID"""
        # Update the lesson title
        self.lesson_title_lb.setText(title)
        self.current_lesson_id = lesson_id
        
        # Reset UI elements
        self.list_widget.clear()
        self.exercises_container_layout.removeWidget(self.exercises_container)
        
        # Reset exercise counters
        self.completed_exercises = 0
        self.total_exercises = 0
        
        if lesson_id:
            print(f"Loading lesson data for ID: {lesson_id}")
            try:
                # Load the real lesson from database 
                lesson = self.lesson_service.get_lesson_by_id(lesson_id)
                
                if lesson:
                    # Set real lesson data
                    self.lesson_title_lb.setText(lesson.title)
                    
                    # Get course information to display in progress section
                    course = lesson.course if hasattr(lesson, 'course') else None
                    if course:
                        self.course_title_lb.setText(f"Course: {course.name}")
                    
                    # Check if the user has completed this lesson
                    user_completed = False
                    try:
                        from src.services.session_manager import SessionManager
                        session_manager = SessionManager()
                        user_data = session_manager.get_current_user_data()
                        
                        if user_data and 'id' in user_data:
                            user_id = user_data['id']
                            user_completed = self.progress_service.has_completed_lesson(user_id, lesson_id)
                    except Exception as e:
                        print(f"Error checking lesson completion: {str(e)}")
                    
                    # If user already completed this lesson, show full progress
                    if user_completed:
                        self.progress_bar.setValue(100)
                        self.progress_status.setText("Прогрес: 100%")
                        self.complete_button.setText("Урок завершено ✓")
                        self.complete_button.setEnabled(False)
                    else:
                        # Set initial progress value
                        self.progress_bar.setValue(0)
                        self.progress_status.setText("Прогрес: 0%")
                        self.complete_button.setText("Завершити урок")
                        self.complete_button.setEnabled(True)
                    
                    # Create theory content HTML
                    content_html = f"<h2>{lesson.title}</h2>"
                    
                    # Add more content details if available 
                    if hasattr(lesson, 'description') and lesson.description:
                        content_html += f"<p>{lesson.description}</p>"
                    else:
                        content_html += "<p>Цей урок проведе вас через важливі концепції та вправи.</p>"
                    
                    # Add lesson-specific theory content
                    lesson_number = lesson.lesson_order if hasattr(lesson, 'lesson_order') else 1
                    
                    if lesson_number == 1:
                        content_html += """
                        <h3>Введення до концепцій</h3>
                        <p>У цьому уроці ми вивчимо фундаментальні концепції, які формують основу цього предмета.</p>
                        <p>Ключові моменти для розуміння:</p>
                        <ul>
                            <li>Основні визначення та властивості</li>
                            <li>Головні принципи та застосування</li>
                            <li>Підходи до вирішення задач</li>
                        </ul>
                        <p>Почнемо з вивчення основ...</p>
                        <h4>Головні принципи</h4>
                        <p>Головний принцип, який ми повинні зрозуміти, - це як різні елементи взаємодіють один з одним.</p>
                        <p>Коли ми вивчаємо ці взаємодії, ми відкриваємо шаблони, які допомагають нам передбачати результати та вирішувати проблеми.</p>
                        """
                    elif lesson_number == 2:
                        content_html += """
                        <h3>Розширені застосування</h3>
                        <p>Тепер, коли ми розуміємо основи, давайте розглянемо більш складні застосування.</p>
                        <p>Ці застосування демонструють, як концепції можна використовувати для вирішення реальних проблем:</p>
                        <ol>
                            <li>Розпізнавання шаблонів у складних системах</li>
                            <li>Методи оптимізації для ефективності</li>
                            <li>Предиктивне моделювання на основі історичних даних</li>
                        </ol>
                        <p>Давайте детально розглянемо кожне з них...</p>
                        """
                    elif lesson_number == 3:
                        content_html += """
                        <h3>Практична реалізація</h3>
                        <p>У цьому заключному розділі ми зосередимося на практичній реалізації того, що ми вивчили.</p>
                        <p>Ключові кроки в реалізації цих концепцій:</p>
                        <ol>
                            <li>Аналіз проблемної області</li>
                            <li>Визначення відповідних технік</li>
                            <li>Систематичне застосування методів</li>
                            <li>Оцінка результатів та ітерація за потреби</li>
                        </ol>
                        <p>Давайте попрактикуємося з деякими реалістичними сценаріями...</p>
                        """
                    else:
                        content_html += """
                        <h3>Вивчення теми</h3>
                        <p>У цьому уроці ми глибше розглянемо спеціалізовані області предмета.</p>
                        <p>Ми розглянемо як теоретичні основи, так і практичні застосування.</p>
                        <p>До кінця уроку ви повинні вміти:</p>
                        <ul>
                            <li>Розуміти складні взаємозв'язки між ключовими концепціями</li>
                            <li>Застосовувати спеціалізовані техніки для вирішення специфічних проблем</li>
                            <li>Оцінювати ефективність різних підходів</li>
                        </ul>
                        """
                        
                    # Render the theory content
                    self.lesson_text.setHtml(content_html)
                    
                    # Set difficulty level
                    difficulty = self._get_difficulty_text(lesson)
                    self.lb_difficulty.setText(f"Складність: {difficulty}")
                    
                    # Set the estimated time
                    if hasattr(lesson, 'estimated_time') and lesson.estimated_time:
                        self.lb_time.setText(f"{lesson.estimated_time} min")
                    
                    # Create exercise content
                    self.generate_exercises(lesson_number)
                    
                    # Add practical content
                    self.generate_practice_content(lesson_number)
                    
                    # Add course lessons to the sidebar list
                    if course and hasattr(course, 'id'):
                        try:
                            # Get all lessons for this course
                            course_lessons = self.lesson_service.get_lessons_by_course_id(str(course.id))
                            
                            # Add each lesson to the list widget
                            for course_lesson in course_lessons:
                                item = QtWidgets.QListWidgetItem()
                                
                                # Check if lesson is completed
                                status = "incomplete"
                                if course_lesson.id == lesson.id:
                                    status = "active"
                                    
                                # Check if lesson is completed in the database
                                try:
                                    from src.services.session_manager import SessionManager
                                    session_manager = SessionManager()
                                    user_data = session_manager.get_current_user_data()
                                    
                                    if user_data and 'id' in user_data:
                                        user_id = user_data['id']
                                        is_completed = self.progress_service.has_completed_lesson(user_id, course_lesson.id)
                                        if is_completed:
                                            status = "done"
                                            # If this is the current lesson, update progress bar
                                            if course_lesson.id == lesson.id:
                                                self.progress_bar.setValue(100)
                                                self.progress_status.setText("Progress: 100%")
                                except Exception as e:
                                    print(f"Error checking lesson completion: {str(e)}")
                                
                                # Format estimated time
                                time_str = f"{course_lesson.estimated_time} min" if hasattr(course_lesson, 'estimated_time') else "~30 min"
                                widget = LessonItem(course_lesson.title, time_str, status)
                                item.setSizeHint(widget.sizeHint())
                                item.setData(QtCore.Qt.UserRole, str(course_lesson.id))  # Store lesson ID
                                self.list_widget.addItem(item)
                                self.list_widget.setItemWidget(item, widget)
                        except Exception as e:
                            print(f"Error loading course lessons: {str(e)}")
                    
                    # Connect the lesson item click handler
                    self.list_widget.itemClicked.connect(self.on_item_click)
                    
                    # Set progress widget and toolbar visibility
                    self.progress_widget.setVisible(True)
                    self.tools_widget.setVisible(True)
                    
                    # Go to the first tab
                    self.task_tabs.setCurrentIndex(0)
                else:
                    # Lesson not found, show error
                    self.lesson_text.setHtml(f"<h2>Урок не знайдено</h2><p>Урок з ID {lesson_id} не вдалося знайти.</p>")
                    self.tools_widget.setVisible(True)
                    self.progress_widget.setVisible(False)
            except Exception as e:
                print(f"Error loading lesson data: {str(e)}")
                self.lesson_text.setHtml(f"<h2>Помилка завантаження уроку</h2><p>Сталася помилка під час завантаження уроку: {str(e)}</p>")
                self.tools_widget.setVisible(True)
                self.progress_widget.setVisible(False)
        else:
            # No lesson ID provided, show placeholder
            self.lesson_text.setHtml(f"<h2>{title}</h2><p>Дані уроку недоступні. Будь ласка, виберіть урок зі сторінки курсу.</p>")
            self.tools_widget.setVisible(False)
            self.progress_widget.setVisible(False)

    def generate_exercises(self, lesson_number):
        """Generate exercise content for the lesson"""
        # Clear existing exercises
        for i in reversed(range(self.exercises_container_layout.count())):
            widget = self.exercises_container_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
                
        self.total_exercises = 5  # We'll create 5 exercises per lesson
        
        # Different exercises based on lesson number
        if lesson_number == 1:
            exercise_data = [
                {"question": "Який головний принцип розглядається в цьому уроці?", 
                 "options": ["Взаємодія елементів", "Статистичний аналіз", "Квантова теорія", "Економічні моделі"],
                 "correct": 0},
                {"question": "Який із цих пунктів НЕ згадується як ключовий у уроці?", 
                 "options": ["Основні визначення", "Головні принципи", "Підходи до вирішення задач", "Історичний контекст"],
                 "correct": 3},
                {"question": "Згідно з уроком, що допомагає нам передбачати результати?", 
                 "options": ["Випадковий вибір", "Розпізнавання шаблонів", "Комп'ютерні алгоритми", "Особиста інтуїція"],
                 "correct": 1},
                {"question": "Скільки основних пунктів перераховано у вступі?", 
                 "options": ["2", "3", "4", "5"],
                 "correct": 1},
                {"question": "Що є головним фокусом цього уроку?", 
                 "options": ["Розширені додатки", "Практична реалізація", "Вступ до концепцій", "Історичний розвиток"],
                 "correct": 2}
            ]
        elif lesson_number == 2:
            exercise_data = [
                {"question": "Що є основним фокусом цього уроку?", 
                 "options": ["Основні концепції", "Розширені застосування", "Історичний розвиток", "Майбутні прогнози"],
                 "correct": 1},
                {"question": "Скільки застосувань конкретно перераховано в уроці?", 
                 "options": ["2", "3", "4", "5"],
                 "correct": 1},
                {"question": "Який із цих пунктів НЕ згадується як застосування у уроці?", 
                 "options": ["Розпізнавання шаблонів", "Методи оптимізації", "Предиктивне моделювання", "Розподіл ресурсів"],
                 "correct": 3},
                {"question": "Який тип даних згадується для предиктивного моделювання?", 
                 "options": ["Майбутні дані", "Дані реального часу", "Історичні дані", "Симульовані дані"],
                 "correct": 2},
                {"question": "Які типи систем згадуються у зв'язку з розпізнаванням шаблонів?", 
                 "options": ["Прості системи", "Складні системи", "Лінійні системи", "Закриті системи"],
                 "correct": 1}
            ]
        else:
            exercise_data = [
                {"question": "Що є головним фокусом цього уроку?", 
                 "options": ["Теоретичні основи", "Історичний контекст", "Практична реалізація", "Майбутні розробки"],
                 "correct": 2},
                {"question": "Скільки ключових кроків перераховано для реалізації?", 
                 "options": ["2", "3", "4", "5"],
                 "correct": 2},
                {"question": "Який крок іде першим в процесі реалізації?", 
                 "options": ["Застосування методів", "Оцінка результатів", "Визначення технік", "Аналіз проблемної області"],
                 "correct": 3},
                {"question": "Який останній крок в процесі реалізації?", 
                 "options": ["Аналіз проблеми", "Оцінка результатів", "Застосування методів", "Визначення технік"],
                 "correct": 1},
                {"question": "Відповідно до уроку, що потрібно робити після оцінки результатів?", 
                 "options": ["Розпочати новий проект", "Документувати результати", "Ітерувати за необхідністю", "Представити висновки"],
                 "correct": 2}
            ]
            
        # Create exercise widgets
        for i, exercise in enumerate(exercise_data):
            exercise_widget = QtWidgets.QGroupBox(f"Вправа {i+1}")
            exercise_layout = QtWidgets.QVBoxLayout(exercise_widget)
            
            # Question label
            question_label = QtWidgets.QLabel(exercise["question"])
            question_label.setWordWrap(True)
            question_label.setProperty("type", "lb_name_lesson")
            exercise_layout.addWidget(question_label)
            
            # Radio button group for options
            option_group = QtWidgets.QButtonGroup(exercise_widget)
            
            for j, option_text in enumerate(exercise["options"]):
                option = QtWidgets.QRadioButton(option_text)
                option_group.addButton(option, j)
                exercise_layout.addWidget(option)
                
            # Check answer button
            check_button = QtWidgets.QPushButton("Перевірити відповідь")
            check_button.setProperty("type", "start_continue")
            
            # Store the correct answer index
            check_button.setProperty("correct_answer", exercise["correct"])
            check_button.setProperty("exercise_index", i)
            
            # Result label
            result_label = QtWidgets.QLabel("")
            result_label.setVisible(False)
            
            exercise_layout.addWidget(check_button)
            exercise_layout.addWidget(result_label)
            
            # Connect button to check function
            check_button.clicked.connect(lambda checked, btn=check_button, group=option_group, label=result_label: 
                                        self.check_exercise_answer(btn, group, label))
            
            self.exercises_container_layout.addWidget(exercise_widget)
    
    def generate_practice_content(self, lesson_number):
        """Generate practice content for the lesson"""
        # Clear the practice tab
        for i in reversed(range(self.practice_layout.count())):
            widget = self.practice_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
                
        # Create different practice content based on lesson number
        practice_html = f"<h2>Практичні завдання</h2>"
        
        if lesson_number == 1:
            practice_html += """
            <h3>Інтерактивна вправа</h3>
            <p>Спробуйте вирішити ці задачі самостійно для практики:</p>
            <div style="background-color: #f5f5f5; padding: 10px; border-left: 4px solid #007bff;">
                <p><strong>Сценарій:</strong> Ви аналізуєте набір даних взаємодій клієнтів із веб-сайтом. 
                Ваше завдання — визначити шаблони, які могли б передбачити поведінку клієнтів.</p>
                
                <p><strong>Подумайте про:</strong></p>
                <ol>
                    <li>Які шаблони ви могли б шукати в даних?</li>
                    <li>Як кожен шаблон може бути використаний для прогнозування майбутньої поведінки?</li>
                    <li>Як би ви перевірили свої прогнози?</li>
                </ol>
            </div>
            
            <h3>Точки для роздумів</h3>
            <p>Розгляньте ці питання під час навчання:</p>
            <ol>
                <li>Як концепції з цього уроку пов'язані з вашим власним досвідом?</li>
                <li>З якими викликами ви можете зіткнутися при застосуванні цих концепцій?</li>
                <li>Яка додаткова інформація допомогла б вам краще зрозуміти ці концепції?</li>
            </ol>
            """
        elif lesson_number == 2:
            practice_html += """
            <h3>Розбір практичного випадку</h3>
            <p>Розгляньте цей випадок і подумайте над питаннями:</p>
            <div style="background-color: #f5f5f5; padding: 10px; border-left: 4px solid #007bff;">
                <p><strong>Практичний випадок:</strong> Транспортна компанія намагається оптимізувати свої маршрути доставки для мінімізації витрат палива та часу доставки.</p>
                
                <p><strong>Питання для розгляду:</strong></p>
                <ol>
                    <li>Які методи оптимізації з уроку були б найбільш застосовними?</li>
                    <li>Які дані вам потрібно було б зібрати для впровадження вашого рішення?</li>
                    <li>Як би ви вимірювали успіх ваших зусиль з оптимізації?</li>
                    <li>З якими викликами ви можете зіткнутися під час впровадження?</li>
                </ol>
            </div>
            
            <h3>Інтерактивна симуляція</h3>
            <p>Досліджуйте ці концепції за допомогою інтерактивної симуляції:</p>
            <div style="background-color: #e6f7ff; padding: 10px; border-left: 4px solid #0099cc;">
                <p>Відвідайте <a href="https://phet.colorado.edu/en/simulations/category/math">PhET Math Simulations</a> для інтерактивних моделей, пов'язаних з цією темою.</p>
                <p>Ці симуляції дозволяють експериментувати з концепціями та бачити негайні результати без необхідності оцінювання.</p>
            </div>
            """
        else:
            practice_html += """
            <h3>Практичний проект</h3>
            <p>Завершіть цей міні-проект, щоб застосувати свої знання:</p>
            <div style="background-color: #f5f5f5; padding: 10px; border-left: 4px solid #007bff;">
                <p><strong>Проектне завдання:</strong> Вам потрібно впровадити найпростіший варіант системи, використовуючи принципи з цього уроку.</p>
                
                <p><strong>Кроки:</strong></p>
                <ol>
                    <li>Визначте основні компоненти системи.</li>
                    <li>Окресліть, як ці компоненти будуть взаємодіяти.</li>
                    <li>Розгляньте потенційні виклики та обмеження.</li>
                    <li>Опишіть, як ви будете тестувати та оцінювати рішення.</li>
                </ol>
                
                <p><strong>Примітка:</strong> Сконцентруйтеся на розробці документа прототипу, а не на повній реалізації.</p>
            </div>
            
            <h3>Групове обговорення</h3>
            <p>Ці питання найкраще обговорювати в групі:</p>
            <ol>
                <li>Як відрізняються підходи до впровадження залежно від масштабу та комплексності проблеми?</li>
                <li>Які інструменти та технології найефективніші для різних типів впровадження?</li>
                <li>Як би ви підготувалися до потенційних викликів під час процесу впровадження?</li>
            </ol>
            """
            
        # Create a QTextBrowser for the practice content
        practice_browser = QtWidgets.QTextBrowser()
        practice_browser.setHtml(practice_html)
        
        # Complete button for practice
        self.practice_complete_button = QtWidgets.QPushButton("Завершити практику")
        self.practice_complete_button.setProperty("type", "start_continue")
        self.practice_complete_button.clicked.connect(self.complete_practice_section)
        
        # Add widgets to the practice tab
        self.practice_layout.addWidget(practice_browser)
        self.practice_layout.addWidget(self.practice_complete_button)
    
    def check_exercise_answer(self, button, option_group, result_label):
        """Check if the selected exercise answer is correct"""
        selected_button = option_group.checkedButton()
        correct_answer = button.property("correct_answer")
        
        if selected_button:
            selected_id = option_group.id(selected_button)
            if selected_id == correct_answer:
                result_label.setText("✓ Правильно!")
                result_label.setStyleSheet("color: green;")
            else:
                result_label.setText("✗ Неправильно, спробуйте ще раз.")
                result_label.setStyleSheet("color: red;")
            result_label.setVisible(True)
            
            # Update progress on correct answer
            if selected_id == correct_answer:
                # Update tab progress
                self.update_progress(tab_index=1)  # Index 1 is the Exercises tab
                
                # Check if all exercises are correct to auto-complete
                self.check_all_exercises_completed()
    
    def complete_practice_section(self):
        """Mark the practice section as completed"""
        # Update progress for practice tab
        self.update_progress(tab_index=2)  # Index 2 is the Practice tab
        
        # Update button
        self.practice_complete_button.setText("Практику завершено ✓")
        self.practice_complete_button.setEnabled(False)
        
        # Check if all sections are completed to mark the lesson as completed
        self.check_lesson_completion()
    
    def update_progress(self, tab_index=None):
        """Update progress based on completed exercises and tabs visited"""
        # Calculate progress percentage based on exercises completed and tabs visited
        tab_count = self.task_tabs.count()
        tabs_visited = set()
        
        # If tab_index is provided, add it to visited tabs
        if tab_index is not None:
            tabs_visited.add(tab_index)
            
        # Calculate progress
        exercise_weight = 0.6  # Exercises count for 60% of progress
        tab_weight = 0.4  # Visiting tabs counts for 40% of progress
        
        # Exercise progress (what percentage of exercises are completed)
        exercise_progress = 0
        if self.total_exercises > 0:
            exercise_progress = (self.completed_exercises / self.total_exercises) * 100
            
        # Tab progress (what percentage of tabs have been visited)
        tab_progress = (len(tabs_visited) / tab_count) * 100
        
        # Total progress
        total_progress = int((exercise_progress * exercise_weight) + (tab_progress * tab_weight))
        
        # Update UI
        self.progress_bar.setValue(total_progress)
        self.progress_status.setText(f"Прогрес: {total_progress}%")
        
        # If progress is 100%, mark the lesson as complete in the database
        if total_progress >= 100 and self.current_lesson_id:
            self.auto_complete_lesson()
    
    def auto_complete_lesson(self):
        """Automatically complete the lesson when all requirements are met"""
        if not self.current_lesson_id:
            return
            
        try:
            # Get the current user ID from session
            from src.services.session_manager import SessionManager
            session_manager = SessionManager()
            user_data = session_manager.get_current_user_data()
            
            if not user_data or 'id' not in user_data:
                return
                
            user_id = user_data['id']
            
            # Get lesson details
            lesson = self.lesson_service.get_lesson_by_id(self.current_lesson_id)
            if not lesson:
                return
                
            # Check if already completed
            is_completed = self.progress_service.has_completed_lesson(user_id, self.current_lesson_id)
            if is_completed:
                return
                
            # Mark the lesson as complete
            result = self.progress_service.complete_lesson(
                user_id=user_id,
                lesson_id=self.current_lesson_id,
                course_id=lesson.course_id,
                time_spent=30  # Default to 30 minutes
            )
            
            if result:
                # Update lesson list items to show this lesson as completed
                for i in range(self.list_widget.count()):
                    item = self.list_widget.item(i)
                    item_lesson_id = item.data(QtCore.Qt.UserRole)
                    
                    if item_lesson_id == self.current_lesson_id:
                        # Update the UI to show this lesson as completed
                        widget = self.list_widget.itemWidget(item)
                        time_str = f"{lesson.estimated_time} min" if hasattr(lesson, 'estimated_time') else "~30 min"
                        new_widget = LessonItem(widget.title_label.text(), time_str, "done")
                        item.setSizeHint(new_widget.sizeHint())
                        self.list_widget.setItemWidget(item, new_widget)
                        break
                
                # Show success message
                QtWidgets.QMessageBox.information(
                    self, 
                    "Урок завершено", 
                    f"Вітаємо! Ви завершили урок: {lesson.title}"
                )
        except Exception as e:
            print(f"Error completing lesson: {str(e)}")
    
    def manual_complete_lesson(self):
        """Handle the manual completion of a lesson via the complete button"""
        if not self.current_lesson_id:
            QtWidgets.QMessageBox.warning(
                self,
                "Не вибрано урок",
                "Будь ласка, спочатку виберіть урок."
            )
            return
            
        try:
            # Get the current user ID from session
            from src.services.session_manager import SessionManager
            session_manager = SessionManager()
            user_data = session_manager.get_current_user_data()
            
            if not user_data or 'id' not in user_data:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Не виконано вхід",
                    "Вам потрібно увійти в систему, щоб завершувати уроки."
                )
                return
                
            user_id = user_data['id']
            
            # Get lesson details
            lesson = self.lesson_service.get_lesson_by_id(self.current_lesson_id)
            if not lesson:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Урок не знайдено",
                    "Вибраний урок не вдалося знайти."
                )
                return
                
            # Check if already completed
            is_completed = self.progress_service.has_completed_lesson(user_id, self.current_lesson_id)
            if is_completed:
                QtWidgets.QMessageBox.information(
                    self,
                    "Вже завершено",
                    f"Ви вже завершили цей урок: {lesson.title}"
                )
                return
                
            # Ask for confirmation
            reply = QtWidgets.QMessageBox.question(
                self,
                "Завершити урок",
                f"Ви впевнені, що хочете позначити цей урок як завершений: {lesson.title}?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            
            if reply == QtWidgets.QMessageBox.Yes:
                # Mark the lesson as complete
                result = self.progress_service.complete_lesson(
                    user_id=user_id,
                    lesson_id=self.current_lesson_id,
                    course_id=lesson.course_id,
                    time_spent=30  # Default to 30 minutes
                )
                
                if result:
                    # Update the complete button state
                    self.complete_button.setText("Урок завершено ✓")
                    self.complete_button.setEnabled(False)
                    
                    # Update lesson list items to show this lesson as completed
                    for i in range(self.list_widget.count()):
                        item = self.list_widget.item(i)
                        item_lesson_id = item.data(QtCore.Qt.UserRole)
                        
                        if item_lesson_id == self.current_lesson_id:
                            # Update the UI to show this lesson as completed
                            widget = self.list_widget.itemWidget(item)
                            time_str = f"{lesson.estimated_time} min" if hasattr(lesson, 'estimated_time') else "~30 min"
                            new_widget = LessonItem(widget.title_label.text(), time_str, "done")
                            item.setSizeHint(new_widget.sizeHint())
                            self.list_widget.setItemWidget(item, new_widget)
                            break
                    
                    # Update progress bar to 100%
                    self.progress_bar.setValue(100)
                    self.progress_status.setText("Progress: 100%")
                    
                    # Show success message
                    QtWidgets.QMessageBox.information(
                        self, 
                        "Lesson Completed", 
                        f"Congratulations! You've completed the lesson: {lesson.title}"
                    )
                else:
                    # Failed to complete the lesson
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Помилка",
                        "Не вдалося позначити урок як завершений. Будь ласка, спробуйте ще раз."
                    )
        except Exception as e:
            print(f"Error completing lesson: {str(e)}")
            QtWidgets.QMessageBox.warning(
                self,
                "Error",
                f"An error occurred while completing the lesson: {str(e)}"
            )
    
    def _get_difficulty_text(self, lesson):
        """Get a formatted difficulty text from a lesson object
        
        Args:
            lesson: The lesson object
            
        Returns:
            A string representing the difficulty level
        """
        if not hasattr(lesson, 'difficulty_level'):
            return "Basic"  # Default
            
        difficulty = lesson.difficulty_level
        if difficulty is None:
            return "Базовий"
            
        # Handle if it's an enum
        if hasattr(difficulty, 'value'):
            difficulty_value = difficulty.value
            if difficulty_value == "Базовий":
                return "Базовий"
            elif difficulty_value == "Середній":
                return "Середній"
            elif difficulty_value == "Досвідчений":
                return "Досвідчений"
            elif difficulty_value == "Basic":
                return "Базовий"
            elif difficulty_value == "Medium":
                return "Середній"
            elif difficulty_value == "Advanced":
                return "Досвідчений"
            return difficulty_value
            
        # Handle if it's a string
        difficulty_str = str(difficulty)
        if difficulty_str.lower() in ["basic", "beginner", "базовий"]:
            return "Базовий"
        elif difficulty_str.lower() in ["medium", "intermediate", "середній"]:
            return "Середній"
        elif difficulty_str.lower() in ["advanced", "expert", "досвідчений"]:
            return "Досвідчений"
            
        return difficulty_str
    
    def on_item_click(self, item):
        """Handle lesson item click in the sidebar list"""
        # Get the lesson ID stored in the item
        lesson_id = item.data(QtCore.Qt.UserRole)
        if lesson_id:
            # Get the lesson from the database
            try:
                lesson = self.lesson_service.get_lesson_by_id(lesson_id)
                if lesson:
                    # Update the UI with the selected lesson
                    self.set_lesson_data(lesson.title, lesson_id)
            except Exception as e:
                print(f"Error loading lesson: {str(e)}")
                # Show error in lesson content
                self.lesson_text.setHtml(f"<h2>Error</h2><p>Failed to load lesson: {str(e)}</p>")
        else:
            # No lesson ID available
            widget = self.list_widget.itemWidget(item)
            if widget:
                self.lesson_title_lb.setText(widget.title_label.text())
                self.lesson_text.setHtml(f"<h2>{widget.title_label.text()}</h2><p>No data available for this lesson.</p>")
    
    def set_parent_pages(self, lessons_page=None, stack=None):
        """Set the parent pages for navigation"""
        self.parent_lessons_page = lessons_page
        self.parent_stack = stack
    
    def go_back_to_lessons(self):
        """Navigate back to the lessons list page"""
        if self.parent_stack and self.parent_lessons_page:
            self.parent_stack.setCurrentWidget(self.parent_lessons_page)
        else:
            print("Warning: Cannot navigate back - parent pages not set")
    