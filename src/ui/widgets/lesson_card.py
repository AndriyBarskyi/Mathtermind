from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QProgressBar, QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QIcon

from src.ui.models.course import Course
from src.ui.styles.constants import COLORS, FONTS
from src.ui.theme import ThemeManager

class LessonCard(QFrame):
    """
    Widget representing a single lesson card in the lessons grid.
    Displays lesson information and provides interaction.
    """
    # Signal emitted when the start button is clicked
    lesson_started = pyqtSignal(str)  # Emits lesson ID
    
    # Card dimensions
    MIN_CARD_WIDTH = 280
    MIN_CARD_HEIGHT = 320  # Smaller than course card
    MAX_DESCRIPTION_LENGTH = 120
    
    def __init__(self, lesson, parent=None):
        super().__init__(parent)
        self.lesson = lesson
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the card UI"""
        # Configure frame
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumSize(self.MIN_CARD_WIDTH, self.MIN_CARD_HEIGHT)
        self.setMaximumSize(int(self.MIN_CARD_WIDTH * 1.5), int(self.MIN_CARD_HEIGHT * 1.5))
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Use ThemeManager for card styling
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {ThemeManager.get_color('card_background')};
                border-radius: 25px;
                border: 1px solid {ThemeManager.get_color('border_color')};
            }}
            QFrame:hover {{
                border: 1px solid {ThemeManager.get_color('border_hover_color')};
            }}
        """)
        
        # Create card layout
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # 1. Lesson number and type
        header_layout = QHBoxLayout()
        
        # Lesson number
        lesson_number = QLabel(f"Урок {self.lesson.lesson_order}")
        lesson_number.setFont(FONTS.SUBTITLE)
        
        # Use ThemeManager for lesson number text color
        lesson_number.setStyleSheet(f"color: {ThemeManager.get_color('primary_text')};")
        
        # Lesson type (Theory, Practice, Quiz, etc.)
        lesson_type = QLabel(self._get_lesson_type_ukr())
        lesson_type.setFont(FONTS.BODY)
        
        # Use ThemeManager for lesson type text color
        lesson_type.setStyleSheet(f"color: {ThemeManager.get_color('secondary_text')};")
        lesson_type.setProperty("class", "metadata")
        
        header_layout.addWidget(lesson_number)
        header_layout.addStretch()
        header_layout.addWidget(lesson_type)
        
        # 2. Lesson title
        title = QLabel(self.lesson.title)
        title.setFont(FONTS.TITLE)
        title.setWordWrap(True)
        title.setFixedHeight(60)
        title.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        # Use ThemeManager for title text color
        title.setStyleSheet(f"color: {ThemeManager.get_color('primary_text')};")
        
        # 3. Metadata layout (difficulty, time, tasks)
        metadata_layout = self._create_metadata_layout()
        
        # 4. Start button or completion status
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 8, 0, 0)
        
        # Create start button
        start_btn = self._create_start_button()
        button_layout.addStretch()
        button_layout.addWidget(start_btn)
        
        # Add all elements to card layout
        layout.addLayout(header_layout)
        layout.addWidget(title)
        layout.addStretch()
        layout.addLayout(metadata_layout)
        layout.addLayout(button_layout)
    
    def _create_metadata_layout(self):
        """Create the layout for lesson metadata"""
        metadata_layout = QHBoxLayout()
        metadata_layout.setSpacing(16)
        
        # Video duration
        video_label = QLabel(f"Відео {self.lesson.estimated_time} хв")
        video_label.setFont(QFont("Inter", 11))
        
        # Use ThemeManager for metadata text color
        video_label.setStyleSheet(f"color: {ThemeManager.get_color('secondary_text')};")
        video_label.setProperty("class", "metadata")
        
        # Number of tasks if available
        tasks_count = getattr(self.lesson, 'tasks_count', 0)
        if tasks_count > 0:
            tasks_text = f"{tasks_count} {'Завдань' if tasks_count != 1 else 'Завдання'}"
            tasks_label = QLabel(tasks_text)
            tasks_label.setFont(QFont("Inter", 11))
            
            # Use ThemeManager for tasks label text color
            tasks_label.setStyleSheet(f"color: {ThemeManager.get_color('secondary_text')};")
            tasks_label.setProperty("class", "metadata")
            
            metadata_layout.addWidget(tasks_label)
        
        # Difficulty level
        difficulty_label = QLabel(self._get_difficulty_ukr())
        difficulty_label.setFont(QFont("Inter", 11))
        
        # Use ThemeManager for difficulty label text color
        difficulty_label.setStyleSheet(f"color: {ThemeManager.get_color('secondary_text')};")
        difficulty_label.setProperty("class", "metadata")
        
        metadata_layout.addWidget(video_label)
        metadata_layout.addWidget(difficulty_label)
        metadata_layout.addStretch()
        
        return metadata_layout
    
    def _create_start_button(self):
        """Create the start lesson button"""
        start_btn = QPushButton("Продовжити урок" if self._is_in_progress() else "Почати урок")
        start_btn.setFont(QFont("Inter", 13))
        start_btn.setCursor(Qt.PointingHandCursor)
        start_btn.setFixedHeight(36)
        start_btn.setMinimumWidth(140)
        
        # Style based on completion status
        if self._is_completed():
            start_btn.setText("Пройдено")
            start_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ThemeManager.get_color('success')};
                    color: white;
                    border-radius: 25px;
                    padding: 0 16px;
                }}
                QPushButton:hover {{
                    background-color: {ThemeManager.get_color('success')};
                    opacity: 0.9;
                }}
            """)
        else:
            # Use ThemeManager for button styling
            start_btn.setStyleSheet(ThemeManager.get_start_button_style())
        
        # Connect the button click to emit the signal
        start_btn.clicked.connect(lambda: self.lesson_started.emit(str(self.lesson.id)))
        
        return start_btn
    
    def _is_completed(self):
        """Check if the lesson is completed"""
        # This would normally check user progress data
        # For now, return False as a placeholder
        return False
    
    def _is_in_progress(self):
        """Check if the lesson is in progress"""
        # This would normally check user progress data
        # For now, return False as a placeholder
        return False
    
    def _truncate_description(self, text, max_length):
        """Truncate text and add ellipsis if it's longer than max_length"""
        if len(text) <= max_length:
            return text
        return text[:max_length].rstrip() + "..."
    
    def _get_difficulty_ukr(self):
        """Get Ukrainian translation of difficulty level"""
        difficulty_map = {
            "Beginner": "Початковий",
            "Intermediate": "Середній",
            "Advanced": "Просунутий"
        }
        return difficulty_map.get(self.lesson.difficulty_level, self.lesson.difficulty_level)
    
    def _get_lesson_type_ukr(self):
        """Get Ukrainian translation of lesson type"""
        type_map = {
            "Theory": "Теорія",
            "Practice": "Практика",
            "Quiz": "Тест",
            "Challenge": "Завдання"
        }
        return type_map.get(self.lesson.lesson_type, self.lesson.lesson_type)
    
    def sizeHint(self):
        """Return the preferred size of the card"""
        return QSize(self.MIN_CARD_WIDTH, self.MIN_CARD_HEIGHT)
        
    def update_theme_styles(self):
        """Update all component styles when theme changes"""
        # Update card background
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {ThemeManager.get_color('card_background')};
                border-radius: 25px;
                border: 1px solid {ThemeManager.get_color('border_color')};
            }}
            QFrame:hover {{
                border: 1px solid {ThemeManager.get_color('border_hover_color')};
            }}
        """)
        
        # Update all child widgets
        for child in self.findChildren(QWidget):
            if isinstance(child, QLabel):
                if child.property("class") == "metadata":
                    child.setStyleSheet(f"color: {ThemeManager.get_color('secondary_text')};")
                else:
                    child.setStyleSheet(f"color: {ThemeManager.get_color('primary_text')};")
            elif isinstance(child, QPushButton):
                if self._is_completed():
                    child.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {ThemeManager.get_color('success')};
                            color: white;
                            border-radius: 25px;
                            padding: 0 16px;
                        }}
                        QPushButton:hover {{
                            background-color: {ThemeManager.get_color('success')};
                            opacity: 0.9;
                        }}
                    """)
                else:
                    child.setStyleSheet(ThemeManager.get_start_button_style()) 