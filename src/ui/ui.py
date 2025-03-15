from PyQt5 import QtWidgets, QtCore, QtGui
from src.ui.main_win import DashboardPage
from src.ui.course_win import CoursesPage
from src.ui.progress_win import ProgressPage
from src.ui.settings_win import SettingsPage
from src.ui.lesson_win import LessonDetailPage
from src.ui.theme import ThemeManager

class MainWindowUI(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        
        # Get screen dimensions and set window size relative to screen
        screen = QtWidgets.QDesktopWidget().availableGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        
        # Set window size to 80% of screen width and 90% of screen height
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.9)
        MainWindow.resize(window_width, window_height)

        appIcon = QtGui.QIcon()
        appIcon.addPixmap(QtGui.QPixmap("icon/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(appIcon)

        # Use theme manager for background color
        MainWindow.setStyleSheet(f"background-color: {ThemeManager.get_color('app_background')};")
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        self.sidebarLayout = QtWidgets.QVBoxLayout()
        self.sidebarLayout.setSpacing(0)
        self.sidebarLayout.setObjectName("sidebarLayout")
        self.sidebarContainer = QtWidgets.QWidget(self.centralwidget)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sidebarContainer.sizePolicy().hasHeightForWidth())
        self.sidebarContainer.setSizePolicy(sizePolicy)
        
        # Set sidebar width relative to screen width (15-20% of screen width)
        sidebar_min_width = max(200, int(screen_width * 0.15))
        sidebar_max_width = max(250, int(screen_width * 0.2))
        
        self.sidebarContainer.setMinimumSize(QtCore.QSize(sidebar_min_width, 50))
        self.sidebarContainer.setMaximumSize(QtCore.QSize(sidebar_max_width, 2000))
        
        # Use theme manager for sidebar styling
        self.sidebarContainer.setStyleSheet(f"background-color: {ThemeManager.get_color('sidebar_background')};\n"
"    min-height: 50px; /* Мінімальна висота */\n"
"    max-height: 2000px; /* Максимальна висота */")
        
        self.sidebarContainer.setObjectName("sidebarContainer")
        self.sidebarHorizontalLayout = QtWidgets.QHBoxLayout(self.sidebarContainer)
        self.sidebarHorizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.sidebarHorizontalLayout.setSpacing(0)
        self.sidebarHorizontalLayout.setObjectName("sidebarHorizontalLayout")
        self.menuButtonsLayout = QtWidgets.QVBoxLayout()
        self.menuButtonsLayout.setSpacing(0)
        self.menuButtonsLayout.setObjectName("menuButtonsLayout")
        self.logoLabel = QtWidgets.QLabel(self.sidebarContainer)
        self.logoLabel.setText("")
        self.logoLabel.setPixmap(QtGui.QPixmap(":/icon/logo.png"))
        self.logoLabel.setObjectName("logoLabel")
        self.menuButtonsLayout.addWidget(self.logoLabel)
               

        # Create menu buttons list
        self.menuButtonsConfig = [
            {"name": "btn_main", "icon_normal": "gray_icon/gray_home.PNG", "icon_active": "blue_icon/blue_home.PNG", "text": "Головна"},
            {"name": "btn_courses", "icon_normal": "gray_icon/gray_courses.PNG", "icon_active": "blue_icon/blue_course.PNG", "text": "Курси"},
            {"name": "btn_lessons", "icon_normal": "gray_icon/gray_lessons.PNG", "icon_active": "blue_icon/blue_lessons.PNG", "text": "Уроки"},
            {"name": "btn_progress", "icon_normal": "gray_icon/gray_progress.PNG", "icon_active": "blue_icon/blue_progress.PNG", "text": "Успішність"},
            {"name": "btn_settings", "icon_normal": "gray_icon/gray_settings.PNG", "icon_active": "blue_icon/blue_settings.PNG", "text": "Налаштування"},
        ]

        self.menuButtons = {}
        def updateActiveButton(clickedButton):
                for name, btn in self.menuButtons.items():
                        if btn == clickedButton:
                                iconPath = next(item for item in self.menuButtonsConfig if item["name"] == name)["icon_active"]
                                btn.setIcon(QtGui.QIcon(iconPath))
                                btn.setChecked(True)
                        else:
                                iconPath = next(item for item in self.menuButtonsConfig if item["name"] == name)["icon_normal"]
                                btn.setIcon(QtGui.QIcon(iconPath))
                                btn.setChecked(False)

        for buttonConfig in self.menuButtonsConfig:
                button = QtWidgets.QPushButton(self.sidebarContainer)
                
                button.setLayoutDirection(QtCore.Qt.LeftToRight)
                
                # Use theme manager for button styling
                button.setStyleSheet(f"""
                        QPushButton {{
                        background-color: {ThemeManager.get_color('sidebar_background')};
                        border-radius: 25px;
                        font-size: 18px;
                        min-height: 50px;
                        max-height: 100px;
                        min-width: 50px;
                        color: {ThemeManager.get_color('primary_text')};
                        }}
                        QPushButton:hover {{
                        background-color: {ThemeManager.get_color('button_hover_background')};
                        }}
                        QPushButton:checked {{
                        font-weight: bold;
                        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                                                        stop:0.034 {ThemeManager.get_color('accent_primary')}, 
                                                        stop:0.039 {ThemeManager.get_color('sidebar_background')});
                        color: {ThemeManager.get_color('accent_primary')};
                        }}
                """)

                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(buttonConfig["icon_normal"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                icon.addPixmap(QtGui.QPixmap(buttonConfig["icon_active"]), QtGui.QIcon.Active, QtGui.QIcon.On)
                button.setIcon(icon)

                button.setText(buttonConfig["text"])
                button.setIconSize(QtCore.QSize(30, 30))
                button.setCheckable(True)
                button.setObjectName(buttonConfig["name"])
                self.menuButtons[buttonConfig["name"]] = button  
                self.menuButtonsLayout.addWidget(button)
                button.clicked.connect(lambda checked, btn=button, page=buttonConfig["name"]: (
                        updateActiveButton(btn),
                        self.stackedWidget.setCurrentWidget(getattr(self, f"pg_{page.split('_')[1]}"))  
                ))
        
        
        spacerItem = QtWidgets.QSpacerItem(20, 328, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.menuButtonsLayout.addItem(spacerItem)
        self.exitButton = QtWidgets.QPushButton(self.sidebarContainer)
        self.exitButton.setProperty("class", "menu")
        exitIcon = QtGui.QIcon()
        exitIcon.addPixmap(QtGui.QPixmap("icon/icon_exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exitButton.setIcon(exitIcon)
        self.exitButton.setIconSize(QtCore.QSize(30, 30))
        self.exitButton.setCheckable(True)
        self.exitButton.setObjectName("exitButton")
        self.menuButtonsLayout.addWidget(self.exitButton)
        self.sidebarHorizontalLayout.addLayout(self.menuButtonsLayout)
        self.sidebarLayout.addWidget(self.sidebarContainer)
        self.gridLayout.addLayout(self.sidebarLayout, 0, 0, 1, 1)
        
        # Main content container
        self.mainContentContainer = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)  # Give main content more stretch priority
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainContentContainer.sizePolicy().hasHeightForWidth())
        self.mainContentContainer.setSizePolicy(sizePolicy)
        
        # Calculate main content width based on screen size
        main_content_min_width = int(screen_width * 0.6)  # At least 60% of screen width
        
        self.mainContentContainer.setMinimumSize(QtCore.QSize(main_content_min_width, window_height - 20))
        self.mainContentContainer.setStyleSheet("")
        self.mainContentContainer.setObjectName("mainContentContainer")
        self.mainContentLayout = QtWidgets.QVBoxLayout(self.mainContentContainer)
        self.mainContentLayout.setContentsMargins(0, -1, 0, -1)
        self.mainContentLayout.setSpacing(0)
        self.mainContentLayout.setObjectName("mainContentLayout")
        
        # Header container
        self.headerContainer = QtWidgets.QWidget(self.mainContentContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.headerContainer.sizePolicy().hasHeightForWidth())
        self.headerContainer.setSizePolicy(sizePolicy)
        
        # Set header height proportional to window height
        header_height = int(window_height * 0.08)  # 8% of window height
        self.headerContainer.setMaximumSize(QtCore.QSize(16777215, header_height))
        self.headerContainer.setMinimumSize(QtCore.QSize(0, header_height))
        
        self.headerContainer.setObjectName("headerContainer")
        self.headerLayout = QtWidgets.QHBoxLayout(self.headerContainer)
        self.headerLayout.setObjectName("headerLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.headerLayout.addItem(spacerItem1)
        self.searchLayout = QtWidgets.QHBoxLayout()
        self.searchLayout.setObjectName("searchLayout")
        
        # Search input
        self.searchInput = QtWidgets.QLineEdit(self.headerContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.searchInput.sizePolicy().hasHeightForWidth())
        self.searchInput.setSizePolicy(sizePolicy)
        
        # Set search input width relative to screen width
        search_input_width = int(screen_width * 0.3)  # 30% of screen width
        self.searchInput.setMinimumSize(QtCore.QSize(search_input_width, 50))
        
        self.searchInput.setMaximumSize(QtCore.QSize(16777215, 100))
        
        # Use theme manager for search input styling
        self.searchInput.setStyleSheet(f"QLineEdit {{background-color:{ThemeManager.get_color('input_background')};color:{ThemeManager.get_color('primary_text')}}}")
        
        self.searchInput.setProperty("class", "search")
        
        self.searchInput.setObjectName("searchInput")
        self.searchLayout.addWidget(self.searchInput)
        self.searchButton = QtWidgets.QPushButton(self.headerContainer)
        self.searchButton.setMaximumSize(QtCore.QSize(200, 100))
        
        # Use theme manager for search button styling
        self.searchButton.setStyleSheet(f"""
            QPushButton {{
                font-size: 16px;
                border-radius: 15px;
                min-width: 100px;
                min-height: 50px;
                max-width: 200px;
                max-height: 100px;
                background-color: {ThemeManager.get_color('button_background')};
                color: {ThemeManager.get_color('primary_text')};
            }}
        """)
        
        self.searchButton.setText("")
        searchIcon = QtGui.QIcon()
        searchIcon.addPixmap(QtGui.QPixmap("icon/icon_search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.searchButton.setIcon(searchIcon)
        self.searchButton.setCheckable(True)
        self.searchButton.setObjectName("searchButton")
        self.searchLayout.addWidget(self.searchButton)
        self.headerLayout.addLayout(self.searchLayout)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.headerLayout.addItem(spacerItem2)
        self.pointsButton = QtWidgets.QPushButton(self.headerContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pointsButton.sizePolicy().hasHeightForWidth())
        self.pointsButton.setSizePolicy(sizePolicy)
        self.pointsButton.setMaximumSize(QtCore.QSize(50, 100))
        
        # Use theme manager for points button styling
        self.pointsButton.setStyleSheet(f"""
            QPushButton {{
                background-color: {ThemeManager.get_color('app_background')};
                border-radius: 15px;
                min-height: 50px;
                max-height: 100px;
                min-width: 50px;
                color: {ThemeManager.get_color('primary_text')};
            }}
        """)
        
        self.pointsButton.setText("")
        pointsIcon = QtGui.QIcon()
        pointsIcon.addPixmap(QtGui.QPixmap("icon/point.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pointsButton.setIcon(pointsIcon)
        self.pointsButton.setIconSize(QtCore.QSize(50, 50))
        self.pointsButton.setCheckable(True)
        self.pointsButton.setObjectName("pointsButton")
        self.headerLayout.addWidget(self.pointsButton)
        self.pointsLabel = QtWidgets.QLabel(self.headerContainer)
        self.pointsLabel.setObjectName("pointsLabel")
        self.headerLayout.addWidget(self.pointsLabel)
        self.userButton = QtWidgets.QPushButton(self.headerContainer)
        self.userButton.setMinimumSize(QtCore.QSize(50, 50))
        self.userButton.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        
        # Use theme manager for user button styling
        self.userButton.setStyleSheet(f"""
            QPushButton {{
                font-size: 16px;
                border-radius: 15px;
                background-color: {ThemeManager.get_color('button_background')};
                color: {ThemeManager.get_color('primary_text')};
            }}
        """)
        
        self.userButton.setText("")
        userIcon = QtGui.QIcon()
        userIcon.addPixmap(QtGui.QPixmap("icon/icon_users.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.userButton.setIcon(userIcon)
        self.userButton.setIconSize(QtCore.QSize(30, 30))
        self.userButton.setCheckable(True)
        self.userButton.setObjectName("userButton")
        self.headerLayout.addWidget(self.userButton)
        self.mainContentLayout.addWidget(self.headerContainer)
        
        # Content scroll area
        self.contentScrollArea = QtWidgets.QScrollArea(self.mainContentContainer)
        self.contentScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.contentScrollArea.setWidgetResizable(True)
        self.contentScrollArea.setObjectName("contentScrollArea")
        
        self.scrollAreaContent = QtWidgets.QWidget()
        # Let the scroll area content size be determined by its parent
        self.scrollAreaContent.setObjectName("scrollAreaContent")
        
        self.contentGridLayout = QtWidgets.QGridLayout(self.scrollAreaContent)
        self.contentGridLayout.setObjectName("contentGridLayout")
        
        # Stacked widget for different pages
        self.stackedWidget = QtWidgets.QStackedWidget(self.scrollAreaContent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        
        # Set minimum size for stacked widget based on screen dimensions
        stacked_min_width = int(screen_width * 0.5)  # 50% of screen width
        stacked_min_height = int(screen_height * 0.6)  # 60% of screen height
        self.stackedWidget.setMinimumSize(QtCore.QSize(stacked_min_width, stacked_min_height))
        
        self.stackedWidget.setObjectName("stackedWidget")
        self.pg_main = DashboardPage()
        self.pg_main.setObjectName("pg_main")
        self.stackedWidget.addWidget(self.pg_main)
        self.pg_progress = ProgressPage()
        self.pg_progress.setObjectName("pg_progress")
        self.stackedWidget.addWidget(self.pg_progress)
        self.pg_courses = CoursesPage()
        self.pg_courses.setObjectName("pg_courses")
        self.stackedWidget.addWidget(self.pg_courses)
        self.pg_lessons = LessonDetailPage()
        self.pg_lessons.setObjectName("pg_lessons")
        self.stackedWidget.addWidget(self.pg_lessons)
        self.pg_settings = SettingsPage()
        self.pg_settings.setObjectName("pg_settings")
        self.stackedWidget.addWidget(self.pg_settings)
        
        self.contentGridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)
        self.contentScrollArea.setWidget(self.scrollAreaContent)
        self.mainContentLayout.addWidget(self.contentScrollArea)
        self.gridLayout.addWidget(self.mainContentContainer, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.stackedWidget.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def update_theme_styles(self):
        """Update all UI component styles when theme changes"""
        # Update main window background
        self.centralwidget.setStyleSheet(f"background-color: {ThemeManager.get_color('app_background')};")
        
        # Update sidebar
        self.sidebarContainer.setStyleSheet(f"""
            background-color: {ThemeManager.get_color('sidebar_background')};
            min-height: 50px;
            max-height: 2000px;
        """)
        
        # Update all menu buttons
        for name, button in self.menuButtons.items():
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ThemeManager.get_color('sidebar_background')};
                    border-radius: 25px;
                    font-size: 18px;
                    min-height: 50px;
                    max-height: 100px;
                    min-width: 50px;
                    color: {ThemeManager.get_color('primary_text')};
                }}
                QPushButton:hover {{
                    background-color: {ThemeManager.get_color('button_hover_background')};
                }}
                QPushButton:checked {{
                    font-weight: bold;
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                                                    stop:0.034 {ThemeManager.get_color('accent_primary')}, 
                                                    stop:0.039 {ThemeManager.get_color('sidebar_background')});
                    color: {ThemeManager.get_color('accent_primary')};
                }}
            """)
        
        # Update exit button
        self.exitButton.setStyleSheet(f"""
            QPushButton {{
                background-color: {ThemeManager.get_color('sidebar_background')};
                border-radius: 25px;
                font-size: 18px;
                min-height: 50px;
                max-height: 100px;
                min-width: 50px;
                color: {ThemeManager.get_color('primary_text')};
            }}
            QPushButton:hover {{
                background-color: {ThemeManager.get_color('button_hover_background')};
            }}
        """)
        
        # Update search input
        self.searchInput.setStyleSheet(f"""
            QLineEdit {{
                background-color: {ThemeManager.get_color('input_background')};
                color: {ThemeManager.get_color('primary_text')};
                border-radius: 15px;
            }}
        """)
        
        # Update search button
        self.searchButton.setStyleSheet(f"""
            QPushButton {{
                font-size: 16px;
                border-radius: 15px;
                min-width: 100px;
                min-height: 50px;
                max-width: 200px;
                max-height: 100px;
                background-color: {ThemeManager.get_color('button_background')};
                color: {ThemeManager.get_color('primary_text')};
            }}
        """)
        
        # Update points button
        self.pointsButton.setStyleSheet(f"""
            QPushButton {{
                background-color: {ThemeManager.get_color('app_background')};
                border-radius: 15px;
                min-height: 50px;
                max-height: 100px;
                min-width: 50px;
                color: {ThemeManager.get_color('primary_text')};
            }}
        """)
        
        # Update points label
        self.pointsLabel.setStyleSheet(f"color: {ThemeManager.get_color('primary_text')};")
        
        # Update user button
        self.userButton.setStyleSheet(f"""
            QPushButton {{
                font-size: 16px;
                border-radius: 15px;
                background-color: {ThemeManager.get_color('button_background')};
                color: {ThemeManager.get_color('primary_text')};
            }}
        """)
        
        # Update content scroll area
        self.contentScrollArea.setStyleSheet(f"""
            QScrollArea {{
                background-color: {ThemeManager.get_color('app_background')};
                border: none;
            }}
        """)
        
        # Update scroll area content
        self.scrollAreaContent.setStyleSheet(f"""
            QWidget {{
                background-color: {ThemeManager.get_color('app_background')};
            }}
        """)
        
        # Update stacked widget
        self.stackedWidget.setStyleSheet(f"""
            QStackedWidget {{
                background-color: {ThemeManager.get_color('app_background')};
            }}
        """)
        
        # Update all pages
        for page_name in ['pg_main', 'pg_courses', 'pg_lessons', 'pg_progress', 'pg_settings']:
            if hasattr(self, page_name):
                page = getattr(self, page_name)
                page.setStyleSheet(f"""
                    QWidget {{
                        background-color: {ThemeManager.get_color('app_background')};
                        color: {ThemeManager.get_color('primary_text')};
                    }}
                """)
        
    