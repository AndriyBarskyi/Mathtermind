import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QFrame, QPushButton
from src.ui.sidebar import Sidebar
from src.ui.content_area import ContentArea
from src.db import get_db, init_db
from src.db.seed_courses import seed_courses
from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    SIDEBAR_WIDTH,
    STYLESHEET_PATH,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mathtermind")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Set the main window background color
        self.setStyleSheet("background-color: #F7F8FA;")

        # Initialize content area and sidebar
        self.content_area = ContentArea()
        self.content_area.setObjectName("contentArea")
        self.sidebar = Sidebar(self.change_page)
        
        # Create a frame for the sidebar to ensure it has a white background
        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("sidebarFrame")
        sidebar_frame.setStyleSheet("""
            QFrame#sidebarFrame {
                background-color: #FFFFFF !important;
                border-right: 1px solid #E5E7EB;
                border-top-left-radius: 16px;
                border-bottom-left-radius: 16px;
                margin: 10px 0px 10px 10px;
                padding: 0px;
            }
        """)
        
        # Add sidebar to the frame
        sidebar_layout = QHBoxLayout(sidebar_frame)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.addWidget(self.sidebar)
        
        # Ensure sidebar has proper styling
        self.sidebar.setStyleSheet("""
            QWidget#sidebar {
                background-color: #FFFFFF;
                border: none;
            }
        """)

        # Setup central widget and layout
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        
        # Set explicit background color for central widget
        central_widget.setStyleSheet("QWidget#centralWidget { background-color: #F7F8FA; }")
        
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Add sidebar frame and content area to the layout
        layout.addWidget(sidebar_frame)
        layout.addWidget(self.content_area)

        # Apply layout and sidebar width
        self.setCentralWidget(central_widget)
        sidebar_frame.setFixedWidth(SIDEBAR_WIDTH)

        # Load stylesheet
        try:
            with open(STYLESHEET_PATH, "r") as f:
                stylesheet = f.read()
                self.setStyleSheet(stylesheet)
        except FileNotFoundError:
            print(f"Warning: {STYLESHEET_PATH} file not found.")
            
        # Connect profile button
        self._connect_profile_button()
            
        # Set initial page to Courses
        self.change_page("Курси")
        # Set the Courses button as checked in the sidebar
        if "Курси" in self.sidebar.buttons:
            self.sidebar.buttons["Курси"].setChecked(True)

    def _connect_profile_button(self):
        """Connect the profile button to the change_page method."""
        profile_button = self.sidebar.findChild(QPushButton, "profileButton")
        if profile_button:
            profile_button.clicked.connect(lambda: self.change_page("Профіль"))

    def change_page(self, page_name):
        """Handle page navigation."""
        # Update the content area
        self.content_area.update_content(page_name)
        
        # Update the checked state of buttons
        for button_name, button in self.sidebar.buttons.items():
            button.setChecked(button_name == page_name)
        
        # Handle profile button separately since it's not in the buttons dictionary
        profile_button = self.sidebar.findChild(QPushButton, "profileButton")
        if profile_button:
            profile_button.setChecked(page_name == "Профіль")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Initialize the database
    init_db.init_db()
    
    # Seed the database with sample courses
    seed_courses()
    
    # Start the application
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
