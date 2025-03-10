from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QSizePolicy, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from src.ui.models.course import Course
from src.ui.styles.constants import COLORS, FONTS

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
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        # Create card layout
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # 1. Lesson number and type
        header_layout = QHBoxLayout()
        
        # Lesson number
        lesson_number = QLabel(f"Урок {self.lesson.lesson_order}")
        lesson_number.setFont(FONTS.SUBTITLE)
        
        # Lesson type (Theory, Practice, Quiz, etc.)
        lesson_type = QLabel(self._get_lesson_type_ukr())
        lesson_type.setFont(FONTS.BODY)
        lesson_type.setStyleSheet(f"color: {COLORS.METADATA_TEXT};")
        
        header_layout.addWidget(lesson_number)
        header_layout.addStretch()
        header_layout.addWidget(lesson_type)
        
        # 2. Lesson title
        title = QLabel(self.lesson.title)
        title.setFont(FONTS.TITLE)
        title.setWordWrap(True)
        title.setFixedHeight(60)
        title.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        # 3. Lesson description
        description = QLabel(self._truncate_description(self.lesson.description, self.MAX_DESCRIPTION_LENGTH))
        description.setWordWrap(True)
        description.setFont(FONTS.BODY)
        description.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        description.setFixedHeight(80)
        
        # 4. Lesson metadata
        metadata_layout = self._create_metadata_layout()
        
        # 5. Start button
        start_btn = self._create_start_button()
        
        # Add all elements to card layout
        layout.addLayout(header_layout)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch()
        layout.addLayout(metadata_layout)
        layout.addWidget(start_btn)
    
    def _create_metadata_layout(self):
        """Create the layout for lesson metadata"""
        metadata_layout = QHBoxLayout()
        metadata_layout.setSpacing(8)
        
        # Difficulty level
        difficulty = QLabel(self._get_difficulty_ukr())
        
        # Duration
        duration = QLabel(f"{self.lesson.estimated_time} хв")
        
        for label in [difficulty, duration]:
            label.setFont(QFont("Inter", 10))
            label.setProperty("class", "metadata")
            label.setStyleSheet(f"color: {COLORS.METADATA_TEXT};")
        
        metadata_layout.addWidget(difficulty)
        metadata_layout.addStretch()
        metadata_layout.addWidget(duration)
        
        return metadata_layout
    
    def _create_start_button(self):
        """Create the start lesson button"""
        start_btn = QPushButton("Почати урок")
        start_btn.setFont(QFont("Inter", 13, QFont.Weight.DemiBold))
        start_btn.setFixedHeight(36)
        start_btn.setStyleSheet(f"background-color: {COLORS.PRIMARY}; color: white; border-radius: 18px;")
        
        # Connect the button click to emit the signal
        start_btn.clicked.connect(lambda: self.lesson_started.emit(str(self.lesson.id)))
        
        return start_btn
    
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