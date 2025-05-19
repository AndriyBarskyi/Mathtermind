from PyQt5.QtWidgets import QWidget, QGridLayout,QVBoxLayout, QLabel,QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from src.services.progress_service import ProgressService
from src.services.course_service import CourseService
from src.services.lesson_service import LessonService
from src.models.progress import Progress
from src.db.models.enums import Topic # Import Topic enum


class TopicProgressBarChart(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.topic_progress_data = {}
        self.setMinimumHeight(150) # Ensure it has some default height
        self.topic_colors = {
            Topic.MATHEMATICS: QtGui.QColor("#4CAF50"), # Green
            Topic.INFORMATICS: QtGui.QColor("#2196F3"), # Blue
            # Add more colors if you have more topics
            "DEFAULT": QtGui.QColor("#FFC107") # Amber for any other
        }
        self.topic_names = {
            Topic.MATHEMATICS: "Математика",
            Topic.INFORMATICS: "Інформатика",
        }


    def update_data(self, data):
        self.topic_progress_data = data
        self.update() # Trigger repaint

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        if not self.topic_progress_data:
            painter.drawText(self.rect(), QtCore.Qt.AlignCenter, "Немає даних для відображення")
            return

        bar_width_ratio = 0.6 # How much of the available space each bar will take
        spacing_ratio = (1 - bar_width_ratio) / 2 # Space on each side of the bar
        
        num_topics = len(self.topic_progress_data)
        if num_topics == 0: return

        # Calculate width for each bar including spacing
        total_bar_unit_width = self.width() / num_topics
        actual_bar_width = total_bar_unit_width * bar_width_ratio
        bar_spacing = total_bar_unit_width * spacing_ratio

        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        fm = QtGui.QFontMetrics(font)
        text_height = fm.height()

        max_bar_height = self.height() - text_height - 15 # 15 for padding and text above bar

        for i, (topic_enum, percentage) in enumerate(self.topic_progress_data.items()):
            bar_height = (percentage / 100) * max_bar_height
            
            # X position for the bar, considering spacing
            bar_x = (i * total_bar_unit_width) + bar_spacing
            
            # Y position for the bar (from bottom up)
            bar_y = self.height() - bar_height - text_height - 5 # 5 for padding below text

            # Color
            color = self.topic_colors.get(topic_enum, self.topic_colors["DEFAULT"])
            painter.setBrush(QtGui.QBrush(color))
            painter.setPen(QtCore.Qt.NoPen) # No border for the bar

            painter.drawRect(int(bar_x), int(bar_y), int(actual_bar_width), int(bar_height))

            # Draw percentage text above bar
            percent_text = f"{int(percentage)}%"
            text_x = bar_x + (actual_bar_width - fm.width(percent_text)) / 2
            painter.setPen(QtGui.QColor(QtCore.Qt.black)) # Text color
            painter.drawText(int(text_x), int(bar_y - 2), percent_text) # 2 for padding above bar

            # Draw topic name below bar
            topic_name_str = self.topic_names.get(topic_enum, str(topic_enum))
            topic_text_x = bar_x + (actual_bar_width - fm.width(topic_name_str)) / 2
            painter.drawText(int(topic_text_x), int(self.height() - 5), topic_name_str) # 5 for padding from bottom


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
        self.topic_progress_data = {} # Initialize data for the graph
        
        self.pg_progress = QtWidgets.QWidget()
        self.pg_progress.setObjectName("pg_progress")
        
        # Connect to show event to refresh data when page becomes visible
        self.showEvent = self.on_show_event
        
        self.main_progress_layout = QtWidgets.QGridLayout(self.pg_progress)
        self.main_progress_layout.setHorizontalSpacing(7)
        self.main_progress_layout.setObjectName("main_progress_layout")

        # Make main left (col 0) and right (col 2) content areas take equal width
        self.main_progress_layout.setColumnStretch(0, 1)
        self.main_progress_layout.setColumnStretch(1, 0) # Spacer column, no stretch
        self.main_progress_layout.setColumnStretch(2, 1)

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
        
        self.success_graph_widget = TopicProgressBarChart(self.success_widget) # Use custom widget
        self.success_graph_widget.setObjectName("success_graph_widget")
        # self.success_graph_widget.setProperty("type", "w_pg") # Style handled by custom widget or its parent
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

        # Make the two columns in activity_layout (for summary cards) take equal width
        self.activity_layout.setColumnStretch(0, 1)
        self.activity_layout.setColumnStretch(1, 1)
        
        self.lb_activity = QtWidgets.QLabel(self.activity_widget)
        self.lb_activity.setText("Активність")
        self.lb_activity.setProperty("type", "page_section")
        self.lb_activity.setObjectName("lb_activity")
        self.activity_layout.addWidget(self.lb_activity, 0, 0, 1, 1)
        
        self.courses_card_widget = QtWidgets.QWidget(self.activity_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.courses_card_widget.setSizePolicy(sizePolicy)
        self.courses_card_widget.setProperty("type", "w_pg")
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
        self.courses_description_label.setWordWrap(True)
        self.courses_description_label.setTextFormat(QtCore.Qt.RichText)
        self.courses_description_label.setProperty("type","lb_description")
        self.courses_description_label.setObjectName("courses_description_label")
        self.courses_card_layout.addWidget(self.courses_description_label, 1, 0, 1, 2)
        self.activity_layout.addWidget(self.courses_card_widget, 1, 0, 1, 1)
        
        self.lessons_card_widget = QtWidgets.QWidget(self.activity_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lessons_card_widget.sizePolicy().hasHeightForWidth())
        self.lessons_card_widget.setSizePolicy(sizePolicy)
        self.lessons_card_widget.setProperty("type", "w_pg")
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
        self.lessons_description_label.setWordWrap(True)
        self.lessons_description_label.setTextFormat(QtCore.Qt.RichText)
        self.lessons_description_label.setProperty("type","lb_description")
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
        self.awards_card_widget.setProperty("type", "w_pg")
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
        self.awards_description_label.setWordWrap(True)
        self.awards_description_label.setTextFormat(QtCore.Qt.RichText)
        self.awards_description_label.setProperty("type","lb_description")
        self.awards_description_label.setObjectName("awards_description_label")
        
        self.awards_card_layout.addWidget(self.awards_description_label, 1, 0, 1, 2)
        self.activity_layout.addWidget(self.awards_card_widget, 2, 0, 1, 1)
        self.tasks_card_widget = QtWidgets.QWidget(self.activity_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tasks_card_widget.sizePolicy().hasHeightForWidth())
        
        self.tasks_card_widget.setSizePolicy(sizePolicy)
        self.tasks_card_widget.setProperty("type", "w_pg")
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
        self.tasks_description_label.setWordWrap(True)
        self.tasks_description_label.setTextFormat(QtCore.Qt.RichText)
        self.tasks_description_label.setProperty("type","lb_description")
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
        self.scroll_courses_success_content.setProperty("type", "w_pg")
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
        self.courses_success_layout_inner.setContentsMargins(11, 20, 11, 20)
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
        self.tabs_courses_success.setProperty("type", "w_pg")
        
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
        self.load_success_tabs()

    def load_user_progress(self):
        """Load and display user progress data from database"""
        try:
            # Get the current user from the session
            from src.services.session_manager import SessionManager
            session_manager = SessionManager()
            user_data = session_manager.get_current_user_data()
            
            if not user_data or 'id' not in user_data:
                print("No user logged in, can't load progress")
                placeholder_widget = self.add_course_info_widget(
                    name="No User Logged In",
                    completed_lessons=0,
                    total_lessons=5,
                    percentage=0
                )
                if placeholder_widget:
                    self.courses_main_layout.addWidget(placeholder_widget, 0, 0, 1, 1)
                return
                
            user_id = user_data['id']
            
            # Get user progress data
            progress_records = self.progress_service.get_user_progress(user_id)
            if not progress_records:
                print("No progress records found for user")
                placeholder_widget = self.add_course_info_widget(
                    name="No Courses Started Yet",
                    completed_lessons=0,
                    total_lessons=0,
                    percentage=0
                )
                if placeholder_widget:
                    self.courses_main_layout.addWidget(placeholder_widget, 0, 0, 1, 1)
                return
            
            print(f"Found {len(progress_records)} progress records")
            
            # Clear existing widgets in the courses_main_layout
            self._clear_layout(self.courses_main_layout)
                
            # Sort progress records by percentage - show highest completion first
            progress_records.sort(key=lambda x: x.progress_percentage, reverse=True)
            
            # Update the total numbers displays
            total_courses = len(progress_records)
            completed_courses = sum(1 for p in progress_records if p.is_completed)
            total_lessons = 0
            completed_lessons = 0
            
            # Create a QWidget to hold all course entries
            courses_widget = QtWidgets.QWidget()
            courses_layout = QtWidgets.QVBoxLayout(courses_widget)
            courses_layout.setSpacing(10)
            
            # Add each progress record with its corresponding course
            for i, progress in enumerate(progress_records):
                try:
                    # Get course info
                    course = self.course_service.get_course_by_id(str(progress.course_id))
                    if not course:
                        continue
                    
                    # Get lessons for this course
                    lessons = self.lesson_service.get_lessons_by_course_id(str(course.id))
                    if not lessons:
                        continue
                        
                    # Get completed lessons for this course
                    course_completed_lessons = self.progress_service.get_course_completed_lessons(
                        user_id, str(course.id)
                    )
                    
                    # Update total counts
                    total_lessons += len(lessons)
                    completed_lessons += len(course_completed_lessons)
                    
                    # Create a widget for this course
                    course_widget = self._create_course_progress_widget(
                        course, 
                        lessons, 
                        course_completed_lessons, 
                        progress, 
                        i
                    )
                    
                    # Add this course widget to the main layout
                    courses_layout.addWidget(course_widget)
                    
                except Exception as e:
                    print(f"Error processing progress for course: {str(e)}")
                    import traceback
                    traceback.print_exc()
            
            # Set the scroll area content
            self.courses_layout.addWidget(courses_widget, 0, 0, 1, 1)
            
            # --- Aggregate data for Topic Progress Bar Chart ---
            topic_progress_summary = {}
            topic_course_counts = {}

            for progress_record in progress_records: # Iterate again, or store course info earlier
                course = self.course_service.get_course_by_id(str(progress_record.course_id))
                if course and course.topic:
                    topic_enum = course.topic # This is the Topic Enum
                    if topic_enum not in topic_progress_summary:
                        topic_progress_summary[topic_enum] = 0
                        topic_course_counts[topic_enum] = 0
                    topic_progress_summary[topic_enum] += progress_record.progress_percentage
                    topic_course_counts[topic_enum] += 1
            
            self.topic_progress_data = {}
            for topic_enum, total_percentage in topic_progress_summary.items():
                if topic_course_counts[topic_enum] > 0:
                    average_percentage = total_percentage / topic_course_counts[topic_enum]
                    self.topic_progress_data[topic_enum] = average_percentage
            
            self.success_graph_widget.update_data(self.topic_progress_data)
            # --- End of Topic Progress Bar Chart data aggregation ---

            # Update summary information in the activity widgets
            self._update_summary_widgets(
                total_courses=total_courses,
                completed_courses=completed_courses,
                total_lessons=total_lessons,
                completed_lessons=completed_lessons
            )
            
        except Exception as e:
            print(f"Error loading user progress: {str(e)}")
            import traceback
            traceback.print_exc()
            # Clear graph data on error too
            self.success_graph_widget.update_data({})
    
    def _create_course_progress_widget(self, course, lessons, completed_lessons, progress, index):
        """Create a widget displaying course progress information"""
        course_widget = QtWidgets.QWidget()
        course_widget.setProperty("type", "card")
        course_widget.setMinimumHeight(100)
        course_layout = QtWidgets.QVBoxLayout(course_widget)
        
        # Course name label
        name_label = QtWidgets.QLabel(course.name)
        name_label.setProperty("type", "lb_name_lesson")
        name_label.setWordWrap(True)
        course_layout.addWidget(name_label)
        
        # Description label (optional)
        if course.description:
            desc_label = QtWidgets.QLabel(course.description)
            desc_label.setProperty("type", "lb_description")
            desc_label.setWordWrap(True)
            desc_label.setMaximumHeight(40)  # Limit height to avoid long descriptions
            course_layout.addWidget(desc_label)
        
        # Progress info
        info_label = QtWidgets.QLabel(f"{len(completed_lessons)}/{len(lessons)} уроків")
        info_label.setProperty("type", "lb_small")
        course_layout.addWidget(info_label)
        
        # Progress bar
        progress_bar = QtWidgets.QProgressBar()
        progress_bar.setMinimumSize(QtCore.QSize(0, 20))
        progress_bar.setMaximumSize(QtCore.QSize(16777215, 20))
        progress_bar.setValue(int(progress.progress_percentage))
        progress_bar.setTextVisible(False)
        progress_bar.setOrientation(QtCore.Qt.Horizontal)
        progress_bar.setObjectName(f"progress_{index}")
        course_layout.addWidget(progress_bar)
        
        # Status row (percentage and completed status)
        status_row = QtWidgets.QWidget()
        status_layout = QtWidgets.QHBoxLayout(status_row)
        status_layout.setContentsMargins(0, 0, 0, 0)
        
        # Percentage label
        percentage_label = QtWidgets.QLabel(f"{int(progress.progress_percentage)}%")
        percentage_label.setProperty("type", "lb_small")
        status_layout.addWidget(percentage_label)
        
        # Completed status
        if progress.is_completed:
            completed_label = QtWidgets.QLabel("Завершено")
            completed_label.setProperty("type", "lb_success")
            completed_label.setStyleSheet("color: green;")
            status_layout.addWidget(completed_label, alignment=QtCore.Qt.AlignRight)
        
        course_layout.addWidget(status_row)
        
        return course_widget
    
    def _update_summary_widgets(self, total_courses, completed_courses, total_lessons, completed_lessons):
        """Update the summary widgets with progress statistics"""
        # Courses info
        self.lb_num_of_courses.setText(f"🎓 {total_courses}")
        self.courses_description_label.setTextFormat(QtCore.Qt.RichText)
        self.courses_description_label.setText(
            f"Курсів загалом: {total_courses}<br>Завершено: {completed_courses}"
        )
        
        # Lessons info
        self.lb_num_of_lessons.setText(f"📚 {total_lessons}")
        self.lessons_description_label.setTextFormat(QtCore.Qt.RichText)
        self.lessons_description_label.setText(
            f"Уроків загалом: {total_lessons}<br>Завершено: {completed_lessons}"
        )
        
        # Awards count (based on completed courses)
        self.lb_num_of_awards.setText(f"🏆 {completed_courses}")
        self.awards_description_label.setText(f"Нагороди за завершені курси")
        
        # Tasks count (placeholder - could be replaced with actual task counts)
        self.lb_num_of_tasks.setText(f"✔ {completed_lessons}")
        self.tasks_description_label.setText(f"Виконані завдання (уроки)")
    
    def _clear_layout(self, layout):
        """Clear all widgets from a layout"""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                elif item.layout() is not None:
                    self._clear_layout(item.layout())

    def add_course_info_widget(self, name, completed_lessons, total_lessons, percentage):
        """Add a course info widget to the progress page"""
        try:
            # Clear existing items first if there are any
            for i in reversed(range(self.courses_main_layout.count())):
                item = self.courses_main_layout.itemAt(i)
                if item and item.widget():
                    item.widget().deleteLater()
            
            # Create a new course info widget
            widget = QtWidgets.QWidget()
            widget.setProperty("type", "w_pg")
            widget.setMinimumHeight(80) 
            layout = QtWidgets.QVBoxLayout(widget)

            name_label = QtWidgets.QLabel(name)
            name_label.setProperty("type", "lb_description")
            name_label.setWordWrap(True)
            layout.addWidget(name_label)

            info_label = QtWidgets.QLabel(f"{completed_lessons}/{total_lessons} уроків")
            info_label.setProperty("type", "lb_small")
            layout.addWidget(info_label)

            progress_bar = QtWidgets.QProgressBar()
            progress_bar.setMinimumSize(QtCore.QSize(0, 20))
            progress_bar.setMaximumSize(QtCore.QSize(16777215, 20))
            progress_bar.setProperty("value", percentage)
            progress_bar.setTextVisible(False)
            progress_bar.setOrientation(QtCore.Qt.Horizontal)
            progress_bar.setObjectName(f"pg4_progress_{name}")
            layout.addWidget(progress_bar)

            lb_interest = QtWidgets.QLabel(f"{percentage}% ({completed_lessons}/{total_lessons} lessons)")
            lb_interest.setMinimumSize(QtCore.QSize(0, 50))
            lb_interest.setMaximumSize(QtCore.QSize(16777215, 50))
            lb_interest.setObjectName("lb_interest")
            lb_interest.setProperty("type", "lb_small")
            layout.addWidget(lb_interest)

            return widget  # Return the widget for reference
        except Exception as e:
            print(f"Error adding course info widget: {str(e)}")
            import traceback
            traceback.print_exc()

    def load_success_tabs(self):
        """Load progress data for the success tabs with visualizations"""
        try:
            # Clear existing tabs
            while self.tabs_courses_success.count() > 0:
                self.tabs_courses_success.removeTab(0)
                
            # Get the current user from the session
            from src.services.session_manager import SessionManager
            session_manager = SessionManager()
            user_data = session_manager.get_current_user_data()
            
            if not user_data or 'id' not in user_data:
                # Just create a placeholder tab
                self.create_tab_with_widgets("Немає даних", 5, 1, 5)
                return
                
            user_id = user_data['id']
            
            # Get user progress data
            progress_records = self.progress_service.get_user_progress(user_id)
            if not progress_records:
                # Create a placeholder tab
                self.create_tab_with_widgets("Немає даних", 5, 1, 5)
                return
            
            # Group courses by topic
            courses_by_topic = {}
            
            for progress in progress_records:
                course = self.course_service.get_course_by_id(str(progress.course_id))
                if not course:
                    continue
                    
                if course.topic not in courses_by_topic:
                    courses_by_topic[course.topic] = []
                    
                courses_by_topic[course.topic].append((course, progress))
            
            # Create a tab for each topic
            for topic, course_progress_list in courses_by_topic.items():
                # Create a tab with empty grid
                tab_widget = QtWidgets.QWidget()
                tab_widget.setObjectName(f"tab_{topic}")
                tab_widget.setProperty("type", "w_pg")
                
                # Outer layout for the tab page, will center the cards_panel
                page_layout = QtWidgets.QHBoxLayout(tab_widget)
                page_layout.setContentsMargins(2, 10, 2, 10) # Margins for the entire tab page content
                # No explicit spacing for page_layout, stretches will manage space

                # Panel to hold the actual grid of cards
                cards_panel = QtWidgets.QWidget()
                cards_panel.setProperty("type", "w_pg")
                # cards_panel.setStyleSheet("background-color: rgba(0, 255, 0, 50);") # Optional: for visual debugging

                grid_layout_for_cards = QtWidgets.QGridLayout(cards_panel) # Layout for the cards_panel
                grid_layout_for_cards.setContentsMargins(0, 0, 0, 0) # No margins for the card grid itself
                grid_layout_for_cards.setSpacing(5) # Spacing between cards
                
                # Sort courses by progress percentage
                course_progress_list.sort(key=lambda x: x[1].progress_percentage, reverse=True)
                
                # Create boxes for each course and add them to grid_layout_for_cards
                max_cards_per_row = 3
                for i, (course, progress) in enumerate(course_progress_list):
                    row = i // max_cards_per_row
                    col = i % max_cards_per_row # col will be 0, 1, or 2
                    
                    course_box = self._create_course_success_box(course, progress)
                    grid_layout_for_cards.addWidget(course_box, row, col, 1, 1)
                
                # Add the cards_panel to the page_layout, surrounded by stretches for centering
                page_layout.addStretch(1)
                page_layout.addWidget(cards_panel)
                page_layout.addStretch(1)
                
                # Add the tab
                topic_name = str(topic).replace("MATHEMATICS", "Математика").replace("INFORMATICS", "Інформатика")
                self.tabs_courses_success.addTab(tab_widget, topic_name)
            
            # If no tabs were added, add a placeholder
            if self.tabs_courses_success.count() == 0:
                self.create_tab_with_widgets("Немає даних", 5, 1, 5)
                
        except Exception as e:
            print(f"Error loading success tabs: {str(e)}")
            import traceback
            traceback.print_exc()
            # Add placeholder tab in case of error
            self.create_tab_with_widgets("Помилка", 5, 1, 5)

    def _create_course_success_box(self, course, progress):
        """Create a box displaying course success info"""
        box = QtWidgets.QFrame()
        box.setFrameShape(QtWidgets.QFrame.Box)
        box.setFrameShadow(QtWidgets.QFrame.Raised)
        box.setLineWidth(1)
        box.setProperty("type", "card")
        # Adjusted min/max size to allow more cards to fit
        box.setMinimumSize(QtCore.QSize(100, 90)) # Further reduced minimum width
        box.setMaximumSize(QtCore.QSize(150, 140)) # Further reduced maximum width
        
        layout = QtWidgets.QVBoxLayout(box)
        layout.setContentsMargins(5, 5, 5, 5) # Reduced main layout margins
        layout.setSpacing(3) # Reduced spacing in main layout
        
        # Course name
        name_label = QtWidgets.QLabel(course.name)
        name_label.setProperty("type", "lb_name_lesson")
        name_label.setAlignment(QtCore.Qt.AlignCenter)
        name_label.setWordWrap(True)
        layout.addWidget(name_label)
        
        # Progress visualization
        progress_value = int(progress.progress_percentage)
        
        # Container for rows of squares
        squares_container_widget = QtWidgets.QWidget()
        squares_container_layout = QtWidgets.QVBoxLayout(squares_container_widget)
        squares_container_layout.setContentsMargins(0, 0, 0, 0)
        squares_container_layout.setSpacing(2) # Reduced spacing between rows of squares

        # Create progress squares
        square_count = 10
        squares_per_row = 5
        
        current_row_layout = None

        for i in range(square_count):
            if i % squares_per_row == 0:
                # Start a new row
                current_row_widget = QtWidgets.QWidget()
                current_row_layout = QtWidgets.QHBoxLayout(current_row_widget)
                current_row_layout.setContentsMargins(0,0,0,0) # No margins for the row itself
                current_row_layout.setSpacing(2) # Reduced spacing between squares
                current_row_layout.setAlignment(QtCore.Qt.AlignCenter) # Center squares in the row
                squares_container_layout.addWidget(current_row_widget)

            square = QtWidgets.QWidget()
            square.setFixedSize(15, 15) # Reduced square size
            square.setProperty("type","progress")
            
            # Set color based on completion
            if i < progress_value / 10:  # For 10 squares, each represents 10%
                square.setStyleSheet("background-color: #4CAF50; border: 1px solid #388E3C;")
            else:
                square.setStyleSheet("background-color: #E0E0E0; border: 1px solid #9E9E9E;")
                
            current_row_layout.addWidget(square)
        
        # Add a spacer to push squares to the center if the last row is not full
        if current_row_layout and current_row_layout.count() < squares_per_row:
            current_row_layout.addStretch()


        layout.addWidget(squares_container_widget)
        
        # Progress percentage
        percentage_label = QtWidgets.QLabel(f"{progress_value}%")
        percentage_label.setAlignment(QtCore.Qt.AlignCenter)
        percentage_label.setProperty("type", "lb_small")
        layout.addWidget(percentage_label)
        
        return box