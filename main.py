import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from src.ui.sidebar import Sidebar
from src.ui.content_area import ContentArea
from config import (WINDOW_WIDTH, WINDOW_HEIGHT, SIDEBAR_WIDTH,
                    SIDEBAR_RATIO, CONTENT_RATIO, STYLESHEET_PATH)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mathtermind")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Initialize content area and sidebar
        self.content_area = ContentArea()
        self.sidebar = Sidebar(self.change_page)

        # Setup central widget and layout
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Add sidebar and content area to the layout
        layout.addWidget(self.sidebar, SIDEBAR_RATIO)
        layout.addWidget(self.content_area, CONTENT_RATIO)

        # Apply layout and sidebar width
        self.setCentralWidget(central_widget)
        self.sidebar.setFixedWidth(SIDEBAR_WIDTH)

        # Load stylesheet
        try:
            with open(STYLESHEET_PATH, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Warning: {STYLESHEET_PATH} file not found.")

    def change_page(self, page_name):
        """Handle page navigation."""
        self.content_area.update_content(page_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())