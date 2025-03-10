from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QComboBox, QCheckBox, QTimeEdit, QSpinBox, QFrame, 
    QScrollArea, QGroupBox, QFormLayout, QTabWidget,
    QMessageBox
)
from PyQt6.QtCore import Qt, QTime
from PyQt6.QtGui import QFont, QIcon
from src.ui.services.settings_service import SettingsService

class SettingsPage(QWidget):
    """
    Settings page allowing users to customize their experience.
    Includes theme settings, notifications, accessibility options, and study preferences.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings_service = SettingsService()
        self.current_settings = self.settings_service.get_user_settings()
        self._setup_ui()
        self._load_settings()
        
    def _setup_ui(self):
        """Setup the UI components."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Page title
        title_label = QLabel("Налаштування")
        title_label.setObjectName("pageTitle")
        title_label.setStyleSheet("""
            QLabel#pageTitle {
                font-size: 24px;
                font-weight: bold;
                color: #0F1D35;
                margin-bottom: 20px;
            }
        """)
        
        # Create tabs for different settings categories
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                background-color: white;
                padding: 10px;
            }
            QTabBar::tab {
                background-color: #F7F8FA;
                border: 1px solid #E5E7EB;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 8px 16px;
                margin-right: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 1px solid white;
                font-weight: bold;
                color: #566CD2;
            }
        """)
        
        # Create the different settings tabs
        appearance_tab = self._create_appearance_tab()
        notifications_tab = self._create_notifications_tab()
        accessibility_tab = self._create_accessibility_tab()
        study_tab = self._create_study_preferences_tab()
        
        # Add tabs to the tab widget
        tabs.addTab(appearance_tab, "Зовнішній вигляд")
        tabs.addTab(notifications_tab, "Сповіщення")
        tabs.addTab(accessibility_tab, "Доступність")
        tabs.addTab(study_tab, "Навчання")
        
        # Create save button
        save_button = QPushButton("Зберегти зміни")
        save_button.setObjectName("saveButton")
        save_button.setStyleSheet("""
            QPushButton#saveButton {
                background-color: #566CD2;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton#saveButton:hover {
                background-color: #4A5FBF;
            }
            QPushButton#saveButton:pressed {
                background-color: #3A4DA6;
            }
        """)
        save_button.clicked.connect(self._save_settings)
        
        # Add widgets to main layout
        main_layout.addWidget(title_label)
        main_layout.addWidget(tabs)
        
        # Add a spacer before the save button
        main_layout.addStretch()
        
        # Create a container for the save button to align it to the right
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        
        main_layout.addWidget(button_container)
        
    def _create_appearance_tab(self):
        """Create the appearance settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Theme selection
        theme_group = QGroupBox("Тема")
        theme_layout = QFormLayout(theme_group)
        
        theme_selector = QComboBox()
        theme_selector.addItems(["Світла", "Темна"])
        theme_selector.setObjectName("themeSelector")
        
        theme_layout.addRow("Виберіть тему:", theme_selector)
        
        # Color accent selection
        accent_selector = QComboBox()
        accent_selector.addItems(["Синій", "Зелений", "Фіолетовий", "Червоний"])
        accent_selector.setObjectName("accentSelector")
        
        theme_layout.addRow("Колір акценту:", accent_selector)
        
        layout.addWidget(theme_group)
        layout.addStretch()
        
        return tab
        
    def _create_notifications_tab(self):
        """Create the notifications settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Notifications group
        notif_group = QGroupBox("Налаштування сповіщень")
        notif_layout = QVBoxLayout(notif_group)
        
        # Daily reminder checkbox
        daily_reminder = QCheckBox("Щоденні нагадування про навчання")
        daily_reminder.setObjectName("dailyReminder")
        
        # Achievement alerts checkbox
        achievement_alerts = QCheckBox("Сповіщення про досягнення")
        achievement_alerts.setObjectName("achievementAlerts")
        
        # Study time selection
        time_container = QWidget()
        time_layout = QHBoxLayout(time_container)
        time_layout.setContentsMargins(0, 0, 0, 0)
        
        time_label = QLabel("Час для нагадування:")
        study_time = QTimeEdit()
        study_time.setObjectName("studyTime")
        study_time.setTime(QTime(18, 0))  # Default to 6:00 PM
        study_time.setDisplayFormat("HH:mm")
        
        time_layout.addWidget(time_label)
        time_layout.addWidget(study_time)
        time_layout.addStretch()
        
        # Add widgets to notification layout
        notif_layout.addWidget(daily_reminder)
        notif_layout.addWidget(achievement_alerts)
        notif_layout.addWidget(time_container)
        
        layout.addWidget(notif_group)
        layout.addStretch()
        
        return tab
        
    def _create_accessibility_tab(self):
        """Create the accessibility settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Accessibility group
        access_group = QGroupBox("Налаштування доступності")
        access_layout = QFormLayout(access_group)
        
        # Font size selection
        font_size = QComboBox()
        font_size.addItems(["Малий", "Середній", "Великий"])
        font_size.setCurrentIndex(1)  # Default to medium
        font_size.setObjectName("fontSize")
        
        # High contrast mode
        high_contrast = QCheckBox()
        high_contrast.setObjectName("highContrast")
        
        # Add widgets to accessibility layout
        access_layout.addRow("Розмір шрифту:", font_size)
        access_layout.addRow("Високий контраст:", high_contrast)
        
        layout.addWidget(access_group)
        layout.addStretch()
        
        return tab
        
    def _create_study_preferences_tab(self):
        """Create the study preferences settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Study preferences group
        study_group = QGroupBox("Налаштування навчання")
        study_layout = QFormLayout(study_group)
        
        # Daily goal in minutes
        daily_goal = QSpinBox()
        daily_goal.setObjectName("dailyGoal")
        daily_goal.setMinimum(5)
        daily_goal.setMaximum(240)
        daily_goal.setSingleStep(5)
        daily_goal.setValue(30)  # Default to 30 minutes
        daily_goal.setSuffix(" хв")
        
        # Preferred subject
        preferred_subject = QComboBox()
        preferred_subject.addItems(["Математика", "Інформатика"])
        preferred_subject.setObjectName("preferredSubject")
        
        # Difficulty preference
        difficulty = QComboBox()
        difficulty.addItems(["Початковий", "Середній", "Просунутий"])
        difficulty.setObjectName("difficultyPreference")
        
        # Add widgets to study layout
        study_layout.addRow("Щоденна ціль:", daily_goal)
        study_layout.addRow("Бажаний предмет:", preferred_subject)
        study_layout.addRow("Рівень складності:", difficulty)
        
        layout.addWidget(study_group)
        layout.addStretch()
        
        return tab
    
    def _load_settings(self):
        """Load settings from the database and update UI components."""
        # Theme
        theme_selector = self.findChild(QComboBox, "themeSelector")
        if self.current_settings["theme"] == "light":
            theme_selector.setCurrentText("Світла")
        else:
            theme_selector.setCurrentText("Темна")
            
        # Notifications
        daily_reminder = self.findChild(QCheckBox, "dailyReminder")
        daily_reminder.setChecked(self.current_settings["notifications"]["daily_reminder"])
        
        achievement_alerts = self.findChild(QCheckBox, "achievementAlerts")
        achievement_alerts.setChecked(self.current_settings["notifications"]["achievement_alerts"])
        
        study_time = self.findChild(QTimeEdit, "studyTime")
        time_parts = self.current_settings["notifications"]["study_time"].split(":")
        study_time.setTime(QTime(int(time_parts[0]), int(time_parts[1])))
        
        # Accessibility
        font_size = self.findChild(QComboBox, "fontSize")
        font_size_map = {"small": 0, "medium": 1, "large": 2}
        font_size.setCurrentIndex(font_size_map.get(self.current_settings["accessibility"]["font_size"], 1))
        
        high_contrast = self.findChild(QCheckBox, "highContrast")
        high_contrast.setChecked(self.current_settings["accessibility"]["high_contrast"])
        
        # Study preferences
        daily_goal = self.findChild(QSpinBox, "dailyGoal")
        daily_goal.setValue(self.current_settings["study_preferences"]["daily_goal_minutes"])
        
        preferred_subject = self.findChild(QComboBox, "preferredSubject")
        if self.current_settings["study_preferences"]["preferred_subject"] == "Math":
            preferred_subject.setCurrentText("Математика")
        else:
            preferred_subject.setCurrentText("Інформатика")
        
    def _save_settings(self):
        """Save the user's settings to the database."""
        # Collect all settings from the UI components
        settings = {
            "theme": "light" if self.findChild(QComboBox, "themeSelector").currentText() == "Світла" else "dark",
            "notifications": {
                "daily_reminder": self.findChild(QCheckBox, "dailyReminder").isChecked(),
                "achievement_alerts": self.findChild(QCheckBox, "achievementAlerts").isChecked(),
                "study_time": self.findChild(QTimeEdit, "studyTime").time().toString("HH:mm")
            },
            "accessibility": {
                "font_size": ["small", "medium", "large"][self.findChild(QComboBox, "fontSize").currentIndex()],
                "high_contrast": self.findChild(QCheckBox, "highContrast").isChecked()
            },
            "study_preferences": {
                "daily_goal_minutes": self.findChild(QSpinBox, "dailyGoal").value(),
                "preferred_subject": "Math" if self.findChild(QComboBox, "preferredSubject").currentText() == "Математика" else "Informatics"
            }
        }
        
        # Save settings using the service
        success = self.settings_service.save_user_settings(settings)
        
        # Show success or error message
        if success:
            QMessageBox.information(self, "Успіх", "Налаштування успішно збережено!")
            # Update current settings
            self.current_settings = settings
        else:
            QMessageBox.warning(self, "Помилка", "Не вдалося зберегти налаштування. Спробуйте ще раз.") 