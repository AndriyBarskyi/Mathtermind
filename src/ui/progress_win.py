from PyQt5.QtWidgets import QWidget, QGridLayout,QVBoxLayout, QLabel,QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from src.services.progress_service import ProgressService
from src.services.course_service import CourseService
from src.services.lesson_service import LessonService
from src.models.progress import Progress


class Progress_page(QWidget):
    def create_tab_with_widgets(self, name, num_widgets, rows=3, cols=5):
        tab_widget = QtWidgets.QWidget()
        tab_widget.setObjectName("tab_widget")
        grid_layout = QtWidgets.QGridLayout(tab_widget)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setHorizontalSpacing(0)
        grid_layout.setObjectName("gridLayout_17")

        for i in range(1, num_widgets + 1):
                widget = QtWidgets.QWidget(tab_widget)
                widget.setMinimumSize(QtCore.QSize(41, 41))
                widget.setMaximumSize(QtCore.QSize(41, 41))
                widget.setProperty("type","progress")
                widget.setObjectName(f"tab1_w{i}")
                widget.setToolTip(f"Це {widget.objectName()}")
                row = (i - 1) // cols
                col = (i - 1) % cols
                grid_layout.addWidget(widget, row, col, 1, 1)
        self.tabs_courses_success.addTab(tab_widget, name)
        tab_widget.setProperty("type", "w_pg")

        

    def __init__(self):
        super().__init__()
        
        # Initialize services
        self.progress_service = ProgressService()
        self.course_service = CourseService()
        self.lesson_service = LessonService()
        
        self.pg_progress = QtWidgets.QWidget()
        self.pg_progress.setObjectName("pg_progress")
        
        # Connect to show event to refresh data when page becomes visible
        self.showEvent = self.on_show_event
        
        self.main_progress_layout = QtWidgets.QGridLayout(self.pg_progress)
        self.main_progress_layout.setHorizontalSpacing(7)
        self.main_progress_layout.setObjectName("main_progress_layout")
        self.success_widget = QtWidgets.QWidget(self.pg_progress)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        self.success_widget.setSizePolicy(sizePolicy)
        self.success_widget.setMinimumSize(QtCore.QSize(311, 341))
        self.success_widget.setProperty("type","w_pg") 
        self.success_widget.setObjectName("success_widget")
        self.success_layout = QtWidgets.QGridLayout(self.success_widget)
        self.success_layout.setObjectName("success_layout")
        
        self.lb_success = QtWidgets.QLabel(self.success_widget)
        self.lb_success.setText("Успішність")
        self.lb_success.setProperty("type", "page_section")
        self.lb_success.setMaximumSize(QtCore.QSize(16777215, 50))
        self.lb_success.setObjectName("lb_success")
        self.success_layout.addWidget(self.lb_success, 0, 0, 1, 1)
        
        self.success_graph_widget = QtWidgets.QWidget(self.success_widget)
        self.success_graph_widget.setObjectName("success_graph_widget")
        self.success_graph_widget.setProperty("type", "w_pg")
        self.success_layout.addWidget(self.success_graph_widget, 1, 0, 1, 1)
        self.main_progress_layout.addWidget(self.success_widget, 1, 2, 3, 1)
        
        self.activity_widget = QtWidgets.QWidget(self.pg_progress)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.activity_widget.setSizePolicy(sizePolicy)
        self.activity_widget.setMinimumSize(QtCore.QSize(311, 341))
        self.activity_widget.setProperty("type","w_pg")
        self.activity_widget.setObjectName("activity_widget")
        self.activity_layout = QtWidgets.QGridLayout(self.activity_widget)
        self.activity_layout.setObjectName("activity_layout")
        
        self.lb_activity = QtWidgets.QLabel(self.activity_widget)
        self.lb_activity.setText("Активність")
        self.lb_activity.setProperty("type", "page_section")
        self.lb_activity.setObjectName("lb_activity")
        self.activity_layout.addWidget(self.lb_activity, 0, 0, 1, 1)
        
        self.courses_card_widget = QtWidgets.QWidget(self.activity_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.courses_card_widget.setSizePolicy(sizePolicy)
        self.courses_card_widget.setProperty("type", "card")
        self.courses_card_widget.setObjectName("courses_card_widget")
        self.courses_card_layout = QtWidgets.QGridLayout(self.courses_card_widget)
        self.courses_card_layout.setObjectName("courses_card_layout")
        
        self.courses_icon = QtWidgets.QLabel(self.courses_card_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.courses_icon.setSizePolicy(sizePolicy)
        self.courses_icon.setMaximumSize(QtCore.QSize(100, 16777215))
        self.courses_icon.setProperty("type","lb_small")
        self.courses_icon.setStyleSheet("image: url(icon/icon_hat.PNG);")
        self.courses_icon.setText("")
        self.courses_icon.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.courses_icon.setObjectName("courses_icon")
        self.courses_card_layout.addWidget(self.courses_icon, 0, 0, 1, 1)
        
        self.lb_num_of_courses = QtWidgets.QLabel(self.courses_card_widget)
        self.lb_num_of_courses.setText("8")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.lb_num_of_courses.setSizePolicy(sizePolicy)
        self.lb_num_of_courses.setMinimumSize(QtCore.QSize(200, 0))
        self.lb_num_of_courses.setProperty("type","lb_name_lesson")
        self.lb_num_of_courses.setObjectName("lb_num_of_courses")
        self.courses_card_layout.addWidget(self.lb_num_of_courses, 0, 1, 1, 1)
        self.courses_description_label = QtWidgets.QLabel(self.courses_card_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.courses_description_label.sizePolicy().hasHeightForWidth())
        
        self.courses_description_label.setSizePolicy(sizePolicy)
        self.courses_description_label.setMinimumSize(QtCore.QSize(0, 58))
        self.courses_description_label.setProperty("type","lb_name_lesson")
        self.courses_description_label.setObjectName("courses_description_label")
        self.courses_card_layout.addWidget(self.courses_description_label, 1, 0, 1, 2)
        self.activity_layout.addWidget(self.courses_card_widget, 1, 0, 1, 1)
        
        self.lessons_card_widget = QtWidgets.QWidget(self.activity_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lessons_card_widget.sizePolicy().hasHeightForWidth())
        self.lessons_card_widget.setSizePolicy(sizePolicy)
        self.lessons_card_widget.setProperty("type", "card")
        self.lessons_card_widget.setObjectName("lessons_card_widget")
        self.lessons_card_layout = QtWidgets.QGridLayout(self.lessons_card_widget)
        self.lessons_card_layout.setObjectName("lessons_card_layout")
        
        self.lb_num_of_lessons = QtWidgets.QLabel(self.lessons_card_widget)
        self.lb_num_of_lessons.setText("8")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.lb_num_of_lessons.setSizePolicy(sizePolicy)
        self.lb_num_of_lessons.setMinimumSize(QtCore.QSize(200, 0))
        self.lb_num_of_lessons.setProperty("type","lb_name_lesson")
        self.lb_num_of_lessons.setObjectName("lb_num_of_lessons")
        self.lessons_card_layout.addWidget(self.lb_num_of_lessons, 0, 1, 1, 1)
        
        self.lessons_description_label = QtWidgets.QLabel(self.lessons_card_widget)
        self.lessons_description_label.setProperty("type","lb_name_lesson")
        self.lessons_description_label.setObjectName("lessons_description_label")
        self.lessons_card_layout.addWidget(self.lessons_description_label, 1, 0, 1, 2)
        
        self.lessons_icon = QtWidgets.QLabel(self.lessons_card_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.lessons_icon.setSizePolicy(sizePolicy)
        self.lessons_icon.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lessons_icon.setProperty("type","lb_small")
        self.lessons_icon.setStyleSheet("image: url(icon/icon_book2.PNG);")
        self.lessons_icon.setText("")
        self.lessons_icon.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lessons_icon.setObjectName("lessons_icon")
        self.lessons_card_layout.addWidget(self.lessons_icon, 0, 0, 1, 1)
        self.activity_layout.addWidget(self.lessons_card_widget, 1, 1, 1, 1)
        
        self.awards_card_widget = QtWidgets.QWidget(self.activity_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.awards_card_widget.sizePolicy().hasHeightForWidth())
        self.awards_card_widget.setSizePolicy(sizePolicy)
        self.awards_card_widget.setProperty("type", "card")
        self.awards_card_widget.setObjectName("awards_card_widget")
        self.awards_card_layout = QtWidgets.QGridLayout(self.awards_card_widget)
        self.awards_card_layout.setObjectName("awards_card_layout")
        
        self.lb_num_of_awards = QtWidgets.QLabel(self.awards_card_widget)
        self.lb_num_of_awards.setText("8")
        self.lb_num_of_awards.setMinimumSize(QtCore.QSize(200, 0))
        self.lb_num_of_awards.setProperty("type","lb_name_lesson")
        self.lb_num_of_awards.setObjectName("lb_num_of_awards")
        self.awards_card_layout.addWidget(self.lb_num_of_awards, 0, 1, 1, 1)

        self.awards_icon = QtWidgets.QLabel(self.awards_card_widget)
        self.awards_icon.setMaximumSize(QtCore.QSize(100, 16777215))
        self.awards_icon.setProperty("type","lb_small")
        self.awards_icon.setStyleSheet("image: url(icon/icon_award.PNG);")
        self.awards_icon.setText("")
        self.awards_icon.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.awards_icon.setObjectName("awards_icon")
        self.awards_card_layout.addWidget(self.awards_icon, 0, 0, 1, 1)

        self.awards_description_label = QtWidgets.QLabel(self.awards_card_widget)
        self.awards_description_label.setProperty("type","lb_name_lesson")
        self.awards_description_label.setObjectName("awards_description_label")
        
        self.awards_card_layout.addWidget(self.awards_description_label, 1, 0, 1, 2)
        self.activity_layout.addWidget(self.awards_card_widget, 2, 0, 1, 1)
        self.tasks_card_widget = QtWidgets.QWidget(self.activity_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tasks_card_widget.sizePolicy().hasHeightForWidth())
        
        self.tasks_card_widget.setSizePolicy(sizePolicy)
        self.tasks_card_widget.setProperty("type", "card")
        self.tasks_card_widget.setObjectName("tasks_card_widget")
        self.tasks_card_layout = QtWidgets.QGridLayout(self.tasks_card_widget)
        self.tasks_card_layout.setObjectName("tasks_card_layout")
        
        self.lb_num_of_tasks = QtWidgets.QLabel(self.tasks_card_widget)
        self.lb_num_of_tasks.setText("8")
        self.lb_num_of_tasks.setMinimumSize(QtCore.QSize(200, 0))
        self.lb_num_of_tasks.setProperty("type","lb_name_lesson")
        self.lb_num_of_tasks.setObjectName("lb_num_of_tasks")
        self.tasks_card_layout.addWidget(self.lb_num_of_tasks, 0, 1, 1, 1)
        
        self.tasks_icon = QtWidgets.QLabel(self.tasks_card_widget)
        self.tasks_icon.setMaximumSize(QtCore.QSize(100, 16777215))
        self.tasks_icon.setProperty("type","lb_small")
        self.tasks_icon.setStyleSheet("image: url(icon/icon_tasks.PNG);")
        self.tasks_icon.setText("")
        self.tasks_icon.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tasks_icon.setObjectName("tasks_icon")
        self.tasks_card_layout.addWidget(self.tasks_icon, 0, 0, 1, 1)
        
        self.tasks_description_label = QtWidgets.QLabel(self.tasks_card_widget)
        self.tasks_description_label.setProperty("type","lb_name_lesson")
        self.tasks_description_label.setObjectName("tasks_description_label")
        self.tasks_card_layout.addWidget(self.tasks_description_label, 1, 0, 1, 2)
        self.activity_layout.addWidget(self.tasks_card_widget, 2, 1, 1, 1)
        self.main_progress_layout.addWidget(self.activity_widget, 4, 0, 1, 1)
        
        self.courses_success_scroll_area = QtWidgets.QScrollArea(self.pg_progress)
        self.courses_success_scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.courses_success_scroll_area.setWidgetResizable(True)
        self.courses_success_scroll_area.setObjectName("courses_success_scroll_area")
        self.scroll_courses_success_content = QtWidgets.QWidget()
        self.scroll_courses_success_content.setGeometry(QtCore.QRect(0, 0, 664, 341))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        
        self.scroll_courses_success_content.setSizePolicy(sizePolicy)
        self.scroll_courses_success_content.setObjectName("scroll_courses_success_content")
        self.courses_success_layout = QtWidgets.QGridLayout(self.scroll_courses_success_content)
        self.courses_success_layout.setContentsMargins(0, 0, 0, 0)
        self.courses_success_layout.setObjectName("courses_success_layout")
        self.widget_courses_success = QtWidgets.QWidget(self.scroll_courses_success_content)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_courses_success.sizePolicy().hasHeightForWidth())
        
        self.widget_courses_success.setSizePolicy(sizePolicy)
        self.widget_courses_success.setMinimumSize(QtCore.QSize(311, 341))
        self.widget_courses_success.setProperty("type","w_pg")
        self.widget_courses_success.setObjectName("widget_courses_success")
        
        self.courses_success_layout_inner = QtWidgets.QGridLayout(self.widget_courses_success)
        self.courses_success_layout_inner.setContentsMargins(11, 20, 0, 0)
        self.courses_success_layout_inner.setSpacing(0)
        self.courses_success_layout_inner.setObjectName("courses_success_layout_inner")
        
        self.lb_course_success = QtWidgets.QLabel(self.widget_courses_success)
        self.lb_course_success.setText("Успішність по курсах")
        self.lb_course_success.setProperty("type", "page_section")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_course_success.sizePolicy().hasHeightForWidth())
        self.lb_course_success.setSizePolicy(sizePolicy)
        self.lb_course_success.setObjectName("lb_course_success")
        self.courses_success_layout_inner.addWidget(self.lb_course_success, 0, 0, 1, 1)
        
        self.tabs_courses_success = QtWidgets.QTabWidget(self.widget_courses_success)
        self.tabs_courses_success.setMinimumSize(QtCore.QSize(660, 300))
        self.tabs_courses_success.setLayoutDirection(QtCore.Qt.LeftToRight)        
        self.tabs_courses_success.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabs_courses_success.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabs_courses_success.setObjectName("tabs_courses_success")
        
        # Використання функції для створення вкладки з віджетами:
        self.create_tab_with_widgets("1", 13, 3, 5)  
        self.create_tab_with_widgets("2", 25, 10, 5)   

        self.courses_success_layout_inner.addWidget(self.tabs_courses_success, 1, 0, 1, 1)
        self.courses_success_layout.addWidget(self.widget_courses_success, 0, 0, 1, 1)
        self.courses_success_scroll_area.setWidget(self.scroll_courses_success_content)
        self.main_progress_layout.addWidget(self.courses_success_scroll_area, 4, 2, 1, 1)
        
        self.courses_scroll_area = QtWidgets.QScrollArea(self.pg_progress)
        self.courses_scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.courses_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.courses_scroll_area.setWidgetResizable(True)
        self.courses_scroll_area.setObjectName("courses_scroll_area")
        
        self.scroll_courses_content = QtWidgets.QWidget()
        self.scroll_courses_content.setGeometry(QtCore.QRect(0, 0, 685, 341))
        self.scroll_courses_content.setObjectName("scroll_courses_content")
        
        self.courses_layout = QtWidgets.QGridLayout(self.scroll_courses_content)
        self.courses_layout.setContentsMargins(0, 0, 0, 0)
        self.courses_layout.setSpacing(0)
        self.courses_layout.setObjectName("courses_layout")
        
        self.widget_courses_main = QtWidgets.QWidget(self.scroll_courses_content)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_courses_main.sizePolicy().hasHeightForWidth())
        self.widget_courses_main.setSizePolicy(sizePolicy)
        self.widget_courses_main.setMinimumSize(QtCore.QSize(321, 341))
        self.widget_courses_main.setProperty("type","w_pg")
        self.widget_courses_main.setObjectName("widget_courses_main")
        self.courses_main_layout = QtWidgets.QGridLayout(self.widget_courses_main)
        self.courses_main_layout.setObjectName("courses_main_layout")

        labels_data = [
        ("lb_course_1", "Назва курсу 1", 24),
        ("lb_course_2", "Назва курсу 2", 50),
        ("lb_course_3", "Назва курсу 3", 75),
        ("lb_course_4", "Назва курсу 4", 100)
        ]
      
        # Цикл для створення QLabel і ProgressBar
        for idx, (label_name, label_text, progress_value) in enumerate(labels_data):
                label = QtWidgets.QLabel(self.widget_courses_main)
                label.setText(label_text)
                label.setMinimumSize(QtCore.QSize(0, 50))
                label.setMaximumSize(QtCore.QSize(16777215, 50))
                label.setObjectName(label_name)
                label.setProperty("type", "lb_small")
                self.courses_main_layout.addWidget(label, idx * 3, 0, 1, 1)

                progress_bar = QtWidgets.QProgressBar(self.widget_courses_main)
                progress_bar.setMinimumSize(QtCore.QSize(0, 20))
                progress_bar.setMaximumSize(QtCore.QSize(16777215, 20))
                progress_bar.setProperty("value", progress_value)
                progress_bar.setTextVisible(False)
                progress_bar.setOrientation(QtCore.Qt.Horizontal)
                progress_bar.setObjectName(f"pg4_progress{idx+1}")

                lb_interest = QtWidgets.QLabel(self.widget_courses_main)
                lb_interest.setText(f"{progress_value}%")
                lb_interest.setMinimumSize(QtCore.QSize(0, 50))
                lb_interest.setMaximumSize(QtCore.QSize(16777215, 50))
                lb_interest.setObjectName("lb_interest")
                lb_interest.setProperty("type", "lb_small")

                self.courses_main_layout.addWidget(lb_interest, idx * 3 + 1, 2, 1, 1)        
                self.courses_main_layout.addWidget(progress_bar, idx * 3 + 1, 0, 1, 2)

        self.courses_layout.addWidget(self.widget_courses_main, 0, 0, 1, 1)
        self.courses_scroll_area.setWidget(self.scroll_courses_content)
        self.main_progress_layout.addWidget(self.courses_scroll_area, 1, 0, 3, 1)
        
        self.lb_progress = QtWidgets.QLabel(self.pg_progress)
        self.lb_progress.setText("Успішність")
        self.lb_progress.setProperty("type", "title")
        self.lb_progress.setObjectName("lb_progress")

        self.main_progress_layout.addWidget(self.lb_progress, 0, 0, 1, 1)
        self.setLayout(self.main_progress_layout)

    def on_show_event(self, event):
        """Handle show event to refresh progress data"""
        print("Progress page is now visible - loading user progress")
        # Load progress data when widget becomes visible
        self.load_user_progress()

    def load_user_progress(self):
        """Load and display user progress data"""
        try:
            # Clear existing content - Fix the list error by correctly accessing widget children
            try:
                children = self.widget_courses_main.findChildren(QtWidgets.QLabel) + self.widget_courses_main.findChildren(QtWidgets.QProgressBar)
                for child in children:
                    if child:
                        child.deleteLater()
            except Exception as e:
                print(f"Error clearing widgets: {str(e)}")
            
            # Get the current user from the session
            from src.services.session_manager import SessionManager
            session_manager = SessionManager()
            user_data = session_manager.get_current_user_data()
            
            if not user_data or 'id' not in user_data:
                print("No user logged in, can't load progress")
                # Add placeholder content for testing
                self.add_course_info_widget(
                    name="No User Logged In",
                    completed_lessons=0,
                    total_lessons=5,
                    percentage=0
                )
                return
                
            user_id = user_data['id']
            
            # Get all courses
            courses = self.course_service.get_all_courses()
            if not courses:
                print("No courses available")
                return
            
            # Track if any progress was found
            found_progress = False
            
            # Add each course with its progress
            for course in courses:
                try:
                    course_id = str(course.id)
                    # Get progress for this course
                    progress = self.progress_service.get_course_progress(user_id, course_id)
                    
                    if progress:
                        # Get lessons completed
                        lessons = self.lesson_service.get_lessons_by_course_id(course_id)
                        total_lessons = len(lessons) if lessons else 0
                        
                        # Calculate completed lessons based on progress percentage
                        percentage = progress.progress_percentage or 0
                        completed_lessons = int((percentage / 100) * total_lessons) if total_lessons > 0 else 0
                        
                        # Add the course widget with progress
                        self.add_course_info_widget(
                            name=course.name,
                            completed_lessons=completed_lessons,
                            total_lessons=total_lessons,
                            percentage=percentage
                        )
                        found_progress = True
                except Exception as e:
                    print(f"Error processing course {course.name}: {str(e)}")
            
            # If no courses with progress were found, show a message
            if not found_progress:
                self.add_course_info_widget(
                    name="No Courses Started Yet",
                    completed_lessons=0,
                    total_lessons=0,
                    percentage=0
                )
        except Exception as e:
            print(f"Error loading user progress: {str(e)}")
            # Add error message
            self.add_course_info_widget(
                name="Error Loading Progress",
                completed_lessons=0,
                total_lessons=0,
                percentage=0
            )

    def add_course_info_widget(self, name, completed_lessons, total_lessons, percentage):
        """Add a course info widget to the progress page"""
        try:
            # Clear existing items first if there are any
            for i in reversed(range(self.courses_main_layout.count())):
                item = self.courses_main_layout.itemAt(i)
                if item and item.widget():
                    item.widget().deleteLater()
            
            # Create a new course info widget
            label = QtWidgets.QLabel(self.widget_courses_main)
            label.setText(name)
            label.setMinimumSize(QtCore.QSize(0, 50))
            label.setMaximumSize(QtCore.QSize(16777215, 50))
            label.setObjectName(f"lb_course_{name}")
            label.setProperty("type", "lb_small")
            self.courses_main_layout.addWidget(label, 0, 0, 1, 1)
            
            # Create progress bar
            progress_bar = QtWidgets.QProgressBar(self.widget_courses_main)
            progress_bar.setMinimumSize(QtCore.QSize(0, 20))
            progress_bar.setMaximumSize(QtCore.QSize(16777215, 20))
            progress_bar.setProperty("value", percentage)
            progress_bar.setTextVisible(False)
            progress_bar.setOrientation(QtCore.Qt.Horizontal)
            progress_bar.setObjectName(f"pg4_progress_{name}")
            self.courses_main_layout.addWidget(progress_bar, 1, 0, 1, 2)
            
            # Create percentage label
            lb_interest = QtWidgets.QLabel(self.widget_courses_main)
            lb_interest.setText(f"{percentage}% ({completed_lessons}/{total_lessons} lessons)")
            lb_interest.setMinimumSize(QtCore.QSize(0, 50))
            lb_interest.setMaximumSize(QtCore.QSize(16777215, 50))
            lb_interest.setObjectName("lb_interest")
            lb_interest.setProperty("type", "lb_small")
            self.courses_main_layout.addWidget(lb_interest, 1, 2, 1, 1)
            
            return label  # Return the label for reference
        except Exception as e:
            print(f"Error adding course info widget: {str(e)}")
            import traceback
            traceback.print_exc()