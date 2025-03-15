from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QSizePolicy, QCheckBox, QHBoxLayout
from PyQt5 import QtWidgets, QtCore, QtGui
from src.ui.theme import ThemeManager

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.pg_settings = QtWidgets.QWidget()
        self.pg_settings.setObjectName("pg_settings")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.pg_settings)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.widget_19 = QtWidgets.QWidget(self.pg_settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_19.sizePolicy().hasHeightForWidth())
        self.widget_19.setSizePolicy(sizePolicy)
        self.widget_19.setMinimumSize(QtCore.QSize(1390, 0))
        self.widget_19.setMaximumSize(QtCore.QSize(2000, 16777215))
        self.widget_19.setProperty("class", "with_border")
        
        # Use theme manager for widget background
        self.widget_19.setStyleSheet(f"""
            QWidget {{
                border-radius: 25px;
                background-color: {ThemeManager.get_color('card_background')};
                color: {ThemeManager.get_color('primary_text')};
            }}
        """)
        
        self.widget_19.setObjectName("widget_19")
        self.formLayout_2 = QtWidgets.QFormLayout(self.widget_19)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setContentsMargins(30, -1, -1, -1)
        self.formLayout_2.setHorizontalSpacing(11)
        self.formLayout_2.setVerticalSpacing(0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.widget_14 = QtWidgets.QWidget(self.widget_19)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_14.sizePolicy().hasHeightForWidth())
        self.widget_14.setSizePolicy(sizePolicy)
        self.widget_14.setMinimumSize(QtCore.QSize(500, 100))
        self.widget_14.setMaximumSize(QtCore.QSize(500, 100))
        self.widget_14.setObjectName("widget_14")
        self.formLayout = QtWidgets.QFormLayout(self.widget_14)
        self.formLayout.setContentsMargins(0, 20, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.lb_welcome = QtWidgets.QLabel(self.widget_14)
        self.lb_welcome.setText("Вітаємо,")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_welcome.sizePolicy().hasHeightForWidth())
        self.lb_welcome.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lb_welcome.setFont(font)
        self.lb_welcome.setObjectName("lb_welcome")
        self.horizontalLayout_8.addWidget(self.lb_welcome)
        self.lb_username = QtWidgets.QLabel(self.widget_14)
        self.lb_username.setText("Олена")
        self.lb_username.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lb_username.setFont(font)
        self.lb_username.setObjectName("lb_username")
        self.horizontalLayout_8.addWidget(self.lb_username)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.horizontalLayout_8)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.widget_14)
        self.lb_email = QtWidgets.QLabel(self.widget_19)
        self.lb_email.setText("Електронна адреса")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_email.sizePolicy().hasHeightForWidth())
        self.lb_email.setSizePolicy(sizePolicy)
        self.lb_email.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lb_email.setFont(font)
        self.lb_email.setObjectName("lb_email")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lb_email)
        self.le_email = QtWidgets.QLineEdit(self.widget_19)
        self.le_email.setPlaceholderText("qwerty@gmail.com")
        self.le_email.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_email.setFont(font)
        self.le_email.setInputMask("")
        self.le_email.setText("")
        
        # Use theme manager for input styling
        self.le_email.setStyleSheet(f"""
            QLineEdit {{
                background-color: {ThemeManager.get_color('input_background')};
                color: {ThemeManager.get_color('primary_text')};
                border-radius: 15px;
                padding: 5px 10px;
            }}
        """)
        
        self.le_email.setObjectName("le_email")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.le_email)
        self.btn_email = QtWidgets.QPushButton(self.widget_19)
        self.btn_email.setText("Оновити електронну адресу")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_email.sizePolicy().hasHeightForWidth())
        self.btn_email.setSizePolicy(sizePolicy)
        self.btn_email.setMinimumSize(QtCore.QSize(300, 50))
        self.btn_email.setMaximumSize(QtCore.QSize(300, 50))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.btn_email.setFont(font)
        
        # Use theme manager for button styling
        self.btn_email.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid {ThemeManager.get_color('border_color')};
                border-radius: 25px;
                background: {ThemeManager.get_color('accent_primary')};
                text-align: center;
                font: 75 15pt "Bahnschrift";
                color: white;
            }}
            QPushButton:hover {{
                background: {ThemeManager.get_color('accent_secondary')};
                color: {ThemeManager.get_color('accent_primary')};
            }}
        """)
        
        self.btn_email.setObjectName("btn_email")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.btn_email)
        self.lb_password = QtWidgets.QLabel(self.widget_19)
        self.lb_password.setText("Змінити пароль")
        self.lb_password.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lb_password.setFont(font)
        self.lb_password.setObjectName("lb_password")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.lb_password)
        self.le_password = QtWidgets.QLineEdit(self.widget_19)
        self.le_password.setPlaceholderText("Введи пароль")
        self.le_password.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_password.setFont(font)
        
        # Use theme manager for password input styling
        self.le_password.setStyleSheet(f"""
            QLineEdit {{
                background-color: {ThemeManager.get_color('input_background')};
                color: {ThemeManager.get_color('primary_text')};
                border-radius: 15px;
                padding: 5px 10px;
            }}
        """)
        
        self.le_password.setObjectName("le_password")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.le_password)
        self.btn_password = QtWidgets.QPushButton(self.widget_19)
        self.btn_password.setText("Оновити пароль")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_password.sizePolicy().hasHeightForWidth())
        self.btn_password.setSizePolicy(sizePolicy)
        self.btn_password.setMinimumSize(QtCore.QSize(300, 50))
        self.btn_password.setMaximumSize(QtCore.QSize(300, 50))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.btn_password.setFont(font)
        
        # Use theme manager for password button styling
        self.btn_password.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid {ThemeManager.get_color('border_color')};
                border-radius: 25px;
                background: {ThemeManager.get_color('accent_primary')};
                text-align: center;
                font: 75 15pt "Bahnschrift";
                color: white;
            }}
            QPushButton:hover {{
                background: {ThemeManager.get_color('accent_secondary')};
                color: {ThemeManager.get_color('accent_primary')};
            }}
        """)
        
        self.btn_password.setObjectName("btn_password")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.btn_password)
        
        # Add theme settings section
        self.lb_theme = QtWidgets.QLabel(self.widget_19)
        self.lb_theme.setText("Налаштування теми")
        self.lb_theme.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lb_theme.setFont(font)
        self.lb_theme.setObjectName("lb_theme")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.lb_theme)
        
        # Theme toggle container
        self.themeContainer = QtWidgets.QWidget(self.widget_19)
        self.themeContainer.setMinimumSize(QtCore.QSize(500, 50))
        self.themeContainer.setMaximumSize(QtCore.QSize(500, 50))
        self.themeContainer.setObjectName("themeContainer")
        
        # Horizontal layout for theme toggle
        self.themeLayout = QtWidgets.QHBoxLayout(self.themeContainer)
        self.themeLayout.setContentsMargins(0, 0, 0, 0)
        self.themeLayout.setObjectName("themeLayout")
        
        # Light theme label
        self.lb_light_theme = QtWidgets.QLabel(self.themeContainer)
        self.lb_light_theme.setText("Світла тема")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lb_light_theme.setFont(font)
        self.lb_light_theme.setObjectName("lb_light_theme")
        self.themeLayout.addWidget(self.lb_light_theme)
        
        # Theme toggle switch - use theme manager colors
        self.themeToggle = QtWidgets.QCheckBox(self.themeContainer)
        self.themeToggle.setText("")
        self.themeToggle.setObjectName("themeToggle")
        
        # Use theme manager for toggle styling
        self.themeToggle.setStyleSheet(f"""
            QCheckBox {{
                spacing: 5px;
            }}
            QCheckBox::indicator {{
                width: 60px;
                height: 30px;
                border-radius: 15px;
                background-color: {ThemeManager.get_color('card_background')};
                border: 2px solid {ThemeManager.get_color('border_color')};
            }}
            QCheckBox::indicator:checked {{
                background-color: {ThemeManager.get_color('accent_primary')};
                border: 2px solid {ThemeManager.get_color('accent_primary')};
            }}
        """)
        
        self.themeLayout.addWidget(self.themeToggle)
        
        # Dark theme label
        self.lb_dark_theme = QtWidgets.QLabel(self.themeContainer)
        self.lb_dark_theme.setText("Темна тема")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lb_dark_theme.setFont(font)
        self.lb_dark_theme.setObjectName("lb_dark_theme")
        self.themeLayout.addWidget(self.lb_dark_theme)
        
        # Add spacer to push everything to the left
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.themeLayout.addItem(spacerItem)
        
        # Add theme container to form layout
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.themeContainer)
        
        self.gridLayout_7.addWidget(self.widget_19, 1, 0, 1, 1)
        self.lb_settings = QtWidgets.QLabel(self.pg_settings)
        self.lb_settings.setText("Налаштування")
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lb_settings.setFont(font)
        self.lb_settings.setObjectName("lb_settings")
        
        # Use theme manager for settings label
        self.lb_settings.setStyleSheet(f"color: {ThemeManager.get_color('primary_text')};")
        
        self.gridLayout_7.addWidget(self.lb_settings, 0, 0, 1, 1)
        self.setLayout(self.gridLayout_7)
        
        # Set the initial state of the theme toggle based on the current theme
        self.themeToggle.setChecked(ThemeManager.get_current_theme() == ThemeManager.DARK_THEME)
        
    def update_theme_styles(self):
        """Update all component styles when theme changes"""
        # Update widget background
        self.widget_19.setStyleSheet(f"""
            QWidget {{
                border-radius: 25px;
                background-color: {ThemeManager.get_color('card_background')};
                color: {ThemeManager.get_color('primary_text')};
            }}
        """)
        
        # Update input fields
        input_style = f"""
            QLineEdit {{
                background-color: {ThemeManager.get_color('input_background')};
                color: {ThemeManager.get_color('primary_text')};
                border-radius: 15px;
                padding: 5px 10px;
            }}
        """
        self.le_email.setStyleSheet(input_style)
        self.le_password.setStyleSheet(input_style)
        
        # Update buttons
        button_style = f"""
            QPushButton {{
                border: 1px solid {ThemeManager.get_color('border_color')};
                border-radius: 25px;
                background: {ThemeManager.get_color('accent_primary')};
                text-align: center;
                font: 75 15pt "Bahnschrift";
                color: white;
            }}
            QPushButton:hover {{
                background: {ThemeManager.get_color('accent_secondary')};
                color: {ThemeManager.get_color('accent_primary')};
            }}
        """
        self.btn_email.setStyleSheet(button_style)
        self.btn_password.setStyleSheet(button_style)
        
        # Update toggle
        self.themeToggle.setStyleSheet(f"""
            QCheckBox {{
                spacing: 5px;
            }}
            QCheckBox::indicator {{
                width: 60px;
                height: 30px;
                border-radius: 15px;
                background-color: {ThemeManager.get_color('card_background')};
                border: 2px solid {ThemeManager.get_color('border_color')};
            }}
            QCheckBox::indicator:checked {{
                background-color: {ThemeManager.get_color('accent_primary')};
                border: 2px solid {ThemeManager.get_color('accent_primary')};
            }}
        """)
        
        # Update settings label
        self.lb_settings.setStyleSheet(f"color: {ThemeManager.get_color('primary_text')};")