from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel
from functools import partial

# Constants for styling and layout
LOGO_ICON_PATH = "src/ui/assets/icons/logo.svg"
PROFILE_ICON_PATH = "src/ui/assets/icons/profile.svg"
SIDEBAR_ICON_SIZE = QSize(24, 24)  # Slightly smaller icons to fit with text
LOGO_SIZE = QSize(64, 64)
LOGO_ICON_SIZE = QSize(32, 32)
BUTTON_SIZE = QSize(140, 40)  # Reduced width from 160 to 140
BUTTON_SPACING = 15
BUTTON_TOP_MARGIN = 20
BUTTON_BOTTOM_MARGIN = 20

ICON_PATHS = {
    "Головна": "src/ui/assets/icons/dashboard.svg",
    "Курси": "src/ui/assets/icons/courses.svg",
    "Уроки": "src/ui/assets/icons/quiz.svg",
    "Успішність": "src/ui/assets/icons/dashboard.svg",
    "Налаштування": "src/ui/assets/icons/dashboard.svg"
}

class Sidebar(QWidget):
    def __init__(self, on_button_clicked):
        super().__init__()
        self.on_button_clicked = on_button_clicked
        self.setObjectName("sidebar")
        self._setup_ui()
        # Set maximum width for the sidebar
        self.setMaximumWidth(200)  # Reduced from default

    def _setup_ui(self):
        """Setup the sidebar layout."""
        self.setLayout(self._create_main_layout())
        
        # Apply styling to make the sidebar have a white background
        self.setStyleSheet("""
            QWidget#sidebar {
                background-color: #FFFFFF !important;
                border: none;
            }
        """)

    def _create_main_layout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)
        layout.addLayout(self._create_logo_layout())
        layout.addSpacing(10)
        layout.addLayout(self._create_button_layout())
        layout.addStretch()
        layout.addWidget(self._create_separator())
        layout.addLayout(self._create_profile_btn_layout())
        return layout

    def _create_logo_layout(self):
        logo_layout = QHBoxLayout()
        logo_layout.setContentsMargins(0, 0, 0, 10)
        
        # Create logo container
        logo_container = QWidget()
        logo_container_layout = QHBoxLayout(logo_container)
        logo_container_layout.setContentsMargins(5, 5, 5, 5)
        
        # Create logo with app name
        app_logo = QPushButton()
        app_logo.setObjectName("logo")
        app_logo.setIcon(QIcon(LOGO_ICON_PATH))
        app_logo.setIconSize(LOGO_ICON_SIZE)
        app_logo.setStyleSheet("""
            QPushButton#logo {
                background-color: transparent;
                border: none;
                text-align: left;
                padding: 5px;
            }
        """)
        
        # Create app name label
        app_name = QLabel("MathTermind")
        app_name.setObjectName("appName")
        app_name.setStyleSheet("""
            QLabel#appName {
                font-weight: bold;
                font-size: 16px;
                color: #0F1D35;
            }
        """)
        
        logo_container_layout.addWidget(app_logo)
        logo_container_layout.addWidget(app_name)
        logo_container_layout.addStretch()
        
        logo_layout.addWidget(logo_container)
        
        return logo_layout
    
    def _create_profile_btn_layout(self):
        profile_layout = QHBoxLayout()
        profile_layout.setContentsMargins(5, 5, 5, 5)
        
        profile_btn = QPushButton("Профіль")  # Ukrainian translation
        profile_btn.setObjectName("profileButton")
        profile_btn.setIcon(QIcon(PROFILE_ICON_PATH))
        profile_btn.setIconSize(SIDEBAR_ICON_SIZE)
        profile_btn.setCheckable(True)  # Make the button checkable like other buttons
        profile_btn.setStyleSheet("""
            QPushButton#profileButton {
                background-color: transparent;
                border: none;
                text-align: left;
                padding: 8px 12px;
                border-radius: 10px;
            }
            QPushButton#profileButton:hover {
                background-color: #DDE2F6;
            }
            QPushButton#profileButton:checked {
                background-color: #DDE2F6;
                color: #566CD2;
                font-weight: 500;
            }
        """)
        
        profile_layout.addWidget(profile_btn)
        profile_layout.addStretch()
        
        return profile_layout

    def _create_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("""
            QFrame {
                background-color: rgba(133, 138, 148, 0.2);
                max-height: 1px;
                margin: 5px 0px;
            }
        """)
        return separator

    def _create_button_layout(self):
        button_layout = QVBoxLayout()
        button_layout.setSpacing(BUTTON_SPACING)
        button_layout.setContentsMargins(5, BUTTON_TOP_MARGIN, 5, BUTTON_BOTTOM_MARGIN)

        self.buttons = {}
        for name, icon_path in ICON_PATHS.items():
            # Create button with text
            button = QPushButton(name)
            button.setIcon(QIcon(icon_path))
            button.setIconSize(SIDEBAR_ICON_SIZE)
            button.setCheckable(True)
            button.clicked.connect(partial(self.on_button_clicked, name))
            
            # Set button style
            button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    text-align: left;
                    padding: 8px 12px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #DDE2F6;
                }
                QPushButton:checked {
                    background-color: #DDE2F6;
                    color: #566CD2;
                    font-weight: 500;
                }
            """)
            
            # Add button to layout
            button_layout.addWidget(button)
            
            self.buttons[name] = button

        # Set the Courses button as checked by default
        if "Курси" in self.buttons:
            self.buttons["Курси"].setChecked(True)

        return button_layout
