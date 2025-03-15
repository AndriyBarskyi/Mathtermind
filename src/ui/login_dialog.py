from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QFormLayout, QMessageBox, QCheckBox, QComboBox,
    QStackedWidget, QWidget
)
from src.services.user_service import UserService
from src.services.credentials_manager import CredentialsManager


class LoginDialog(QDialog):
    """Dialog for user authentication and registration."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user = None
        self.setWindowTitle("Вхід до Mathtermind")
        self.setMinimumSize(400, 300)
        self.setup_ui()
        self.load_saved_credentials()
        
    def setup_ui(self):
        """Set up the user interface."""
        main_layout = QVBoxLayout(self)
        
        # Logo or welcome message
        welcome_label = QLabel("Ласкаво просимо до Mathtermind!")
        welcome_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        welcome_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(welcome_label)
        
        # Create stacked widget for login and registration forms
        self.stacked_widget = QStackedWidget()
        
        # Create login page
        login_page = QWidget()
        login_layout = QVBoxLayout(login_page)
        
        # Description for login
        login_description = QLabel("Увійдіть, щоб продовжити навчання")
        login_description.setAlignment(QtCore.Qt.AlignCenter)
        login_layout.addWidget(login_description)
        
        # Form layout for login inputs
        login_form = QFormLayout()
        
        # Email field
        self.login_email = QLineEdit()
        self.login_email.setPlaceholderText("Введіть email")
        login_form.addRow("Email:", self.login_email)
        
        # Password field
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Введіть пароль")
        self.login_password.setEchoMode(QLineEdit.Password)
        login_form.addRow("Пароль:", self.login_password)
        
        # Remember me checkbox
        self.remember_checkbox = QCheckBox("Запам'ятати мене")
        login_form.addRow("", self.remember_checkbox)
        
        login_layout.addLayout(login_form)
        
        # Login buttons layout
        login_buttons = QHBoxLayout()
        
        # Login button
        self.login_button = QPushButton("Увійти")
        self.login_button.setDefault(True)
        self.login_button.clicked.connect(self.authenticate)
        
        # Register link
        self.register_link = QPushButton("Зареєструватися")
        self.register_link.setFlat(True)
        self.register_link.setCursor(QtCore.Qt.PointingHandCursor)
        self.register_link.clicked.connect(self.show_register_page)
        
        # Cancel button
        self.login_cancel = QPushButton("Скасувати")
        self.login_cancel.clicked.connect(self.reject)
        
        login_buttons.addWidget(self.register_link)
        login_buttons.addStretch()
        login_buttons.addWidget(self.login_cancel)
        login_buttons.addWidget(self.login_button)
        
        login_layout.addLayout(login_buttons)
        
        # Create registration page
        register_page = QWidget()
        register_layout = QVBoxLayout(register_page)
        
        # Description for registration
        register_description = QLabel("Створіть новий обліковий запис")
        register_description.setAlignment(QtCore.Qt.AlignCenter)
        register_layout.addWidget(register_description)
        
        # Form layout for registration inputs
        register_form = QFormLayout()
        
        # Username field
        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText("Введіть ім'я користувача")
        register_form.addRow("Ім'я користувача:", self.register_username)
        
        # Email field
        self.register_email = QLineEdit()
        self.register_email.setPlaceholderText("Введіть email")
        register_form.addRow("Email:", self.register_email)
        
        # Password field
        self.register_password = QLineEdit()
        self.register_password.setPlaceholderText("Введіть пароль")
        self.register_password.setEchoMode(QLineEdit.Password)
        register_form.addRow("Пароль:", self.register_password)
        
        # Confirm password field
        self.register_confirm_password = QLineEdit()
        self.register_confirm_password.setPlaceholderText("Підтвердіть пароль")
        self.register_confirm_password.setEchoMode(QLineEdit.Password)
        register_form.addRow("Підтвердження:", self.register_confirm_password)
        
        # Age group field
        self.register_age_group = QComboBox()
        self.register_age_group.addItems(["10-12", "13-14", "15-17"])
        register_form.addRow("Вікова група:", self.register_age_group)
        
        register_layout.addLayout(register_form)
        
        # Registration buttons layout
        register_buttons = QHBoxLayout()
        
        # Back to login link
        self.login_link = QPushButton("Вже маєте обліковий запис? Увійти")
        self.login_link.setFlat(True)
        self.login_link.setCursor(QtCore.Qt.PointingHandCursor)
        self.login_link.clicked.connect(self.show_login_page)
        
        # Register button
        self.register_button = QPushButton("Зареєструватися")
        self.register_button.setDefault(True)
        self.register_button.clicked.connect(self.register_user)
        
        # Cancel button
        self.register_cancel = QPushButton("Скасувати")
        self.register_cancel.clicked.connect(self.reject)
        
        register_buttons.addWidget(self.login_link)
        register_buttons.addStretch()
        register_buttons.addWidget(self.register_cancel)
        register_buttons.addWidget(self.register_button)
        
        register_layout.addLayout(register_buttons)
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(login_page)
        self.stacked_widget.addWidget(register_page)
        
        # Add stacked widget to main layout
        main_layout.addWidget(self.stacked_widget)
        
        # Set initial focus
        self.login_email.setFocus()
    
    def load_saved_credentials(self):
        """Load saved credentials if they exist."""
        credentials = CredentialsManager.load_credentials()
        if credentials:
            self.login_email.setText(credentials.get("email", ""))
            self.login_password.setText(credentials.get("password", ""))
            self.remember_checkbox.setChecked(True)
    
    def auto_login(self):
        """This functionality has been moved to the main application."""
        pass
    
    def show_login_page(self):
        """Switch to the login page."""
        self.stacked_widget.setCurrentIndex(0)
        self.login_email.setFocus()
    
    def show_register_page(self):
        """Switch to the registration page."""
        self.stacked_widget.setCurrentIndex(1)
        self.register_username.setFocus()
    
    def authenticate(self):
        """Authenticate the user with provided credentials."""
        email = self.login_email.text().strip()
        password = self.login_password.text()
        
        if not email or not password:
            QMessageBox.warning(self, "Помилка", "Будь ласка, введіть email та пароль")
            return
        
        # Try to authenticate
        user = UserService.authenticate_user(email, password)
        
        if user:
            # Save credentials if "Remember me" is checked
            if self.remember_checkbox.isChecked():
                CredentialsManager.save_credentials(email, password)
            else:
                # Clear saved credentials if "Remember me" is unchecked
                CredentialsManager.clear_credentials()
                
            self.user = user
            self.accept()
        else:
            QMessageBox.warning(self, "Помилка", "Невірний email або пароль")
            self.login_password.clear()
            self.login_password.setFocus()
    
    def register_user(self):
        """Register a new user."""
        username = self.register_username.text().strip()
        email = self.register_email.text().strip()
        password = self.register_password.text()
        confirm_password = self.register_confirm_password.text()
        age_group = self.register_age_group.currentText()
        
        # Validate inputs
        if not username or not email or not password or not confirm_password:
            QMessageBox.warning(self, "Помилка", "Будь ласка, заповніть усі поля")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "Помилка", "Паролі не співпадають")
            self.register_confirm_password.clear()
            self.register_confirm_password.setFocus()
            return
        
        # Check if email already exists
        if UserService.get_user_by_email(email):
            QMessageBox.warning(self, "Помилка", f"Користувач з email {email} вже існує")
            return
        
        try:
            # Create new user
            user = UserService.create_new_user(
                username=username,
                email=email,
                password=password,
                age_group=age_group
            )
            
            self.user = user
            
            # Automatically check "Remember me" for new users
            self.remember_checkbox.setChecked(True)
            CredentialsManager.save_credentials(email, password)
            
            QMessageBox.information(self, "Успіх", "Реєстрація успішна!")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Помилка при створенні користувача: {str(e)}")
    
    def get_user(self):
        """Return the authenticated user."""
        return self.user 