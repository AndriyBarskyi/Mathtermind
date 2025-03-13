import unittest
from unittest.mock import MagicMock, patch
import sys
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication

from src.ui.widgets.search_bar import SearchBar


# Create a QApplication instance for testing
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)


class TestSearchBar(unittest.TestCase):
    """Test cases for the SearchBar widget"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create a SearchBar instance
        self.search_bar = SearchBar()
        
        # Create a mock for the search_changed signal
        self.search_changed_mock = MagicMock()
        self.search_bar.search_changed.connect(self.search_changed_mock)
        
        # Create a mock for the filter_button_clicked signal
        self.filter_button_clicked_mock = MagicMock()
        self.search_bar.filter_button_clicked.connect(self.filter_button_clicked_mock)
        
        # Patch the QTimer to make tests faster
        self.timer_patcher = patch.object(QTimer, 'start')
        self.mock_timer_start = self.timer_patcher.start()
        
    def tearDown(self):
        """Clean up after each test method"""
        self.timer_patcher.stop()
        self.search_bar.deleteLater()
    
    def test_initial_state(self):
        """Test the initial state of the SearchBar"""
        # Assert that the search input is empty
        self.assertEqual(self.search_bar.get_search_text(), "")
        
        # Assert that the search input has the correct placeholder text
        self.assertEqual(self.search_bar.search_input.placeholderText(), "Пошук")
    
    def test_search_text_changed(self):
        """Test that typing in the search input emits the search_changed signal after a delay"""
        # Type text in the search input
        QTest.keyClicks(self.search_bar.search_input, "test")
        
        # Assert that the timer was started with the correct delay
        self.mock_timer_start.assert_called_with(SearchBar.SEARCH_DELAY)
        
        # Assert that the search_changed signal was not emitted yet (due to the delay)
        self.search_changed_mock.assert_not_called()
        
        # Manually trigger the timeout to simulate the delay
        self.search_bar._emit_search_text()
        
        # Assert that the search_changed signal was emitted with the correct text
        self.search_changed_mock.assert_called_with("test")
    
    def test_filter_button_clicked(self):
        """Test that clicking the filter button emits the filter_button_clicked signal"""
        # Click the filter button
        QTest.mouseClick(self.search_bar.filter_btn, Qt.MouseButton.LeftButton)
        
        # Assert that the filter_button_clicked signal was emitted
        self.filter_button_clicked_mock.assert_called_once()
    
    def test_clear_search(self):
        """Test that clearing the search input works correctly"""
        # Type text in the search input
        QTest.keyClicks(self.search_bar.search_input, "test")
        
        # Clear the search input
        self.search_bar.clear_search()
        
        # Assert that the search input is empty
        self.assertEqual(self.search_bar.get_search_text(), "")
        
        # Assert that the search_changed signal was emitted with an empty string
        self.search_changed_mock.assert_called_with("")
    
    def test_update_filter_button_state(self):
        """Test that updating the filter button state changes its style"""
        # Get the initial style
        initial_style = self.search_bar.filter_btn.styleSheet()
        
        # Update the filter button state to active
        self.search_bar.update_filter_button_state(True)
        
        # Assert that the style has changed
        self.assertNotEqual(self.search_bar.filter_btn.styleSheet(), initial_style)
        
        # Update the filter button state to inactive
        self.search_bar.update_filter_button_state(False)
        
        # Assert that the style has been reset
        self.assertEqual(self.search_bar.filter_btn.styleSheet(), initial_style)


if __name__ == '__main__':
    unittest.main() 