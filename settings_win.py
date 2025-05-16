from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QFormLayout, QHBoxLayout,
    QGridLayout, QSizePolicy, QPushButton, QVBoxLayout)
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

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

        self.layout_settings_form = QFormLayout(self.widget_settings_content)
        self.layout_settings_form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.layout_settings_form.setContentsMargins(30, 20, 30, 20)
        self.layout_settings_form.setHorizontalSpacing(12)
        self.layout_settings_form.setVerticalSpacing(8)

        self.add_user_greeting()
        self.add_form_field("Повне ім'я", "Олександр Петренко", "le_name")
        self.add_form_field("Електронна адреса", "oleksandr.petrenko@example.com", "le_email")
        self.add_form_field("Телефон", "+380501234567", "le_phone")
        self.add_form_field("Дата народження", "12.05.2005", "le_birthday")
        self.add_password_field("Пароль", "12.05.2005", "le_birthday")

        self.btn_save = QPushButton("Зберегти", self.widget_settings_content)
        self.btn_save.setObjectName("btn_save")
        self.btn_save.setMinimumSize(QtCore.QSize(300, 50))
        self.btn_save.setMaximumSize(QtCore.QSize(300, 50))
        self.btn_save.setProperty("type","start_continue")
        self.layout_settings_form.addRow(self.btn_save)

        self.layout_settings_main.addWidget(self.widget_settings_content)

    def apply_size_policy(self, widget, min_width=0, max_width=16777215, min_height=0, max_height=16777215):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(size_policy)
        widget.setMinimumSize(min_width, min_height)
        widget.setMaximumSize(max_width, max_height)

    def add_user_greeting(self):
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

        lb_username = QLabel("Олександр", widget_user_greeting)
        lb_username.setProperty("type", "page_section")
        layout_user_greeting.addWidget(lb_username)

        self.layout_settings_form.addRow(widget_user_greeting)

    def add_form_field(self, label_text, placeholder_text, obj_name):
        label = QLabel(label_text, self.widget_settings_content)
        label.setProperty("type", "page_section")
        label.setMaximumHeight(50)
        self.apply_size_policy(label)
        self.layout_settings_form.addRow(label)

        input_field = QLineEdit(self.widget_settings_content)
        input_field.setPlaceholderText(placeholder_text)
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
        input_field.setMaximumHeight(50)
        input_field.setObjectName(obj_name)
        input_field.setProperty("type", "settings")
        self.layout_settings_form.addRow(input_field)
