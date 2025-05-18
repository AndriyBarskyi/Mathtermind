from PyQt5.QtWidgets import QWidget, QScrollArea,QGridLayout,QVBoxLayout, QLabel,QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QDrag,QPixmap,QIcon
from graphs import *
from tasks import *
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
        self.task_tabs.addTab(self.theory_tab, "Theory")
        self.task_tabs.addTab(self.exercises_tab, "Exercises")
        self.task_tabs.addTab(self.practice_tab, "Practice")
        
        self.task_tabs_layout.addWidget(self.task_tabs, 0, 0, 1, 1)
        self.task_scroll_layout.addWidget(self.tab_container_widget, 0, 0, 1, 1)
        self.task_section_scroll_area.setWidget(self.scroll_task_section_content)
        self.main_content_layout.addWidget(self.task_section_scroll_area, 3, 0, 1, 1)
        
        # Add tools and navigation widget
        self.tools_widget = QtWidgets.QWidget()
        tools_layout = QtWidgets.QHBoxLayout(self.tools_widget)
        
        self.backButton = QtWidgets.QPushButton("Back to Lessons")
        self.backButton.setProperty("type", "start_continue")
        self.backButton.setFixedWidth(150)
        self.backButton.clicked.connect(self.go_back_to_lessons)
        tools_layout.addWidget(self.backButton)
        
        # Progress widget instead of complete button
        self.progress_widget = QtWidgets.QWidget()
        self.progress_widget.setProperty("type", "w_pg")
        progress_layout = QtWidgets.QVBoxLayout(self.progress_widget)
        
        # Progress labels
        self.progress_status = QtWidgets.QLabel("Progress: 0%")
        self.progress_status.setProperty("type", "lb_name_lesson")
        progress_layout.addWidget(self.progress_status)
        
        # Progress bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        
        # Complete Lesson button
        self.complete_button = QtWidgets.QPushButton("Complete Lesson")
        self.complete_button.setProperty("type", "start_continue")
        self.complete_button.clicked.connect(self.manual_complete_lesson)
        progress_layout.addWidget(self.complete_button)
        
        # Info container
        info_container = QtWidgets.QWidget()
        info_layout = QtWidgets.QHBoxLayout(info_container)
        info_layout.setContentsMargins(0, 0, 0, 0)
        
        # Lesson metadata
        self.lb_difficulty = QtWidgets.QLabel("Difficulty: Basic")
        self.lb_difficulty.setProperty("type", "lb_small")
        info_layout.addWidget(self.lb_difficulty)
        
        self.lb_time = QtWidgets.QLabel("30 min")
        self.lb_time.setProperty("type", "lb_small")
        info_layout.addWidget(self.lb_time)
        
        progress_layout.addWidget(info_container)
        
        self.main_content_layout.addWidget(self.tools_widget, 0, 0, 1, 1)
        self.main_content_layout.addWidget(self.progress_widget, 4, 0, 1, 1)
        
        self.title_main_lb = QtWidgets.QLabel(self.main_scroll_content)
        self.title_main_lb.setObjectName("title_main_lb")
        self.main_content_layout.addWidget(self.title_main_lb, 0, 0, 1, 1)
        self.main_scroll_area.setWidget(self.main_scroll_content)
        
        self.main_grid_layout.addWidget(self.main_scroll_area, 0, 0, 1, 1)
        
        self.setLayout(self.main_grid_layout)
        
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
                        self.progress_status.setText("Progress: 100%")
                        self.complete_button.setText("Lesson Completed ✓")
                        self.complete_button.setEnabled(False)
                    else:
                        # Set initial progress value
                        self.progress_bar.setValue(0)
                        self.progress_status.setText("Progress: 0%")
                        self.complete_button.setText("Complete Lesson")
                        self.complete_button.setEnabled(True)
                    
                    # Create theory content HTML
                    content_html = f"<h2>{lesson.title}</h2>"
                    
                    # Add more content details if available 
                    if hasattr(lesson, 'description') and lesson.description:
                        content_html += f"<p>{lesson.description}</p>"
                    else:
                        content_html += "<p>This lesson will guide you through important concepts and exercises.</p>"
                    
                    # Add lesson-specific theory content
                    lesson_number = lesson.lesson_order if hasattr(lesson, 'lesson_order') else 1
                    
                    if lesson_number == 1:
                        content_html += """
                        <h3>Introduction to the Concepts</h3>
                        <p>In this lesson, we'll learn the fundamental concepts that form the foundation of this subject.</p>
                        <p>Key points to understand:</p>
                        <ul>
                            <li>Basic definitions and properties</li>
                            <li>Core principles and applications</li>
                            <li>Problem-solving approaches</li>
                        </ul>
                        <p>Let's begin by exploring the basics...</p>
                        <h4>Core Principles</h4>
                        <p>The main principle we need to understand is how different elements interact with each other.</p>
                        <p>When we study these interactions, we discover patterns that help us predict outcomes and solve problems.</p>
                        """
                    elif lesson_number == 2:
                        content_html += """
                        <h3>Advanced Applications</h3>
                        <p>Now that we understand the basics, let's explore more advanced applications.</p>
                        <p>These applications demonstrate how the concepts can be used to solve real-world problems:</p>
                        <ol>
                            <li>Pattern recognition in complex systems</li>
                            <li>Optimization techniques for efficiency</li>
                            <li>Predictive modeling based on historical data</li>
                        </ol>
                        <p>Let's examine each of these in detail...</p>
                        """
                    elif lesson_number == 3:
                        content_html += """
                        <h3>Practical Implementation</h3>
                        <p>In this final section, we'll focus on practical implementation of what we've learned.</p>
                        <p>The key steps in implementing these concepts are:</p>
                        <ol>
                            <li>Analyzing the problem domain</li>
                            <li>Identifying the appropriate techniques</li>
                            <li>Applying the methods systematically</li>
                            <li>Evaluating results and iterating as needed</li>
                        </ol>
                        <p>Let's practice with some realistic scenarios...</p>
                        """
                    else:
                        content_html += """
                        <h3>Exploring the Topic</h3>
                        <p>In this lesson, we'll delve deeper into specialized areas of the subject.</p>
                        <p>We'll examine both theoretical foundations and practical applications.</p>
                        <p>By the end, you should be able to:</p>
                        <ul>
                            <li>Understand complex relationships between key concepts</li>
                            <li>Apply specialized techniques to solve domain-specific problems</li>
                            <li>Evaluate the effectiveness of different approaches</li>
                        </ul>
                        """
                        
                    # Render the theory content
                    self.lesson_text.setHtml(content_html)
                    
                    # Set difficulty level
                    difficulty = self._get_difficulty_text(lesson)
                    self.lb_difficulty.setText(f"Difficulty: {difficulty}")
                    
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
                    self.lesson_text.setHtml(f"<h2>Lesson Not Found</h2><p>The lesson with ID {lesson_id} could not be found.</p>")
                    self.tools_widget.setVisible(True)
                    self.progress_widget.setVisible(False)
            except Exception as e:
                print(f"Error loading lesson data: {str(e)}")
                self.lesson_text.setHtml(f"<h2>Error Loading Lesson</h2><p>An error occurred while loading the lesson: {str(e)}</p>")
                self.tools_widget.setVisible(True)
                self.progress_widget.setVisible(False)
        else:
            # No lesson ID provided, show placeholder
            self.lesson_text.setHtml(f"<h2>{title}</h2><p>No lesson data available. Please select a lesson from the course page.</p>")
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
                {"question": "What is the main principle discussed in this lesson?", 
                 "options": ["Element interactions", "Statistical analysis", "Quantum theory", "Economic models"],
                 "correct": 0},
                {"question": "Which of these is NOT mentioned as a key point in the lesson?", 
                 "options": ["Basic definitions", "Core principles", "Problem-solving approaches", "Historical context"],
                 "correct": 3},
                {"question": "According to the lesson, what helps us predict outcomes?", 
                 "options": ["Random guessing", "Pattern recognition", "Computer algorithms", "Personal intuition"],
                 "correct": 1},
                {"question": "How many core points are listed in the introduction?", 
                 "options": ["2", "3", "4", "5"],
                 "correct": 1},
                {"question": "What is the main focus of this lesson?", 
                 "options": ["Advanced applications", "Practical implementation", "Introduction to concepts", "Historical development"],
                 "correct": 2}
            ]
        elif lesson_number == 2:
            exercise_data = [
                {"question": "What is the main focus of this lesson?", 
                 "options": ["Basic concepts", "Advanced applications", "Historical development", "Future predictions"],
                 "correct": 1},
                {"question": "How many applications are specifically listed in the lesson?", 
                 "options": ["2", "3", "4", "5"],
                 "correct": 1},
                {"question": "Which of these is NOT mentioned as an application in the lesson?", 
                 "options": ["Pattern recognition", "Optimization techniques", "Predictive modeling", "Resource allocation"],
                 "correct": 3},
                {"question": "What type of data is mentioned for predictive modeling?", 
                 "options": ["Future data", "Real-time data", "Historical data", "Simulated data"],
                 "correct": 2},
                {"question": "What kind of systems are mentioned in relation to pattern recognition?", 
                 "options": ["Simple systems", "Complex systems", "Linear systems", "Closed systems"],
                 "correct": 1}
            ]
        else:
            exercise_data = [
                {"question": "What is the main focus of this lesson?", 
                 "options": ["Theoretical foundations", "Historical context", "Practical implementation", "Future developments"],
                 "correct": 2},
                {"question": "How many key steps are listed for implementation?", 
                 "options": ["2", "3", "4", "5"],
                 "correct": 2},
                {"question": "Which step comes first in the implementation process?", 
                 "options": ["Applying methods", "Evaluating results", "Identifying techniques", "Analyzing the problem domain"],
                 "correct": 3},
                {"question": "What is the last step in the implementation process?", 
                 "options": ["Analyzing the problem", "Evaluating results", "Applying methods", "Identifying techniques"],
                 "correct": 1},
                {"question": "According to the lesson, what should you do after evaluating results?", 
                 "options": ["Start a new project", "Document findings", "Iterate as needed", "Present conclusions"],
                 "correct": 2}
            ]
            
        # Create exercise widgets
        for i, exercise in enumerate(exercise_data):
            exercise_widget = QtWidgets.QGroupBox(f"Exercise {i+1}")
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
            check_button = QtWidgets.QPushButton("Check Answer")
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
        practice_html = f"<h2>Practice Activities</h2>"
        
        if lesson_number == 1:
            practice_html += """
            <h3>Interactive Exercise</h3>
            <p>Try to solve these problems on your own for practice:</p>
            <div style="background-color: #f5f5f5; padding: 10px; border-left: 4px solid #007bff;">
                <p><strong>Scenario:</strong> You are analyzing a dataset of customer interactions with a website. 
                Your task is to identify patterns that could predict customer behavior.</p>
                
                <p><strong>Think about:</strong></p>
                <ol>
                    <li>What patterns might you look for in the data?</li>
                    <li>How could each pattern be used to predict future behavior?</li>
                    <li>How would you validate your predictions?</li>
                </ol>
            </div>
            
            <h3>Reflection Points</h3>
            <p>Consider these questions as you learn:</p>
            <ol>
                <li>How do the concepts from this lesson relate to your own experiences?</li>
                <li>What challenges might you face when applying these concepts?</li>
                <li>What additional information would help you better understand these concepts?</li>
            </ol>
            """
        elif lesson_number == 2:
            practice_html += """
            <h3>Case Study Exploration</h3>
            <p>Review this case study and think about the questions:</p>
            <div style="background-color: #f5f5f5; padding: 10px; border-left: 4px solid #007bff;">
                <p><strong>Case Study:</strong> A transportation company is trying to optimize their delivery routes to minimize fuel consumption and delivery time.</p>
                
                <p><strong>Questions to consider:</strong></p>
                <ol>
                    <li>Which optimization techniques from the lesson would be most applicable?</li>
                    <li>What data would you need to collect to implement your solution?</li>
                    <li>How would you measure the success of your optimization efforts?</li>
                    <li>What challenges might you encounter during implementation?</li>
                </ol>
            </div>
            
            <h3>Interactive Simulation</h3>
            <p>Explore these concepts with an interactive simulation:</p>
            <div style="background-color: #e6f7ff; padding: 10px; border-left: 4px solid #0099cc;">
                <p>Visit <a href="https://phet.colorado.edu/en/simulations/category/math">PhET Math Simulations</a> to explore interactive models related to this topic.</p>
                <p>These simulations allow you to experiment with concepts and see immediate results without needing evaluation.</p>
            </div>
            """
        else:
            practice_html += """
            <h3>Guided Self-Assessment</h3>
            <p>Test your understanding with these self-assessment questions:</p>
            <div style="background-color: #f5f5f5; padding: 10px; border-left: 4px solid #007bff;">
                <p><strong>Problem:</strong> You're helping an organization implement the techniques discussed in this lesson.</p>
                
                <p><strong>Consider these points:</strong></p>
                <ol>
                    <li>How would you create an implementation plan following the steps in the lesson?</li>
                    <li>What timeline and milestones would be appropriate?</li>
                    <li>Who are the potential stakeholders and what roles would they play?</li>
                    <li>How would you monitor progress and measure outcomes?</li>
                </ol>
            </div>
            
            <h3>Interactive Resources</h3>
            <p>Explore these additional resources to deepen your understanding:</p>
            <ul>
                <li><a href="https://www.khanacademy.org/math">Khan Academy Math</a> - Free practice exercises and videos</li>
                <li><a href="https://www.geogebra.org/">GeoGebra</a> - Interactive mathematical tools</li>
                <li><a href="https://www.wolframalpha.com/">Wolfram Alpha</a> - Computational knowledge engine</li>
            </ul>
            """
            
        # Create a text browser to display the practice content
        practice_browser = QtWidgets.QTextBrowser()
        practice_browser.setOpenExternalLinks(True)
        practice_browser.setHtml(practice_html)
        
        # Add "Complete Section" button that automatically marks progress
        complete_button = QtWidgets.QPushButton("Complete Practice Section")
        complete_button.setProperty("type", "start_continue")
        complete_button.clicked.connect(self.complete_practice_section)
        
        # Add widgets to the practice tab
        self.practice_layout.addWidget(practice_browser)
        self.practice_layout.addWidget(complete_button)
    
    def check_exercise_answer(self, button, option_group, result_label):
        """Check if the selected answer is correct"""
        selected_button = option_group.checkedId()
        correct_answer = button.property("correct_answer")
        exercise_index = button.property("exercise_index")
        
        if selected_button == -1:
            # No option selected
            result_label.setText("Please select an answer")
            result_label.setStyleSheet("color: orange;")
            result_label.setVisible(True)
            return
            
        if selected_button == correct_answer:
            # Correct answer
            result_label.setText("Correct! ✓")
            result_label.setStyleSheet("color: green;")
            
            # Mark this exercise as completed if not already
            if not button.property("completed"):
                button.setProperty("completed", True)
                self.completed_exercises += 1
                self.update_progress()
        else:
            # Wrong answer
            result_label.setText("Incorrect. Try again.")
            result_label.setStyleSheet("color: red;")
            
        result_label.setVisible(True)
    
    def complete_practice_section(self):
        """Handle completion of practice section"""
        # Mark practice as completed
        self.completed_exercises += 1
        self.update_progress()
        
        # Show confirmation
        QtWidgets.QMessageBox.information(
            self,
            "Section Completed",
            "Great job exploring this practice section!"
        )
    
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
        self.progress_status.setText(f"Progress: {total_progress}%")
        
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
                    "Lesson Completed", 
                    f"Congratulations! You've completed the lesson: {lesson.title}"
                )
        except Exception as e:
            print(f"Error completing lesson: {str(e)}")
    
    def manual_complete_lesson(self):
        """Handle the manual completion of a lesson via the complete button"""
        if not self.current_lesson_id:
            QtWidgets.QMessageBox.warning(
                self,
                "No Lesson Selected",
                "Please select a lesson first."
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
                    "Not Logged In",
                    "You need to be logged in to complete lessons."
                )
                return
                
            user_id = user_data['id']
            
            # Get lesson details
            lesson = self.lesson_service.get_lesson_by_id(self.current_lesson_id)
            if not lesson:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Lesson Not Found",
                    "The selected lesson could not be found."
                )
                return
                
            # Check if already completed
            is_completed = self.progress_service.has_completed_lesson(user_id, self.current_lesson_id)
            if is_completed:
                QtWidgets.QMessageBox.information(
                    self,
                    "Already Completed",
                    f"You have already completed this lesson: {lesson.title}"
                )
                return
                
            # Ask for confirmation
            reply = QtWidgets.QMessageBox.question(
                self,
                "Complete Lesson",
                f"Are you sure you want to mark this lesson as completed: {lesson.title}?",
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
                    self.complete_button.setText("Lesson Completed ✓")
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
                        "Error",
                        "Failed to mark the lesson as completed. Please try again."
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
            return "Basic"
            
        # Handle if it's an enum
        if hasattr(difficulty, 'value'):
            difficulty_value = difficulty.value
            # Translate Ukrainian to English if needed
            if difficulty_value == "Базовий":
                return "Basic"
            elif difficulty_value == "Середній":
                return "Medium"
            elif difficulty_value == "Досвідчений":
                return "Advanced"
            return difficulty_value
            
        # Handle if it's a string
        difficulty_str = str(difficulty)
        if difficulty_str.lower() in ["basic", "beginner", "базовий"]:
            return "Basic"
        elif difficulty_str.lower() in ["medium", "intermediate", "середній"]:
            return "Medium"
        elif difficulty_str.lower() in ["advanced", "expert", "досвідчений"]:
            return "Advanced"
            
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
    