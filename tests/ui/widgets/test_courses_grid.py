import unittest
from unittest.mock import MagicMock, patch
import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QResizeEvent

from src.ui.widgets.courses_grid import CoursesGrid
from src.ui.models.course import Course
from datetime import datetime, timezone
import uuid


# Create a QApplication instance for testing
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)


class TestCoursesGrid(unittest.TestCase):
    """Test cases for the CoursesGrid widget"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create sample courses for testing
        self.sample_courses = [
            Course(
                id=str(uuid.uuid4()),
                topic="Informatics",
                name="Вступ до машинного навчання",
                description="Цей курс надає базові знання з машинного навчання.",
                metadata={
                    "difficulty_level": "Beginner",
                    "tags": ["ML", "AI", "Python"]
                },
                created_at=datetime(2023, 1, 1, tzinfo=timezone.utc)
            ),
            Course(
                id=str(uuid.uuid4()),
                topic="Math",
                name="Лінійна алгебра",
                description="Основи лінійної алгебри для програмістів.",
                metadata={
                    "difficulty_level": "Intermediate",
                    "tags": ["Math", "Linear Algebra"]
                },
                created_at=datetime(2022, 6, 1, tzinfo=timezone.utc)
            ),
        ]
        
        # Create a CoursesGrid instance
        self.courses_grid = CoursesGrid()
        
        # Create a mock for the course_started signal
        self.course_started_mock = MagicMock()
        self.courses_grid.course_started.connect(self.course_started_mock)
        
        # Patch the QTimer to make tests faster
        self.timer_patcher = patch('src.ui.widgets.courses_grid.QTimer')
        self.mock_timer = self.timer_patcher.start()
        
        # Create a mock timer instance
        self.mock_timer_instance = MagicMock()
        self.mock_timer.return_value = self.mock_timer_instance
        
        # Replace the refresh timer with our mock
        self.courses_grid.refresh_timer = self.mock_timer_instance
        
    def tearDown(self):
        """Clean up after each test method"""
        self.timer_patcher.stop()
        self.courses_grid.deleteLater()
    
    def test_initial_state(self):
        """Test the initial state of the CoursesGrid"""
        # Assert that the courses list is empty
        self.assertEqual(self.courses_grid.courses, [])
        
        # Assert that the no results label is hidden
        self.assertFalse(self.courses_grid.no_results_label.isVisible())
    
    def test_set_courses(self):
        """Test setting courses in the grid"""
        # Set courses
        self.courses_grid.set_courses(self.sample_courses)
        
        # Assert that the courses were set
        self.assertEqual(self.courses_grid.courses, self.sample_courses)
        
        # Assert that the refresh timer was started
        self.mock_timer_instance.start.assert_called_once()
    
    def test_show_no_results_message(self):
        """Test showing the no results message"""
        # Make the no_results_label visible property return True when called
        original_is_visible = self.courses_grid.no_results_label.isVisible
        self.courses_grid.no_results_label.isVisible = MagicMock(return_value=True)
        self.courses_grid.no_results_label.show = MagicMock()
        
        # Show the no results message
        self.courses_grid.show_no_results_message("Test message")
        
        # Assert that the message was set and show was called
        self.assertEqual(self.courses_grid.no_results_label.text(), "Test message")
        self.courses_grid.no_results_label.show.assert_called_once()
        
        # Restore the original isVisible method
        self.courses_grid.no_results_label.isVisible = original_is_visible
    
    def test_hide_no_results_message(self):
        """Test hiding the no results message"""
        # Mock the hide method
        self.courses_grid.no_results_label.hide = MagicMock()
        
        # Call hide_no_results_message
        self.courses_grid.hide_no_results_message()
        
        # Assert that hide was called
        self.courses_grid.no_results_label.hide.assert_called_once()
    
    def test_refresh_grid_with_courses(self):
        """Test refreshing the grid with courses"""
        # Set courses
        self.courses_grid.set_courses(self.sample_courses)
        
        # Manually call refresh grid
        self.courses_grid._refresh_grid()
        
        # Assert that the flow layout has items
        self.assertGreater(self.courses_grid.flow_layout.count(), 0)
        
        # Assert that the no results label is hidden
        self.assertFalse(self.courses_grid.no_results_label.isVisible())
    
    def test_refresh_grid_with_no_courses(self):
        """Test refreshing the grid with no courses"""
        # Set empty courses list
        self.courses_grid.set_courses([])
        
        # Mock the show_no_results_message method
        self.courses_grid.show_no_results_message = MagicMock()
        
        # Manually call refresh grid
        self.courses_grid._refresh_grid()
        
        # Assert that show_no_results_message was called
        self.courses_grid.show_no_results_message.assert_called_once()
    
    def test_clear_grid(self):
        """Test clearing the grid"""
        # First set some courses
        self.courses_grid.set_courses(self.sample_courses)
        self.courses_grid._refresh_grid()
        
        # Then clear the grid
        self.courses_grid._clear_grid()
        
        # Assert that the flow layout is empty
        self.assertEqual(self.courses_grid.flow_layout.count(), 0)
    
    def test_resize_event(self):
        """Test that resize events trigger a delayed refresh"""
        # Create a proper QResizeEvent
        old_size = QSize(100, 100)
        new_size = QSize(200, 200)
        resize_event = QResizeEvent(new_size, old_size)
        
        # Trigger a resize event
        self.courses_grid.resizeEvent(resize_event)
        
        # Assert that the refresh timer was started
        self.mock_timer_instance.start.assert_called_with(150)


if __name__ == '__main__':
    unittest.main() 