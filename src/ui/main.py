import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from sidebar import Sidebar
from content_area import ContentArea
from database_manager import DatabaseManager

# Constants for layout and styling
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
SIDEBAR_WIDTH = 64
SIDEBAR_RATIO = 1
CONTENT_RATIO = 18
STYLESHEET_PATH = "styles.qss"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mathtermind")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
         # Initialize the database
        self.db_manager = DatabaseManager()
        self.db_manager.setup_database()
        self.db_manager.connect()

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
        
    def closeEvent(self, event):
        """Ensure the database connection is closed properly."""
        self.db_manager.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())