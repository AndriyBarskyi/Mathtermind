from PyQt5.QtWidgets import QWidget, QScrollArea,QGridLayout,QVBoxLayout, QLabel,QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QDrag,QPixmap,QIcon
from graphs import *
from tasks import *
from src.services import LessonService, ProgressService, SessionManager, ContentService, CourseService
from src.models.content import TheoryContent, ExerciseContent, AssessmentContent, InteractiveContent
import logging
import markdown

logger = logging.getLogger(__name__)


class LessonItem(QWidget):
    def __init__(self, title, duration, status="incomplete"):
        super().__init__()
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("background-color: transparent;")
        duration_label = QLabel(duration)
        duration_label.setStyleSheet("color: gray; background-color: transparent;")
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
    def __init__(self, lesson_id=None):
        super().__init__()
        
        self.lesson_service = LessonService()
        self.progress_service = ProgressService()
        self.content_service = ContentService()
        self.course_service = CourseService()
        
        self.current_lesson_id = lesson_id
        self.current_lesson = None
        
        self.lesson_data = {}

        self.pg_lesson = QtWidgets.QWidget()
        self.pg_lesson.setObjectName("pg_lesson")
        
        self.main_grid_layout = QtWidgets.QGridLayout(self.pg_lesson)
        self.main_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.main_grid_layout.setObjectName("main_grid_layout")
        
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
        """self.video_widget = QVideoWidget(self.main_scroll_content)
        self.video_widget.setMinimumSize(QtCore.QSize(1000, 350))
        self.video_widget.setMaximumSize(QtCore.QSize(16777215, 350))
        self.video_widget.setProperty("type","w_pg")
        self.video_widget.setObjectName("video_widget")
        self.main_content_layout.addWidget(self.video_widget, 1, 0, 2, 1)"""
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
        
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tab_container_widget.setProperty("type", "w_pg")
        #self.task_tabs.addTab(self.createScrollableTab(task_window.create_theory()), "Теорія")
        #self.task_tabs.addTab(self.createScrollableTab(task_window.create_tasks_tab()),"Всі завдання")

        self.task_tabs_layout.addWidget(self.task_tabs, 0, 0, 1, 1)
        self.task_scroll_layout.addWidget(self.tab_container_widget, 0, 0, 1, 1)
        self.task_section_scroll_area.setWidget(self.scroll_task_section_content)
        self.main_content_layout.addWidget(self.task_section_scroll_area, 4, 0, 1, 1)
        self.title_main_lb = QtWidgets.QLabel(self.main_scroll_content)
        self.title_main_lb.setMinimumSize(QtCore.QSize(1000, 40))
        self.title_main_lb.setMaximumSize(QtCore.QSize(16777215, 40))
        self.title_main_lb.setText("Урок")
        self.title_main_lb.setProperty("type", "title")
        self.title_main_lb.setObjectName("title_main_lb")
        self.main_content_layout.addWidget(self.title_main_lb, 0, 0, 1, 1)
        self.main_scroll_area.setWidget(self.main_scroll_content)
        
        self.main_grid_layout.addWidget(self.main_scroll_area, 0, 0, 1, 1)
        
        self.setLayout(self.main_grid_layout)

        # If lesson_id is provided, load lesson data
        if self.current_lesson_id:
            self.load_lesson(self.current_lesson_id)
        else:
            # Initialize with empty UI
            self._init_lesson_list()

    def _markdown_to_html(self, md_text):
        """Converts Markdown text to HTML."""
        if not md_text:
            return ""
        try:
            # Basic conversion, can be extended with extensions
            html = markdown.markdown(md_text, extensions=['fenced_code', 'tables'])
            return html
        except Exception as e:
            logger.error(f"Error converting markdown to HTML: {e}")
            return md_text # Fallback to original text if conversion fails

    def _init_lesson_list(self):
        """Initialize the lesson list with real data from related lessons."""
        self.list_widget.clear()
        
        try:
            self.list_widget.itemClicked.disconnect(self.on_item_click)
        except TypeError:
            pass
        self.list_widget.itemClicked.connect(self.on_item_click)
        
        if not self.current_lesson:
            logger.warning("LessonPage: _init_lesson_list called without a current_lesson.")
            return
        
        current_user_data = SessionManager.get_current_user()
        user_id = None
        if current_user_data and isinstance(current_user_data, dict) and 'id' in current_user_data:
            user_id = current_user_data['id']
        else:
            logger.warning("LessonPage: Could not get user_id for lesson list status.")

        try:
            course_id = self.current_lesson.course_id
            related_lessons = self.lesson_service.get_lessons_by_course_id(course_id)
            
            for lesson_item_data in related_lessons:
                status = "incomplete"
                if user_id and self.progress_service.has_completed_lesson(user_id, lesson_item_data.id):
                    status = "done"
                
                if lesson_item_data.id == self.current_lesson_id:
                    status = "active"

                difficulty_tag = getattr(lesson_item_data, 'difficulty_level', '')
                if hasattr(difficulty_tag, 'value'):
                    difficulty_tag = difficulty_tag.value
                
                item_widget = LessonItem(
                    lesson_item_data.title, 
                    f"Тривалість: {lesson_item_data.estimated_time} хв", 
                    status
                )
                list_item = QtWidgets.QListWidgetItem(self.list_widget)
                list_item.setData(Qt.UserRole, lesson_item_data.id) 
                list_item.setSizeHint(item_widget.sizeHint())
                self.list_widget.addItem(list_item)
                self.list_widget.setItemWidget(list_item, item_widget)

        except Exception as e:
            print(f"Error initializing lesson list: {e}")

    def load_lesson(self, lesson_id):
        """Load lesson data from LessonService"""
        if not lesson_id:
            return
            
        self.current_lesson_id = lesson_id
        self.current_lesson = self.lesson_service.get_lesson_by_id(lesson_id)
        
        if not self.current_lesson:
            return
            
        self.lesson_title_lb.setText(self.current_lesson.title)
        
        course_name = self._get_course_name(self.current_lesson.course_id)
        self.course_title_lb.setText(course_name)
        
        self._update_lesson_progress()
        
        self._init_lesson_list()
        
        self._load_lesson_content()
        
        self.update_task_tabs()

    def _get_course_name(self, course_id):
        """Get course name from course ID."""
        if not course_id:
            logger.warning("LessonPage: Attempted to get course name with no course_id.")
            return "Невідомий курс"
        try:
            course = self.course_service.get_course_by_id(str(course_id))
            if course and course.name:
                return course.name
            else:
                logger.warning(f"LessonPage: Course not found or has no name for course_id: {course_id}")
                return "Невідомий курс"
        except Exception as e:
            logger.error(f"LessonPage: Error getting course name for course_id {course_id}: {e}", exc_info=True)
            return "Помилка завантаження курсу"

    def _update_lesson_progress(self):
        """Update the lesson progress bar based on user's progress."""
        current_user_data = SessionManager.get_current_user()
        if current_user_data and isinstance(current_user_data, dict) and 'id' in current_user_data:
            user_id = current_user_data['id']
            completed = self.progress_service.has_completed_lesson(user_id, self.current_lesson_id)
            self.lesson_progress_bar.setValue(100 if completed else 24)
        else:
            logger.warning("LessonPage: Could not get current user ID to update progress.")
            self.lesson_progress_bar.setValue(0)

    def _load_lesson_content(self):
        """Load lesson content and convert to UI format."""
        logger.info(f"_load_lesson_content called for lesson ID: {self.current_lesson_id}")
        if not self.current_lesson:
            self.lesson_data = {}
            logger.warning("_load_lesson_content: No current_lesson found.")
            return
            
        content_items = self.content_service.get_lesson_content(self.current_lesson.id)
        logger.info(f"_load_lesson_content: Received {len(content_items)} content items from service.")
        for i, item_check in enumerate(content_items):
            logger.info(f"  Item {i}: title='{getattr(item_check, 'title', 'N/A')}', type='{getattr(item_check, 'content_type', 'N/A')}', id='{getattr(item_check, 'id', 'N/A')}', actual_type={type(item_check)}")

        
        self.lesson_data = {
            "theory": [],
            "exercise": [],
            "assessment": [],
            "interactive": []
        }
        
        for item in content_items:
            if isinstance(item, TheoryContent):
                self.lesson_data["theory"].append({
                    "title": item.title,
                    "text_content": getattr(item, 'text_content', "Немає вмісту."),
                    "examples": getattr(item, 'examples', {}),
                    "references": getattr(item, 'references', {})
                })
            elif isinstance(item, ExerciseContent):
                self.lesson_data["exercise"].append({
                    "title": item.title,
                    "problems": getattr(item, 'problems', {}).get("exercises", []) if isinstance(getattr(item, 'problems', {}), dict) else [],
                    "estimated_time": getattr(item, 'estimated_time', 0) 
                })
            elif isinstance(item, AssessmentContent):
                self.lesson_data["assessment"].append({
                    "title": item.title,
                    "questions": getattr(item, 'questions', {}).get("questions", []) if isinstance(getattr(item, 'questions', {}), dict) else [],
                    "time_limit": getattr(item, 'time_limit', 0),
                    "passing_score": getattr(item, 'passing_score', 0)
                })
            elif isinstance(item, InteractiveContent):
                self.lesson_data["interactive"].append({
                    "title": item.title,
                    "interactive_type": getattr(item, 'interactive_type', ""),
                    "configuration": getattr(item, 'configuration', {}),
                    "instructions": getattr(item, 'instructions', "")
                })
            else:
                original_item_type_str = getattr(item, 'content_type', 'N/A_ATTR')
                logger.warning(f"_load_lesson_content: Unhandled content item type: title='{getattr(item, 'title', 'N/A')}', "
                               f"original_content_type_attr='{original_item_type_str}', "
                               f"actual_instance_type='{type(item)}'")

        logger.info(f"_load_lesson_content: Populated self.lesson_data:")
        logger.info(f"  Theory items: {len(self.lesson_data['theory'])}")
        logger.info(f"  Exercise items: {len(self.lesson_data['exercise'])}")
        logger.info(f"  Assessment items: {len(self.lesson_data['assessment'])}")
        logger.info(f"  Interactive items: {len(self.lesson_data['interactive'])}")

        if not any(self.lesson_data.values()):
            logger.warning("_load_lesson_content: No content items were categorized into self.lesson_data. Falling back to old structure.")
            theory_content_fallback = "Немає вмісту для цього уроку."
            if self.current_lesson.content:
                theory_content_fallback = self.current_lesson.content.get("theory", "Немає вмісту для цього уроку.")
            self.lesson_data = {
                self.current_lesson.title: {
                    "theory": theory_content_fallback,
                    "test_question": self.current_lesson.content.get("test_question", "Приклад запитання?"),
                    "test_options": self.current_lesson.content.get("test_options", ["Варіант 1", "Варіант 2", "Варіант 3"]),
                    "test_answer": self.current_lesson.content.get("test_answer", "Варіант 1"),
                }
            }

    def set_lesson_data(self, lesson_data):
        """Set the lesson data and update UI"""
        if isinstance(lesson_data, dict) and 'id' in lesson_data:
            self.load_lesson(lesson_data['id'])
        elif isinstance(lesson_data, str):
            self.lesson_title_lb.setText(lesson_data)
            self.update_task_tabs()

    def update_task_tabs(self):
        """Update the task tabs with the current lesson data"""
        while self.task_tabs.count() > 0:
            self.task_tabs.removeTab(0)
        
        if not self.current_lesson or not self.lesson_data:
            no_data_widget = QtWidgets.QWidget()
            no_data_layout = QtWidgets.QVBoxLayout(no_data_widget)
            no_data_label = QtWidgets.QLabel("Немає даних для цього уроку.")
            no_data_label.setAlignment(QtCore.Qt.AlignCenter)
            no_data_layout.addWidget(no_data_label)
            self.task_tabs.addTab(self.createScrollableTab(no_data_widget), "Інформація")
            return

        if "theory" in self.lesson_data and self.lesson_data["theory"]:
            for theory_item in self.lesson_data["theory"]:
                theory_widget = QtWidgets.QWidget()
                theory_layout = QtWidgets.QVBoxLayout(theory_widget)
                
                title_label = QtWidgets.QLabel(theory_item.get("title", "Теорія"))
                title_label.setProperty("type", "sub_title")
                theory_layout.addWidget(title_label)

                html_content = self._markdown_to_html(theory_item.get("text_content", "Немає тексту."))
                text_content_label = QtWidgets.QLabel(html_content)
                text_content_label.setWordWrap(True)
                text_content_label.setTextFormat(Qt.RichText)
                text_content_label.setOpenExternalLinks(True)
                theory_layout.addWidget(text_content_label)
                
                examples = theory_item.get("examples", {})
                if examples:
                    examples_title = QtWidgets.QLabel("Приклади:")
                    examples_title.setProperty("type", "sub_title_small")
                    theory_layout.addWidget(examples_title)
                    for ex_num, ex_data in examples.items():
                        html_question = self._markdown_to_html(ex_data.get('question', ''))
                        ex_q_label = QtWidgets.QLabel(f"<b>Запитання {ex_num}:</b> {html_question}")
                        ex_q_label.setWordWrap(True)
                        ex_q_label.setTextFormat(Qt.RichText)
                        ex_q_label.setOpenExternalLinks(True)
                        theory_layout.addWidget(ex_q_label)
                        
                        html_solution = self._markdown_to_html(ex_data.get('solution', ''))
                        ex_s_label = QtWidgets.QLabel(f"<i>Рішення:</i> {html_solution}")
                        ex_s_label.setWordWrap(True)
                        ex_s_label.setTextFormat(Qt.RichText)
                        ex_s_label.setOpenExternalLinks(True)
                        theory_layout.addWidget(ex_s_label)
                        theory_layout.addSpacing(10)


                # Add references if any
                references = theory_item.get("references", {})
                if references:
                    refs_title = QtWidgets.QLabel("Додаткові матеріали:")
                    refs_title.setProperty("type", "sub_title_small")
                    theory_layout.addWidget(refs_title)
                    if "books" in references:
                        books_html_list = [self._markdown_to_html(book) for book in references['books']]
                        books_label = QtWidgets.QLabel(f"<b>Книги:</b> { '<br>'.join(books_html_list) }")
                        books_label.setWordWrap(True)
                        books_label.setTextFormat(Qt.RichText)
                        theory_layout.addWidget(books_label)
                    if "websites" in references:
                        sites_html_parts = []
                        for site in references['websites']:
                            if '<a href=' in site:
                                sites_html_parts.append(site)
                            elif '[' in site and '](' in site:
                                sites_html_parts.append(self._markdown_to_html(site))
                            else:
                                sites_html_parts.append(f'<a href="{site}">{site}</a>')
                        sites_label = QtWidgets.QLabel(f"<b>Веб-сайти:</b> { '<br>'.join(sites_html_parts) }")
                        sites_label.setWordWrap(True)
                        sites_label.setTextFormat(Qt.RichText)
                        sites_label.setOpenExternalLinks(True)
                        theory_layout.addWidget(sites_label)
                
                theory_layout.addStretch()
                self.task_tabs.addTab(self.createScrollableTab(theory_widget), theory_item.get("title", "Теорія"))

        if "exercise" in self.lesson_data and self.lesson_data["exercise"]:
            for exercise_item in self.lesson_data["exercise"]:
                exercise_widget = QtWidgets.QWidget()
                exercise_layout = QtWidgets.QVBoxLayout(exercise_widget)
                title_label = QtWidgets.QLabel(exercise_item.get("title", "Вправи"))
                title_label.setProperty("type", "sub_title")
                exercise_layout.addWidget(title_label)

                problems = exercise_item.get("problems", [])
                for i, problem in enumerate(problems):
                    problem_label = QtWidgets.QLabel(f"<b>Вправа {i+1}:</b> {problem.get('question', '')}")
                    problem_label.setWordWrap(True)
                    exercise_layout.addWidget(problem_label)
                    exercise_layout.addSpacing(10)
                
                est_time_label = QtWidgets.QLabel(f"<i>Орієнтовний час: {exercise_item.get('estimated_time', 'N/A')} хв</i>")
                exercise_layout.addWidget(est_time_label)
                exercise_layout.addStretch()
                self.task_tabs.addTab(self.createScrollableTab(exercise_widget), exercise_item.get("title", "Вправи"))

        if "assessment" in self.lesson_data and self.lesson_data["assessment"]:
            for assessment_item in self.lesson_data["assessment"]:
                assessment_widget = QtWidgets.QWidget()
                assessment_layout = QtWidgets.QVBoxLayout(assessment_widget)
                title_label = QtWidgets.QLabel(assessment_item.get("title", "Тест"))
                title_label.setProperty("type", "sub_title")
                assessment_layout.addWidget(title_label)

                questions = assessment_item.get("questions", [])
                for i, q_data in enumerate(questions):
                    q_label = QtWidgets.QLabel(f"<b>Запитання {i+1}:</b> {q_data.get('question', '')}")
                    q_label.setWordWrap(True)
                    assessment_layout.addWidget(q_label)
                    if q_data.get("type") == "multiple_choice" and "options" in q_data:
                        options_label = QtWidgets.QLabel(f"Варіанти: {', '.join(q_data['options'])}")
                        assessment_layout.addWidget(options_label)
                    assessment_layout.addSpacing(10)
                
                time_limit_label = QtWidgets.QLabel(f"<i>Часовий ліміт: {assessment_item.get('time_limit', 'N/A')} хв, Прохідний бал: {assessment_item.get('passing_score', 'N/A')}%</i>")
                assessment_layout.addWidget(time_limit_label)
                assessment_layout.addStretch()
                self.task_tabs.addTab(self.createScrollableTab(assessment_widget), assessment_item.get("title", "Тест"))

        if "interactive" in self.lesson_data and self.lesson_data["interactive"]:
            for interactive_item in self.lesson_data["interactive"]:
                interactive_widget = QtWidgets.QWidget()
                interactive_layout = QtWidgets.QVBoxLayout(interactive_widget)
                title_label = QtWidgets.QLabel(interactive_item.get("title", "Інтерактив"))
                title_label.setProperty("type", "sub_title")
                interactive_layout.addWidget(title_label)
                
                instr_label = QtWidgets.QLabel(f"<b>Інструкції:</b>\n{interactive_item.get('instructions', 'Немає інструкцій.')}")
                instr_label.setWordWrap(True)
                interactive_layout.addWidget(instr_label)

                config = interactive_item.get("configuration", {})
                if "challenges" in config:
                    challenges_title = QtWidgets.QLabel("Завдання:")
                    challenges_title.setProperty("type", "sub_title_small")
                    interactive_layout.addWidget(challenges_title)
                    for challenge in config["challenges"]:
                        chal_desc_label = QtWidgets.QLabel(challenge.get("description", ""))
                        chal_desc_label.setWordWrap(True)
                        interactive_layout.addWidget(chal_desc_label)
                        interactive_layout.addSpacing(5)
                
                interactive_layout.addStretch()
                self.task_tabs.addTab(self.createScrollableTab(interactive_widget), interactive_item.get("title", "Інтерактив"))
        
        if not self.task_tabs.count() and self.current_lesson and self.current_lesson.title in self.lesson_data :
            lesson_data_fallback = self.lesson_data[self.current_lesson.title]
            
            theory_widget_fallback = QtWidgets.QWidget()
            theory_layout_fallback = QtWidgets.QVBoxLayout(theory_widget_fallback)
            theory_label_fallback = QtWidgets.QLabel(lesson_data_fallback.get("theory", "Немає теорії."))
            theory_label_fallback.setWordWrap(True)
            theory_layout_fallback.addWidget(theory_label_fallback)
            theory_layout_fallback.addStretch()
            self.task_tabs.addTab(self.createScrollableTab(theory_widget_fallback), "Теорія (запасний варіант)")

            test_widget_fallback = QtWidgets.QWidget()
            test_layout_fallback = QtWidgets.QVBoxLayout(test_widget_fallback)
            question_label_fallback = QtWidgets.QLabel(lesson_data_fallback.get("test_question", "Немає запитання."))
            test_layout_fallback.addWidget(question_label_fallback)
            
            options_fallback = lesson_data_fallback.get("test_options", [])
            for option_text_fallback in options_fallback:
                option_rb_fallback = QtWidgets.QRadioButton(option_text_fallback)
                test_layout_fallback.addWidget(option_rb_fallback)
            test_layout_fallback.addStretch()
            self.task_tabs.addTab(self.createScrollableTab(test_widget_fallback), "Тест (запасний варіант)")

    def createScrollableTab(self, inner_widget):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(inner_widget)
        inner_widget.setProperty("type", "w_pg")
        return scroll_area

    def on_item_click(self, item):
        """Handle lesson list item click."""
        index = self.list_widget.indexFromItem(item)
        item_widget = self.list_widget.itemWidget(item)
        if item_widget:
            lesson_title = item_widget.title_label.text()
            self.lesson_title_lb.setText(lesson_title)
            
            if self.current_lesson and self.current_lesson.course_id:
                course_lessons = self.lesson_service.get_lessons_by_course_id(self.current_lesson.course_id)
                for lesson in course_lessons:
                    if lesson.title == lesson_title:
                        self.load_lesson(lesson.id)
                        return
                        
            self.set_lesson_data(lesson_title)
    