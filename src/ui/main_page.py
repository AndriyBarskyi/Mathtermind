from PyQt5 import QtWidgets, QtCore, QtGui
from main_win import Main_page
from course_win import Course_page
from lessons_list_win import Lessons_page
from progress_win import Progress_page
from settings_win import Settings_page
from lesson_win import Lesson_page
import sys

class Ui_MainWindow(object):
    def open_lesson_page(self, widget):
        lesson_page = Lesson_page()
        lesson_page.setObjectName("pg_lesson")
        self.stackedWidget.addWidget(lesson_page)
        self.stackedWidget.setCurrentWidget(lesson_page)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1742, 865)


        self.main_stacked_widget = QtWidgets.QStackedWidget(MainWindow)
        self.main_stacked_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.centralwidget = QtWidgets.QWidget()
        
        self.centralwidget.setObjectName("centralwidget")
        self.main_layout = QtWidgets.QGridLayout(self.centralwidget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setObjectName("main_layout")
        
        self.sidebar_main_layout = QtWidgets.QVBoxLayout()
        self.sidebar_main_layout.setSpacing(0)
        self.sidebar_main_layout.setObjectName("sidebar_main_layout")
        self.sidebar_widget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sidebar_widget.sizePolicy().hasHeightForWidth())
        self.sidebar_widget.setSizePolicy(sizePolicy)
        self.sidebar_widget.setMinimumSize(QtCore.QSize(200, 50))
        self.sidebar_widget.setMaximumSize(QtCore.QSize(250, 2000))
        self.sidebar_widget.setObjectName("sidebar_widget")
        
        # Continue with the rest of the UI setup
        
        self.sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar_widget)
        self.sidebar_layout.setObjectName("sidebar_layout")
        
        self.sidebar_header_layout = QtWidgets.QVBoxLayout()
        self.sidebar_header_layout.setObjectName("sidebar_header_layout")
        
        self.sidebar_logo_label = QtWidgets.QLabel(self.sidebar_widget)
        self.sidebar_logo_label.setMinimumSize(QtCore.QSize(200, 100))
        self.sidebar_logo_label.setMaximumSize(QtCore.QSize(200, 150))
        self.sidebar_logo_label.setText("")
        self.sidebar_logo_label.setPixmap(QtGui.QPixmap("icon/logo.png"))
        self.sidebar_logo_label.setScaledContents(True)
        self.sidebar_logo_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sidebar_logo_label.setObjectName("sidebar_logo_label")
        self.sidebar_header_layout.addWidget(self.sidebar_logo_label)
        
        self.sidebar_layout.addLayout(self.sidebar_header_layout)
        
        self.sidebar_buttons_layout = QtWidgets.QVBoxLayout()
        self.sidebar_buttons_layout.setSpacing(11)
        self.sidebar_buttons_layout.setObjectName("sidebar_buttons_layout")
        
        self.menu_buttons = [
            {
                "name": "btn_main",
                "text": "Головна",
                "icon_normal": "icon/main.png",
                "icon_active": "icon/main_active.png"
            },
            {
                "name": "btn_progress",
                "text": "Прогрес",
                "icon_normal": "icon/progress.png",
                "icon_active": "icon/progress_active.png"
            },
            {
                "name": "btn_courses",
                "text": "Курси",
                "icon_normal": "icon/course.png",
                "icon_active": "icon/course_active.png"
            },
            {
                "name": "btn_lessons",
                "text": "Уроки",
                "icon_normal": "icon/lessons.png",
                "icon_active": "icon/lessons_active.png"
            },
            {
                "name": "btn_settings",
                "text": "Налаштування",
                "icon_normal": "icon/settings.png",
                "icon_active": "icon/settings_active.png"
            }
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
                button = QtWidgets.QPushButton(self.sidebar_widget)
                
                button.setLayoutDirection(QtCore.Qt.LeftToRight)
                button.setProperty("type", "main")

                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(button_config["icon_normal"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                icon.addPixmap(QtGui.QPixmap(button_config["icon_active"]), QtGui.QIcon.Active, QtGui.QIcon.On)
                button.setIcon(icon)

                button.setText(button_config["text"])
                button.setIconSize(QtCore.QSize(30, 30))
                button.setCheckable(True)
                button.setObjectName(button_config["name"])
                self.buttons_dict[button_config["name"]] = button  
                self.sidebar_buttons_layout.addWidget(button)
                button.clicked.connect(lambda checked, btn=button, page=button_config["name"]: (
                        update_buttons(btn),
                        self.stackedWidget.setCurrentWidget(getattr(self, f"pg_{page.split('_')[1]}"))  
                ))
        
        spacerItem = QtWidgets.QSpacerItem(20, 328, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.sidebar_buttons_layout.addItem(spacerItem)
        
        self.sidebar_layout.addLayout(self.sidebar_buttons_layout)
        
        self.btn_user = QtWidgets.QPushButton(self.sidebar_widget)
        self.btn_user.setText("Користувач")
        self.btn_user.setProperty("type", "user")
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/user.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_user.setIcon(icon)
        
        self.btn_user.setIconSize(QtCore.QSize(30, 30))
        self.btn_user.setObjectName("btn_user")
        
        self.sidebar_layout.addWidget(self.btn_user)
        
        self.sidebar_main_layout.addWidget(self.sidebar_widget)
        self.main_layout.addLayout(self.sidebar_main_layout, 0, 0, 1, 1)
        
        self.content_widget = QtWidgets.QWidget(self.centralwidget)
        self.content_widget.setObjectName("content_widget")
        self.content_layout = QtWidgets.QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        self.content_layout.setObjectName("content_layout")
        
        self.scrollArea = QtWidgets.QScrollArea(self.content_widget)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1421, 768))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.main_content_layout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.main_content_layout.setObjectName("main_content_layout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMinimumSize(QtCore.QSize(500, 600))
        self.stackedWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.stackedWidget.setObjectName("stackedWidget")
        self.pg_lesson=Lesson_page()
        self.pg_lesson.setObjectName("pg_lesson")
        
        
        
        self.pg_main = Main_page(self.stackedWidget, self.pg_lesson)
        self.pg_main.setObjectName("pg_main")
        self.stackedWidget.addWidget(self.pg_main)
        self.pg_progress = Progress_page()
        self.pg_progress.setObjectName("pg_progress")
        self.stackedWidget.addWidget(self.pg_progress)
        
        self.pg_lessons = Lessons_page(self.stackedWidget, self.pg_lesson)
        self.pg_lessons.setObjectName("pg_lessons")
        self.stackedWidget.addWidget(self.pg_lessons)
        
        self.pg_courses = Course_page(self.stackedWidget, self.pg_lessons)
        self.pg_courses.setObjectName("pg_courses")
        self.stackedWidget.addWidget(self.pg_courses)
        
        self.pg_settings = Settings_page()
        self.pg_settings.setObjectName("pg_settings")
        self.stackedWidget.addWidget(self.pg_settings)
        
        self.stackedWidget.addWidget(self.pg_lesson)
        
        self.main_content_layout.addWidget(self.stackedWidget, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.content_layout.addWidget(self.scrollArea)
        self.main_layout.addWidget(self.content_widget, 0, 1, 1, 1)
        
        self.main_stacked_widget.addWidget(self.centralwidget)
        MainWindow.setCentralWidget(self.main_stacked_widget) 

        
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow) 