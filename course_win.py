from PyQt5.QtWidgets import QWidget, QGridLayout,QVBoxLayout, QLabel,QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from slider import RangeSlider
from lessons_list_win import Lessons_page
from ui import *


class Course_page(QWidget):
    def __init__(self,stack=None, lessons_page=None):
        super().__init__()
        self.stack = None
        self.pg_lessons = None
        self.stack = stack
        self.pg_lessons = lessons_page

        self.pg_courses = QtWidgets.QWidget()
        self.pg_courses.setObjectName("pg_courses")
        self.main_courses_layout = QtWidgets.QGridLayout(self.pg_courses)
        self.main_courses_layout.setObjectName("main_courses_layout")
        self.filter_buttons_widget = QtWidgets.QWidget(self.pg_courses)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.filter_buttons_widget.setSizePolicy(sizePolicy)
        self.filter_buttons_widget.setMinimumSize(QtCore.QSize(1020, 50))
        self.filter_buttons_widget.setMaximumSize(QtCore.QSize(1600000, 50))
        self.filter_buttons_widget.setProperty("type", "w_pg") 
        self.filter_buttons_widget.setObjectName("filter_buttons_widget")
        self.filter_buttons_layout = QtWidgets.QHBoxLayout(self.filter_buttons_widget)
        self.filter_buttons_layout.setContentsMargins(-1, 0, -1, -1)
        self.filter_buttons_layout.setObjectName("filter_buttons_layout")
        
        self.btn_all = QtWidgets.QPushButton(self.filter_buttons_widget)
        self.btn_all.setText("Всі курси")        
        self.btn_all.setSizePolicy(sizePolicy)        
        self.btn_all.setProperty("type", "start_continue_complete")
        self.btn_all.setObjectName("btn_all")
        self.filter_buttons_layout.addWidget(self.btn_all)
        self.btn_started_all = QtWidgets.QPushButton(self.filter_buttons_widget)
        self.btn_started_all.setText("Розпочаті")
        
        
        self.btn_started_all.setSizePolicy(sizePolicy)
        self.btn_started_all.setProperty("type", "start_continue_complete")
        self.btn_started_all.setObjectName("btn_started_all")
        self.filter_buttons_layout.addWidget(self.btn_started_all)
        self.btn_completed = QtWidgets.QPushButton(self.filter_buttons_widget)
        self.btn_completed.setText("Завершені")     
        self.btn_completed.setSizePolicy(sizePolicy)
        self.btn_completed.setProperty("type", "start_continue_complete")
        self.btn_completed.setObjectName("btn_completed")
        self.filter_buttons_layout.addWidget(self.btn_completed)
        self.main_courses_layout.addWidget(self.filter_buttons_widget, 1, 0, 1, 1)

        self.left_filter_section = QtWidgets.QWidget(self.pg_courses)
        self.left_filter_section.setMinimumSize(QtCore.QSize(300, 0))
        self.left_filter_section.setMaximumSize(QtCore.QSize(300, 16777215))
        self.left_filter_section.setProperty("type", "w_pg") 
        self.left_filter_section.setObjectName("left_filter_section")
        self.left_filter_layout = QtWidgets.QGridLayout(self.left_filter_section)
        self.left_filter_layout.setContentsMargins(-1, 0, -1, 0)
        self.left_filter_layout.setSpacing(0)
        self.left_filter_layout.setObjectName("left_filter_layout")
        
        self.subject_filter_widget = QtWidgets.QWidget(self.left_filter_section)
        self.subject_filter_widget.setMinimumSize(QtCore.QSize(0, 100))
        self.subject_filter_widget.setMaximumSize(QtCore.QSize(16777215, 200))
        self.subject_filter_widget.setProperty("type", "w_pg")
        self.subject_filter_widget.setObjectName("subject_filter_widget")
        self.subject_filter_layout = QtWidgets.QGridLayout(self.subject_filter_widget)
        self.subject_filter_layout.setContentsMargins(-1, 0, -1, 0)
        self.subject_filter_layout.setHorizontalSpacing(7)
        self.subject_filter_layout.setVerticalSpacing(0)
        self.subject_filter_layout.setObjectName("subject_filter_layout")
        
        self.lb_subject = QtWidgets.QLabel(self.subject_filter_widget)
        self.lb_subject.setText("Предмет")
        self.lb_subject.setProperty("type", "lb_description")
        self.lb_subject.setSizePolicy(sizePolicy)
        self.lb_subject.setMaximumSize(QtCore.QSize(16777215, 50))
        self.lb_subject.setObjectName("lb_subject")
        self.subject_filter_layout.addWidget(self.lb_subject, 0, 0, 1, 1)
        
        self.cb_subject1 = QtWidgets.QCheckBox(self.subject_filter_widget)
        self.cb_subject1.setText("Математика")
        self.cb_subject1.setObjectName("cb_subject1")
        self.subject_filter_layout.addWidget(self.cb_subject1, 1, 0, 1, 1)
        
        self.cb_subject2 = QtWidgets.QCheckBox(self.subject_filter_widget)
        self.cb_subject2.setText("Інформатика")
        self.cb_subject2.setObjectName("cb_subject2")
        self.subject_filter_layout.addWidget(self.cb_subject2, 2, 0, 1, 1)
        self.left_filter_layout.addWidget(self.subject_filter_widget, 1, 0, 1, 1)
        
        self.level_filter_widget = QtWidgets.QWidget(self.left_filter_section)
        self.level_filter_widget.setMinimumSize(QtCore.QSize(0, 50))
        self.level_filter_widget.setMaximumSize(QtCore.QSize(16777215, 300))
        self.level_filter_widget.setProperty("type", "w_pg")
        self.level_filter_widget.setObjectName("level_filter_widget")
        self.level_filter_layout = QtWidgets.QGridLayout(self.level_filter_widget)
        self.level_filter_layout.setContentsMargins(11, 0, -1, 0)
        self.level_filter_layout.setObjectName("level_filter_layout")

        self.range_label = QtWidgets.QLabel(self.level_filter_widget)
        self.range_label.setText("Оновлення")
        self.range_label.setProperty("type", "lb_description")
        self.range_label.setMaximumSize(QtCore.QSize(16777215, 50))
        self.range_label.setObjectName("lb_range")
        self.subject_filter_layout.addWidget(self.range_label, 3, 0, 1, 1)

        self.range_slider = RangeSlider(min_value=0, max_value=500, start_min=50, start_max=250)
        self.subject_filter_layout.addWidget(self.range_slider, 4, 0, 1, 1)

        self.lb_level = QtWidgets.QLabel(self.level_filter_widget)
        self.lb_level.setText("Рівень")
        self.lb_level.setProperty("type", "lb_description")
        self.lb_level.setMaximumSize(QtCore.QSize(16777215, 50))
        self.lb_level.setObjectName("lb_level")
        self.level_filter_layout.addWidget(self.lb_level, 0, 0, 1, 1)
        
        self.rb_level1 = QtWidgets.QRadioButton(self.level_filter_widget)
        self.rb_level1.setText("Базовий")
        self.rb_level1.setObjectName("rb_level1")
        self.level_filter_layout.addWidget(self.rb_level1, 1, 0, 1, 1)
        
        self.rb_level2 = QtWidgets.QRadioButton(self.level_filter_widget)
        self.rb_level2.setText("Середній")
        self.rb_level2.setObjectName("rb_level2")
        self.level_filter_layout.addWidget(self.rb_level2, 2, 0, 1, 1)
        
        self.rb_level3 = QtWidgets.QRadioButton(self.level_filter_widget)
        self.rb_level3.setText("Високий")
        self.rb_level3.setObjectName("rb_level3")
        self.level_filter_layout.addWidget(self.rb_level3, 3, 0, 1, 1)
        
        spacerItem = QtWidgets.QSpacerItem(20, 200, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.level_filter_layout.addItem(spacerItem)
        self.left_filter_layout.addWidget(self.level_filter_widget, 2, 0, 1, 1)
        
        self.btn_clear = QtWidgets.QPushButton(self.left_filter_section)
        self.btn_clear.setText("Очистити все")
        self.btn_clear.setSizePolicy(sizePolicy)
        self.btn_clear.setMinimumSize(QtCore.QSize(0, 50))
        self.btn_clear.setMaximumSize(QtCore.QSize(16777215, 50))
        self.btn_clear.setObjectName("btn_clear")
        self.btn_clear.setProperty("type", "register")
        self.left_filter_layout.addWidget(self.btn_clear, 0, 1, 1, 1)
        
        self.btn_apply = QtWidgets.QPushButton(self.left_filter_section)
        self.btn_apply.setText("Застосувати")
        self.btn_apply.setMinimumSize(QtCore.QSize(0, 50))
        self.btn_apply.setProperty("type","start_continue")
        self.btn_apply.setObjectName("btn_apply")
        self.left_filter_layout.addWidget(self.btn_apply, 3, 0, 1, 2)
        self.main_courses_layout.addWidget(self.left_filter_section, 2, 1, 4, 1)

        self.courses_scroll_area = QtWidgets.QScrollArea(self.pg_courses)
        self.courses_scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.courses_scroll_area.setWidgetResizable(True)
        self.courses_scroll_area.setObjectName("courses_scroll_area")
        
        self.scroll_area_content = QtWidgets.QWidget()
        self.scroll_area_content.setGeometry(QtCore.QRect(-111, -476, 1110, 1066))
        self.scroll_area_content.setObjectName("scroll_area_content")
        self.course_cards_layout = QtWidgets.QGridLayout(self.scroll_area_content)
        self.course_cards_layout.setObjectName("course_cards_layout")        

        self.courses_scroll_area.setWidget(self.scroll_area_content)
        self.main_courses_layout.addWidget(self.courses_scroll_area, 2, 0, 1, 1)
        self.courses_filter_layout = QtWidgets.QHBoxLayout()
        self.courses_filter_layout.setObjectName("courses_filter_layout")
        self.main_courses_layout.addLayout(self.courses_filter_layout, 3, 0, 1, 1)
        self.lb_courses = QtWidgets.QLabel(self.pg_courses)
        self.lb_courses.setProperty("type", "title")
        self.lb_courses.setObjectName("lb_courses")
        self.lb_courses.setText("Курси")
        self.main_courses_layout.addWidget(self.lb_courses, 0, 0, 1, 1)
        self.setLayout(self.main_courses_layout)
        
        #Перелік курсів
        self.course_widgets_complete = []  # список для збереження карток
        self.add_course_widget("Python Basics", "Introduction to Python", "Математика", "Базовий", 10,8)
        self.add_course_widget("Data Science", "Learn Data Analysis", "Математика", "Середній", 15,10)
        self.add_course_widget("Web Development", "HTML, CSS, JavaScript", "Математика", "Високий", 20,20)
        self.add_course_widget("Python Basics", "Introduction to Python", "Інформатика", "Базовий", 10,7)
        self.add_course_widget("Data Science", "Learn Data Analysis", "Математика", "Базовий", 15,10)
        self.add_course_widget("Web Development", "HTML, CSS, JavaScript", "Інформатика", "Середній", 20,10)
        self.add_course_widget("Python Basics", "Introduction to Python", "Математика", "Базовий", 10,3)
        self.add_course_widget("Data Science", "Learn Data Analysis", "Інформатика", "Середній", 15,5)
        self.add_course_widget("Web Development", "HTML, CSS, JavaScript", "Інформатика", "Середній", 20,19)
        self.add_course_widget("Data Science", "Learn Data Analysis", "Інформатика", "Високий", 15,15)
        self.add_course_widget("Web Development", "HTML, CSS, JavaScript", "Інформатика", "Високий", 20,15)
        
        self.btn_completed.clicked.connect(self.show_completed_courses)
        self.btn_all.clicked.connect(self.show_all_courses)
        self.btn_started_all.clicked.connect(self.show_started_courses)
        self.btn_apply.clicked.connect(self.apply_filters)
        self.btn_clear.clicked.connect(self.clear_filters)

    def add_course_widget(self, name, description, subject, level, lessons, complete_lessons=0):
        course_card_widget = QtWidgets.QWidget(self.scroll_area_content)
        course_card_widget.setMinimumSize(QtCore.QSize(360, 330))
        course_card_widget.setProperty("type", "card")
        
        card_grid_layout = QtWidgets.QGridLayout(course_card_widget) 
        card_grid_layout.setContentsMargins(10, 10, 10, 10)  

        lb_name = QtWidgets.QLabel(course_card_widget)
        lb_name.setText(name)
        lb_name.setProperty("type", "card")
        lb_name.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        card_grid_layout.addWidget(lb_name, 0, 0, 1, 1)

        lb_description = QtWidgets.QLabel(course_card_widget)
        lb_description.setText(description)
        lb_description.setProperty("type", "lb_description")
        lb_description.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        card_grid_layout.addWidget(lb_description, 1, 0, 1, 1)

        widget_info = QtWidgets.QWidget(course_card_widget)
        widget_info.setMinimumSize(QtCore.QSize(335, 50))
        widget_info.setMaximumSize(QtCore.QSize(16666, 50))
        layout_info = QtWidgets.QHBoxLayout(widget_info)
        layout_info.setContentsMargins(0, 0, 0, 0)
        widget_info.setProperty("type", "w_pg") 
        
        lb_subject = QtWidgets.QLabel(widget_info)
        lb_subject.setText(subject)
        lb_subject.setProperty("type","lb_name_course")
        lb_subject.setMinimumSize(QtCore.QSize(165, 40))
        lb_subject.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout_info.addWidget(lb_subject)

        lb_level = QtWidgets.QLabel(widget_info)
        lb_level.setText(level)
        lb_level.setProperty("type","lb_name_course")
        lb_level.setMinimumSize(QtCore.QSize(165, 40))
        lb_level.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout_info.addWidget(lb_level)

        card_grid_layout.addWidget(widget_info, 2, 0, 1, 1)

        lb_lessons = QtWidgets.QLabel(course_card_widget)
        lb_lessons.setText(f"Lessons: {lessons}")
        lb_lessons.setMinimumSize(QtCore.QSize(0,25))
        lb_lessons.setMaximumSize(QtCore.QSize(1666666,25))
        lb_lessons.setProperty("type","lb_small")
        card_grid_layout.addWidget(lb_lessons, 3, 0, 1, 1)

        course_action_stack = QtWidgets.QStackedWidget(course_card_widget)
        course_action_stack.setMaximumSize(QtCore.QSize(16777215, 75))
        course_action_stack.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        page_start = QtWidgets.QWidget()
        page_start.setProperty("type","w_pg")
        layout_start = QtWidgets.QGridLayout(page_start)
        
        btn_start = QtWidgets.QPushButton(page_start)
        btn_start.setText("Start Course")
        btn_start.setMinimumSize(QtCore.QSize(310, 50))
        btn_start.setMaximumSize(QtCore.QSize(310, 50))
        btn_start.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        btn_start.setProperty("type","start_continue")
        layout_start.addWidget(btn_start, 0, 0, 1, 1)
        page_start.setLayout(layout_start)

        page_continue = QtWidgets.QWidget()
        page_continue.setProperty("type","w_pg")
        layout_continue = QtWidgets.QGridLayout(page_continue)  
        layout_continue.setContentsMargins(0, 0, 0, 0)
        
        btn_continue = QtWidgets.QPushButton(page_continue)
        btn_continue.setText("Continue")
        btn_continue.setMinimumSize(QtCore.QSize(310, 50))
        btn_continue.setMaximumSize(QtCore.QSize(310, 50))
        btn_continue.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        btn_continue.setProperty("type","start_continue")

        progress_bar = QtWidgets.QProgressBar(page_continue)
        progress_bar.setMinimumSize(QtCore.QSize(310, 20))
        progress_bar.setMaximumSize(QtCore.QSize(310, 20))
        progress_bar.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        progress_bar.setMaximum(lessons)
        progress_bar.setValue(complete_lessons)  
        
        layout_continue.addWidget(btn_continue, 0, 0, 1, 1)  
        layout_continue.addWidget(progress_bar, 1, 0, 1, 1)  

        page_continue.setLayout(layout_continue)

        course_action_stack.addWidget(page_start)
        course_action_stack.addWidget(page_continue)
        self.course_widgets_complete.append((course_card_widget, progress_bar, lessons))
        course_card_widget.subject = subject
        course_card_widget.level = level

        def switch_to_continue():
            course_action_stack.setCurrentWidget(page_continue)

        btn_start.clicked.connect(switch_to_continue)
        def open_lessons_page():
            print(f"Клік по уроці: {name}")
            self.pg_lessons.set_lesson_tab_by_name(name)
            self.stack.setCurrentWidget(self.pg_lessons)
           
        btn_continue.clicked.connect(open_lessons_page)

        card_grid_layout.addWidget(course_action_stack, 4, 0, 1, 1)  
        total_course_cards = self.course_cards_layout.count()
        columns = 3
        row = total_course_cards // columns
        col = total_course_cards % columns
        self.course_cards_layout.addWidget(course_card_widget, row, col, 1, 1)
        self.course_cards_layout.setColumnStretch(col, 1)
        self.course_cards_layout.setRowStretch(row, 1)

        
    def show_completed_courses(self):
        # Очистити всі курси
        for i in reversed(range(self.course_cards_layout.count())):
            item = self.course_cards_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    self.course_cards_layout.removeWidget(widget)
                    widget.setParent(None)
        # Додати завершені
        visible_index = 0
        columns = 3
        for course_card_widget, progress_bar, total_lessons in self.course_widgets_complete:
            if progress_bar.value() == total_lessons:
                row = visible_index // columns
                col = visible_index % columns
                self.course_cards_layout.addWidget(course_card_widget, row, col, 1, 1)
                visible_index += 1

    def show_all_courses(self):
        for i in reversed(range(self.course_cards_layout.count())):
            item = self.course_cards_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    self.course_cards_layout.removeWidget(widget)
                    widget.setParent(None)
        # Додати всі курси
        for i, (course_card_widget, _, _) in enumerate(self.course_widgets_complete):
            row = i // 3
            col = i % 3
            self.course_cards_layout.addWidget(course_card_widget, row, col, 1, 1)


    def show_started_courses(self):
        for i in reversed(range(self.course_cards_layout.count())):
            item = self.course_cards_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    self.course_cards_layout.removeWidget(widget)
                    widget.setParent(None)
        # Додати завершені
        visible_index = 0
        columns = 3
        for course_card_widget, progress_bar, total_lessons in self.course_widgets_complete:
            if progress_bar.value() != total_lessons:
                row = visible_index // columns
                col = visible_index % columns
                self.course_cards_layout.addWidget(course_card_widget, row, col, 1, 1)
                visible_index += 1

    def apply_filters(self):
        selected_subjects = []
        if self.cb_subject1.isChecked():
            selected_subjects.append("Математика")
        if self.cb_subject2.isChecked():
            selected_subjects.append("Інформатика")

        selected_level = None
        if self.rb_level1.isChecked():
            selected_level = "Базовий"
        elif self.rb_level2.isChecked():
            selected_level = "Середній"
        elif self.rb_level3.isChecked():
            selected_level = "Високий"
        
        for i in reversed(range(self.course_cards_layout.count())):
            item = self.course_cards_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    self.course_cards_layout.removeWidget(widget)
                    widget.setParent(None)

        # Додати курси
        visible_index = 0
        for card_widget, _, _ in self.course_widgets_complete:
            subject_match = not selected_subjects or card_widget.subject in selected_subjects
            level_match = not selected_level or card_widget.level == selected_level

            if subject_match and level_match:
                row = visible_index // 3
                col = visible_index % 3
                self.course_cards_layout.addWidget(card_widget, row, col, 1, 1)
                visible_index += 1


    def clear_filters(self):
        self.cb_subject1.setChecked(False)
        self.cb_subject2.setChecked(False)
        self.rb_level1.setAutoExclusive(False)
        self.rb_level2.setAutoExclusive(False)
        self.rb_level3.setAutoExclusive(False)
        self.rb_level1.setChecked(False)
        self.rb_level2.setChecked(False)
        self.rb_level3.setChecked(False)
        self.rb_level1.setAutoExclusive(True)
        self.rb_level2.setAutoExclusive(True)
        self.rb_level3.setAutoExclusive(True)
        self.show_all_courses()



    