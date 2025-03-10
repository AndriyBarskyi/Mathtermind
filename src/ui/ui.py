from PyQt5 import QtWidgets, QtCore, QtGui
from main_win import Page1
from course_win import Page2
from lessons_win import Page3
from progress_win import Page4
from settings_win import Page5
from lesson_win import Page6
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1742, 865)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        MainWindow.setStyleSheet("background-color: rgb(243, 246, 250);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_full = QtWidgets.QWidget(self.centralwidget)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_full.sizePolicy().hasHeightForWidth())
        self.widget_full.setSizePolicy(sizePolicy)
        self.widget_full.setMinimumSize(QtCore.QSize(200, 50))
        self.widget_full.setMaximumSize(QtCore.QSize(250, 2000))
        self.widget_full.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"    min-height: 50px; /* Мінімальна висота */\n"
"    max-height: 2000px; /* Максимальна висота */")
        self.widget_full.setObjectName("widget_full")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_full)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lb_icon = QtWidgets.QLabel(self.widget_full)
        self.lb_icon.setText("")
        self.lb_icon.setPixmap(QtGui.QPixmap(":/icon/logo.png"))
        self.lb_icon.setObjectName("lb_icon")
        self.verticalLayout_3.addWidget(self.lb_icon)
               

        # Створюємо список кнопок меню
        self.menu_buttons = [
        {"name": "btn_main", "icon_normal": "gray_icon/gray_home.PNG", "icon_active": "blue_icon/blue_home.PNG", "text": "Головна"},
        {"name": "btn_courses", "icon_normal": "gray_icon/gray_courses.PNG", "icon_active": "blue_icon/blue_course.PNG", "text": "Курси"},
        {"name": "btn_lessons", "icon_normal": "gray_icon/gray_lessons.PNG", "icon_active": "blue_icon/blue_lessons.PNG", "text": "Уроки"},
        {"name": "btn_progress", "icon_normal": "gray_icon/gray_progress.PNG", "icon_active": "blue_icon/blue_progress.PNG", "text": "Успішність"},
        {"name": "btn_settings", "icon_normal": "gray_icon/gray_settings.PNG", "icon_active": "blue_icon/blue_settings.PNG", "text": "Налаштування"},
        ]

        self.buttons_dict = {}
        def update_buttons(clicked_button):
                for name, btn in self.buttons_dict.items():
                        if btn == clicked_button:
                                icon_path = next(item for item in self.menu_buttons if item["name"] == name)["icon_active"]
                                btn.setIcon(QtGui.QIcon(icon_path))
                                btn.setChecked(True)
                        else:
                                icon_path = next(item for item in self.menu_buttons if item["name"] == name)["icon_normal"]
                                btn.setIcon(QtGui.QIcon(icon_path))
                                btn.setChecked(False)

        for button_config in self.menu_buttons:
                button = QtWidgets.QPushButton(self.widget_full)
                
                button.setLayoutDirection(QtCore.Qt.LeftToRight)
                button.setStyleSheet("""
                        QPushButton {
                        background-color: rgb(255, 255, 255);
                        border-radius: 25px;
                        font-size: 18px;
                        min-height: 50px;
                        max-height: 100px;
                        min-width: 50px;
                        }
                        QPushButton:hover {
                        background-color: rgb(230, 230, 230);
                        }
                        QPushButton:checked {
                        font-weight: bold;
                        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.034 rgba(0, 85, 255, 255), stop:0.039 rgba(255, 255, 255, 255));
                        color: rgb(81, 110, 217);
                        }
                """)

                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(button_config["icon_normal"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                icon.addPixmap(QtGui.QPixmap(button_config["icon_active"]), QtGui.QIcon.Active, QtGui.QIcon.On)
                button.setIcon(icon)

                button.setText(button_config["text"])
                button.setIconSize(QtCore.QSize(30, 30))
                button.setCheckable(True)
                button.setObjectName(button_config["name"])
                self.buttons_dict[button_config["name"]] = button  
                self.verticalLayout_3.addWidget(button)
                button.clicked.connect(lambda checked, btn=button, page=button_config["name"]: (
                        update_buttons(btn),
                        self.stackedWidget.setCurrentWidget(getattr(self, f"pg_{page.split('_')[1]}"))  
                ))
        
        
        spacerItem = QtWidgets.QSpacerItem(20, 328, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.btn_exit = QtWidgets.QPushButton(self.widget_full)
        self.btn_exit.setProperty("class", "menu")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icon/icon_exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_exit.setIcon(icon5)
        self.btn_exit.setIconSize(QtCore.QSize(30, 30))
        self.btn_exit.setCheckable(True)
        self.btn_exit.setObjectName("btn_exit")
        self.verticalLayout_3.addWidget(self.btn_exit)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout.addWidget(self.widget_full)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(1421, 850))
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_4.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMaximumSize(QtCore.QSize(1700, 75))
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.le_search = QtWidgets.QLineEdit(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.le_search.sizePolicy().hasHeightForWidth())
        self.le_search.setSizePolicy(sizePolicy)
        self.le_search.setMinimumSize(QtCore.QSize(600, 50))
        self.le_search.setMaximumSize(QtCore.QSize(16777215, 100))
        self.le_search.setStyleSheet("QLineEdit {background-color:rgb(230, 230, 230);}")
        self.le_search.setProperty("class", "search")
        
        self.le_search.setObjectName("le_search")
        self.horizontalLayout_16.addWidget(self.le_search)
        self.btn_search = QtWidgets.QPushButton(self.widget_2)
        self.btn_search.setMaximumSize(QtCore.QSize(200, 100))
        self.btn_search.setStyleSheet("QPushButton {\n"
"\n"
"    font-size: 16px;\n"
"\n"
"    border-radius: 15px;\n"
"min-width: 100px; /* Мінімальна ширина */\n"
"    min-height: 50px; /* Мінімальна висота */\n"
"    max-width: 200px; /* Максимальна ширина */\n"
"    max-height: 100px; /* Максимальна висота */\n"
"background-color: rgb(230, 230, 230);\n"
"}\n"
"\n"
"\n"
"")
        self.btn_search.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icon/icon_search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_search.setIcon(icon6)
        self.btn_search.setCheckable(True)
        self.btn_search.setObjectName("btn_search")
        self.horizontalLayout_16.addWidget(self.btn_search)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_16)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.btn_points = QtWidgets.QPushButton(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_points.sizePolicy().hasHeightForWidth())
        self.btn_points.setSizePolicy(sizePolicy)
        self.btn_points.setMaximumSize(QtCore.QSize(50, 100))
        self.btn_points.setStyleSheet("QPushButton {\n"
"background-color: rgb(243, 246, 250);\n"
"    border-radius: 15px;\n"
"\n"
"    min-height: 50px; /* Мінімальна висота */\n"
"\n"
"    max-height: 100px; /* Максимальна висота */\n"
"min-width: 50px; /* Мінімальна ширина */\n"
"}\n"
"\n"
"\n"
"")
        self.btn_points.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icon/point.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_points.setIcon(icon7)
        self.btn_points.setIconSize(QtCore.QSize(50, 50))
        self.btn_points.setCheckable(True)
        self.btn_points.setObjectName("btn_points")
        self.horizontalLayout_3.addWidget(self.btn_points)
        self.lb_points = QtWidgets.QLabel(self.widget_2)
        self.lb_points.setObjectName("lb_points")
        self.horizontalLayout_3.addWidget(self.lb_points)
        self.btn_user = QtWidgets.QPushButton(self.widget_2)
        self.btn_user.setMinimumSize(QtCore.QSize(50, 50))
        self.btn_user.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.btn_user.setStyleSheet("QPushButton {\n"
"    \n"
"    font-size: 16px;\n"
"\n"
"    border-radius: 15px;\n"
"\n"
"   \n"
"    background-color: rgb(230, 230, 230);\n"
"}\n"
"")
        self.btn_user.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icon/icon_users.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_user.setIcon(icon8)
        self.btn_user.setIconSize(QtCore.QSize(30, 30))
        self.btn_user.setCheckable(True)
        self.btn_user.setObjectName("btn_user")
        self.horizontalLayout_3.addWidget(self.btn_user)
        self.verticalLayout_4.addWidget(self.widget_2)
        self.scrollArea = QtWidgets.QScrollArea(self.widget)
        self.scrollArea.setMaximumSize(QtCore.QSize(1700, 16777215))
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 1421, 768))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.stackedWidget = QtWidgets.QStackedWidget(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMinimumSize(QtCore.QSize(500, 600))
        self.stackedWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.stackedWidget.setObjectName("stackedWidget")
        self.pg_main = Page1()
        self.pg_main.setObjectName("pg_main")
        self.stackedWidget.addWidget(self.pg_main)
        self.pg_progress = Page4()
        self.pg_progress.setObjectName("pg_progress")
        self.stackedWidget.addWidget(self.pg_progress)
        self.pg_courses = Page2()
        self.pg_courses.setObjectName("pg_courses")
        self.stackedWidget.addWidget(self.pg_courses)
        self.pg_lessons = Page3()
        self.pg_lessons.setObjectName("pg_lessons")
        self.stackedWidget.addWidget(self.pg_lessons)
        self.pg_settings = Page5()
        self.pg_settings.setObjectName("pg_settings")
        self.stackedWidget.addWidget(self.pg_settings)
        


        self.pg_lesson=Page6()
        self.pg_lesson.setObjectName("pg_lesson")
        self.stackedWidget.addWidget(self.pg_lesson)
        
        self.gridLayout_3.addWidget(self.stackedWidget, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_4.addWidget(self.scrollArea)
        self.gridLayout.addWidget(self.widget, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.stackedWidget.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        
    