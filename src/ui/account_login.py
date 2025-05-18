from PyQt5 import QtWidgets, QtCore
import sys
import os

# Add parent directory to path to import services
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.services.auth_service import AuthService
from src.core import app_state
from src.core.error_handling import LoginError


class LoginPage(QtWidgets.QWidget):
    login_successful = QtCore.pyqtSignal()  
    goto_register = QtCore.pyqtSignal()     

    def __init__(self):
        super().__init__()
        
        # Initialize auth service
        self.auth_service = AuthService()

        self.setObjectName("pg_login")
        self.setMinimumSize(800, 600)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.widget = QtWidgets.QWidget()
        self.widget.setMinimumSize(QtCore.QSize(1600, 865))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.widget.setProperty("type", "continue_viewing")
        
        self.label_title = QtWidgets.QLabel("Вхід до системи")
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setProperty("type", "title")

        self.input_login = QtWidgets.QLineEdit()
        self.input_login.setPlaceholderText("Логін або Email")
        self.input_login.setProperty("type", "settings")
        self.input_login.setMinimumSize(QtCore.QSize(200, 50))
        self.input_login.setMaximumSize(QtCore.QSize(400, 50))

        self.input_password = QtWidgets.QLineEdit()
        self.input_password.setPlaceholderText("Пароль")
        self.input_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_password.setProperty("type", "settings")
        self.input_password.setFixedSize(QtCore.QSize(200, 50))
        self.input_password.setMaximumSize(QtCore.QSize(400, 50))
        
        # Remember me checkbox
        self.remember_checkbox = QtWidgets.QCheckBox("Запам'ятати мене")
        self.remember_checkbox.setChecked(False)
        
        # Style the checkbox
        self.remember_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #516ed9;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid #dde2f6;
            }
            QCheckBox::indicator:checked {
                background-color: #516ed9;
                border: 1px solid #516ed9;
            }
        """)

        self.btn_login = QtWidgets.QPushButton("Увійти")
        self.btn_login.clicked.connect(self.check_credentials)
        self.btn_login.setProperty("type", "start_continue")
        self.btn_login.setMinimumSize(QtCore.QSize(200, 50))
        self.btn_login.setMaximumSize(QtCore.QSize(400, 2000))
        
        # Force rounded corners on the login button
        self.btn_login.setStyleSheet("""
            QPushButton {
                border-radius: 25px;
                background-color: #516ed9;
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #8fb4ff;
            }
        """)

        self.btn_register = QtWidgets.QPushButton("Зареєструватися")
        self.btn_register.setProperty("type", "register")
        self.btn_register.clicked.connect(self.goto_register.emit)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setSpacing(20)
        layout.addWidget(self.label_title)
        layout.addWidget(self.input_login)
        layout.addWidget(self.input_password)
        layout.addWidget(self.remember_checkbox)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_register)
        

    def check_credentials(self):
        login = self.input_login.text()
        password = self.input_password.text()
        remember_me = self.remember_checkbox.isChecked()
        
        try:
            # Attempt login with AuthService
            success, session_token, user_data = self.auth_service.login(login, password)
            
            if success and user_data:
                # Store the user data in app_state
                app_state.set_current_user(user_data)
                
                # Print debug info
                print("\n----- LOGIN SUCCESSFUL -----")
                print(f"User data type: {type(user_data)}")
                if isinstance(user_data, dict):
                    print("User data contents:")
                    for key, value in user_data.items():
                        print(f"  {key}: {value} (type: {type(value)})")
                else:
                    print(f"WARNING: User data is not a dictionary: {user_data}")
                print("---------------------------\n")
                
                # Save login info if Remember Me is checked
                if remember_me:
                    self.save_login_info(login)
                
                # Emit signal to change to main interface
                self.login_successful.emit()
            else:
                QtWidgets.QMessageBox.warning(self, "Помилка", "Невірний логін або пароль")
                
        except LoginError as e:
            QtWidgets.QMessageBox.warning(self, "Помилка входу", str(e))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Помилка системи", f"Не вдалося виконати вхід: {str(e)}")
    
    def save_login_info(self, login):
        """Save the login information locally"""
        try:
            # Here you would implement persistence of the login info
            # For example, using QSettings:
            settings = QtCore.QSettings("Mathtermind", "Auth")
            settings.setValue("saved_login", login)
            settings.setValue("remember_me", True)
            
            # Save password for auto-login (in a real app, this should be securely encrypted)
            if self.remember_checkbox.isChecked():
                settings.setValue("saved_password", self.input_password.text())
        except Exception as e:
            print(f"Error saving login info: {str(e)}")
    
    def load_saved_login(self):
        """Load saved login if available and auto-login if Remember Me is checked"""
        try:
            settings = QtCore.QSettings("Mathtermind", "Auth")
            if settings.value("remember_me", False, type=bool):
                saved_login = settings.value("saved_login", "")
                self.input_login.setText(saved_login)
                self.remember_checkbox.setChecked(True)
                
                # Get saved password if available (in a real app, this should be securely encrypted)
                saved_password = settings.value("saved_password", "")
                if saved_password:
                    self.input_password.setText(saved_password)
                    # Auto-login with a short delay to allow the UI to update
                    QtCore.QTimer.singleShot(500, self.auto_login)
        except Exception as e:
            print(f"Error loading saved login: {str(e)}")
    
    def auto_login(self):
        """Automatically log in using saved credentials"""
        # Only auto-login if username and password fields are filled
        if self.input_login.text() and self.input_password.text():
            self.check_credentials()

    def logout(self):
        """Logout the current user"""
        # Clear the current user from app state
        app_state.clear_current_user()
        
        # Clear the auto-login settings when explicitly logging out
        # This prevents auto-login after a manual logout
        try:
            settings = QtCore.QSettings("Mathtermind", "Auth")
            settings.setValue("saved_password", "")  # Remove the password but keep the username
            # We keep the remember_me flag and username for convenience
        except Exception as e:
            print(f"Error clearing auto-login settings: {str(e)}")
        
        # Clear the password field in the UI
        self.input_password.clear()
        
    def action1_triggered(self):
        """Handler for 'Change user' action"""
        # Clear both username and password for "Change user" action
        try:
            settings = QtCore.QSettings("Mathtermind", "Auth")
            settings.setValue("saved_password", "")  # Remove the password
            settings.setValue("saved_login", "")  # Also remove the username
            settings.setValue("remember_me", False)  # Disable remember me
        except Exception as e:
            print(f"Error clearing saved credentials: {str(e)}")
            
        # Clear both fields in the UI
        self.input_login.clear()
        self.input_password.clear()
        self.remember_checkbox.setChecked(False)
        
        # Complete the logout process
        self.logout()

    def showEvent(self, event):
        """Override showEvent to load saved login when the page is shown"""
        super().showEvent(event)
        self.load_saved_login()
