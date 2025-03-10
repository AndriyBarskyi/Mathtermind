import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import Qt, QRectF
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

        # Create a QRectF instead of QRect for better precision
        rect = QRectF(self.rect().adjusted(10, 10, -10, -10))
        
        # Draw background circle
        center = rect.center()
        radius = min(rect.width(), rect.height()) / 2
        pen = QPen(QColor(234, 235, 239), 10)
        painter.setPen(pen)
        painter.drawEllipse(center, radius, radius)

        # Set color based on progress value
        if self.value <= 25:
            pen.setColor(QColor(255, 33, 34))
        elif self.value <= 50:
            pen.setColor(QColor(255, 214, 15))
        elif self.value <= 75:
            pen.setColor(QColor(22, 210, 222))
        else:
            pen.setColor(QColor(4, 214, 87))
        painter.setPen(pen)
        
        # Convert float to int for the arc angle
        start_angle = -90 * 16  # Start at 12 o'clock position (in 1/16 degrees)
        span_angle = int(-self.value * 3.6 * 16)  # Convert percentage to degrees, then to 1/16 degrees
        
        # Draw the progress arc
        painter.drawArc(rect.toRect(), start_angle, span_angle)

        # Draw the text
        painter.setPen(Qt.black)
        font_size = int(min(self.width(), self.height()) / 6)  # Responsive font size
        painter.setFont(QFont("Arial", font_size, QFont.Bold))
        text = f"{self.value}%"
        painter.drawText(self.rect(), Qt.AlignCenter, text)
        
        # Ensure painter is properly ended
        painter.end()
