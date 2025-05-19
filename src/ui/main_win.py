from PyQt5.QtWidgets import QWidget, QGridLayout,QVBoxLayout, QLabel,QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from circular_progress import *
from graphs import *
from lesson_win import Lesson_page
from src.services.course_service import CourseService
from src.services.progress_service import ProgressService
from src.services.lesson_service import LessonService
from src.services.session_manager import SessionManager
import random
from datetime import datetime, timedelta, date as dt_date
import pyqtgraph as pg


class ClickFilter(QtCore.QObject):
    clicked = QtCore.pyqtSignal()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self.clicked.emit()
        return False 
    

class Main_page(QWidget):
    def __init__(self, stack=None, lesson_page=None):
        super().__init__()
        self.stack = stack
        self.lesson_page = lesson_page
        
        # Initialize services
        self.progress_service = ProgressService()
        self.course_service = CourseService()
        self.lesson_service = LessonService()
        
        # Connect to show event to refresh data when page becomes visible
        self.showEvent = self.on_show_event
        
        self.pg_main = QtWidgets.QWidget(self)
        self.pg_main.setObjectName("pg_main")
        self.main_layout = QtWidgets.QGridLayout(self.pg_main)
        self.main_layout.setObjectName("main_layout")
        self.main_layout.setContentsMargins(15, 2, 15, 2) # left, top, right, bottom
        self.main_layout.setVerticalSpacing(2) # Explicitly set main layout vertical spacing
        
        # Set column stretches if needed (e.g., column 0 wider than column 1)
        self.main_layout.setColumnStretch(0, 2) # Main content column (Continue, Courses)
        self.main_layout.setColumnStretch(1, 1) # Side content column (Recommended, Activity)

        # Set row stretches for vertical distribution
        self.main_layout.setRowStretch(0, 0)  # Title row "Головна" - minimal stretch
        self.main_layout.setRowStretch(1, 1)  # Row for "Continue Viewing" and "Recommended"
        self.main_layout.setRowStretch(2, 1)  # Row for "Courses" and "Activity"
        # Add a final row stretch to push content up if there's lots of empty space
        # However, if the goal is to fill space, this might be counterproductive unless sections have max heights.
        # Let's rely on Expanding size policies for now.
        # self.main_layout.setRowStretch(3, 10) 

        self.continue_viewing_section = QtWidgets.QWidget(self.pg_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.continue_viewing_section.sizePolicy().hasHeightForWidth())
        self.continue_viewing_section.setSizePolicy(sizePolicy)
        # Adjusted min and max height for "Continue Viewing" section
        self.continue_viewing_section.setMinimumSize(QtCore.QSize(900, 200)) # Reduced minimum height
        self.continue_viewing_section.setMaximumSize(QtCore.QSize(16777215, 250)) # Set a maximum height 
        self.continue_viewing_section.setObjectName("continue_viewing_section")
        self.continue_viewing_section.setProperty("type", "w_pg")
        self.grid_continue_section = QtWidgets.QGridLayout(self.continue_viewing_section)
        self.grid_continue_section.setObjectName("grid_continue_section")
        self.grid_continue_section.setContentsMargins(15, 5, 15, 5) # Reduced top/bottom margins
        
        self.continue_viewing_label = QtWidgets.QLabel(self.continue_viewing_section)
        self.continue_viewing_label.setText("Продовжити перегляд")
        self.continue_viewing_label.setProperty("type", "page_section")
        self.continue_viewing_label.setMinimumSize(QtCore.QSize(0, 30)) # Ensure min height
        self.continue_viewing_label.setMaximumSize(QtCore.QSize(16777215, 30)) # Reduced max height
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
        self.btn_scroll_next.setText("→")
        self.btn_scroll_next.setFixedSize(40, 40)
        self.btn_scroll_next.setStyleSheet(""" 
            QPushButton {
                border: 1px solid #cccccc;
                background-color: transparent;
                border-radius: 20px;
                font-size: 22px; /* Increased font size for arrow visibility */
                padding: 0px; /* Helps with centering */
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
        """)
        self.btn_scroll_next.setObjectName("btn_scroll_next")
        self.grid_continue_section.addWidget(self.btn_scroll_next, 1, 2, 1, 1)
        
        self.btn_scroll_prev = QtWidgets.QPushButton(self.continue_viewing_section)
        self.btn_scroll_prev.setProperty("type", "next_previous")
        self.btn_scroll_prev.setText("←")
        self.btn_scroll_prev.setFixedSize(40, 40)
        self.btn_scroll_prev.setStyleSheet("""
            QPushButton {
                border: 1px solid #cccccc;
                background-color: transparent;
                border-radius: 20px;
                font-size: 22px; /* Increased font size for arrow visibility */
                padding: 0px; /* Helps with centering */
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
        """)
        self.btn_scroll_prev.setObjectName("btn_scroll_prev")
        self.grid_continue_section.addWidget(self.btn_scroll_prev, 1, 0, 1, 1)
        self.main_layout.addWidget(self.continue_viewing_section, 1, 0, 1, 1)
        
        self.courses_section = QtWidgets.QWidget(self.pg_main)
        self.courses_section.setSizePolicy(sizePolicy)
        self.courses_section.setProperty("type", "w_pg")
        # Adjusted minimum height to better accommodate 2 rows of 180px + title + spacing
        self.courses_section.setMinimumSize(QtCore.QSize(900, 10)) # TEMPORARY TEST: Drastically reduced minimum height
        self.courses_section.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.courses_section.setObjectName("courses_section")
        
        self.gridLayout_14 = QtWidgets.QGridLayout(self.courses_section)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.gridLayout_14.setVerticalSpacing(5) # Match other sections (e.g., lb_activity)
        # self.gridLayout_14.setHorizontalSpacing(10) # Keep as default or adjust if needed
        self.gridLayout_14.setContentsMargins(15, 5, 15, 5) # Match other sections (e.g., lb_activity)

        self.lb_my_courses = QtWidgets.QLabel(self.courses_section)
        self.lb_my_courses.setMaximumSize(QtCore.QSize(16777215, 30)) # Changed from 28 to 30
        self.lb_my_courses.setMinimumSize(QtCore.QSize(0, 30)) # Changed from 28 to 30
        self.lb_my_courses.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed) # Ensure vertical policy is Fixed
        self.lb_my_courses.setText("Курси")
        self.lb_my_courses.setProperty("type", "page_section")
        self.lb_my_courses.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        # self.lb_my_courses.setStyleSheet("background-color: lime;") # TEMPORARY DEBUGGING

        self.gridLayout_14.addWidget(self.lb_my_courses, 0, 0, 1, self.gridLayout_14.columnCount() or 4)
        
        # Set row stretches: title row less stretch, course rows more stretch
        self.gridLayout_14.setRowStretch(0, 0) # Title row - minimal stretch
        self.gridLayout_14.setRowStretch(1, 1) # First row of courses
        self.gridLayout_14.setRowStretch(2, 1) # Second row of courses
        # Add a stretch factor for any potential space below the courses if needed
        # self.gridLayout_14.setRowStretch(3, 10) 

        course_names = [
            "Python для початківців",
            "Основи веб-розробки",
            "Алгоритми і структури даних",
            "Бази даних",
            "Машинне навчання",
            "Штучний інтелект",
            "Frontend розробка",
            "Backend розробка"
        ]
        for i in range(1, 9):
            course_widget = QWidget(self.courses_section)
            layout = QVBoxLayout(course_widget)
            layout.setContentsMargins(layout.contentsMargins().left(), 0, layout.contentsMargins().right(), layout.contentsMargins().bottom()) # Set top margin to 0
            layout.setAlignment(QtCore.Qt.AlignCenter)
            course_widget.setMinimumSize(180, 180) 
            course_widget.setMaximumSize(180, 180) 
            course_widget.setProperty("type","transparent_widget")

            course_label = QLabel(course_names[i-1])
            course_label.setAlignment(QtCore.Qt.AlignCenter)
            course_label.setProperty("type", "lb_small")
            course_label.setMinimumWidth(150)
            course_label.setMaximumWidth(170)
            course_label.setWordWrap(True)

            circular_progress = CircularProgress(course_widget)
            circular_progress.setObjectName(f"circular_progress_{i}")
            circular_progress.setToolTip(f"Це {circular_progress.objectName()}")
            circular_progress.setMinimumSize(140, 140)
            circular_progress.setMaximumSize(140, 140)
            circular_progress.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            circular_progress.set_value(i * 10) 

            layout.addWidget(course_label)
            layout.addWidget(circular_progress)

            row = (i - 1) // 4 + 1
            col = (i - 1) % 4
            self.gridLayout_14.addWidget(course_widget, row, col, 1, 1)
            
        self.main_layout.addWidget(self.courses_section, 2, 0, 1, 1)
        self.activity_section = QtWidgets.QWidget(self.pg_main)
        self.activity_section.setSizePolicy(sizePolicy)
        self.activity_section.setMinimumSize(QtCore.QSize(312, 340))
        self.activity_section.setMaximumSize(QtCore.QSize(500, 16777215))
        self.activity_section.setProperty("type", "w_pg")
        self.activity_section.setObjectName("activity_section")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.activity_section)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.gridLayout_13.setContentsMargins(15, 5, 15, 5)
        
        # Activity section header
        self.lb_activity = QtWidgets.QLabel(self.activity_section)
        self.lb_activity.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Work Sans")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.lb_activity.setFont(font)
        self.lb_activity.setText("Активність")
        self.lb_activity.setObjectName("lb_activity")
        self.gridLayout_13.addWidget(self.lb_activity, 0, 0, 1, 1)
        
        # Replace static_activity_label with pg.PlotWidget
        self.plot = pg.PlotWidget(self.activity_section) # Create PlotWidget as child of activity_section
        self.plot.setObjectName("activity_plot_widget")
        # Ensure plot expands:
        sizePolicyPlot = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.plot.setSizePolicy(sizePolicyPlot)
        self.plot.setMinimumSize(QtCore.QSize(0, 260)) # Match old label's min height for now
        self.gridLayout_13.addWidget(self.plot, 1, 0, 1, 1) # Add plot to the grid
        
        self.recommended_section = QtWidgets.QWidget(self.pg_main)
        # Match size policy of other expanding sections
        sizePolicyRec = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicyRec.setHorizontalStretch(0)
        sizePolicyRec.setVerticalStretch(0)
        sizePolicyRec.setHeightForWidth(self.recommended_section.sizePolicy().hasHeightForWidth())
        self.recommended_section.setSizePolicy(sizePolicyRec)

        self.recommended_section.setMinimumSize(QtCore.QSize(300, 200)) # Added minimum size
        self.recommended_section.setMaximumSize(QtCore.QSize(500, 250)) # Set maximum height, width was 500
        self.recommended_section.setProperty("type", "w_pg")
        self.recommended_section.setObjectName("recommended_section")
        self.grid_rec_activity_section = QtWidgets.QGridLayout(self.recommended_section)
        self.grid_rec_activity_section.setObjectName("grid_rec_activity_section")
        self.grid_rec_activity_section.setContentsMargins(15, 5, 15, 5) # Reduced top/bottom margins
        
        self.recommended_label = QtWidgets.QLabel(self.recommended_section)
        self.recommended_label.setText("Можливо цікавить")
        self.recommended_label.setProperty("type", "page_section")
        self.recommended_label.setMinimumSize(QtCore.QSize(0,30)) # Ensure min height
        self.recommended_label.setMaximumSize(QtCore.QSize(16777215,30)) # Set max height
        self.recommended_label.setObjectName("recommended_label")
        self.grid_rec_activity_section.addWidget(self.recommended_label, 0, 0, 1, 1)
        
        self.recommended_graph_widget = QtWidgets.QWidget(self.recommended_section) 
        # Adjusted minimum height for the graph widget inside recommended_section
        self.recommended_graph_widget.setMinimumSize(QtCore.QSize(0, 150)) # Reduced from 275
        self.recommended_graph_widget.setObjectName("recommended_graph_widget")
        self.recommended_graph_widget.setProperty("type", "w_pg")
        
        # Add layout to recommended_graph_widget
        self.recommended_graph_widget_layout = QtWidgets.QVBoxLayout(self.recommended_graph_widget)
        self.recommended_graph_widget_layout.setContentsMargins(0, 5, 0, 5) # Small vertical margins
        self.recommended_graph_widget_layout.setSpacing(10) # Spacing between recommended items
        self.recommended_graph_widget.setLayout(self.recommended_graph_widget_layout)

        self.grid_rec_activity_section.addWidget(self.recommended_graph_widget, 1, 0, 1, 1)
        self.main_layout.addWidget(self.recommended_section, 1, 1, 1, 1)
        
        # Add the activity section to the main layout
        self.main_layout.addWidget(self.activity_section, 2, 1, 1, 1)
        
        self.title_main_lb = QtWidgets.QLabel(self.pg_main)
        self.title_main_lb.setText("Головна")
        self.title_main_lb.setProperty("type", "title")
        self.title_main_lb.setObjectName("title_main_lb")
        self.main_layout.addWidget(self.title_main_lb, 0, 0, 1, 1) # Title only in first column now
        self.setLayout(self.main_layout)

        self.btn_scroll_next.clicked.connect(self.scroll_right)
        self.btn_scroll_prev.clicked.connect(self.scroll_left)
        self.continue_viewing_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Initialize the components in the main window
        # This includes setting up the activity section
        self.initialize_components()

    def initialize_components(self):
        """Initialize and set up UI components safely"""
        print("Initializing main window components")
        
        try:
            # Set up the activity section title label
            if hasattr(self, 'lb_activity'):
                self.lb_activity.setText("Активність")
            
            # self.plot is initialized in setupUi and data loaded by on_show_event
            # No specific initialization for self.plot needed here beyond what setupUi does.

        except Exception as e:
            print(f"Error initializing components: {str(e)}")
            import traceback
            traceback.print_exc()

    def scroll_left(self):
        scroll_bar = self.continue_viewing_scroll_area.horizontalScrollBar()
        scroll_bar.setValue(scroll_bar.value() - 150)

    def scroll_right(self):
        scroll_bar = self.continue_viewing_scroll_area.horizontalScrollBar()
        scroll_bar.setValue(scroll_bar.value() + 150)
    
    def on_lesson_click(self, widget):
        lesson_id = widget.property("lesson_id")
        lesson_title = widget.property("lesson_title")
        
        if lesson_id and self.lesson_page and self.stack:
            print(f"Opening lesson: {lesson_title} (ID: {lesson_id})")
            self.lesson_page.set_lesson_data(lesson_title, lesson_id)
            self.stack.setCurrentWidget(self.lesson_page)
        else:
            print(f"Could not open lesson. Lesson ID: {lesson_id}, Lesson Page: {self.lesson_page}, Stack: {self.stack}")

    def on_show_event(self, event):
        """Handle show event to refresh progress data"""
        print("Main page is now visible - attempting to refresh data")
        
        try:
            print("Loading recent lessons")
            self.load_recent_lessons()
        except Exception as e:
            print(f"Error loading recent lessons: {str(e)}")
            import traceback
            traceback.print_exc()
            
        try:
            print("Loading courses section data")
            self.load_courses_section_data()
        except Exception as e:
            print(f"Error loading courses section data: {str(e)}")
            import traceback
            traceback.print_exc()

        try:
            print("Loading recommended courses data")
            self.load_recommended_courses_data()
        except Exception as e:
            print(f"Error loading recommended courses data: {str(e)}")
            import traceback
            traceback.print_exc()
            
        try:
            print("Loading activity data")
            self.load_activity_data()
        except Exception as e:
            print(f"Error loading activity data: {str(e)}")
            import traceback
            traceback.print_exc()
        
        super().showEvent(event) # Call base class showEvent if necessary

    def load_activity_data(self):
        print("Attempting to load activity data for the last 7 days...")
        try:
            session_manager = SessionManager()
            user_data = session_manager.get_current_user_data()

            self.plot.clear()
            plot_item = self.plot.getPlotItem()
            # Explicitly clear items from the PlotItem
            if plot_item:
                plot_item.clear() # Clears axes, data items, legend, etc. from the PlotItem
            
            self.plot.setBackground('w') 
            plot_item.getViewBox().setBorder(None)

            if not user_data or 'id' not in user_data:
                print("No user logged in, can't load activity data.")
                plot_item.setTitle("Будь ласка, увійдіть, щоб побачити активність", color=(120,120,120), size="10pt")
                return
            
            user_id = user_data['id']
            print(f"Activity data: User ID: {user_id}")

            completed_lessons = self.progress_service.get_user_completed_lessons(user_id)
            print(f"Fetched {len(completed_lessons)} total completed lessons for user {user_id}.")
            
            today = dt_date.today()
            activity_counts = {today - timedelta(days=i): 0 for i in range(6, -1, -1)} 

            for lesson in completed_lessons:
                if hasattr(lesson, 'completed_at') and lesson.completed_at:
                    completion_datetime = lesson.completed_at
                    if isinstance(completion_datetime, str):
                        try:
                            completion_datetime = datetime.fromisoformat(completion_datetime.replace('Z', '+00:00')) # Handle Z for UTC
                        except ValueError:
                            print(f"Warning: Could not parse date string {completion_datetime} for lesson {lesson.id}")
                            continue
                    
                    if completion_datetime.tzinfo is not None:
                        completion_date = completion_datetime.astimezone(None).date()
                    else: 
                        completion_date = completion_datetime.date()

                    if completion_date in activity_counts:
                        activity_counts[completion_date] += 1
            
            print(f"Processed activity_counts: {activity_counts}")

            sorted_dates = sorted(activity_counts.keys())
            
            day_names_map = {0: "Пн", 1: "Вт", 2: "Ср", 3: "Чт", 4: "Пт", 5: "Сб", 6: "Нд"}
            labels = [day_names_map[d.weekday()] for d in sorted_dates]
            data = [activity_counts[d] for d in sorted_dates]

            print(f"Activity data for plotting: Labels: {labels}, Counts: {data}")
            
            self.plot.setMouseEnabled(x=False, y=False)

            if any(d > 0 for d in data): 
                left_axis = plot_item.getAxis('left')
                left_axis.setLabel("Уроки", units='')
                left_axis.setPen(None) 
                left_axis.setTextPen(pg.mkPen(color=(80, 80, 80)))
                
                max_val = max(data) if data and max(data) > 0 else 1 
                
                y_ticks_values = list(range(0, int(max_val) + 2, max(1, int(max_val / 4) if max_val > 3 else 1)))
                if not y_ticks_values or (y_ticks_values and max_val > 0 and y_ticks_values[-1] < max_val):
                     y_ticks_values.append(int(max_val)+1)
                if y_ticks_values and y_ticks_values[0] !=0 and 0 not in y_ticks_values : # Ensure 0 is a tick if not present
                     y_ticks_values = [0] + y_ticks_values
                y_ticks_values = sorted(list(set(y_ticks_values))) # Ensure unique and sorted
                
                y_ticks = [[(i, str(i)) for i in y_ticks_values if i >= 0]] # Only non-negative ticks
                left_axis.setTicks(y_ticks)

                bar_color = pg.mkColor('#516ed9') 
                bar_graph_item = pg.BarGraphItem(x=range(len(data)), height=data, width=0.6, brush=bar_color)
                self.plot.addItem(bar_graph_item)

                x_axis = plot_item.getAxis('bottom')
                x_axis.setPen(None) 
                x_axis.setTextPen(pg.mkPen(color=(80, 80, 80)))
                major_ticks = [(i, labels[i]) for i in range(len(labels))]
                x_axis.setTicks([major_ticks])

                left_axis.setGrid(180) 
                
                plot_item.setTitle("Активність за останній тиждень", color=(50,50,50), size="12pt")
                plot_item.getViewBox().setXRange(-0.5, len(data) - 0.5)
                plot_item.getViewBox().setYRange(0, max(max_val + 1, (y_ticks_values[-1] if y_ticks_values else 2) ))

            else:
                plot_item.setTitle("Немає активності за останній тиждень", color=(120,120,120), size="10pt")
                # Ensure axes are still clean for the message
                left_axis = plot_item.getAxis('left')
                left_axis.setTicks(None)
                left_axis.setLabel("")
                x_axis = plot_item.getAxis('bottom')
                x_axis.setTicks(None)
            
            print("Finished loading activity data with pyqtgraph.")

        except Exception as e:
            print(f"Error loading activity data: {str(e)}")
            import traceback
            traceback.print_exc()
            if hasattr(self, 'plot') and self.plot:
                self.plot.clear() 
                plot_item = self.plot.getPlotItem()
                if plot_item:
                    view_box = plot_item.getViewBox()
                    if view_box:
                        view_box.setBorder(None)
                    else:
                        print("Error: plot_item.getViewBox() is None in exception handler for activity data.")
                    
                    self.plot.setBackground('w')
                    plot_item.setTitle("Помилка завантаження даних активності", color="red", size="10pt")
                else:
                    print("Error: plot_item is None after self.plot.clear() in exception handler for activity data.")
            else:
                print("Error: self.plot is not available in exception handler for activity data.")

    def load_recent_lessons(self):
        """Load and display user's recent lessons with progress"""
        print("Attempting to load recent lessons...")
        try:
            for i in reversed(range(self.continue_viewing_courses_layout.count())):
                widget_item = self.continue_viewing_courses_layout.itemAt(i)
                if widget_item and widget_item.widget():
                    widget_item.widget().setParent(None)
            
            from src.services.session_manager import SessionManager
            session_manager = SessionManager()
            user_data = session_manager.get_current_user_data()
            
            if not user_data or 'id' not in user_data:
                print("No user logged in, can't load recent lessons.")
                return
                
            user_id = user_data['id']
            print(f"User ID: {user_id}")
            
            user_course_progress_list = self.progress_service.get_user_progress(user_id)
            print(f"User course progress list: {user_course_progress_list}")
            
            if not user_course_progress_list:
                print("No progress records found for the user.")
                return

            recent_lessons_data = []
            for progress_entry in user_course_progress_list:
                print(f"Processing progress entry: {progress_entry}")
                if progress_entry.current_lesson_id and progress_entry.last_accessed:
                    lesson_id_str = str(progress_entry.current_lesson_id)
                    is_completed = self.progress_service.has_completed_lesson(user_id, lesson_id_str)
                    print(f"Lesson ID {lesson_id_str}, Completed: {is_completed}")
                    if not is_completed:
                         recent_lessons_data.append({
                            "lesson_id": lesson_id_str,
                            "course_id": str(progress_entry.course_id),
                            "last_accessed": progress_entry.last_accessed
                        })
            
            recent_lessons_data.sort(key=lambda x: x["last_accessed"], reverse=True)
            print(f"Sorted recent lessons data (up to 5): {recent_lessons_data[:5]}")

            count = 0
            MAX_RECENT_LESSONS = 5

            for lesson_data_item in recent_lessons_data:
                if count >= MAX_RECENT_LESSONS:
                    break

                lesson_id = lesson_data_item["lesson_id"]
                course_id = lesson_data_item["course_id"]
                print(f"Fetching lesson: {lesson_id}, course: {course_id}")

                lesson = self.lesson_service.get_lesson_by_id(lesson_id)
                course = self.course_service.get_course_by_id(course_id)
                print(f"Fetched lesson object: {lesson}")
                print(f"Fetched course object: {course}")

                if lesson and course:
                    lesson_progress_percentage = 0
                    if hasattr(lesson, 'content_items') and isinstance(lesson.content_items, list):
                        if len(lesson.content_items) > 0:
                            print(f"Lesson content items: {lesson.content_items}")
                            completed_content_ids = self.progress_service.get_completed_content_ids(user_id, lesson_id)
                            print(f"Completed content IDs for lesson {lesson_id}: {completed_content_ids}")
                            
                            total_items = len(lesson.content_items)
                            completed_items = len(completed_content_ids) if completed_content_ids else 0
                            lesson_progress_percentage = int((completed_items / total_items) * 100)
                            print(f"Lesson {lesson_id}: Total items: {total_items}, Completed: {completed_items}, Progress: {lesson_progress_percentage}%")
                        else:
                            print(f"Lesson {lesson_id} has an empty list of content items. Progress is 0%.")
                            lesson_progress_percentage = 0
                    else:
                        print(f"Lesson {lesson_id} 'content_items' is missing, None, or not a list. Progress is 0%.")
                        lesson_progress_percentage = 0
                    
                    print(f"Creating widget for lesson: {lesson.title}, progress: {lesson_progress_percentage}%")
                    widget = self.create_continue_lesson_widget(
                        lesson_title=lesson.title,
                        course_name=course.name,
                        lesson_description=f"Part of {course.name}",
                        progress=lesson_progress_percentage,
                        lesson_id=lesson.id,
                        course_id=course.id 
                    )
                    self.continue_viewing_courses_layout.addWidget(widget)
                    count += 1
                else:
                    print(f"Skipping lesson ID {lesson_id} because lesson or course object is None.")
            
            if count == 0:
                print("No active lessons to display in 'Continue Viewing'.")

        except Exception as e:
            print(f"Error loading recent lessons: {str(e)}")
            import traceback
            traceback.print_exc()

    def load_recommended_courses_data(self):
        """Load and display recommended courses for the user based on interests."""
        print("Attempting to load recommended courses with appeal score...")
        try:
            # Clear existing recommended course widgets
            for i in reversed(range(self.recommended_graph_widget_layout.count())):
                widget_item = self.recommended_graph_widget_layout.itemAt(i)
                if widget_item and widget_item.widget():
                    widget_item.widget().setParent(None)
                    widget_item.widget().deleteLater()

            from src.services.session_manager import SessionManager
            session_manager = SessionManager()
            user_data = session_manager.get_current_user_data()

            if not user_data or 'id' not in user_data:
                print("No user logged in, can't load recommended courses.")
                return
            user_id = user_data['id']

            all_courses = self.course_service.get_all_courses()
            if not all_courses:
                print("No courses available in the system to recommend.")
                return

            user_progress_list = self.progress_service.get_user_progress(user_id)
            
            started_course_ids = set()
            user_interest_tags = set()
            user_interest_topics = set()
            user_interest_difficulties = set()

            if user_progress_list:
                for progress_entry in user_progress_list:
                    started_course_ids.add(str(progress_entry.course_id))
                    # Consider a course for interest profiling if there's some interaction
                    # A more nuanced approach could be progress_percentage > 0 and < 100
                    course_for_interest = self.course_service.get_course_by_id(str(progress_entry.course_id))
                    if course_for_interest:
                        if course_for_interest.tags:
                            user_interest_tags.update(course_for_interest.tags)
                        if course_for_interest.topic:
                            user_interest_topics.add(course_for_interest.topic)
                        if course_for_interest.difficulty_level: # Uses the property
                            user_interest_difficulties.add(course_for_interest.difficulty_level)
            
            print(f"User interest tags: {user_interest_tags}")
            print(f"User interest topics: {user_interest_topics}")
            print(f"User interest difficulties: {user_interest_difficulties}")

            unstarted_courses_with_scores = []
            for course in all_courses:
                if str(course.id) not in started_course_ids:
                    appeal_score = 0
                    if not user_interest_tags and not user_interest_topics and not user_interest_difficulties:
                        # If no user interests identified, give a minimal score or use creation date if available
                        # For now, random shuffle will handle this if all scores are 0
                        pass
                    else:
                        if course.tags:
                            appeal_score += len(set(course.tags).intersection(user_interest_tags)) * 2 # 2 points per matching tag
                        if course.topic and course.topic in user_interest_topics:
                            appeal_score += 3 # 3 points for matching topic
                        if course.difficulty_level and course.difficulty_level in user_interest_difficulties:
                            appeal_score += 1 # 1 point for matching difficulty
                    
                    unstarted_courses_with_scores.append({"course": course, "score": appeal_score})

            if not unstarted_courses_with_scores:
                print("User has started or interacted with all available courses, or no unstarted courses found. No new recommendations.")
                # Optional: display a message
                return

            # Sort by score (descending), then shuffle those with the same score to add some variety,
            # or could sort by another metric like course name or creation date as a tie-breaker.
            # For now, just sort by score.
            unstarted_courses_with_scores.sort(key=lambda x: x["score"], reverse=True)
            
            # If all scores are 0 (e.g. new user, or no matching interests), shuffle the whole list.
            if all(item["score"] == 0 for item in unstarted_courses_with_scores):
                print("No specific user interests matched or new user. Shuffling unstarted courses.")
                random.shuffle(unstarted_courses_with_scores)


            MAX_RECOMMENDATIONS = 3
            recommendations_to_display = [item["course"] for item in unstarted_courses_with_scores[:MAX_RECOMMENDATIONS]]
            
            print(f"Displaying {len(recommendations_to_display)} recommended courses. Scores (top 5): {[(item['course'].name, item['score']) for item in unstarted_courses_with_scores[:5]]}")

            if not recommendations_to_display:
                 print("No courses to recommend after filtering and scoring.")
                 # Optionally display a message here if the layout is empty
                 no_recommendations_label = QtWidgets.QLabel("Немає нових рекомендацій.")
                 no_recommendations_label.setAlignment(Qt.AlignCenter)
                 self.recommended_graph_widget_layout.addWidget(no_recommendations_label)
                 return

            for course in recommendations_to_display:
                course_card = self.create_recommended_course_widget(course)
                self.recommended_graph_widget_layout.addWidget(course_card)
            
            if len(recommendations_to_display) < MAX_RECOMMENDATIONS and len(recommendations_to_display) > 0:
                 self.recommended_graph_widget_layout.addStretch(1) # Push content up if space

        except Exception as e:
            print(f"Error loading recommended courses: {str(e)}")
            import traceback
            traceback.print_exc()

    def create_recommended_course_widget(self, course):
        """Create a widget for a recommended course."""
        card = QtWidgets.QWidget()
        card.setFixedHeight(65) # Adjusted height for fitting 3 items
        card.setProperty("type", "card_simple") # For potential QSS styling
        card.setObjectName(f"recommended_course_card_{course.id}")
        
        card.setProperty("course_id", str(course.id)) # Store course_id

        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(8, 5, 8, 5) # Margins inside the card
        layout.setSpacing(3)                   # Spacing between elements in card

        title_label = QtWidgets.QLabel(course.name)
        title_label.setProperty("type", "lb_recommend_title") # For QSS
        title_label.setWordWrap(True)
        title_label.setStyleSheet("font-weight: bold;") # Simple styling

        description_text = course.description or "Детальніше про курс..."
        # Truncate description if too long
        if len(description_text) > 70: # Arbitrary length limit
            description_text = description_text[:67] + "..."
        
        description_label = QtWidgets.QLabel(description_text)
        description_label.setProperty("type", "lb_recommend_desc") # For QSS
        description_label.setWordWrap(True)
        description_label.setMaximumHeight(35) # Allow for approx 2 lines

        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addStretch(1) # Push content to top if there's extra space in card
        card.setLayout(layout)

        # Make card clickable
        click_filter = ClickFilter(card)
        card.installEventFilter(click_filter)
        # Use a lambda to pass the course_id to the handler
        click_filter.clicked.connect(lambda cid=str(course.id): self.on_recommended_course_click(cid))
        
        # Apply styles if needed (e.g. if QSS relies on this)
        card.style().unpolish(card)
        card.style().polish(card)

        return card

    def on_recommended_course_click(self, course_id):
        print(f"Recommended course card clicked. Course ID: {course_id}")
        # Placeholder for future navigation logic:
        # course = self.course_service.get_course_by_id(course_id)
        # if course:
        #   print(f"Navigate to course: {course.name}")
        #   # Potential: find first lesson and open it via self.lesson_page and self.stack
        #   # first_lesson = self.lesson_service.get_first_lesson_for_course(course_id)
        #   # if first_lesson and self.lesson_page and self.stack:
        #   #     self.lesson_page.set_lesson_data(first_lesson.title, first_lesson.id)
        #   #     self.stack.setCurrentWidget(self.lesson_page)
        #   # else:
        #   #     print(f"Could not find first lesson for course {course_id} or lesson_page/stack is not available.")
        # else:
        #   print(f"Could not retrieve course details for ID: {course_id}")
        pass

    def load_courses_section_data(self):
        """Load and display user's courses with progress in the courses section."""
        print("Attempting to load courses section data (sorted by recent progress, max 8)...")
        try:
            # Clear existing course widgets from self.gridLayout_14
            for i in reversed(range(self.gridLayout_14.count())):
                item = self.gridLayout_14.itemAt(i)
                if item is not None:
                    widget = item.widget()
                    if widget is not None:
                        if widget == self.lb_my_courses: # Keep the title label
                            continue
                        widget.setParent(None)
                        widget.deleteLater()
            
            from src.services.session_manager import SessionManager
            session_manager = SessionManager()
            user_data = session_manager.get_current_user_data()

            if not user_data or 'id' not in user_data:
                print("No user logged in, can't load courses section.")
                return
            user_id = user_data['id']
            print(f"Courses section: User ID: {user_id}")

            user_progress_list = self.progress_service.get_user_progress(user_id)
            if not user_progress_list:
                print("No progress records found for the user to sort courses.")
                return

            # Create a list of (progress_entry, course_object) for sorting
            courses_with_progress_and_access_time = []
            for progress_entry in user_progress_list:
                if progress_entry.course_id and progress_entry.last_accessed:
                    course = self.course_service.get_course_by_id(str(progress_entry.course_id))
                    if course:
                        courses_with_progress_and_access_time.append((progress_entry, course))
            
            # Sort by last_accessed date from progress_entry, descending (most recent first)
            courses_with_progress_and_access_time.sort(key=lambda x: x[0].last_accessed, reverse=True)

            # Limit to a maximum of 8 courses (2 rows of 4)
            MAX_COURSES_DISPLAY = 8
            courses_to_display = courses_with_progress_and_access_time[:MAX_COURSES_DISPLAY]
            
            print(f"Found {len(courses_to_display)} courses to display after sorting and limiting.")

            num_columns = 4 
            row, col = 1, 0 # Start from row 1 as row 0 is the title label

            for progress_entry, course in courses_to_display:
                progress_percentage = 0
                if progress_entry.progress_percentage is not None:
                    progress_percentage = int(progress_entry.progress_percentage)
                
                print(f"Displaying course: {course.name}, Last Accessed: {progress_entry.last_accessed}, Progress: {progress_percentage}%")

                course_widget = QWidget(self.courses_section)
                layout = QVBoxLayout(course_widget)
                layout.setContentsMargins(layout.contentsMargins().left(), 0, layout.contentsMargins().right(), layout.contentsMargins().bottom()) # Set top margin to 0
                layout.setAlignment(QtCore.Qt.AlignCenter)
                course_widget.setMinimumSize(180, 180)
                course_widget.setMaximumSize(180, 180)
                course_widget.setProperty("type", "transparent_widget")

                course_label = QLabel(course.name)
                course_label.setAlignment(QtCore.Qt.AlignCenter)
                course_label.setProperty("type", "lb_small")
                course_label.setMinimumWidth(150)
                course_label.setMaximumWidth(170)
                course_label.setWordWrap(True)

                circular_progress = CircularProgress(course_widget)
                circular_progress.setObjectName(f"circular_progress_course_{str(course.id)}")
                circular_progress.setToolTip(f"Прогрес курсу {course.name}")
                circular_progress.setMinimumSize(140, 140)
                circular_progress.setMaximumSize(140, 140)
                circular_progress.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                circular_progress.set_value(progress_percentage)

                layout.addWidget(course_label)
                layout.addWidget(circular_progress)
                course_widget.setLayout(layout)

                self.gridLayout_14.addWidget(course_widget, row, col, 1, 1)
                
                col += 1
                if col >= num_columns:
                    col = 0
                    row += 1
            
            # Ensure the title spans all columns correctly after widgets are added and grid might resize columnCount
            # This might be redundant if columnCount is fixed at 4, but good for robustness
            current_col_count = self.gridLayout_14.columnCount()
            if current_col_count > 0:
                 self.gridLayout_14.addWidget(self.lb_my_courses, 0, 0, 1, current_col_count)
            else: # Default span if no courses were added, though layout has 4 columns by loop logic
                 self.gridLayout_14.addWidget(self.lb_my_courses, 0, 0, 1, 4)

            print("Finished loading courses section data (sorted and limited).")

        except Exception as e:
            print(f"Error loading courses section data: {str(e)}")
            import traceback
            traceback.print_exc()

    def create_continue_lesson_widget(self, lesson_title="Lesson Title", course_name="Course", lesson_description="Description", progress=0, lesson_id=None, course_id=None):
        """Create a widget for a lesson in the 'Continue Viewing' section"""
        widget = QtWidgets.QWidget()
        widget.setFixedSize(QtCore.QSize(250, 150))
        widget.setProperty("type", "card")
        widget.setObjectName(f"lesson_card_{lesson_id or random.randint(1000,9999)}")

        widget.setProperty("lesson_id", lesson_id)
        widget.setProperty("course_id", course_id)
        widget.setProperty("lesson_title", lesson_title)

        vertical_layout = QtWidgets.QVBoxLayout(widget)
        vertical_layout.setContentsMargins(10, 10, 10, 10)
        vertical_layout.setSpacing(5)

        lesson_name_label = QtWidgets.QLabel(lesson_title)
        lesson_name_label.setProperty("type", "lb_name_lesson")
        lesson_name_label.setWordWrap(True)
        vertical_layout.addWidget(lesson_name_label)
        
        course_name_label = QtWidgets.QLabel(course_name)
        course_name_label.setProperty("type", "lb_name_course")
        course_name_label.setWordWrap(True)
        vertical_layout.addWidget(course_name_label)

        progress_bar_container = QtWidgets.QWidget()
        progress_bar_layout = QtWidgets.QHBoxLayout(progress_bar_container)
        progress_bar_layout.setContentsMargins(0,0,0,0)
        
        lesson_progress_bar = QtWidgets.QProgressBar()
        lesson_progress_bar.setFixedHeight(10)
        lesson_progress_bar.setValue(progress)
        lesson_progress_bar.setTextVisible(False)
        progress_bar_layout.addWidget(lesson_progress_bar)

        progress_text_label = QtWidgets.QLabel(f"{progress}%")
        progress_text_label.setProperty("type", "lb_small")
        progress_bar_layout.addWidget(progress_text_label)
        
        vertical_layout.addWidget(progress_bar_container)
        
        click_filter = ClickFilter(widget)
        widget.installEventFilter(click_filter)
        click_filter.clicked.connect(lambda bound_widget=widget: self.on_lesson_click(bound_widget))
        
        widget.style().unpolish(widget)
        widget.style().polish(widget)

        return widget
        