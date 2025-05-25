from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QFormLayout, QHBoxLayout,
    QGridLayout, QSizePolicy, QPushButton, QVBoxLayout)
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from src.services import SessionManager, UserService, AuthService
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

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
        self.setLayout(self.main_layout)

        self.pg_settings = QWidget(self)
        self.pg_settings.setObjectName("pg_settings")
        self.main_layout.addWidget(self.pg_settings)
        self.layout_settings_main = QGridLayout(self.pg_settings)
        
        self.widget_settings_content = QWidget(self.pg_settings)
        self.apply_size_policy(self.widget_settings_content, min_width=600)
        self.widget_settings_content.setProperty("type", "w_pg")

        self.content_v_layout = QVBoxLayout(self.widget_settings_content)

        self.layout_settings_form = QFormLayout()
        self.layout_settings_form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.layout_settings_form.setContentsMargins(30, 20, 30, 20)
        self.layout_settings_form.setHorizontalSpacing(12)
        self.layout_settings_form.setVerticalSpacing(8)
        self.content_v_layout.addLayout(self.layout_settings_form)

        self.user_service = UserService()
        self.session_manager = SessionManager()
        self.auth_service = AuthService()
        
        self.current_user = None
        self.form_fields = {}
        
        self.btn_save = QPushButton("Зберегти", self.widget_settings_content)
        self.btn_save.setObjectName("btn_save")
        self.btn_save.setMinimumSize(QtCore.QSize(300, 50))
        self.btn_save.setMaximumSize(QtCore.QSize(300, 50))
        self.btn_save.setProperty("type","start_continue")
        self.btn_save.clicked.connect(self._save_settings)
        self.content_v_layout.addWidget(self.btn_save, 0, Qt.AlignCenter)
        self.content_v_layout.addStretch(1)

        self._load_user_data()

        self.layout_settings_main.addWidget(self.widget_settings_content)

    def _clear_form_content(self):
        """Clears all rows from the QFormLayout (layout_settings_form)."""
        for i in reversed(range(self.layout_settings_form.rowCount())):
            self.layout_settings_form.removeRow(i)
        self.form_fields = {}

    def _load_user_data(self):
        """Loads current user data and populates the form."""
        self._clear_form_content()
        self.btn_save.setEnabled(True)

        user_data_dict = self.session_manager.get_current_user()
        if user_data_dict and isinstance(user_data_dict, dict) and 'id' in user_data_dict:
            user_id = user_data_dict['id']
            try:
                self.current_user = self.user_service.get_user_by_id(user_id)
                if self.current_user:
                    self.add_user_greeting(self.current_user.username or "Користувач")
                    
                    self.add_form_field("Повне ім\'я", self.current_user.full_name, "le_name")
                    self.add_form_field("Електронна адреса", getattr(self.current_user, 'email', ''), "le_email")
                    
                    phone_number_val = self.current_user.metadata.get('phone_number', '') if self.current_user.metadata else ''
                    self.add_form_field("Телефон", phone_number_val, "le_phone")
                    
                    dob_text = ''
                    if self.current_user.metadata:
                        dob_from_meta = self.current_user.metadata.get('date_of_birth')
                        if dob_from_meta:
                            try:
                                if isinstance(dob_from_meta, datetime):
                                    dob_text = dob_from_meta.strftime('%d.%m.%Y')
                                elif isinstance(dob_from_meta, str):
                                    dob_text = dob_from_meta 
                            except AttributeError: 
                                dob_text = str(dob_from_meta)
                            except ValueError:
                                logger.warning(f"Could not parse date_of_birth string from metadata: {dob_from_meta}")
                                dob_text = str(dob_from_meta)

                    self.add_form_field("Дата народження", dob_text, "le_birthday")
                    
                    self.add_password_field("Новий пароль", "", "le_new_password") 
                else:
                    logger.warning("Settings: Could not retrieve user details for ID: %s", user_id)
                    self._show_empty_settings("Не вдалося завантажити дані користувача.")
            except Exception as e:
                logger.error("Settings: Error loading user data: %s", e, exc_info=True)
                self._show_empty_settings(f"Помилка завантаження: {e}")
        else:
            logger.warning("Settings: No active user session.")
            self._show_empty_settings("Будь ласка, увійдіть до системи.")
            
    def _show_empty_settings(self, message):
        """Displays a message when user data cannot be loaded."""
        self._clear_form_content()

        self.add_user_greeting("Гість")
        info_label = QLabel(message, self.widget_settings_content)
        info_label.setAlignment(Qt.AlignCenter)
        self.layout_settings_form.addRow(info_label)
        
        self.btn_save.setEnabled(False)


    def apply_size_policy(self, widget, min_width=0, max_width=16777215, min_height=0, max_height=16777215):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(size_policy)
        widget.setMinimumSize(min_width, min_height)
        widget.setMaximumSize(max_width, max_height)

    def add_user_greeting(self, username="Користувач"):
        widget_user_greeting = QWidget(self.widget_settings_content)
        widget_user_greeting.setProperty("type", "w_pg")
        self.apply_size_policy(widget_user_greeting, min_width=500, max_width=500, min_height=100, max_height=100)

        layout_user_greeting = QHBoxLayout(widget_user_greeting)
        layout_user_greeting.setContentsMargins(0, 20, 0, 0)

        lb_image = QLabel(widget_user_greeting)
        lb_image.setMinimumSize(50, 50)
        lb_image.setMaximumSize(50, 50)
        lb_image.setScaledContents(True)
        original_pixmap = QPixmap("icon/icon_users.PNG") #зображення 
        round_pixmap = make_round_pixmap(original_pixmap, QSize(50, 50))
        lb_image.setPixmap(round_pixmap)
        lb_image.setAlignment(Qt.AlignCenter)
        layout_user_greeting.addWidget(lb_image)

        lb_welcome = QLabel("Вітаємо,", widget_user_greeting)
        lb_welcome.setProperty("type", "page_section")
        lb_welcome.setMinimumSize(100, 50)
        lb_welcome.setMaximumSize(100, 50)
        layout_user_greeting.addWidget(lb_welcome)

        lb_username = QLabel(username, widget_user_greeting)
        lb_username.setProperty("type", "page_section")
        layout_user_greeting.addWidget(lb_username)

        self.layout_settings_form.addRow(widget_user_greeting)

    def add_form_field(self, label_text, field_value, obj_name):
        label = QLabel(label_text, self.widget_settings_content)
        label.setProperty("type", "page_section")
        label.setMaximumHeight(50)
        self.apply_size_policy(label)
        self.layout_settings_form.addRow(label)

        input_field = QLineEdit(self.widget_settings_content)
        input_field.setText(field_value)
        if not hasattr(self, 'form_fields'):
            self.form_fields = {}
        self.form_fields[obj_name] = input_field
        input_field.setMaximumHeight(50)
        input_field.setObjectName(obj_name)
        input_field.setProperty("type", "settings")
        self.layout_settings_form.addRow(input_field)


    def add_password_field(self, label_text, placeholder_text, obj_name):
        label = QLabel(label_text, self.widget_settings_content)
        label.setProperty("type", "page_section")
        label.setMaximumHeight(50)
        self.apply_size_policy(label)
        self.layout_settings_form.addRow(label)

        input_field = QLineEdit(self.widget_settings_content)
        input_field.setPlaceholderText(placeholder_text)
        input_field.setEchoMode(QLineEdit.Password)  
        if not hasattr(self, 'form_fields'):
            self.form_fields = {}
        self.form_fields[obj_name] = input_field
        input_field.setMaximumHeight(50)
        input_field.setObjectName(obj_name)
        input_field.setProperty("type", "settings")
        self.layout_settings_form.addRow(input_field)

    def _save_settings(self):
        """Saves the updated user settings."""
        if not self.current_user or not self.current_user.id:
            logger.warning("Settings: Cannot save, no current user or user ID.")
            return

        user_id = self.current_user.id
        updates = {}
        metadata_updates = {}

        try:
            full_name_str = self.form_fields['le_name'].text().strip()
            email_str = self.form_fields['le_email'].text().strip()
            phone_str = self.form_fields['le_phone'].text().strip()
            birthday_str = self.form_fields['le_birthday'].text().strip()
            new_password_str = self.form_fields['le_new_password'].text()

            if email_str != self.current_user.email:
                updates['email'] = email_str
            
            if full_name_str:
                parts = full_name_str.split(' ', 1)
                current_first_name = self.current_user.first_name or ''
                current_last_name = self.current_user.last_name or ''
                
                first_name = parts[0]
                last_name = parts[1] if len(parts) > 1 else ''
                
                if first_name != current_first_name:
                    updates['first_name'] = first_name
                if last_name != current_last_name:
                    updates['last_name'] = last_name
            else:
                if self.current_user.first_name:
                    updates['first_name'] = ''
                if self.current_user.last_name:
                    updates['last_name'] = ''

            current_phone = self.current_user.metadata.get('phone_number', '')
            if phone_str != current_phone:
                metadata_updates['phone_number'] = phone_str

            current_birthday = self.current_user.metadata.get('date_of_birth', '')
            if birthday_str != str(current_birthday): 
                metadata_updates['date_of_birth'] = birthday_str

            if new_password_str:
                if len(new_password_str) < 6:
                    logger.warning("Settings: New password is too short.")
                    return
                
                hashed_password = self.auth_service.hash_password(new_password_str)
                updates['password_hash'] = hashed_password
                logger.info(f"Settings: Password change requested for user {user_id}.")

            updated_user_details = False
            if updates:
                logger.info(f"Settings: Updating user attributes for {user_id}: {updates}")
                self.user_service.update_user(user_id, updates)
                updated_user_details = True
            
            if metadata_updates:
                logger.info(f"Settings: Updating user metadata for {user_id}: {metadata_updates}")
                self.user_service.update_user_metadata(user_id, metadata_updates)
                updated_user_details = True

            if updated_user_details:
                logger.info(f"Settings: User {user_id} updated successfully.")
                self._load_user_data() 
                self.form_fields['le_new_password'].setText('')
            else:
                logger.info(f"Settings: No changes detected for user {user_id}.")

        except Exception as e:
            logger.error(f"Settings: Error saving settings for user {user_id}: {e}", exc_info=True)

