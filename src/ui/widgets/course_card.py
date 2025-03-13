from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QSizePolicy, QWidget, QGridLayout,
    QScrollArea, QLayout
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QRect, QPoint
from PyQt5.QtGui import QFont, QFontMetrics, QIcon

from src.ui.models.course import Course
from src.ui.styles.constants import COLORS, FONTS

# Create a FlowLayout class for better tag display
class FlowLayout(QLayout):
    """
    Custom flow layout for tags that wraps to the next line when needed.
    """
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)
        self._items = []

    def addItem(self, item):
        self._items.append(item)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self._doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        margin = self.contentsMargins().left()
        size += QSize(2 * margin, 2 * margin)
        return size

    def _doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0
        spacing = self.spacing()

        for item in self._items:
            widget = item.widget()
            spaceX = spacing
            spaceY = spacing
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()

class CourseCard(QFrame):
    """
    Widget representing a single course card in the courses grid.
    Displays course information and provides interaction.
    """
    # Signal emitted when the start button is clicked
    course_started = pyqtSignal(str)  # Emits course ID
    
    # Card dimensions - now minimum width instead of fixed
    MIN_CARD_WIDTH = 280
    MIN_CARD_HEIGHT = 380
    MAX_DESCRIPTION_LENGTH = 150
    
    def __init__(self, course: Course, parent=None):
        super().__init__(parent)
        self.course = course
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the card UI"""
        # Configure frame
        self.setFrameShape(QFrame.Shape.StyledPanel)
        # Use minimum size instead of fixed size for responsiveness
        self.setMinimumSize(self.MIN_CARD_WIDTH, self.MIN_CARD_HEIGHT)
        self.setMaximumSize(int(self.MIN_CARD_WIDTH * 1.5), int(self.MIN_CARD_HEIGHT * 1.5))
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #E0E0E0;
            }
            QFrame:hover {
                border: 1px solid #DDE2F6;
            }
        """)
        
        # Create card layout
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # 1. Course title (fixed height)
        title = QLabel(self.course.name)
        title.setFont(FONTS.TITLE)
        title.setWordWrap(True)
        title.setFixedHeight(60)  # Fixed height for title
        title.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        # 2. Course tags (using flow layout)
        tags_container = QWidget()
        tags_layout = self._create_tags_layout(tags_container)
        tags_container.setFixedHeight(60)  # Fixed height for tags section
        
        # 3. Course description (truncated with ellipsis)
        description = QLabel(self._truncate_description(self.course.description, self.MAX_DESCRIPTION_LENGTH))
        description.setWordWrap(True)
        description.setFont(FONTS.BODY)
        description.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        description.setFixedHeight(120)  # Fixed height for description
        
        # 4. Course metadata
        metadata_layout = self._create_metadata_layout()
        
        # 5. Start button
        start_btn = self._create_start_button()
        
        # Add all elements to card layout
        layout.addWidget(title)
        layout.addWidget(tags_container)
        layout.addWidget(description)
        layout.addStretch()
        layout.addLayout(metadata_layout)
        layout.addWidget(start_btn)
    
    def _create_tags_layout(self, parent):
        """Create a flow layout for tags"""
        tags_layout = FlowLayout(parent, margin=0, spacing=8)
        
        # Add subject tag
        subject_tag = QLabel(self.course.topic)
        subject_tag.setProperty("class", "tag subject")
        
        # Add level tag
        level_tag = QLabel(self.course.difficulty_level)
        level_tag.setProperty("class", "tag level")
        
        # Style tags
        for tag in [subject_tag, level_tag]:
            tag.setFont(QFont("Inter", 10))
            tag.setAlignment(Qt.AlignCenter)
            tag.setStyleSheet(f"""
                padding: 4px 8px;
                background-color: {COLORS.TAG_BG};
                color: {COLORS.TAG_TEXT};
                border-radius: 4px;
            """)
        
        # Add tags to layout
        tags_layout.addWidget(subject_tag)
        tags_layout.addWidget(level_tag)
        
        # Add additional tags from course
        for tag_text in self.course.tags[:3]:  # Limit to 3 additional tags
            tag = QLabel(tag_text)
            tag.setFont(QFont("Inter", 10))
            tag.setAlignment(Qt.AlignCenter)
            tag.setStyleSheet(f"""
                padding: 4px 8px;
                background-color: {COLORS.TAG_BG};
                color: {COLORS.TAG_TEXT};
                border-radius: 4px;
            """)
            tags_layout.addWidget(tag)
        
        return tags_layout
    
    def _create_metadata_layout(self):
        """Create the layout for course metadata"""
        metadata_layout = QHBoxLayout()
        metadata_layout.setSpacing(8)
        
        # Duration
        duration = QLabel(self.course.formatted_duration)
        
        # Updated date
        updated = QLabel(self.course.formatted_created_date)
        
        for label in [duration, updated]:
            label.setFont(QFont("Inter", 10))
            label.setProperty("class", "metadata")
            label.setStyleSheet(f"color: {COLORS.METADATA_TEXT};")
        
        metadata_layout.addWidget(duration)
        metadata_layout.addStretch()
        metadata_layout.addWidget(updated)
        
        return metadata_layout
    
    def _create_start_button(self):
        """Create the start course button"""
        start_btn = QPushButton("Почати курс")
        start_btn.setFont(QFont("Inter", 13, QFont.DemiBold))
        start_btn.setFixedHeight(36)
        start_btn.setCursor(Qt.PointingHandCursor)
        start_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS.PRIMARY};
                color: white;
                border-radius: 18px;
                padding: 0 16px;
            }}
            QPushButton:hover {{
                background-color: {COLORS.PRIMARY_DARK};
            }}
        """)
        
        # Connect the button click to emit the signal
        start_btn.clicked.connect(lambda: self.course_started.emit(self.course.id))
        
        return start_btn
    
    def _truncate_description(self, text, max_length):
        """Truncate text and add ellipsis if it's longer than max_length"""
        if len(text) <= max_length:
            return text
        return text[:max_length].rstrip() + "..."

    def sizeHint(self):
        """Return the preferred size of the card"""
        return QSize(self.MIN_CARD_WIDTH, self.MIN_CARD_HEIGHT) 