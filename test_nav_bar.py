import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QScrollArea, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Navigation Bar")
        self.setGeometry(100, 100, 800, 600)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Create the navigation bar
        nav_bar = QScrollArea()
        nav_bar.setWidgetResizable(True)
        nav_bar.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        nav_bar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        nav_bar.setMaximumHeight(50)
        nav_bar.setStyleSheet("""
            QScrollArea {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 20px;
                margin: 0;
                padding: 0;
            }
        """)
        
        # Container for buttons
        container = QWidget()
        container.setStyleSheet("background-color: white;")
        buttons_layout = QHBoxLayout(container)
        buttons_layout.setSpacing(8)
        buttons_layout.setContentsMargins(8, 4, 8, 4)
        
        # Add course buttons
        course_names = [
            "Working with AI", 
            "Business Analytics", 
            "Google AI Essentials", 
            "IBM Data Analyst", 
            "Business Analytics with Excel: Elementary to Advanced",
            "Cloud Computing"
        ]
        
        for i, name in enumerate(course_names):
            button = self.create_course_button(name, i == 0)  # First button is selected
            buttons_layout.addWidget(button)
        
        # Add stretch at the end
        buttons_layout.addStretch()
        
        # Set the container as the widget for the scroll area
        nav_bar.setWidget(container)
        
        # Add to main layout
        main_layout.addWidget(nav_bar)
        main_layout.addStretch()
        
        # Set the main widget
        self.setCentralWidget(main_widget)
    
    def create_course_button(self, name, is_selected=False):
        """Create a button for the navigation bar"""
        button = QPushButton(name)
        button.setCursor(Qt.PointingHandCursor)
        button.setFont(QFont("Inter", 11))
        button.setCheckable(True)
        button.setChecked(is_selected)
        button.setMinimumWidth(120)
        button.setFixedHeight(32)
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-radius: 16px;
                padding: 4px 16px;
                color: #666666;
                font-weight: normal;
                border: none;
                text-align: center;
            }
            QPushButton:hover:!checked {
                background-color: #F5F5F5;
                color: #333333;
            }
            QPushButton:checked {
                background-color: #E6F2FF;
                color: #2196F3;
                font-weight: bold;
            }
        """)
        
        return button

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_()) 