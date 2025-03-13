import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QFont, QColor

class CircularProgress(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = 0

    def set_value(self, value):
        self.value = max(0, min(100, value))  
        self.update() 

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(10, 10, -10, -10) 
        center = rect.center()
        radius = min(rect.width(), rect.height()) // 2
        
        # Background circle - light gray from new theme
        pen = QPen(QColor("#F3F4F6"), 10)
        painter.setPen(pen)
        painter.drawEllipse(center, radius, radius)

        # Progress arc with color based on value
        if self.value <= 25:
            # Red for low progress
            pen.setColor(QColor("#EF4444"))
        elif self.value <= 50:
            # Yellow/Orange for medium-low progress
            pen.setColor(QColor("#F59E0B"))
        elif self.value <= 75:
            # Blue from theme for medium-high progress
            pen.setColor(QColor("#566CD2"))
        else:
            # Green for high progress
            pen.setColor(QColor("#10B981"))
            
        painter.setPen(pen)
        painter.drawArc(
            rect,  
            -90 * 16,
            -self.value * 3.6 * 16 
        )

        # Text color from theme
        painter.setPen(QColor("#0F1D35"))
        painter.setFont(QFont("Inter", 16, QFont.Bold))
        text = f"{self.value}%"
        painter.drawText(self.rect(), Qt.AlignCenter, text)
