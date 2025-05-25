from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from ui import Ui_MainWindow
from src.services import SessionManager

class UiWrapper(QMainWindow):
    def __init__(self):
        super().__init__()

        
        self.setMinimumSize(1700, 865)  
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        # Update user button to display current username
        self.update_user_display()
    
    def update_user_display(self):
        current_user = SessionManager.get_current_user()
        if current_user and isinstance(current_user, dict): # Check if dict
            username = current_user.get('username', "User") # Get from dict
            self.ui.btn_user.setText(username)
        else:
            # Handle cases where current_user is None or not a dict (e.g. if it was an object before)
            self.ui.btn_user.setText("User") # Default text

    def refresh_main_page_data(self):
        if hasattr(self.ui, 'pg_main') and self.ui.pg_main is not None:
            self.ui.pg_main.load_user_specific_data()
            self.ui.pg_main.load_recommended_courses_data()
        else:
            print("[WARN] UiWrapper: pg_main not found or not initialized in ui object.")

    def closeEvent(self, event):
        # Handle the close event
        print("UiWrapper: Closing the window")
        event.accept()
