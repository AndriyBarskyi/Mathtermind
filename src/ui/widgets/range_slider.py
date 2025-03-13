from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal, QRect, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen


class QRangeSlider(QWidget):
    """Custom range slider with two handles."""
    
    valueChanged = pyqtSignal(int, int)  # Emitted when either value changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.min_value = 2013
        self.max_value = 2020
        self.current_min = self.min_value
        self.current_max = self.max_value
        
        self.handle_radius = 9
        self.pressed_handle = None
        self.hover_handle = None
        self.setMinimumHeight(40)
        
        # Colors - updated to blue theme
        self.track_color = QColor("#E5E7EB")
        self.active_track_color = QColor("#566CD2")
        self.handle_color = QColor("#566CD2")
        self.handle_border_color = QColor("#566CD2")
        self.hover_handle_color = QColor("#4557B9")
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.position().x()
            left_handle_x = self._value_to_x(self.current_min)
            right_handle_x = self._value_to_x(self.current_max)
            
            # Check if click is on either handle
            if abs(x - left_handle_x) <= self.handle_radius:
                self.pressed_handle = "left"
            elif abs(x - right_handle_x) <= self.handle_radius:
                self.pressed_handle = "right"
            else:
                # Move closest handle to click position
                if abs(x - left_handle_x) < abs(x - right_handle_x):
                    self.pressed_handle = "left"
                else:
                    self.pressed_handle = "right"
                self._update_value(x)
    
    def mouseMoveEvent(self, event):
        if self.pressed_handle:
            self._update_value(event.position().x())
        else:
            # Update hover state
            x = event.position().x()
            left_handle_x = self._value_to_x(self.current_min)
            right_handle_x = self._value_to_x(self.current_max)
            
            if abs(x - left_handle_x) <= self.handle_radius:
                self.hover_handle = "left"
            elif abs(x - right_handle_x) <= self.handle_radius:
                self.hover_handle = "right"
            else:
                self.hover_handle = None
            self.update()
    
    def mouseReleaseEvent(self, event):
        self.pressed_handle = None
        self.update()
    
    def leaveEvent(self, event):
        self.hover_handle = None
        self.update()
    
    def _update_value(self, x):
        value = self._x_to_value(x)
        if self.pressed_handle == "left":
            self.current_min = max(self.min_value, min(value, self.current_max - 1))
        else:
            self.current_max = min(self.max_value, max(value, self.current_min + 1))
        self.valueChanged.emit(self.current_min, self.current_max)
        self.update()
    
    def _value_to_x(self, value):
        """Convert slider value to x coordinate"""
        width = self.width() - 2 * self.handle_radius
        scale = (value - self.min_value) / (self.max_value - self.min_value)
        return self.handle_radius + scale * width
    
    def _x_to_value(self, x):
        """Convert x coordinate to slider value"""
        width = self.width() - 2 * self.handle_radius
        scale = (x - self.handle_radius) / width
        value = self.min_value + scale * (self.max_value - self.min_value)
        return round(max(self.min_value, min(self.max_value, value)))
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw track
        track_y = self.height() // 2
        track_height = 4
        
        # Background track
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.track_color)
        painter.drawRoundedRect(
            int(self.handle_radius),
            int(track_y - track_height // 2),
            int(self.width() - 2 * self.handle_radius),
            int(track_height),
            2,
            2
        )
        
        # Active track
        left_x = self._value_to_x(self.current_min)
        right_x = self._value_to_x(self.current_max)
        painter.setBrush(self.active_track_color)
        painter.drawRoundedRect(
            int(left_x),
            int(track_y - track_height // 2),
            int(right_x - left_x),
            int(track_height),
            2,
            2
        )
        
        # Draw handles
        for handle, x in [("left", left_x), ("right", right_x)]:
            if handle == self.hover_handle or handle == self.pressed_handle:
                painter.setBrush(self.hover_handle_color)
            else:
                painter.setBrush(self.handle_color)
            
            painter.setPen(QPen(self.handle_border_color, 2))
            painter.drawEllipse(
                QRect(
                    int(x - self.handle_radius),
                    int(track_y - self.handle_radius),
                    int(2 * self.handle_radius),
                    int(2 * self.handle_radius)
                )
            ) 