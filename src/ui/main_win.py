from PyQt5.QtWidgets import QWidget, QGridLayout,QVBoxLayout, QLabel,QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from circular_progress import *
from graphs import *
from lesson_win import Lesson_page
from ui import *
from src.services.user_service import UserService
from src.services.lesson_service import LessonService
from src.services.course_service import CourseService
from src.services.progress_service import ProgressService
from src.services.session_manager import SessionManager
from src.db import get_db
import uuid
import logging


logger = logging.getLogger(__name__)

class ClickFilter(QtCore.QObject):
    clicked = QtCore.pyqtSignal()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self.clicked.emit()
        return False 
    

class Main_page(QWidget):
    def __init__(self, stack=None, lesson_page=None, lessons_list_page=None):
        super().__init__()
        self.stack = None
        self.pg_lesson = None
        self.pg_lessons_list = None
        self.stack = stack
        self.pg_lesson = lesson_page
        self.pg_lessons_list = lessons_list_page
        
        # Initialize services
        self.user_service = UserService()
        self.lesson_service = LessonService()
        self.course_service = CourseService()
        self.progress_service = ProgressService()
        
        self.init_ui()
        
        logger.info("ACTIVITY GRAPH: Initialized main page, will load activity data")
        
        activity_data, activity_labels = self.get_user_activity_data()
        chart_activity = MyGraph(self.plot_activity)
        chart_activity.plot_bar_chart(activity_data, activity_labels)

    def init_ui(self):
        self.pg_main = QtWidgets.QWidget(self)
        self.pg_main.setObjectName("pg_main")
        self.main_layout = QtWidgets.QGridLayout(self.pg_main)
        self.main_layout.setObjectName("main_layout")
        
        self.continue_viewing_section = QtWidgets.QWidget(self.pg_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.continue_viewing_section.sizePolicy().hasHeightForWidth())
        self.continue_viewing_section.setSizePolicy(sizePolicy)
        self.continue_viewing_section.setMinimumSize(QtCore.QSize(900, 335))
        self.continue_viewing_section.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.continue_viewing_section.setObjectName("continue_viewing_section")
        self.continue_viewing_section.setProperty("type", "w_pg")
        self.grid_continue_section = QtWidgets.QGridLayout(self.continue_viewing_section)
        self.grid_continue_section.setObjectName("grid_continue_section")
        
        self.continue_viewing_label = QtWidgets.QLabel(self.continue_viewing_section)
        self.continue_viewing_label.setText("Продовжити перегляд")
        self.continue_viewing_label.setProperty("type", "page_section")
        
       
        #self.continue_viewing_label.setMinimumSize(QtCore.QSize(0, 50))

        self.continue_viewing_label.setMinimumSize(QtCore.QSize(900, 50))
        self.continue_viewing_label.setMaximumSize(QtCore.QSize(16777215, 50))
        self.continue_viewing_label.setObjectName("continue_viewing_label")
        
        self.continue_viewing_label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.grid_continue_section.addWidget(self.continue_viewing_label, 0, 1, 1, 1)
        
        self.continue_viewing_scroll_area = QtWidgets.QScrollArea(self.continue_viewing_section)
        self.continue_viewing_scroll_area.setWidgetResizable(True)
        self.continue_viewing_scroll_area.setObjectName("continue_viewing_scroll_area")
        
        self.scroll_area_content_widget = QtWidgets.QWidget()
        self.scroll_area_content_widget .setProperty("type", "w_pg")
        self.scroll_area_content_widget.setGeometry(QtCore.QRect(-329, 0, 1816, 250))
        self.scroll_area_content_widget.setObjectName("scroll_area_content_widget")
        
        self.scroll_area_main_layout = QtWidgets.QHBoxLayout(self.scroll_area_content_widget)
        self.scroll_area_main_layout.setObjectName("scroll_area_main_layout")
        self.continue_viewing_courses_layout = QtWidgets.QHBoxLayout()
        self.continue_viewing_courses_layout.setObjectName("continue_viewing_courses_layout")
        
        self.scroll_area_main_layout.addLayout(self.continue_viewing_courses_layout)
        self.continue_viewing_scroll_area.setWidget(self.scroll_area_content_widget)
        self.grid_continue_section.addWidget(self.continue_viewing_scroll_area, 1, 1, 1, 1)
        self.btn_scroll_next = QtWidgets.QPushButton(self.continue_viewing_section)
        self.btn_scroll_next.setProperty("type", "next_previous")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("icon/next.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_scroll_next.setIcon(icon9)
        self.btn_scroll_next.setIconSize(QtCore.QSize(30, 30))
        self.btn_scroll_next.setObjectName("btn_scroll_next")
        self.grid_continue_section.addWidget(self.btn_scroll_next, 1, 2, 1, 1)
        
        self.btn_scroll_prev = QtWidgets.QPushButton(self.continue_viewing_section)
        self.btn_scroll_prev.setProperty("type", "next_previous")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("icon/previous.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_scroll_prev.setIcon(icon10)
        self.btn_scroll_prev.setIconSize(QtCore.QSize(30, 30))
        self.btn_scroll_prev.setObjectName("btn_scroll_prev")
        self.grid_continue_section.addWidget(self.btn_scroll_prev, 1, 0, 1, 1)
        self.main_layout.addWidget(self.continue_viewing_section, 1, 0, 1, 1)
        
        self.courses_section = QtWidgets.QWidget(self.pg_main)
        self.courses_section.setSizePolicy(sizePolicy)
        self.courses_section.setProperty("type", "w_pg")
        #self.courses_section.setMinimumSize(QtCore.QSize(900, 341))
        self.courses_section.setMinimumSize(QtCore.QSize(900, 335))
        self.courses_section.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.courses_section.setObjectName("courses_section")
        
        self.gridLayout_14 = QtWidgets.QGridLayout(self.courses_section)
        self.gridLayout_14.setObjectName("gridLayout_14")       

        self.lb_my_courses = QtWidgets.QLabel(self.courses_section)
        
        self.lb_my_courses.setMaximumSize(QtCore.QSize(900, 50))
        self.lb_my_courses.setMaximumSize(QtCore.QSize(16777215, 50))
        self.lb_my_courses.setText("Курси")
        self.lb_my_courses.setProperty("type", "page_section")
        self.lb_my_courses.setObjectName("lb_my_courses")
        self.gridLayout_14.addWidget(self.lb_my_courses, 0, 0, 1, 1)
        self.lb_my_courses.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        
        all_courses = self.course_service.get_all_courses()
        logger.info(f"Loaded {len(all_courses)} courses from database")
        
        current_user_data = SessionManager.get_current_user()
        current_user_id = None
        if current_user_data and isinstance(current_user_data, dict):
            current_user_id = current_user_data.get('id')
        
        row, col = 1, 0
        max_courses = 8
        
        for i, course in enumerate(all_courses[:max_courses]):
            course_widget = QWidget(self.courses_section)
            layout = QVBoxLayout(course_widget)
            layout.setAlignment(QtCore.Qt.AlignCenter)
            course_widget.setMinimumSize(180, 180) 
            course_widget.setMaximumSize(180, 180) 
            course_widget.setProperty("type", "transparent_widget")

            # Get course name from database
            course_name = course.name if hasattr(course, 'name') and course.name else f"Course {i+1}"
            course_label = QLabel(course_name)
            course_label.setAlignment(QtCore.Qt.AlignCenter)
            course_label.setProperty("type", "lb_small")
            course_label.setFixedSize(160, 20)

            circular_progress = CircularProgress(course_widget)
            circular_progress.setObjectName(f"circular_progress_{i+1}")
            circular_progress.setMinimumSize(140, 140)
            circular_progress.setMaximumSize(140, 140)
            circular_progress.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            
            progress_value = (i + 1) * 10
            
            if current_user_id:
                try:
                    course_progress = self.progress_service.get_course_progress(str(current_user_id), str(course.id))
                    if course_progress and hasattr(course_progress, 'progress_percentage'):
                        progress_value = int(course_progress.progress_percentage)
                    else:
                        weighted_progress, _ = self.progress_service.calculate_weighted_course_progress(
                            str(current_user_id), str(course.id))
                        if weighted_progress is not None:
                            progress_value = int(weighted_progress)
                except Exception as e:
                    logger.error(f"Error getting progress for course {course_name}: {e}")
            
            circular_progress.set_value(progress_value)

            layout.addWidget(course_label)
            layout.addWidget(circular_progress)
            
            # Make course widget clickable
            course_widget.setCursor(Qt.PointingHandCursor)
            course_widget.setProperty("course_id", course.id)
            click_filter = ClickFilter(course_widget)
            course_widget.installEventFilter(click_filter)
            click_filter.clicked.connect(lambda c_id=course.id: self.on_course_click(c_id))

            col = i % 4
            row = (i // 4) + 1
            self.gridLayout_14.addWidget(course_widget, row, col, 1, 1)
            
        while i+1 < max_courses:
            i += 1
            empty_widget = QWidget(self.courses_section)
            empty_widget.setMinimumSize(180, 180)
            empty_widget.setMaximumSize(180, 180)
            empty_widget.setProperty("type", "transparent_widget")
            
            col = i % 4
            row = (i // 4) + 1
            self.gridLayout_14.addWidget(empty_widget, row, col, 1, 1)
            
        self.main_layout.addWidget(self.courses_section, 2, 0, 1, 1)
        self.activity_section = QtWidgets.QWidget(self.pg_main)
        self.activity_section.setSizePolicy(sizePolicy)
        self.activity_section.setMinimumSize(QtCore.QSize(312, 340))
        self.activity_section.setMaximumSize(QtCore.QSize(500, 16777215))
        self.activity_section.setProperty("type", "w_pg")
        self.activity_section.setObjectName("activity_section")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.activity_section)
        self.gridLayout_13.setObjectName("gridLayout_13")
        
        self.lb_activity = QtWidgets.QLabel(self.activity_section)
        self.lb_activity.setMinimumSize(QtCore.QSize(0, 50))
        self.lb_activity.setMaximumSize(QtCore.QSize(16777215, 50))
        self.lb_activity.setText("Активність")
        self.lb_activity.setProperty("type", "page_section")
        self.lb_activity.setObjectName("lb_activity")
        self.gridLayout_13.addWidget(self.lb_activity, 0, 0, 1, 1)
        
        self.activity_graph_widget = QtWidgets.QWidget(self.activity_section)
        self.activity_graph_widget.setObjectName("activity_graph_widget")
        self.activity_graph_widget.setProperty("type", "w_pg")
        self.gridLayout_13.addWidget(self.activity_graph_widget, 1, 0, 1, 1)
        self.main_layout.addWidget(self.activity_section, 2, 1, 1, 1)
        
        self.recommended_section = QtWidgets.QWidget(self.pg_main)
        self.recommended_section.setSizePolicy(sizePolicy)
        self.recommended_section.setMaximumSize(QtCore.QSize(500, 16777215))
        self.recommended_section.setProperty("type", "w_pg")
        self.recommended_section.setObjectName("recommended_section")
        self.grid_rec_activity_section = QtWidgets.QGridLayout(self.recommended_section)
        self.grid_rec_activity_section.setObjectName("grid_rec_activity_section")
        
        self.recommended_label = QtWidgets.QLabel(self.recommended_section)
        self.recommended_label.setText("Можливо цікавить")
        self.recommended_label.setProperty("type", "page_section")
        self.recommended_label.setObjectName("recommended_label")
        self.grid_rec_activity_section.addWidget(self.recommended_label, 0, 0, 1, 1)
        
        self.recommended_scroll_area = QtWidgets.QScrollArea(self.recommended_section)
        self.recommended_scroll_area.setWidgetResizable(True)
        self.recommended_scroll_area.setObjectName("recommended_scroll_area")
        self.recommended_scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.recommended_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.recommended_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.recommended_scroll_content_widget = QtWidgets.QWidget()
        self.recommended_scroll_content_widget.setProperty("type", "w_pg")
        self.recommended_scroll_content_widget.setObjectName("recommended_scroll_content_widget")
        
        self.recommended_cards_layout = QtWidgets.QVBoxLayout(self.recommended_scroll_content_widget)
        self.recommended_cards_layout.setObjectName("recommended_cards_layout")
        self.recommended_cards_layout.setAlignment(Qt.AlignTop)

        self.recommended_scroll_area.setWidget(self.recommended_scroll_content_widget)
        self.grid_rec_activity_section.addWidget(self.recommended_scroll_area, 1, 0, 1, 1)

        self.main_layout.addWidget(self.recommended_section, 1, 1, 1, 1)
        
        self.title_main_lb = QtWidgets.QLabel(self.pg_main)
        self.title_main_lb.setText("Головна")
        self.title_main_lb.setProperty("type", "title")
        self.title_main_lb.setObjectName("title_main_lb")
        self.main_layout.addWidget(self.title_main_lb, 0, 0, 1, 1)
        self.setLayout(self.main_layout)
        
        self.layout_activity_graph = QVBoxLayout(self.activity_graph_widget)
        self.plot_activity = pg.PlotWidget() 
        self.layout_activity_graph.addWidget(self.plot_activity)
        chart_activity = MyGraph(self.plot_activity)
        
        activity_data, activity_labels = self.get_user_activity_data()
        chart_activity.plot_bar_chart(activity_data, activity_labels)

        self.btn_scroll_next.clicked.connect(self.scroll_right)
        self.btn_scroll_prev.clicked.connect(self.scroll_left)
        self.continue_viewing_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.load_user_specific_data()
        self.load_recommended_courses_data()

        logger.info("ACTIVITY GRAPH: Initialized main page, will load activity data")
        
        # Bind the activity data
        activity_data, activity_labels = self.get_user_activity_data()
        chart_activity = MyGraph(self.plot_activity)
        chart_activity.plot_bar_chart(activity_data, activity_labels)

    def on_course_click(self, course_id):
        """Handle clicking on a course widget in the courses grid"""
        logger.info(f"Course clicked: ID {course_id}")
        if hasattr(self, 'pg_lessons_list') and self.pg_lessons_list and hasattr(self.pg_lessons_list, '_load_course_lessons'):
            try:
                self.pg_lessons_list._load_course_lessons(str(course_id))
                if self.stack:
                    self.stack.setCurrentWidget(self.pg_lessons_list)
                    logger.info(f"Switched to lessons list page for course {course_id}")
                else:
                    logger.error("[ERROR] Main_page: self.stack is None, cannot switch to lessons list page.")
            except Exception as e:
                logger.error(f"[ERROR] Main_page: Error calling _load_course_lessons for course {course_id}: {e}")
        else:
            missing_attrs = []
            if not hasattr(self, 'pg_lessons_list') or not self.pg_lessons_list:
                missing_attrs.append("self.pg_lessons_list is not available")
            elif not hasattr(self.pg_lessons_list, '_load_course_lessons'):
                missing_attrs.append("self.pg_lessons_list does not have _load_course_lessons method")
            logger.warning(f"[WARN] Main_page: Cannot navigate to lessons list. Issues: {', '.join(missing_attrs)} for course_id: {course_id}")

    def _create_recommended_course_card(self, course):
        card_widget = QtWidgets.QWidget()
        card_widget.setProperty("type", "card_simple") 
        card_widget.setMinimumHeight(80)
        card_widget.setMaximumHeight(100)
        card_widget.setCursor(Qt.PointingHandCursor)

        card_layout = QtWidgets.QVBoxLayout(card_widget)

        course_name_label = QtWidgets.QLabel(course.name)
        course_name_label.setProperty("type", "lb_name_course_recommended") 
        course_name_label.setWordWrap(True)
        card_layout.addWidget(course_name_label)

        description_text = getattr(course, 'description', "Опис відсутній") or "Опис відсутній"
        max_desc_len = 90
        if len(description_text) > max_desc_len:
            description_text = description_text[:max_desc_len] + "..."
            
        course_description_label = QtWidgets.QLabel(description_text)
        course_description_label.setProperty("type", "lb_small_recommended") 
        course_description_label.setWordWrap(True)
        card_layout.addWidget(course_description_label)
        
        card_layout.addStretch() 

        card_widget.setProperty("course_id", course.id)
        
        click_filter = ClickFilter(card_widget)
        card_widget.installEventFilter(click_filter)
        click_filter.clicked.connect(lambda c_id=course.id: self.on_recommended_course_click(c_id))

        return card_widget

    def load_recommended_courses_data(self):
        self.clear_layout(self.recommended_cards_layout)
        logger.info("--- Loading Recommended Courses Data ---") 

        try:
            all_courses_raw = self.course_service.get_all_courses()
            if not all_courses_raw:
                logger.debug("No courses found by CourseService.")
                no_courses_label = QtWidgets.QLabel("Цікаві курси скоро з\'являться!")
                no_courses_label.setAlignment(Qt.AlignCenter)
                self.recommended_cards_layout.addWidget(no_courses_label)
                return
            
            all_courses = [c for c in all_courses_raw if c and hasattr(c, 'id') and c.id and hasattr(c, 'name') and c.name]
            logger.debug(f"All valid courses ({len(all_courses)}): {[(c.name, c.id) for c in all_courses]}")

            recommended_courses = []
            current_user_data = SessionManager.get_current_user()
            current_user_id = None

            if current_user_data and isinstance(current_user_data, dict):
                current_user_id = current_user_data.get('id')
            
            logger.debug(f"Current User ID: {current_user_id}")
            
            if current_user_id:
                try:
                    user_progress_list = self.progress_service.get_user_progress(str(current_user_id))
                    logger.debug(f"User Progress List ({len(user_progress_list if user_progress_list else [])}):")
                    if user_progress_list:
                        for p_item in user_progress_list:
                            logger.debug(f"  Progress Item: course_id={getattr(p_item, 'course_id', 'N/A')}, lesson_id={getattr(p_item, 'current_lesson_id', 'N/A')}, completed={getattr(p_item, 'is_completed', 'N/A')}") #Debug
                    
                    started_course_ids = set()
                    if user_progress_list:
                        started_course_ids = {str(p.course_id) for p in user_progress_list if p and hasattr(p, 'course_id') and p.course_id}
                    
                    logger.debug(f"Started Course IDs: {started_course_ids}")
                    
                    recommended_courses = [course for course in all_courses if str(course.id) not in started_course_ids]
                    logger.debug(f"Recommended courses after filtering ({len(recommended_courses)}): {[(c.name, c.id) for c in recommended_courses] if recommended_courses else 'None'}") # Debug
                    
                    if not recommended_courses and started_course_ids:
                        all_started_label = QtWidgets.QLabel("Ви вже розпочали всі доступні курси!")
                        all_started_label.setAlignment(Qt.AlignCenter)
                        self.recommended_cards_layout.addWidget(all_started_label)
                except Exception as e:
                    logger.error(f"Error fetching user progress for recommendations: {e}") 
                    recommended_courses = all_courses
            else:
                logger.debug("No user logged in. Recommending from all courses.")
                recommended_courses = all_courses

            if not recommended_courses:
                if not self.recommended_cards_layout.count():
                    no_new_courses_label = QtWidgets.QLabel("Немає нових курсів для рекомендації.")
                    no_new_courses_label.setAlignment(Qt.AlignCenter)
                    self.recommended_cards_layout.addWidget(no_new_courses_label)
                logger.debug("No recommended_courses to display after all checks.")
                return

            num_to_display = 4
            final_courses_to_display = recommended_courses[:num_to_display]
            logger.debug(f"Final courses to display ({len(final_courses_to_display)}): {[(c.name, c.id) for c in final_courses_to_display]}") # Debug

            if not final_courses_to_display:
                if not self.recommended_cards_layout.count():
                    no_rec_label = QtWidgets.QLabel("Наразі немає рекомендацій.")
                    no_rec_label.setAlignment(Qt.AlignCenter)
                    self.recommended_cards_layout.addWidget(no_rec_label)
                logger.debug("No final_courses_to_display to show.")
                return

            for course in final_courses_to_display:
                course_card = self._create_recommended_course_card(course)
                if course_card:
                    self.recommended_cards_layout.addWidget(course_card)
            
            if len(recommended_courses) < num_to_display :
                 spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                 self.recommended_cards_layout.addSpacerItem(spacer)

        except Exception as e:
            logger.error(f"Error loading recommended courses: {e}")
            error_label = QtWidgets.QLabel("Не вдалося завантажити рекомендовані курси.")
            error_label.setAlignment(Qt.AlignCenter)
            self.recommended_cards_layout.addWidget(error_label)

    def on_recommended_course_click(self, course_id):
        logger.info(f"Recommended course clicked: ID {course_id}")
        if hasattr(self, 'pg_lessons_list') and self.pg_lessons_list and hasattr(self.pg_lessons_list, '_load_course_lessons'):
            try:
                self.pg_lessons_list._load_course_lessons(str(course_id)) 
                if self.stack:
                    self.stack.setCurrentWidget(self.pg_lessons_list)
                    logger.info(f"Switched to lessons list page for course {course_id}")
                else:
                    logger.error("[ERROR] Main_page: self.stack is None, cannot switch to lessons list page.")
            except Exception as e:
                logger.error(f"[ERROR] Main_page: Error calling _load_course_lessons for course {course_id}: {e}")
        else:
            missing_attrs = []
            if not hasattr(self, 'pg_lessons_list') or not self.pg_lessons_list:
                missing_attrs.append("self.pg_lessons_list is not available")
            elif not hasattr(self.pg_lessons_list, '_load_course_lessons'):
                missing_attrs.append("self.pg_lessons_list does not have _load_course_lessons method")
            logger.warning(f"[WARN] Main_page: Cannot navigate to lessons list. Issues: {', '.join(missing_attrs)} for course_id: {course_id}")

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    sub_layout = item.layout()
                    if sub_layout is not None:
                        self.clear_layout(sub_layout)
    
    def load_user_specific_data(self):
        
        self.clear_layout(self.continue_viewing_courses_layout)

        current_user_data = SessionManager.get_current_user() 
        current_user_id = None
        if current_user_data and isinstance(current_user_data, dict):
            current_user_id = current_user_data.get('id') 
        
        lessons_to_display = []
        if not current_user_id:
            logger.warning("No current user ID found in session data. Cannot load courses.") 
        else:
            user_progress_list = self.progress_service.get_user_progress(str(current_user_id))

            if not user_progress_list:
                logger.warning(f"No progress items found for user {current_user_id}.")
            else:
                temp_lessons_to_display = []
                for progress_item in user_progress_list:
                    if progress_item.is_completed:
                        continue

                    lesson_to_use = None
                    if progress_item.current_lesson_id:
                        lesson_to_use = self.lesson_service.get_lesson_by_id(str(progress_item.current_lesson_id))
                    else:
                        course_lessons = self.lesson_service.get_lessons_by_course_id(str(progress_item.course_id))
                        if course_lessons:
                            lesson_to_use = course_lessons[0]

                    if lesson_to_use:
                        course = self.course_service.get_course_by_id(str(progress_item.course_id))
                        if course:
                            temp_lessons_to_display.append({
                                "lesson_id": str(lesson_to_use.id),
                                "lesson": lesson_to_use.title,
                                "course": course.name,
                                "desc": getattr(lesson_to_use, 'description', "Опис відсутній") or "Опис відсутній",
                                "progress": int(progress_item.progress_percentage),
                                "last_accessed": progress_item.last_accessed
                            })
                
                temp_lessons_to_display.sort(key=lambda x: x["last_accessed"], reverse=True)
                
                seen_lesson_course_pairs = set()
                for item_data in temp_lessons_to_display:
                    lesson_course_pair = (item_data["lesson_id"], item_data["course"])
                    if lesson_course_pair not in seen_lesson_course_pairs:
                        lessons_to_display.append(item_data)
                        seen_lesson_course_pairs.add(lesson_course_pair)
                    if len(lessons_to_display) >= 9:
                        break
                
                if not lessons_to_display:
                    logger.warning(f"No lessons to display for user {current_user_id} after processing progress.")


        for i, lesson_data in enumerate(lessons_to_display, start=1):
            widget = QtWidgets.QWidget(self.scroll_area_content_widget)
            widget.setMinimumSize(QtCore.QSize(250, 0))
            widget.setMaximumSize(QtCore.QSize(250, 16777215))    
            widget.setProperty("type", "card")            
            widget.style().unpolish(widget)
            widget.style().polish(widget)
            widget.setObjectName(f"w_pg1_les{i}")

            vertical_layout = QtWidgets.QVBoxLayout(widget)
            vertical_layout.setObjectName(f"verticalLayout_{i}")

            lesson_name_label = QtWidgets.QLabel(widget)
            lesson_name_label.setProperty("type", "lb_name_lesson")
            lesson_name_label.setObjectName(f"lb_n_les{i}")
            lesson_name_label.setText(lesson_data["lesson"])
            vertical_layout.addWidget(lesson_name_label)
            
            widget.lesson_label = lesson_name_label
            
            course_name_label = QtWidgets.QLabel(widget)
            course_name_label.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding))
            course_name_label.setMinimumSize(QtCore.QSize(0, 50))
            course_name_label.setMaximumSize(QtCore.QSize(16777215, 50))
            course_name_label.setProperty("type", "lb_name_course")
            course_name_label.setObjectName(f"course_name_label{i}")
            course_name_label.setText(lesson_data["course"])
            vertical_layout.addWidget(course_name_label)

            lesson_description_label = QtWidgets.QLabel(widget)
            lesson_description_label.setProperty("type", "lb_small")
            lesson_description_label.setObjectName(f"lesson_description_label{i}")
            lesson_description_label.setText(lesson_data["desc"])
            vertical_layout.addWidget(lesson_description_label)

            lesson_progress_bar = QtWidgets.QProgressBar(widget)
            lesson_progress_bar.setObjectName(f"lesson_progress_bar{i}")
            lesson_progress_bar.setValue(lesson_data["progress"])
            vertical_layout.addWidget(lesson_progress_bar)
            
            widget.setProperty("lesson_id", lesson_data["lesson_id"])

            click_filter = ClickFilter(widget)
            widget.installEventFilter(click_filter)
            
            click_filter.clicked.connect(lambda w=widget: self.on_lesson_click(w))

            self.continue_viewing_courses_layout.addWidget(widget)
        
        self.continue_viewing_scroll_area.setWidget(self.scroll_area_content_widget)
        self.scroll_area_content_widget.adjustSize()

    def scroll_left(self):
        scroll_bar = self.continue_viewing_scroll_area.horizontalScrollBar()
        scroll_bar.setValue(scroll_bar.value() - 150)

    def scroll_right(self):
        scroll_bar = self.continue_viewing_scroll_area.horizontalScrollBar()
        scroll_bar.setValue(scroll_bar.value() + 150)
    
    def on_lesson_click(self, widget):
        lesson_id = widget.property("lesson_id")
        if lesson_id and self.pg_lesson:
            logger.info(f"Continue Viewing: Clicked lesson_id: {lesson_id}")
            self.pg_lesson.load_lesson(lesson_id) 
            if self.stack:
                self.stack.setCurrentWidget(self.pg_lesson)
            else:
                logger.error("[ERROR] Main_page: self.stack is None, cannot switch page.")
        else:
            if not lesson_id:
                logger.warning(f"[WARN] Main_page: lesson_id not found on clicked widget: {widget}")
            if not self.pg_lesson:
                logger.warning(f"[WARN] Main_page: self.pg_lesson is None, cannot load lesson.")
    
    def get_user_activity_data(self):
        """
        Get user completed lessons for the last 7 days to populate the activity graph.
        
        Returns:
            Tuple containing (list of activity counts, list of day labels)
        """
        logger.info("===== ACTIVITY GRAPH: Loading user activity data for last 7 days =====")
        
        default_data = [1, 0, 3, 2, 4, 2, 1]
        default_labels = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
        
        current_user_data = SessionManager.get_current_user()
        if not current_user_data or not isinstance(current_user_data, dict):
            logger.warning("No user data available for activity graph")
            return default_data, default_labels
            
        current_user_id = current_user_data.get('id')
        if not current_user_id:
            logger.warning("No user ID found in session data")
            return default_data, default_labels
        
        return self.progress_service.get_user_activity_by_day(str(current_user_id))
        