from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QFormLayout, QHBoxLayout,
    QGridLayout, QSizePolicy, QPushButton, QVBoxLayout, QFrame, QScrollArea)
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5 import QtWidgets, QtCore, QtGui

from src.core.app_state import get_current_user

def make_round_pixmap(pixmap, size):
    pixmap = pixmap.scaled(size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
    rounded = QPixmap(size)
    rounded.fill(Qt.transparent)

    painter = QPainter(rounded)
    painter.setRenderHint(QPainter.Antialiasing)
    path = QPainterPath()
    path.addEllipse(0, 0, size.width(), size.height())
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, pixmap)
    painter.end()
    return rounded



class Settings_page(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)
        
        # Get real user data
        self.user_data = get_current_user()
        
        # Debug user data to console
        print("\n----- USER DATA DEBUG -----")
        print(f"Full user_data object: {self.user_data}")
        if self.user_data:
            print(f"User data type: {type(self.user_data)}")
            if isinstance(self.user_data, dict):
                for key, value in self.user_data.items():
                    print(f"Key: '{key}', Value: '{value}', Type: {type(value)}")
            else:
                print(f"User data is not a dictionary: {self.user_data}")
        else:
            print("No user data available")
        print("--------------------------\n")
        
        # Extract initial data
        name = ""
        email = ""
        phone = ""
        birthday = ""
        
        if self.user_data and isinstance(self.user_data, dict):
            email = self.user_data.get("email", "")
            username = self.user_data.get("username", "")
            name = username  # Default to username
            
            # Try to build full name
            if "first_name" in self.user_data or "last_name" in self.user_data:
                first_name = self.user_data.get("first_name", "")
                last_name = self.user_data.get("last_name", "")
                if first_name and last_name:
                    name = f"{first_name} {last_name}"
                elif first_name:
                    name = first_name
                elif last_name:
                    name = last_name
                    
            print(f"Extracted data: name={name}, email={email}")

        # Continue with UI setup
        self.pg_settings = QWidget(self)
        self.pg_settings.setObjectName("pg_settings")
        self.main_layout.addWidget(self.pg_settings)
        self.layout_settings_main = QGridLayout(self.pg_settings)
        self.layout_settings_main.setContentsMargins(10, 10, 10, 10)
        
        # Create scroll area
        self.scroll_area = QScrollArea(self.pg_settings)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setObjectName("settings_scroll_area")
        
        # Create the content widget that will go inside the scroll area
        self.widget_settings_content = QWidget()
        self.apply_size_policy(self.widget_settings_content, min_width=580)
        self.widget_settings_content.setProperty("type", "w_pg")

        self.layout_settings_form = QFormLayout(self.widget_settings_content)
        self.layout_settings_form.setLabelAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.layout_settings_form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.layout_settings_form.setContentsMargins(20, 20, 20, 20)
        self.layout_settings_form.setHorizontalSpacing(12)
        self.layout_settings_form.setVerticalSpacing(12)

        # Add page title - left aligned
        title_label = QLabel("Налаштування профілю", self.widget_settings_content)
        title_label.setProperty("type", "title")
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setContentsMargins(0, 10, 0, 20)
        self.layout_settings_form.addRow(title_label)
        
        # Add instructions
        instructions_label = QLabel("Тут ви можете змінити свої особисті дані", self.widget_settings_content)
        instructions_label.setProperty("type", "lb_description")
        instructions_label.setAlignment(Qt.AlignLeft)
        instructions_label.setContentsMargins(0, 0, 0, 20)
        self.layout_settings_form.addRow(instructions_label)

        self.add_user_greeting()
        
        # Add a separator
        separator = QFrame(self.widget_settings_content)
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #dde2f6;")
        separator.setFixedHeight(2)
        self.layout_settings_form.addRow(separator)
        
        # Add section label
        personal_info_label = QLabel("Особиста інформація", self.widget_settings_content)
        personal_info_label.setProperty("type", "page_section")
        personal_info_label.setContentsMargins(0, 10, 0, 10)
        self.layout_settings_form.addRow(personal_info_label)
        
        # Create form fields but store them as instance variables so we can update them
        self.name_field = self.add_form_field_with_placeholder("Повне ім'я", name, "Введіть ваше повне ім'я", "le_name")
        self.email_field = self.add_form_field_with_placeholder("Електронна адреса", email, "Введіть вашу електронну адресу", "le_email")
        self.phone_field = self.add_form_field_with_placeholder("Телефон", phone, "Введіть ваш номер телефону", "le_phone")
        self.birthday_field = self.add_form_field_with_placeholder("Дата народження", birthday, "дд.мм.рррр", "le_birthday")
        
        # Add another separator
        separator2 = QFrame(self.widget_settings_content)
        separator2.setFrameShape(QFrame.HLine)
        separator2.setFrameShadow(QFrame.Sunken)
        separator2.setStyleSheet("background-color: #dde2f6;")
        separator2.setFixedHeight(2)
        self.layout_settings_form.addRow(separator2)
        
        # Add section label
        security_label = QLabel("Безпека", self.widget_settings_content)
        security_label.setProperty("type", "page_section")
        security_label.setContentsMargins(0, 10, 0, 10)
        self.layout_settings_form.addRow(security_label)
        
        self.password_field = self.add_password_field("Пароль", "", "le_password")
        
        # Add status message label (hidden by default)
        self.status_label = QLabel("", self.widget_settings_content)
        self.status_label.setProperty("type", "lb_description")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setContentsMargins(0, 10, 0, 10)
        self.status_label.setStyleSheet("color: #516ed9; font-weight: bold;")
        self.status_label.setVisible(False)
        self.layout_settings_form.addRow(self.status_label)

        # Buttons in a separate widget for layout
        buttons_widget = QWidget(self.widget_settings_content)
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 10, 0, 10)
        
        # Add space to center the save button
        buttons_layout.addStretch()
        
        # Save button
        self.btn_save = QPushButton("Зберегти", buttons_widget)
        self.btn_save.setObjectName("btn_save")
        self.btn_save.setMinimumSize(QtCore.QSize(160, 36))
        self.btn_save.setMaximumSize(QtCore.QSize(160, 36))
        self.btn_save.setProperty("type","start_continue")
        # Force rounded corners on the button
        self.btn_save.setStyleSheet("""
            QPushButton {
                border-radius: 18px;
                background-color: #516ed9;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8fb4ff;
            }
        """)
        self.btn_save.clicked.connect(self.save_settings)
        buttons_layout.addWidget(self.btn_save)
        
        # Add space to center the save button
        buttons_layout.addStretch()
        
        self.layout_settings_form.addRow(buttons_widget)
        
        # Set the content widget as the scroll area's widget
        self.scroll_area.setWidget(self.widget_settings_content)
        
        # Add the scroll area to the main layout
        self.layout_settings_main.addWidget(self.scroll_area)
        
        # Try to retrieve real user data
        self.refresh_user_data()

    def apply_size_policy(self, widget, min_width=0, max_width=16777215, min_height=0, max_height=16777215):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(size_policy)
        widget.setMinimumSize(min_width, min_height)
        widget.setMaximumSize(max_width, max_height)

    def add_user_greeting(self):
        widget_user_greeting = QWidget(self.widget_settings_content)
        widget_user_greeting.setProperty("type", "w_pg")
        self.apply_size_policy(widget_user_greeting, min_width=500, max_width=500, min_height=60, max_height=60)

        layout_user_greeting = QHBoxLayout(widget_user_greeting)
        layout_user_greeting.setContentsMargins(0, 10, 0, 0)

        lb_image = QLabel(widget_user_greeting)
        lb_image.setMinimumSize(40, 40)
        lb_image.setMaximumSize(40, 40)
        lb_image.setScaledContents(True)
        original_pixmap = QPixmap("icon/icon_users.PNG") 
        round_pixmap = make_round_pixmap(original_pixmap, QSize(40, 40))
        lb_image.setPixmap(round_pixmap)
        lb_image.setAlignment(Qt.AlignCenter)
        layout_user_greeting.addWidget(lb_image)

        lb_welcome = QLabel("Вітаємо,", widget_user_greeting)
        lb_welcome.setProperty("type", "page_section")
        lb_welcome.setMinimumSize(80, 40)
        lb_welcome.setMaximumSize(80, 40)
        layout_user_greeting.addWidget(lb_welcome)
        
        # Default username
        display_name = "користувач"
        
        # Try to get a better name if possible
        if self.user_data and isinstance(self.user_data, dict):
            # Try username first
            username = self.user_data.get("username", "")
            if username:
                display_name = username
                
            # Try first name if available (preferred)
            first_name = self.user_data.get("first_name", "")
            if first_name:
                display_name = first_name
                
            print(f"User greeting will display: {display_name}")
        
        # Store the label so we can update it
        self.username_label = QLabel(display_name, widget_user_greeting)
        self.username_label.setProperty("type", "page_section")
        layout_user_greeting.addWidget(self.username_label)
        
        # Add stretch at the end to keep everything left-aligned
        layout_user_greeting.addStretch()

        self.layout_settings_form.addRow(widget_user_greeting)

    def add_form_field_with_placeholder(self, label_text, text_value, placeholder_text, obj_name):
        label = QLabel(label_text, self.widget_settings_content)
        label.setProperty("type", "page_section")
        label.setFixedHeight(20)
        self.layout_settings_form.addRow(label)

        input_field = QLineEdit(self.widget_settings_content)
        
        # Set text if available, otherwise use placeholder
        if text_value:
            input_field.setText(text_value)
        else:
            input_field.setPlaceholderText(placeholder_text)
            
        input_field.setFixedHeight(28)
        input_field.setObjectName(obj_name)
        input_field.setProperty("type", "settings")
        
        # Improve field styling
        input_field.setStyleSheet("""
            QLineEdit[type="settings"] {
                font: \"MS Shell Dlg 2\";
                font-size: 12px;
                border-radius: 4px;
                padding: 1px 6px;
                background-color: #f7f7f7;
                border: 1px solid #dde2f6;
            }
            
            QLineEdit[type="settings"]:focus {
                border: 1px solid #516ed9;
                background-color: white;
            }
        """)
        
        self.layout_settings_form.addRow(input_field)
        return input_field

    def add_password_field(self, label_text, placeholder_text, obj_name):
        label = QLabel(label_text, self.widget_settings_content)
        label.setProperty("type", "page_section")
        label.setFixedHeight(20)
        self.layout_settings_form.addRow(label)

        input_field = QLineEdit(self.widget_settings_content)
        input_field.setPlaceholderText("Введіть пароль")  # Clear text, use placeholder
        input_field.setEchoMode(QLineEdit.Password)  
        input_field.setFixedHeight(28)
        input_field.setObjectName(obj_name)
        input_field.setProperty("type", "settings")
        
        # Improve field styling
        input_field.setStyleSheet("""
            QLineEdit[type="settings"] {
                font: \"MS Shell Dlg 2\";
                font-size: 12px;
                border-radius: 4px;
                padding: 1px 6px;
                background-color: #f7f7f7;
                border: 1px solid #dde2f6;
            }
            
            QLineEdit[type="settings"]:focus {
                border: 1px solid #516ed9;
                background-color: white;
            }
        """)
        
        self.layout_settings_form.addRow(input_field)
        return input_field
    
    def refresh_user_data(self):
        """Force refresh of user data fields"""
        # Re-fetch user data from app state
        fresh_user_data = get_current_user()
        self.user_data = fresh_user_data
        
        print("\n----- REFRESHING USER DATA -----")
        print(f"Fresh user data: {self.user_data}")
        
        if fresh_user_data and isinstance(fresh_user_data, dict):
            # Extract and update email
            if "email" in fresh_user_data and fresh_user_data["email"]:
                email = fresh_user_data["email"]
                self.email_field.setText(email)
                self.email_field.setPlaceholderText("")
            else:
                self.email_field.setText("")
                self.email_field.setPlaceholderText("Електронна адреса не вказана")
            
            # Extract name components
            name = ""
            first_name = fresh_user_data.get("first_name", "")
            last_name = fresh_user_data.get("last_name", "")
            username = fresh_user_data.get("username", "")
            
            # Set display name (prefer first name, then username)
            display_name = first_name if first_name else (username if username else "користувач")
            
            # Build full name
            if first_name and last_name:
                name = f"{first_name} {last_name}"
            elif first_name:
                name = first_name
            elif last_name:
                name = last_name
            elif username:
                name = username
                
            # Update name field
            if name:
                self.name_field.setText(name)
                self.name_field.setPlaceholderText("")
            else:
                self.name_field.setText("")
                self.name_field.setPlaceholderText("Ім'я не вказано")
            
            # Update username label
            if hasattr(self, 'username_label') and display_name != "користувач":
                self.username_label.setText(display_name)
                
            # Clear placeholders for empty fields
            self.phone_field.setPlaceholderText("Введіть номер телефону")
            self.birthday_field.setPlaceholderText("дд.мм.рррр")
                
            # Add debug information
            print(f"Updated fields - name: '{name}', email: '{fresh_user_data.get('email', '')}', display_name: '{display_name}'")
            print(f"Name field text: '{self.name_field.text()}'")
            print(f"Email field text: '{self.email_field.text()}'")
        else:
            print("WARNING: No user data available for refresh")
            # Set appropriate placeholders
            self.name_field.setText("")
            self.name_field.setPlaceholderText("Ім'я не вказано")
            self.email_field.setText("")
            self.email_field.setPlaceholderText("Електронна адреса не вказана")
            self.phone_field.setText("")
            self.phone_field.setPlaceholderText("Введіть номер телефону")
            self.birthday_field.setText("")
            self.birthday_field.setPlaceholderText("дд.мм.рррр")
            if hasattr(self, 'username_label'):
                self.username_label.setText("користувач")
                
        print("--------------------------\n")
        
        # No status message for initial load
        if hasattr(self, 'status_label'):
            self.status_label.setVisible(False)

    def save_settings(self):
        # Get values from form fields
        name = self.name_field.text()
        email = self.email_field.text()
        phone = self.phone_field.text()
        birthday = self.birthday_field.text()
        password = self.password_field.text()
        
        # Update user data
        if self.user_data and isinstance(self.user_data, dict) and "id" in self.user_data:
            try:
                # Update user's profile with new information
                # This would typically call a service to update the user's data
                
                # Show success message with animation
                self.status_label.setText("Налаштування успішно збережено!")
                self.status_label.setStyleSheet("color: #32CD32; font-weight: bold;")
                self.status_label.setVisible(True)
                
                # Clear password field
                self.password_field.clear()
                
                # Hide the status message after 3 seconds
                QtCore.QTimer.singleShot(3000, lambda: self.status_label.setVisible(False))
            except Exception as e:
                # Show error message
                self.status_label.setText(f"Помилка: {str(e)}")
                self.status_label.setStyleSheet("color: #FF0000; font-weight: bold;")
                self.status_label.setVisible(True)
                
                # Hide the status message after 3 seconds
                QtCore.QTimer.singleShot(3000, lambda: self.status_label.setVisible(False))
        else:
            # Show not logged in message
            self.status_label.setText("Увійдіть для збереження налаштувань")
            self.status_label.setStyleSheet("color: #FF0000; font-weight: bold;")
            self.status_label.setVisible(True)
            
            # Hide the status message after 3 seconds
            QtCore.QTimer.singleShot(3000, lambda: self.status_label.setVisible(False))

    def showEvent(self, event):
        """Override showEvent to force refresh user data when the page is shown"""
        super().showEvent(event)
        print("Settings page is now visible - refreshing user data")
        
        # Always refresh user data when the settings page is shown
        old_user_data = self.user_data
        self.refresh_user_data()
        
        # Only show a status message if data actually changed
        if old_user_data != self.user_data and self.user_data:
            # Display status only when user data has changed and exists
            self.status_label.setText("Дані оновлено")
            self.status_label.setStyleSheet("color: #32CD32; font-weight: bold;")
            self.status_label.setVisible(True)
            
            # Hide the status message after 2 seconds
            QtCore.QTimer.singleShot(2000, lambda: self.status_label.setVisible(False))
