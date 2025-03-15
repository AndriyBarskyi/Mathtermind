from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QProgressBar, QGridLayout, QSpacerItem, QSizePolicy
)
from src.db.models import User


class UserProfileDialog(QDialog):
    """Dialog for displaying user profile information."""
    
    def __init__(self, user: User, parent=None):
        super().__init__(parent)
        self.user = user
        self.setWindowTitle(f"Профіль користувача: {user.username}")
        self.setMinimumSize(500, 400)
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        main_layout = QVBoxLayout(self)
        
        # User info section
        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.StyledPanel)
        info_layout = QGridLayout(info_frame)
        
        # Username
        username_label = QLabel("Ім'я користувача:")
        username_value = QLabel(self.user.username)
        username_value.setStyleSheet("font-weight: bold;")
        info_layout.addWidget(username_label, 0, 0)
        info_layout.addWidget(username_value, 0, 1)
        
        # Email
        email_label = QLabel("Email:")
        email_value = QLabel(self.user.email)
        email_value.setStyleSheet("font-weight: bold;")
        info_layout.addWidget(email_label, 1, 0)
        info_layout.addWidget(email_value, 1, 1)
        
        # Age group
        age_label = QLabel("Вікова група:")
        age_value = QLabel(self.user.age_group)
        age_value.setStyleSheet("font-weight: bold;")
        info_layout.addWidget(age_label, 2, 0)
        info_layout.addWidget(age_value, 2, 1)
        
        # Experience level
        level_label = QLabel("Рівень досвіду:")
        level_value = QLabel(str(self.user.experience_level))
        level_value.setStyleSheet("font-weight: bold;")
        info_layout.addWidget(level_label, 3, 0)
        info_layout.addWidget(level_value, 3, 1)
        
        # Points
        points_label = QLabel("Бали:")
        points_value = QLabel(str(self.user.points))
        points_value.setStyleSheet("font-weight: bold;")
        info_layout.addWidget(points_label, 4, 0)
        info_layout.addWidget(points_value, 4, 1)
        
        # Total study time
        time_label = QLabel("Загальний час навчання:")
        hours = self.user.total_study_time // 60
        minutes = self.user.total_study_time % 60
        time_value = QLabel(f"{hours} год {minutes} хв")
        time_value.setStyleSheet("font-weight: bold;")
        info_layout.addWidget(time_label, 5, 0)
        info_layout.addWidget(time_value, 5, 1)
        
        main_layout.addWidget(info_frame)
        
        # Progress to next level
        level_progress_label = QLabel("Прогрес до наступного рівня:")
        main_layout.addWidget(level_progress_label)
        
        level_progress = QProgressBar()
        # Calculate progress percentage to next level (100 points per level)
        points_for_current_level = (self.user.experience_level - 1) * 100
        points_for_next_level = self.user.experience_level * 100
        progress_percentage = ((self.user.points - points_for_current_level) / 
                              (points_for_next_level - points_for_current_level)) * 100
        level_progress.setValue(int(progress_percentage))
        main_layout.addWidget(level_progress)
        
        # Spacer
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer)
        
        # Close button
        button_layout = QHBoxLayout()
        close_button = QPushButton("Закрити")
        close_button.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        main_layout.addLayout(button_layout) 