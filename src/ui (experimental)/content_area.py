from PyQt6.QtWidgets import QStackedWidget
from .pages.courses_page import CoursePage
from .pages.placeholder_page import PlaceholderPage
from .pages.settings_page import SettingsPage


class ContentArea(QStackedWidget):
    """A dynamic content area for displaying different pages."""

    def __init__(self):
        super().__init__()
        self.setObjectName("contentArea")
        # Set explicit background color
        self.setStyleSheet("""
            QWidget#contentArea {
                background-color: #F7F8FA;
                border: none;
                margin: 10px 10px 10px 0px;
            }
        """)
        self._setup_ui()

    def _setup_ui(self):
        """Initialize all pages"""
        # Create the courses page
        self.courses_page = CoursePage()
        self.addWidget(self.courses_page)
        
        # Create the settings page
        self.settings_page = SettingsPage()
        
        # Create placeholder pages for other sections
        self.home_page = PlaceholderPage("Головна")
        self.lessons_page = PlaceholderPage("Уроки")
        self.progress_page = PlaceholderPage("Успішність")
        self.profile_page = PlaceholderPage("Профіль")
        
        # Add all pages to the stacked widget
        self.addWidget(self.home_page)
        self.addWidget(self.lessons_page)
        self.addWidget(self.progress_page)
        self.addWidget(self.settings_page)
        self.addWidget(self.profile_page)

    def update_content(self, page_name):
        """Change the displayed page based on navigation"""
        if page_name == "Курси":
            self.setCurrentWidget(self.courses_page)
        elif page_name == "Головна":
            self.setCurrentWidget(self.home_page)
        elif page_name == "Уроки":
            self.setCurrentWidget(self.lessons_page)
        elif page_name == "Успішність":
            self.setCurrentWidget(self.progress_page)
        elif page_name == "Налаштування":
            self.setCurrentWidget(self.settings_page)
        elif page_name == "Профіль":
            self.setCurrentWidget(self.profile_page)
