import unittest
from unittest.mock import MagicMock, patch
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication

from src.ui.pages.courses_page import CoursePage
from src.ui.models.course import Course
from datetime import datetime, timezone
import uuid


# Create a QApplication instance for testing
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)


class TestCoursePage(unittest.TestCase):
    """Test cases for the CoursePage class"""

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
            Course(
                id=str(uuid.uuid4()),
                topic="Informatics",
                name="Глибоке навчання",
                description="Поглиблений курс з нейронних мереж та глибокого навчання.",
                metadata={
                    "difficulty_level": "Advanced",
                    "tags": ["Deep Learning", "Neural Networks", "AI"]
                },
                created_at=datetime(2023, 3, 15, tzinfo=timezone.utc)
            ),
        ]
        
        # Create patchers for the services
        self.course_service_patcher = patch('src.ui.services.course_service.CourseService')
        self.lesson_service_patcher = patch('src.ui.services.lesson_service.LessonService')
        self.courses_grid_patcher = patch('src.ui.widgets.courses_grid.CoursesGrid')
        
        # Start the patchers
        self.mock_course_service_class = self.course_service_patcher.start()
        self.mock_lesson_service_class = self.lesson_service_patcher.start()
        self.mock_courses_grid_class = self.courses_grid_patcher.start()
        
        # Create mock instances
        self.mock_course_service = MagicMock()
        self.mock_lesson_service = MagicMock()
        self.mock_courses_grid = MagicMock()
        
        # Configure the mock classes to return the mock instances
        self.mock_course_service_class.return_value = self.mock_course_service
        self.mock_lesson_service_class.return_value = self.mock_lesson_service
        self.mock_courses_grid_class.return_value = self.mock_courses_grid
        
        # Configure the mock course service to return sample courses
        self.mock_course_service.get_all_courses.return_value = self.sample_courses
        self.mock_course_service.filter_courses.return_value = self.sample_courses
        
        # Create a CoursePage instance
        self.course_page = CoursePage()
        
        # Replace the courses_grid with our mock
        self.course_page.courses_grid = self.mock_courses_grid
        
    def tearDown(self):
        """Clean up after each test method"""
        self.course_service_patcher.stop()
        self.lesson_service_patcher.stop()
        self.courses_grid_patcher.stop()
        self.course_page.deleteLater()
    
    def test_initial_state(self):
        """Test the initial state of the CoursePage"""
        # Assert that the initial tab is "all"
        self.assertEqual(self.course_page.current_tab, "all")
        
        # Assert that the initial search text is empty
        self.assertEqual(self.course_page.search_text, "")
        
        # Assert that the initial filter state includes all options
        self.assertEqual(self.course_page.filter_state["subjects"], ["info", "math"])
        self.assertEqual(self.course_page.filter_state["levels"], ["basic", "intermediate", "advanced"])
        self.assertEqual(self.course_page.filter_state["year_range"], (2010, 2030))
        
        # Assert that the course service was called to get all courses
        self.mock_course_service.get_all_courses.assert_called_once()
    
    def test_search_text_changed(self):
        """Test that changing the search text updates the state and refreshes courses"""
        # Reset the mock to clear previous calls
        self.mock_course_service.filter_courses.reset_mock()
        
        # Simulate changing the search text
        self.course_page._on_search_text_changed("машинного")
        
        # Assert that the search text was updated
        self.assertEqual(self.course_page.search_text, "машинного")
        
        # Assert that filter_courses was called with the correct parameters
        self.mock_course_service.filter_courses.assert_called_with(
            status="all",
            search_text="машинного",
            subjects=["info", "math"],
            levels=["basic", "intermediate", "advanced"],
            year_range=(2010, 2030)
        )
        
        # Assert that the courses grid was updated
        self.mock_course_service.filter_courses.return_value = [self.sample_courses[0]]
        self.course_page._on_search_text_changed("машинного")
        self.mock_courses_grid.set_courses.assert_called_with([self.sample_courses[0]])
    
    def test_tab_changed(self):
        """Test that changing the tab updates the state and refreshes courses"""
        # Reset the mock to clear previous calls
        self.mock_course_service.filter_courses.reset_mock()
        
        # Simulate changing the tab
        self.course_page._on_tab_changed("active")
        
        # Assert that the tab was updated
        self.assertEqual(self.course_page.current_tab, "active")
        
        # Assert that filter_courses was called with the correct parameters
        self.mock_course_service.filter_courses.assert_called_with(
            status="active",
            search_text="",
            subjects=["info", "math"],
            levels=["basic", "intermediate", "advanced"],
            year_range=(2010, 2030)
        )
    
    def test_filters_applied(self):
        """Test that applying filters updates the state and refreshes courses"""
        # Reset the mock to clear previous calls
        self.mock_course_service.filter_courses.reset_mock()
        
        # Simulate applying filters
        new_filter_state = {
            "subjects": ["info"],
            "levels": ["advanced"],
            "year_range": (2023, 2023)
        }
        self.course_page._on_filters_applied(new_filter_state)
        
        # Assert that the filter state was updated
        self.assertEqual(self.course_page.filter_state, new_filter_state)
        
        # Assert that filter_courses was called with the correct parameters
        self.mock_course_service.filter_courses.assert_called_with(
            status="all",
            search_text="",
            subjects=["info"],
            levels=["advanced"],
            year_range=(2023, 2023)
        )
    
    def test_filters_cleared(self):
        """Test that clearing filters resets the state and refreshes courses"""
        # First, apply some filters
        new_filter_state = {
            "subjects": ["info"],
            "levels": ["advanced"],
            "year_range": (2023, 2023)
        }
        self.course_page._on_filters_applied(new_filter_state)
        
        # Reset the mock to clear previous calls
        self.mock_course_service.filter_courses.reset_mock()
        
        # Simulate clearing filters
        self.course_page._on_filters_cleared()
        
        # Assert that the filter state was reset
        self.assertEqual(self.course_page.filter_state, {
            "subjects": ["info", "math"],
            "levels": ["basic", "intermediate", "advanced"],
            "year_range": (2010, 2030)
        })
        
        # Assert that filter_courses was called with the correct parameters
        self.mock_course_service.filter_courses.assert_called_with(
            status="all",
            search_text="",
            subjects=["info", "math"],
            levels=["basic", "intermediate", "advanced"],
            year_range=(2010, 2030)
        )
    
    def test_combined_filters(self):
        """Test that combining search, tab, and filters works correctly"""
        # Reset the mock to clear previous calls
        self.mock_course_service.filter_courses.reset_mock()
        
        # Simulate changing the tab
        self.course_page._on_tab_changed("active")
        
        # Simulate changing the search text
        self.course_page._on_search_text_changed("машинного")
        
        # Simulate applying filters
        new_filter_state = {
            "subjects": ["info"],
            "levels": ["beginner"],
            "year_range": (2023, 2023)
        }
        self.course_page._on_filters_applied(new_filter_state)
        
        # Assert that filter_courses was called with the correct parameters
        self.mock_course_service.filter_courses.assert_called_with(
            status="active",
            search_text="машинного",
            subjects=["info"],
            levels=["beginner"],
            year_range=(2023, 2023)
        )
    
    def test_no_results_message(self):
        """Test that the no results message is shown when no courses match the filters"""
        # Configure the mock course service to return an empty list
        self.mock_course_service.filter_courses.return_value = []
        
        # Simulate changing the search text to something that won't match any courses
        self.course_page._on_search_text_changed("nonexistent")
        
        # Assert that the no results message was shown
        self.mock_courses_grid.show_no_results_message.assert_called_with(
            "Немає курсів, що відповідають пошуку: 'nonexistent'"
        )


if __name__ == '__main__':
    unittest.main() 