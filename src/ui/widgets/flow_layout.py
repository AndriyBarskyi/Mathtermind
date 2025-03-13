from PyQt5.QtWidgets import QLayout, QSizePolicy, QLayoutItem, QWidget
from PyQt5.QtCore import Qt, QSize, QRect, QPoint

class FlowLayout(QLayout):
    """
    Custom layout that arranges widgets in a flow, similar to how text
    wraps in a paragraph. Widgets are arranged from left to right and
    wrap to the next line when they reach the right edge of the layout.
    """
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)
        self._items = []
        
    def __del__(self):
        """Clean up items when layout is deleted"""
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)
            
    def addItem(self, item):
        """Add an item to the layout"""
        self._items.append(item)
        
    def count(self):
        """Return the number of items in the layout"""
        return len(self._items)
        
    def itemAt(self, index):
        """Return the item at the given index"""
        if 0 <= index < len(self._items):
            return self._items[index]
        return None
        
    def takeAt(self, index):
        """Remove and return the item at the given index"""
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None
        
    def clear(self):
        """Remove all items from the layout"""
        while self._items:
            item = self.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
    def expandingDirections(self):
        """Return the expanding directions of the layout"""
        return Qt.Horizontal | Qt.Vertical
        
    def hasHeightForWidth(self):
        """Return whether the layout's preferred height depends on its width"""
        return True
        
    def heightForWidth(self, width):
        """Return the preferred height for the given width"""
        return self._doLayout(QRect(0, 0, width, 0), True)
        
    def setGeometry(self, rect):
        """Set the geometry of the layout"""
        super().setGeometry(rect)
        self._doLayout(rect, False)
        
    def sizeHint(self):
        """Return the preferred size of the layout"""
        return self.minimumSize()
        
    def minimumSize(self):
        """Return the minimum size of the layout"""
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
            
        margin = self.contentsMargins()
        size += QSize(margin.left() + margin.right(), margin.top() + margin.bottom())
        return size
        
    def _doLayout(self, rect, testOnly):
        """
        Arrange items in the layout
        
        Args:
            rect: The rectangle to arrange items in
            testOnly: If True, only calculate the height, don't actually move widgets
            
        Returns:
            The height required for the layout
        """
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
                # Wrap to next line
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0
                
            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
                
            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())
            
        return y + lineHeight - rect.y() 