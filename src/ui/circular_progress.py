import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QFont,QColor

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
        pen = QPen(QColor(234, 235, 239), 10)
        painter.setPen(pen)
        painter.drawEllipse(center, radius, radius)

        if self.value <= 25:
            pen.setColor(QColor(255, 33, 34))
        elif self.value <= 50:
            pen.setColor(QColor(255, 214, 15))
        elif self.value <= 75:
            pen.setColor(QColor(22, 210, 222))
        else:
            pen.setColor(QColor(4, 214, 87))
        painter.setPen(pen)
        
        # Fix for QPainter errors - convert rect to QRect and int values
        painter.drawArc(
            int(rect.x()), int(rect.y()), 
            int(rect.width()), int(rect.height()),
            -90 * 16,
            int(-self.value * 3.6 * 16)
        )

        painter.setPen(Qt.black)
        painter.setFont(QFont("MS Shell Dlg 2", 16, QFont.Bold))
        text = f"{self.value}%"
        painter.drawText(self.rect(), Qt.AlignCenter, text)
        
        # Add painter.end() to properly close the painter
        painter.end()
