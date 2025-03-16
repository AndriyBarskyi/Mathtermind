from PyQt5.QtWidgets import QWidget, QGridLayout,QVBoxLayout, QLabel,QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
#from course import*
class Page2(QWidget):
    def add_course_widget(self, name, description, subject, level, lessons):
        new_widget = QtWidgets.QWidget(self.scrollAreaWidgetContents_7)
        new_widget.setMinimumSize(QtCore.QSize(360, 330))
        new_widget.setStyleSheet("QWidget { border-radius: 25px; border: 2px solid #e6e6e6; background-color: rgb(255, 255, 255); }")
        
        grid_layout = QtWidgets.QGridLayout(new_widget) 
        grid_layout.setContentsMargins(10, 10, 10, 10)  

        lb_name = QtWidgets.QLabel(new_widget)
        lb_name.setText(name)
        lb_name.setStyleSheet("font: 75 14pt 'MS Shell Dlg 2';border-color: rgb(255, 255, 255);")
        lb_name.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        grid_layout.addWidget(lb_name, 0, 0, 1, 1)

        lb_description = QtWidgets.QLabel(new_widget)
        lb_description.setText(description)
        lb_description.setStyleSheet("font: 75 10pt 'MS Shell Dlg 2';border-color: rgb(255, 255, 255);")
        lb_description.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        grid_layout.addWidget(lb_description, 1, 0, 1, 1)

        widget_info = QtWidgets.QWidget(new_widget)
        widget_info.setMinimumSize(QtCore.QSize(335, 50))
        widget_info.setMaximumSize(QtCore.QSize(16666, 50))
        layout_info = QtWidgets.QHBoxLayout(widget_info)
        layout_info.setContentsMargins(0, 0, 0, 0)
        widget_info.setStyleSheet("border-color: rgb(255, 255, 255);")
        lb_subject = QtWidgets.QLabel(widget_info)
        lb_subject.setText(subject)
        lb_subject.setStyleSheet("border-radius: 25px; background-color: #bbebee; border: 2px solid #bbebee;")
        lb_subject.setMinimumSize(QtCore.QSize(165, 40))
        lb_subject.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout_info.addWidget(lb_subject)

        lb_level = QtWidgets.QLabel(widget_info)
        lb_level.setText(level)
        lb_level.setStyleSheet("border-radius: 25px; background-color: #bbebee; border: 2px solid #bbebee;")
        lb_level.setMinimumSize(QtCore.QSize(165, 40))
        lb_level.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout_info.addWidget(lb_level)

        grid_layout.addWidget(widget_info, 2, 0, 1, 1)

        lb_lessons = QtWidgets.QLabel(new_widget)
        lb_lessons.setText(f"Lessons: {lessons}")
        lb_lessons.setMinimumSize(QtCore.QSize(0,25))
        lb_lessons.setMaximumSize(QtCore.QSize(1666666,25))
        lb_lessons.setStyleSheet("border-color: rgb(255, 255, 255);")
        grid_layout.addWidget(lb_lessons, 3, 0, 1, 1)

        stacked_widget = QtWidgets.QStackedWidget(new_widget)
        stacked_widget.setMaximumSize(QtCore.QSize(16777215, 75))
        stacked_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        stacked_widget.setStyleSheet("border-color: rgb(255, 255, 255);")
        page_start = QtWidgets.QWidget()
        layout_start = QtWidgets.QGridLayout(page_start)
        btn_start = QtWidgets.QPushButton(page_start)
        btn_start.setText("Start Course")
        btn_start.setMinimumSize(QtCore.QSize(310, 50))
        btn_start.setMaximumSize(QtCore.QSize(310, 50))
        btn_start.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        btn_start.setStyleSheet("border-radius:25px; background: #516ed9; font: 75 15pt 'Bahnschrift'; color: white;")

        layout_start.addWidget(btn_start, 0, 0, 1, 1)
        page_start.setLayout(layout_start)

        page_continue = QtWidgets.QWidget()
        layout_continue = QtWidgets.QGridLayout(page_continue)  
        layout_continue.setContentsMargins(0, 0, 0, 0)
        btn_continue = QtWidgets.QPushButton(page_continue)
        btn_continue.setText("Continue")
        btn_continue.setMinimumSize(QtCore.QSize(310, 50))
        btn_continue.setMaximumSize(QtCore.QSize(310, 50))
        btn_continue.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        btn_continue.setStyleSheet("border-radius:25px; background: #516ed9; font: 75 15pt 'Bahnschrift'; color: white;")

        progress_bar = QtWidgets.QProgressBar(page_continue)
        progress_bar.setStyleSheet("QProgressBar {border-radius: 8px;background-color: #f3f3f3;}")
        progress_bar.setMinimumSize(QtCore.QSize(310, 20))
        progress_bar.setMaximumSize(QtCore.QSize(310, 20))
        progress_bar.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        progress_bar.setMaximum(lessons)
        progress_bar.setValue(1)  

        layout_continue.addWidget(btn_continue, 0, 0, 1, 1)  
        layout_continue.addWidget(progress_bar, 1, 0, 1, 1)  

        page_continue.setLayout(layout_continue)

        stacked_widget.addWidget(page_start)
        stacked_widget.addWidget(page_continue)

        def switch_to_continue():
                stacked_widget.setCurrentWidget(page_continue)

        btn_start.clicked.connect(switch_to_continue)

        grid_layout.addWidget(stacked_widget, 4, 0, 1, 1)  
        total_widgets = self.gridLayout_38.count()
        columns = 3
        row = total_widgets // columns
        col = total_widgets % columns
        self.gridLayout_38.addWidget(new_widget, row, col, 1, 1)
        self.gridLayout_38.setColumnStretch(col, 1)
        self.gridLayout_38.setRowStretch(row, 1)


    def __init__(self):
        super().__init__()
        self.pg_courses = QtWidgets.QWidget()
        self.pg_courses.setObjectName("pg_courses")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.pg_courses)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.widget_6 = QtWidgets.QWidget(self.pg_courses)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy)
        self.widget_6.setMinimumSize(QtCore.QSize(1020, 50))
        self.widget_6.setMaximumSize(QtCore.QSize(1600000, 50))
        self.widget_6.setStyleSheet("QWidget {\n"
"    border-radius: 25px;\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_all = QtWidgets.QPushButton(self.widget_6)
        self.btn_all.setText("Всі курси")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.btn_all.sizePolicy().hasHeightForWidth())
        self.btn_all.setSizePolicy(sizePolicy)        
        self.btn_all.setProperty("class", "menu")
        self.btn_all.setStyleSheet("""
                        QPushButton {background-color:  #f3f3f3;}
                        QPushButton:hover {background-color: rgb(230, 230, 230);}
                        QPushButton:checked {background-color: rgb(230, 230, 230);}""")
        self.btn_all.setObjectName("btn_all")
        self.horizontalLayout_2.addWidget(self.btn_all)
        self.btn_started_all = QtWidgets.QPushButton(self.widget_6)
        self.btn_started_all.setText("Розпочаті")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.btn_started_all.sizePolicy().hasHeightForWidth())
        self.btn_started_all.setSizePolicy(sizePolicy)
        self.btn_started_all.setProperty("class", "menu")
        self.btn_started_all.setStyleSheet("""
                        QPushButton {background-color:  #f3f3f3;}
                        QPushButton:hover {background-color: rgb(230, 230, 230);}
                        QPushButton:checked {background-color: rgb(230, 230, 230);}""")
        self.btn_started_all.setObjectName("btn_started_all")
        self.horizontalLayout_2.addWidget(self.btn_started_all)
        self.btn_completed = QtWidgets.QPushButton(self.widget_6)
        self.btn_completed.setText("Завершені")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.btn_completed.sizePolicy().hasHeightForWidth())
        self.btn_completed.setSizePolicy(sizePolicy)
        self.btn_completed.setProperty("class", "menu")
        self.btn_completed.setStyleSheet("""
                        QPushButton {background-color:  #f3f3f3;}
                        QPushButton:hover {background-color: rgb(230, 230, 230);}
                        QPushButton:checked {background-color: rgb(230, 230, 230);}""")
        self.btn_completed.setObjectName("btn_completed")
        self.horizontalLayout_2.addWidget(self.btn_completed)
        self.gridLayout_5.addWidget(self.widget_6, 1, 0, 1, 1)
        self.widget_9 = QtWidgets.QWidget(self.pg_courses)
        self.widget_9.setMinimumSize(QtCore.QSize(350, 0))
        self.widget_9.setMaximumSize(QtCore.QSize(350, 16777215))
        self.widget_9.setStyleSheet("QWidget {\n"
"    border-radius: 25px;\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.widget_9.setObjectName("widget_9")
        self.gridLayout_42 = QtWidgets.QGridLayout(self.widget_9)
        self.gridLayout_42.setContentsMargins(-1, 0, -1, 0)
        self.gridLayout_42.setSpacing(0)
        self.gridLayout_42.setObjectName("gridLayout_42")
        self.widget_10 = QtWidgets.QWidget(self.widget_9)
        self.widget_10.setMinimumSize(QtCore.QSize(0, 100))
        self.widget_10.setMaximumSize(QtCore.QSize(16777215, 200))
        self.widget_10.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.widget_10.setObjectName("widget_10")
        self.gridLayout_41 = QtWidgets.QGridLayout(self.widget_10)
        self.gridLayout_41.setContentsMargins(-1, 0, -1, 0)
        self.gridLayout_41.setHorizontalSpacing(7)
        self.gridLayout_41.setVerticalSpacing(0)
        self.gridLayout_41.setObjectName("gridLayout_41")
        self.lb_subject = QtWidgets.QLabel(self.widget_10)
        self.lb_subject.setText("Предмет")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_subject.sizePolicy().hasHeightForWidth())
        self.lb_subject.setSizePolicy(sizePolicy)
        self.lb_subject.setMaximumSize(QtCore.QSize(16777215, 50))
        self.lb_subject.setObjectName("lb_subject")
        self.gridLayout_41.addWidget(self.lb_subject, 0, 0, 1, 1)
        self.cb_subject1 = QtWidgets.QCheckBox(self.widget_10)
        self.cb_subject1.setText("Математика")
        self.cb_subject1.setObjectName("cb_subject1")
        self.gridLayout_41.addWidget(self.cb_subject1, 1, 0, 1, 1)
        self.cb_subject2 = QtWidgets.QCheckBox(self.widget_10)
        self.cb_subject2.setText("Математика")
        self.cb_subject2.setObjectName("cb_subject2")
        self.gridLayout_41.addWidget(self.cb_subject2, 2, 0, 1, 1)
        self.gridLayout_42.addWidget(self.widget_10, 1, 0, 1, 1)
        self.widget_11 = QtWidgets.QWidget(self.widget_9)
        self.widget_11.setMinimumSize(QtCore.QSize(0, 200))
        self.widget_11.setMaximumSize(QtCore.QSize(16777215, 300))
        self.widget_11.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.widget_11.setObjectName("widget_11")
        self.gridLayout_40 = QtWidgets.QGridLayout(self.widget_11)
        self.gridLayout_40.setContentsMargins(11, 0, -1, 0)
        self.gridLayout_40.setVerticalSpacing(0)
        self.gridLayout_40.setObjectName("gridLayout_40")
        self.lb_level = QtWidgets.QLabel(self.widget_11)
        self.lb_level.setText("Рівень")
        self.lb_level.setMaximumSize(QtCore.QSize(16777215, 50))
        self.lb_level.setObjectName("lb_level")
        self.gridLayout_40.addWidget(self.lb_level, 0, 0, 1, 1)
        self.rb_level1 = QtWidgets.QRadioButton(self.widget_11)
        self.rb_level1.setText("1")
        self.rb_level1.setObjectName("rb_level1")
        self.gridLayout_40.addWidget(self.rb_level1, 1, 0, 1, 1)
        self.rb_level2 = QtWidgets.QRadioButton(self.widget_11)
        self.rb_level2.setText("2")
        self.rb_level2.setObjectName("rb_level2")
        self.gridLayout_40.addWidget(self.rb_level2, 2, 0, 1, 1)
        self.rb_level3 = QtWidgets.QRadioButton(self.widget_11)
        self.rb_level3.setText("3")
        self.rb_level3.setObjectName("rb_level3")
        self.gridLayout_40.addWidget(self.rb_level3, 3, 0, 1, 1)
        self.rb_level4 = QtWidgets.QRadioButton(self.widget_11)
        self.rb_level4.setText("4")
        self.rb_level4.setObjectName("rb_level4")
        self.gridLayout_40.addWidget(self.rb_level4, 4, 0, 1, 1)
        self.rb_level5 = QtWidgets.QRadioButton(self.widget_11)
        self.rb_level5.setText("5")
        self.rb_level5.setObjectName("rb_level5")
        self.gridLayout_40.addWidget(self.rb_level5, 5, 0, 1, 1)
        self.gridLayout_42.addWidget(self.widget_11, 2, 0, 1, 1)
        self.btn_clear = QtWidgets.QPushButton(self.widget_9)
        self.btn_clear.setText("Очистити все")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_clear.sizePolicy().hasHeightForWidth())
        self.btn_clear.setSizePolicy(sizePolicy)
        self.btn_clear.setMinimumSize(QtCore.QSize(0, 50))
        self.btn_clear.setMaximumSize(QtCore.QSize(16777215, 50))
        self.btn_clear.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.btn_clear.setObjectName("btn_clear")
        self.gridLayout_42.addWidget(self.btn_clear, 0, 1, 1, 1)
        self.btn_apply = QtWidgets.QPushButton(self.widget_9)
        self.btn_apply.setText("Очистити все")
        self.btn_apply.setMinimumSize(QtCore.QSize(0, 50))
        self.btn_apply.setProperty("class", "blue")
        self.btn_apply.setStyleSheet("QPushButton {background-color: #516ed9;}")
        self.btn_apply.setObjectName("btn_apply")
        self.gridLayout_42.addWidget(self.btn_apply, 3, 0, 1, 2)
        self.gridLayout_5.addWidget(self.widget_9, 1, 1, 4, 1)

        self.scrollArea_6 = QtWidgets.QScrollArea(self.pg_courses)
        self.scrollArea_6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_6.setWidgetResizable(True)
        self.scrollArea_6.setObjectName("scrollArea_6")
        self.scrollAreaWidgetContents_7 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_7.setGeometry(QtCore.QRect(-111, -476, 1110, 1066))
        self.scrollAreaWidgetContents_7.setObjectName("scrollAreaWidgetContents_7")
        self.gridLayout_38 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_7)
        self.gridLayout_38.setObjectName("gridLayout_38")        

        self.add_course_widget("Python Basics", "Introduction to Python", "Python", "Beginner", 10)
        self.add_course_widget("Data Science", "Learn Data Analysis", "Data Science", "Intermediate", 15)
        self.add_course_widget("Web Development", "HTML, CSS, JavaScript", "Web", "Advanced", 20)
        self.add_course_widget("Python Basics", "Introduction to Python", "Python", "Beginner", 10)
        self.add_course_widget("Data Science", "Learn Data Analysis", "Data Science", "Intermediate", 15)
        self.add_course_widget("Web Development", "HTML, CSS, JavaScript", "Web", "Advanced", 20)
        self.add_course_widget("Python Basics", "Introduction to Python", "Python", "Beginner", 10)
        self.add_course_widget("Data Science", "Learn Data Analysis", "Data Science", "Intermediate", 15)
        self.add_course_widget("Web Development", "HTML, CSS, JavaScript", "Web", "Advanced", 20)
        self.add_course_widget("Data Science", "Learn Data Analysis", "Data Science", "Intermediate", 15)
        self.add_course_widget("Web Development", "HTML, CSS, JavaScript", "Web", "Advanced", 20)
      
        self.scrollArea_6.setWidget(self.scrollAreaWidgetContents_7)
        self.gridLayout_5.addWidget(self.scrollArea_6, 2, 0, 1, 1)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.gridLayout_5.addLayout(self.horizontalLayout_18, 3, 0, 1, 1)
        self.lb_courses = QtWidgets.QLabel(self.pg_courses)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lb_courses.setFont(font)
        self.lb_courses.setObjectName("lb_courses")
        self.lb_courses.setText("Курси")
        self.gridLayout_5.addWidget(self.lb_courses, 0, 0, 1, 1)
        self.setLayout(self.gridLayout_5)