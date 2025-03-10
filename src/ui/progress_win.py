from PyQt5.QtWidgets import QWidget, QGridLayout,QVBoxLayout, QLabel,QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
#from course import*
class Page4(QWidget):
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
                widget.setStyleSheet("QWidget {\n"
                                " border-radius: 15px;\n"
                                " background-color: rgb(255, 0, 0);\n"
                                "}")
                widget.setObjectName(f"tab1_w{i}")
                widget.setToolTip(f"Це {widget.objectName()}")
                row = (i - 1) // cols
                col = (i - 1) % cols
                grid_layout.addWidget(widget, row, col, 1, 1)
        self.pg4_tabs.addTab(tab_widget, name)

        

    def __init__(self):
        super().__init__()
        self.pg_progress = QtWidgets.QWidget()
        self.pg_progress.setObjectName("pg_progress")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.pg_progress)
        self.gridLayout_6.setHorizontalSpacing(7)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.w_pg4_success = QtWidgets.QWidget(self.pg_progress)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pg4_success.sizePolicy().hasHeightForWidth())
        self.w_pg4_success.setSizePolicy(sizePolicy)
        self.w_pg4_success.setMinimumSize(QtCore.QSize(311, 341))
        self.w_pg4_success.setStyleSheet("QWidget {\n"
"    border-radius: 25px;\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.w_pg4_success.setObjectName("w_pg4_success")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.w_pg4_success)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.lb_success = QtWidgets.QLabel(self.w_pg4_success)
        self.lb_success.setText("Успішність")
        self.lb_success.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lb_success.setFont(font)
        self.lb_success.setObjectName("lb_success")
        self.gridLayout_15.addWidget(self.lb_success, 0, 0, 1, 1)
        self.graph2 = QtWidgets.QWidget(self.w_pg4_success)
        self.graph2.setObjectName("graph2")
        self.gridLayout_15.addWidget(self.graph2, 1, 0, 1, 1)
        self.gridLayout_6.addWidget(self.w_pg4_success, 1, 2, 3, 1)
        self.w_pg4_activity = QtWidgets.QWidget(self.pg_progress)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pg4_activity.sizePolicy().hasHeightForWidth())
        self.w_pg4_activity.setSizePolicy(sizePolicy)
        self.w_pg4_activity.setMinimumSize(QtCore.QSize(311, 341))
        self.w_pg4_activity.setStyleSheet("QWidget {\n"
"    border-radius: 25px;\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.w_pg4_activity.setObjectName("w_pg4_activity")
        self.gridLayout_155 = QtWidgets.QGridLayout(self.w_pg4_activity)
        self.gridLayout_155.setObjectName("gridLayout_155")
        self.lb_activity_2 = QtWidgets.QLabel(self.w_pg4_activity)
        self.lb_activity_2.setText("Активність")
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lb_activity_2.setFont(font)
        self.lb_activity_2.setObjectName("lb_activity_2")
        self.gridLayout_155.addWidget(self.lb_activity_2, 0, 0, 1, 1)
        self.w_pg4_activity_w1 = QtWidgets.QWidget(self.w_pg4_activity)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pg4_activity_w1.sizePolicy().hasHeightForWidth())
        self.w_pg4_activity_w1.setSizePolicy(sizePolicy)
        self.w_pg4_activity_w1.setStyleSheet("QWidget {\n"
"    border-radius: 25px;\n"
"border: 2px solid #e6e6e6;\n"
"background-color: rgb(255, 255, 255);\n"
"    \n"
"}")
        self.w_pg4_activity_w1.setObjectName("w_pg4_activity_w1")
        self.gridLayout_27 = QtWidgets.QGridLayout(self.w_pg4_activity_w1)
        self.gridLayout_27.setObjectName("gridLayout_27")
        self.im_num_of_courses = QtWidgets.QLabel(self.w_pg4_activity_w1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.im_num_of_courses.sizePolicy().hasHeightForWidth())
        self.im_num_of_courses.setSizePolicy(sizePolicy)
        self.im_num_of_courses.setMaximumSize(QtCore.QSize(100, 16777215))
        self.im_num_of_courses.setStyleSheet("border-color: rgb(255, 255, 255);\n"
"image: url(icon/icon_hat.PNG);\n"
"font: 75 14pt \"MS Shell Dlg 2\";")
        self.im_num_of_courses.setText("")
        self.im_num_of_courses.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.im_num_of_courses.setObjectName("im_num_of_courses")
        self.gridLayout_27.addWidget(self.im_num_of_courses, 0, 0, 1, 1)
        self.lb_num_of_courses = QtWidgets.QLabel(self.w_pg4_activity_w1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_num_of_courses.sizePolicy().hasHeightForWidth())
        self.lb_num_of_courses.setSizePolicy(sizePolicy)
        self.lb_num_of_courses.setMinimumSize(QtCore.QSize(200, 0))
        self.lb_num_of_courses.setStyleSheet("border-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"MS Shell Dlg 2\";")
        self.lb_num_of_courses.setObjectName("lb_num_of_courses")
        self.gridLayout_27.addWidget(self.lb_num_of_courses, 0, 1, 1, 1)
        self.lb_des1 = QtWidgets.QLabel(self.w_pg4_activity_w1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_des1.sizePolicy().hasHeightForWidth())
        self.lb_des1.setSizePolicy(sizePolicy)
        self.lb_des1.setMinimumSize(QtCore.QSize(0, 58))
        self.lb_des1.setStyleSheet("border-color: rgb(255, 255, 255);\n"
"font: 75 10pt \"MS Shell Dlg 2\";")
        self.lb_des1.setObjectName("lb_des1")
        self.gridLayout_27.addWidget(self.lb_des1, 1, 0, 1, 2)
        self.gridLayout_155.addWidget(self.w_pg4_activity_w1, 1, 0, 1, 1)
        self.w_pg4_activity_w2 = QtWidgets.QWidget(self.w_pg4_activity)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pg4_activity_w2.sizePolicy().hasHeightForWidth())
        self.w_pg4_activity_w2.setSizePolicy(sizePolicy)
        self.w_pg4_activity_w2.setStyleSheet("QWidget {\n"
"    border-radius: 25px;\n"
"border: 2px solid #e6e6e6;\n"
"background-color: rgb(255, 255, 255);\n"
"    \n"
"}")
        self.w_pg4_activity_w2.setObjectName("w_pg4_activity_w2")
        self.gridLayout_152 = QtWidgets.QGridLayout(self.w_pg4_activity_w2)
        self.gridLayout_152.setObjectName("gridLayout_152")
        self.lb_num_of_lessons = QtWidgets.QLabel(self.w_pg4_activity_w2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_num_of_lessons.sizePolicy().hasHeightForWidth())
        self.lb_num_of_lessons.setSizePolicy(sizePolicy)
        self.lb_num_of_lessons.setMinimumSize(QtCore.QSize(200, 0))
        self.lb_num_of_lessons.setStyleSheet("border-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"MS Shell Dlg 2\";")
        self.lb_num_of_lessons.setObjectName("lb_num_of_lessons")
        self.gridLayout_152.addWidget(self.lb_num_of_lessons, 0, 1, 1, 1)
        self.lb_des2 = QtWidgets.QLabel(self.w_pg4_activity_w2)
        self.lb_des2.setStyleSheet("border-color: rgb(255, 255, 255);\n"
"font: 75 10pt \"MS Shell Dlg 2\";")
        self.lb_des2.setObjectName("lb_des2")
        self.gridLayout_152.addWidget(self.lb_des2, 1, 0, 1, 2)
        self.im_num_of_lessons = QtWidgets.QLabel(self.w_pg4_activity_w2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.im_num_of_lessons.sizePolicy().hasHeightForWidth())
        self.im_num_of_lessons.setSizePolicy(sizePolicy)
        self.im_num_of_lessons.setMaximumSize(QtCore.QSize(100, 16777215))
        self.im_num_of_lessons.setStyleSheet("border-color: rgb(255, 255, 255);\n"
"image: url(icon/icon_book2.PNG);\n"
"font: 75 14pt \"MS Shell Dlg 2\";")
        self.im_num_of_lessons.setText("")
        self.im_num_of_lessons.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.im_num_of_lessons.setObjectName("im_num_of_lessons")
        self.gridLayout_152.addWidget(self.im_num_of_lessons, 0, 0, 1, 1)
        self.gridLayout_155.addWidget(self.w_pg4_activity_w2, 1, 1, 1, 1)
        self.w_pg4_activity_w3 = QtWidgets.QWidget(self.w_pg4_activity)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pg4_activity_w3.sizePolicy().hasHeightForWidth())
        self.w_pg4_activity_w3.setSizePolicy(sizePolicy)
        self.w_pg4_activity_w3.setStyleSheet("QWidget {\n"
"    border-radius: 25px;\n"
"border: 2px solid #e6e6e6;\n"
"background-color: rgb(255, 255, 255);\n"
"    \n"
"}")
        self.w_pg4_activity_w3.setObjectName("w_pg4_activity_w3")
        self.gridLayout_154 = QtWidgets.QGridLayout(self.w_pg4_activity_w3)
        self.gridLayout_154.setObjectName("gridLayout_154")
        self.lb_num_of_awards = QtWidgets.QLabel(self.w_pg4_activity_w3)
        self.lb_num_of_awards.setMinimumSize(QtCore.QSize(200, 0))
        self.lb_num_of_awards.setStyleSheet("border-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"MS Shell Dlg 2\";")
        self.lb_num_of_awards.setObjectName("lb_num_of_awards")
        self.gridLayout_154.addWidget(self.lb_num_of_awards, 0, 1, 1, 1)
        self.im_num_of_awards = QtWidgets.QLabel(self.w_pg4_activity_w3)
        self.im_num_of_awards.setMaximumSize(QtCore.QSize(100, 16777215))
        self.im_num_of_awards.setStyleSheet("border-color: rgb(255, 255, 255);\n"
"image: url(icon/icon_award.PNG);\n"
"font: 75 14pt \"MS Shell Dlg 2\";")
        self.im_num_of_awards.setText("")
        self.im_num_of_awards.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.im_num_of_awards.setObjectName("im_num_of_awards")
        self.gridLayout_154.addWidget(self.im_num_of_awards, 0, 0, 1, 1)
        self.lb_des3 = QtWidgets.QLabel(self.w_pg4_activity_w3)
        self.lb_des3.setStyleSheet("border-color: rgb(255, 255, 255);\n"
"font: 75 10pt \"MS Shell Dlg 2\";")
        self.lb_des3.setObjectName("lb_des3")
        self.gridLayout_154.addWidget(self.lb_des3, 1, 0, 1, 2)
        self.gridLayout_155.addWidget(self.w_pg4_activity_w3, 2, 0, 1, 1)
        self.w_pg4_activity_w4 = QtWidgets.QWidget(self.w_pg4_activity)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pg4_activity_w4.sizePolicy().hasHeightForWidth())
        self.w_pg4_activity_w4.setSizePolicy(sizePolicy)
        self.w_pg4_activity_w4.setStyleSheet("QWidget {\n"
"    border-radius: 25px;\n"
"border: 2px solid #e6e6e6;\n"
"background-color: rgb(255, 255, 255);\n"
"    \n"
"}")
        self.w_pg4_activity_w4.setObjectName("w_pg4_activity_w4")
        self.gridLayout_153 = QtWidgets.QGridLayout(self.w_pg4_activity_w4)
        self.gridLayout_153.setObjectName("gridLayout_153")
        self.lb_num_of_tasks = QtWidgets.QLabel(self.w_pg4_activity_w4)
        self.lb_num_of_tasks.setMinimumSize(QtCore.QSize(200, 0))
        self.lb_num_of_tasks.setStyleSheet("border-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"MS Shell Dlg 2\";")
        self.lb_num_of_tasks.setObjectName("lb_num_of_tasks")
        self.gridLayout_153.addWidget(self.lb_num_of_tasks, 0, 1, 1, 1)
        self.im_num_of_tasks = QtWidgets.QLabel(self.w_pg4_activity_w4)
        self.im_num_of_tasks.setMaximumSize(QtCore.QSize(100, 16777215))
        self.im_num_of_tasks.setStyleSheet("border-color: rgb(255, 255, 255);\n"
"image: url(icon/icon_tasks.PNG);\n"
"font: 75 14pt \"MS Shell Dlg 2\";")
        self.im_num_of_tasks.setText("")
        self.im_num_of_tasks.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.im_num_of_tasks.setObjectName("im_num_of_tasks")
        self.gridLayout_153.addWidget(self.im_num_of_tasks, 0, 0, 1, 1)
        self.lb_des4 = QtWidgets.QLabel(self.w_pg4_activity_w4)
        self.lb_des4.setStyleSheet("border-color: rgb(255, 255, 255);\n"
"font: 75 10pt \"MS Shell Dlg 2\";")
        self.lb_des4.setObjectName("lb_des4")
        self.gridLayout_153.addWidget(self.lb_des4, 1, 0, 1, 2)
        self.gridLayout_155.addWidget(self.w_pg4_activity_w4, 2, 1, 1, 1)
        self.gridLayout_6.addWidget(self.w_pg4_activity, 4, 0, 1, 1)
        self.scrollArea_3 = QtWidgets.QScrollArea(self.pg_progress)
        self.scrollArea_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 664, 341))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents_4.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_4.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.gridLayout_156 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_4)
        self.gridLayout_156.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_156.setObjectName("gridLayout_156")
        self.w_pg4_course_success_4 = QtWidgets.QWidget(self.scrollAreaWidgetContents_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pg4_course_success_4.sizePolicy().hasHeightForWidth())
        self.w_pg4_course_success_4.setSizePolicy(sizePolicy)
        self.w_pg4_course_success_4.setMinimumSize(QtCore.QSize(311, 341))
        self.w_pg4_course_success_4.setStyleSheet("QWidget {\n"
"    border-radius: 25px;\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.w_pg4_course_success_4.setObjectName("w_pg4_course_success_4")
        self.gridLayout_16 = QtWidgets.QGridLayout(self.w_pg4_course_success_4)
        self.gridLayout_16.setContentsMargins(11, 20, 0, 0)
        self.gridLayout_16.setSpacing(0)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.lb_course_success = QtWidgets.QLabel(self.w_pg4_course_success_4)
        self.lb_course_success.setText("Успішність по курсах")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_course_success.sizePolicy().hasHeightForWidth())
        self.lb_course_success.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lb_course_success.setFont(font)
        self.lb_course_success.setObjectName("lb_course_success")
        self.gridLayout_16.addWidget(self.lb_course_success, 0, 0, 1, 1)
        self.pg4_tabs = QtWidgets.QTabWidget(self.w_pg4_course_success_4)
        self.pg4_tabs.setMinimumSize(QtCore.QSize(660, 300))
        self.pg4_tabs.setLayoutDirection(QtCore.Qt.LeftToRight)
        
        self.pg4_tabs.setTabPosition(QtWidgets.QTabWidget.North)
        self.pg4_tabs.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.pg4_tabs.setObjectName("pg4_tabs")
        
        # Використання функції для створення вкладки з 13 віджетами:
        self.create_tab_with_widgets("1", 13, 3, 5)  # 3 рядки, 5 стовпців
        self.create_tab_with_widgets("2", 25, 10, 5)  # 3 рядки, 5 стовпців
        

        
        self.gridLayout_16.addWidget(self.pg4_tabs, 1, 0, 1, 1)
        self.gridLayout_156.addWidget(self.w_pg4_course_success_4, 0, 0, 1, 1)
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_4)
        self.gridLayout_6.addWidget(self.scrollArea_3, 4, 2, 1, 1)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.pg_progress)
        self.scrollArea_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 685, 341))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.w_pg4_course = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pg4_course.sizePolicy().hasHeightForWidth())
        self.w_pg4_course.setSizePolicy(sizePolicy)
        self.w_pg4_course.setMinimumSize(QtCore.QSize(321, 341))
        self.w_pg4_course.setStyleSheet("QWidget {\n"
"    border-radius: 25px;\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.w_pg4_course.setObjectName("w_pg4_course")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.w_pg4_course)
        self.gridLayout_11.setObjectName("gridLayout_11")

        """self.lb_cources = QtWidgets.QLabel(self.w_pg4_success)
        self.lb_cources.setText("Успішність")
        self.lb_cources.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lb_cources.setFont(font)
        self.lb_cources.setObjectName("lb_cources")
        self.gridLayout_11.addWidget(self.lb_cources, 0, 0, 1, 1)"""




        # Дані для QLabel і ProgressBar
        labels_data = [
        ("lb_course_1", "Назва курсу 1", 24),
        ("lb_course_2", "Назва курсу 2", 50),
        ("lb_course_3", "Назва курсу 3", 75),
        ("lb_course_4", "Назва курсу 4", 100)
        ]
      
        # Цикл для створення QLabel і ProgressBar
        for idx, (label_name, label_text, progress_value) in enumerate(labels_data):
                # Створення QLabel
                label = QtWidgets.QLabel(self.w_pg4_course)
                label.setText(label_text)
                label.setMinimumSize(QtCore.QSize(0, 50))
                label.setMaximumSize(QtCore.QSize(16777215, 50))
                label.setObjectName(label_name)
        
                # Додавання QLabel до layout
                self.gridLayout_11.addWidget(label, idx * 3, 0, 1, 1)  # Можна змінити позицію за потреби

                # Створення QProgressBar
                progress_bar = QtWidgets.QProgressBar(self.w_pg4_course)
                progress_bar.setMinimumSize(QtCore.QSize(0, 20))
                progress_bar.setMaximumSize(QtCore.QSize(16777215, 20))
                progress_bar.setProperty("value", progress_value)
                progress_bar.setTextVisible(False)
                progress_bar.setOrientation(QtCore.Qt.Horizontal)
                progress_bar.setObjectName(f"pg4_progress{idx+1}")
                progress_bar.setStyleSheet("QProgressBar {border-radius: 8px;background-color: #f3f3f3;}")

                # Створення QLabel для відсотків (напроти прогрес-бара)
                lb_interest_2 = QtWidgets.QLabel(self.w_pg4_course)
                lb_interest_2.setText(f"{progress_value}%")
                lb_interest_2.setMinimumSize(QtCore.QSize(0, 50))
                lb_interest_2.setMaximumSize(QtCore.QSize(16777215, 50))
                lb_interest_2.setObjectName("lb_interest_2")

                # Додавання QLabel з відсотками напроти прогрес-бара
                self.gridLayout_11.addWidget(lb_interest_2, idx * 3 + 1, 2, 1, 1)
                
                # Додавання QProgressBar до layout
                self.gridLayout_11.addWidget(progress_bar, idx * 3 + 1, 0, 1, 2)  # Розташування під QLabel




        #self.gridLayout_11.addWidget(self.pg4_progress1, 3, 0, 1, 2)
        self.gridLayout_12.addWidget(self.w_pg4_course, 0, 0, 1, 1)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_6.addWidget(self.scrollArea_2, 1, 0, 3, 1)
        self.lb_progress = QtWidgets.QLabel(self.pg_progress)
        self.lb_progress.setText("Успішність")
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lb_progress.setFont(font)
        self.lb_progress.setObjectName("lb_progress")
        self.gridLayout_6.addWidget(self.lb_progress, 0, 0, 1, 1)

        self.setLayout(self.gridLayout_6)