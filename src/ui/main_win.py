from PyQt5.QtWidgets import QWidget, QGridLayout,QVBoxLayout, QLabel,QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from circular_progress import *
from graphs import *
from lesson_win import Lesson_page
from main_page import *


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
        self.stack = None
        self.pg_lesson = None
        self.stack = stack
        self.pg_lesson = lesson_page
        
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
        
        example_lessons = [
            {"lesson": "Вступ до Python", "course": "Основи програмування", "desc": "Знайомство зі змінними та типами даних", "progress": 20},
            {"lesson": "Умовні оператори", "course": "Основи програмування", "desc": "if, else, elif — як працюють умови", "progress": 40},
            {"lesson": "Цикли for та while", "course": "Основи програмування", "desc": "Повторення дій з циклами", "progress": 55},
            {"lesson": "Списки та словники", "course": "Python базовий", "desc": "Робота з колекціями даних", "progress": 70},
            {"lesson": "Функції", "course": "Python базовий", "desc": "Створення та виклик функцій", "progress": 30},
            {"lesson": "Класи та обʼєкти", "course": "ООП в Python", "desc": "Основи обʼєктно-орієнтованого підходу", "progress": 15},
            {"lesson": "Алгоритми сортування", "course": "Алгоритми", "desc": "Bubble, Merge, Quick sort", "progress": 65},
            {"lesson": "Рекурсія", "course": "Алгоритми", "desc": "Функції, які викликають себе", "progress": 45},
            {"lesson": "Модулі та пакети", "course": "Python середній", "desc": "Імпорт та структура проєкту", "progress": 80},
        ]

        for i, lesson_data in enumerate(example_lessons, start=1):
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
            
            click_filter = ClickFilter(widget)
            widget.installEventFilter(click_filter)
            
            click_filter.clicked.connect(lambda w=widget: self.on_lesson_click(w))

            self.continue_viewing_courses_layout.addWidget(widget)


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
            layout.setAlignment(QtCore.Qt.AlignCenter)
            course_widget.setMinimumSize(180, 180) 
            course_widget.setMaximumSize(180, 180) 
            course_widget.setProperty("type","transparent_widget")

            course_label = QLabel(course_names[i-1])
            course_label.setAlignment(QtCore.Qt.AlignCenter)
            course_label.setProperty("type", "lb_small")
            course_label.setFixedSize(160, 20)

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
        
        self.recommended_graph_widget = QtWidgets.QWidget(self.recommended_section) #якесь оголошення треба  
        self.recommended_graph_widget.setMinimumSize(QtCore.QSize(0, 275))
        self.recommended_graph_widget.setObjectName("recommended_graph_widget")
        self.recommended_graph_widget.setProperty("type", "w_pg")
        self.grid_rec_activity_section.addWidget(self.recommended_graph_widget, 1, 0, 1, 1)
        self.main_layout.addWidget(self.recommended_section, 1, 1, 1, 1)
        
        self.title_main_lb = QtWidgets.QLabel(self.pg_main)
        self.title_main_lb.setText("Головна")
        self.title_main_lb.setProperty("type", "title")
        self.title_main_lb.setObjectName("title_main_lb")
        self.main_layout.addWidget(self.title_main_lb, 0, 0, 1, 1)
        self.setLayout(self.main_layout)
        #графік
        self.layout = QVBoxLayout(self.activity_graph_widget)
        self.plot = pg.PlotWidget() 
        self.layout.addWidget(self.plot)
        chart = MyGraph(self.plot)
        data = [10, 15, 30, 40, 50]
        labels = ["X", "Y", "Z", "W", "V"]
        chart.plot_bar_chart(data, labels)

        self.btn_scroll_next.clicked.connect(self.scroll_right)
        self.btn_scroll_prev.clicked.connect(self.scroll_left)
        self.continue_viewing_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    def scroll_left(self):
        scroll_bar = self.continue_viewing_scroll_area.horizontalScrollBar()
        scroll_bar.setValue(scroll_bar.value() - 150)

    def scroll_right(self):
        scroll_bar = self.continue_viewing_scroll_area.horizontalScrollBar()
        scroll_bar.setValue(scroll_bar.value() + 150)
    
    def on_lesson_click(self, widget):
        name_label = widget.findChild(QtWidgets.QLabel, "lb_n_les3")
        print(f"Клік по уроці: {name_label.text() if name_label else 'Невідомо'}")
        self.pg_lesson.set_lesson_data(widget.lesson_label.text())
        self.stack.setCurrentWidget(self.pg_lesson)
    
        