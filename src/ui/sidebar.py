from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from functools import partial

# Constants for styling and layout
LOGO_ICON_PATH = "src/ui/assets/icons/white_logo.svg"
PROFILE_ICON_PATH = "src/ui/assets/icons/profile.svg"
SIDEBAR_ICON_SIZE = QSize(24, 24)
LOGO_SIZE = QSize(64, 64)
LOGO_ICON_SIZE = QSize(96, 96)
BUTTON_SIZE = QSize(64, 64)
BUTTON_SPACING = 0
BUTTON_TOP_MARGIN = 80
BUTTON_BOTTOM_MARGIN = 80

NAVIGATION_ITEMS = {
    "Dashboard": "src/ui/assets/icons/dashboard.svg",
    "Courses": "src/ui/assets/icons/courses.svg",
    "Quiz": "src/ui/assets/icons/quiz.svg"
}

class Sidebar(QWidget):
    def __init__(self, on_navigation_clicked):
        super().__init__()
        self.on_navigation_clicked = on_navigation_clicked
        self._setup_ui()

    def _setup_ui(self):
        """Setup the sidebar layout."""
        self.setLayout(self._create_main_layout())

    def _create_main_layout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addLayout(self._create_logo_layout())
        layout.addWidget(self._create_separator())
        layout.addLayout(self._create_navigation_layout())
        layout.addStretch()
        layout.addLayout(self._create_profile_layout())
        return layout

    def _create_logo_layout(self):
        app_logo = QPushButton()
        app_logo.setIcon(QIcon(LOGO_ICON_PATH))
        app_logo.setIconSize(LOGO_ICON_SIZE)
        app_logo.setFixedSize(LOGO_SIZE)

        logo_layout = QHBoxLayout()
        logo_layout.addStretch()
        logo_layout.addWidget(app_logo)
        logo_layout.addStretch()
        return logo_layout
    
    def _create_profile_layout(self):
        profile_btn = QPushButton()
        profile_btn.setIcon(QIcon(PROFILE_ICON_PATH))
        profile_btn.setIconSize(SIDEBAR_ICON_SIZE)
        profile_btn.setFixedSize(BUTTON_SIZE)

        profile_layout = QVBoxLayout()
        profile_layout.addStretch()
        profile_layout.addWidget(profile_btn)
        return profile_layout

    def _create_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        return separator

    def _create_navigation_layout(self):
        nav_layout = QVBoxLayout()
        nav_layout.setAlignment(Qt.AlignCenter)
        nav_layout.setSpacing(BUTTON_SPACING)
        nav_layout.setContentsMargins(0, BUTTON_TOP_MARGIN, 0, BUTTON_BOTTOM_MARGIN)

        self.nav_buttons = {}
        for name, icon_path in NAVIGATION_ITEMS.items():
            nav_button = QPushButton()
            nav_button.setIcon(QIcon(icon_path))
            nav_button.setIconSize(SIDEBAR_ICON_SIZE)
            nav_button.setFixedSize(BUTTON_SIZE)
            nav_button.clicked.connect(partial(self.on_navigation_clicked, name))
            self.nav_buttons[name] = nav_button
            nav_layout.addWidget(nav_button)

        return nav_layout
