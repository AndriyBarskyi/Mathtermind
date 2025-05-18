from PyQt5 import QtWidgets, QtCore
import sys
import os
import re

# Add parent directory to path to import services
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.services.auth_service import AuthService
from src.core import app_state

class RegisterPage(QtWidgets.QWidget):
    back_to_login = QtCore.pyqtSignal()  
    registration_successful = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        
        # Initialize auth service
        self.auth_service = AuthService()

        self.setObjectName("pg_register")
        self.setMinimumSize(800, 600)
        
        self.label_title = QtWidgets.QLabel("Реєстрація")
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setStyleSheet("font-size: 28px; font-weight: bold;")

        self.input_username = QtWidgets.QLineEdit()
        self.input_username.setPlaceholderText("Ім'я користувача")
        self.input_username.setProperty("type", "settings")
        self.input_username.setMinimumSize(QtCore.QSize(200, 50))
        self.input_username.setMaximumSize(QtCore.QSize(400, 50))

        self.input_email = QtWidgets.QLineEdit()
        self.input_email.setPlaceholderText("Електронна адреса користувача")
        self.input_email.setProperty("type", "settings")
        self.input_email.setMinimumSize(QtCore.QSize(200, 50))
        self.input_email.setMaximumSize(QtCore.QSize(400, 50))


        self.input_password = QtWidgets.QLineEdit()
        self.input_password.setPlaceholderText("Пароль")
        self.input_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_password.setProperty("type", "settings")
        self.input_password.setMinimumSize(QtCore.QSize(200, 50))
        self.input_password.setMaximumSize(QtCore.QSize(400, 50))

        self.input_confirm = QtWidgets.QLineEdit()
        self.input_confirm.setPlaceholderText("Повторіть пароль")
        self.input_confirm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_confirm.setProperty("type", "settings")
        self.input_confirm.setMinimumSize(QtCore.QSize(200, 50))
        self.input_confirm.setMaximumSize(QtCore.QSize(400, 50))

        self.btn_register = QtWidgets.QPushButton("Зареєструватися")
        self.btn_register.setProperty("type", "start_continue")
        self.btn_register.setMinimumSize(QtCore.QSize(200, 50))
        self.btn_register.setMaximumSize(QtCore.QSize(400, 50))
        self.btn_register.clicked.connect(self.register_user)

        self.btn_back = QtWidgets.QPushButton("← Назад до входу")
        self.btn_back.clicked.connect(self.back_to_login.emit)
        self.btn_back.setProperty("type", "register")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setSpacing(15)
        layout.addWidget(self.label_title)
        layout.addWidget(self.input_username)
        layout.addWidget(self.input_email)
        layout.addWidget(self.input_password)
        layout.addWidget(self.input_confirm)
        layout.addWidget(self.btn_register)
        layout.addWidget(self.btn_back)
        
    def register_user(self):
        """Register a new user with the auth service"""
        username = self.input_username.text()
        email = self.input_email.text()
        password = self.input_password.text()
        confirm_password = self.input_confirm.text()
        
        # Validate inputs
        if not username:
            self.show_error("Ім'я користувача не може бути порожнім")
            return
            
        if not email:
            self.show_error("Електронна адреса не може бути порожньою")
            return
            
        if not password:
            self.show_error("Пароль не може бути порожнім")
            return
            
        if password != confirm_password:
            self.show_error("Паролі не співпадають")
            return
            
        # Validate email format using regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            self.show_error("Невірний формат електронної адреси")
            return
        
        try:
            # Call the auth service to register the user
            success, user_id, error_message = self.auth_service.register(
                username=username,
                email=email,
                password=password
            )
            
            if success:
                # Show success message
                QtWidgets.QMessageBox.information(
                    self, 
                    "Реєстрація успішна", 
                    "Ви успішно зареєструвалися. Тепер ви можете увійти у систему."
                )
                
                # Navigate back to login page
                self.clear_fields()
                self.back_to_login.emit()
            else:
                # Show error message
                self.show_error(error_message or "Помилка реєстрації")
                
        except Exception as e:
            self.show_error(f"Не вдалося зареєструвати користувача: {str(e)}")
    
    def show_error(self, message):
        """Show an error message dialog"""
        QtWidgets.QMessageBox.warning(self, "Помилка", message)
        
    def clear_fields(self):
        """Clear all input fields"""
        self.input_username.clear()
        self.input_email.clear()
        self.input_password.clear()
        self.input_confirm.clear()
