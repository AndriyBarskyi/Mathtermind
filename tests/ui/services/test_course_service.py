import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
import uuid

from src.ui.services.course_service import CourseService
from src.ui.models.course import Course


class TestCourseService(unittest.TestCase):
    """Test cases for the CourseService class"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create a mock database session
        self.mock_db = MagicMock()
        
        # Create a patcher for the get_db function
        self.get_db_patcher = patch('src.ui.services.course_service.get_db')
        self.mock_get_db = self.get_db_patcher.start()
        self.mock_get_db.return_value.__next__.return_value = self.mock_db
        
        # Create the CourseService instance
        self.course_service = CourseService()
        
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
        
    def tearDown(self):
        """Clean up after each test method"""
        self.get_db_patcher.stop()
    
    def test_filter_courses_by_search_text_in_name(self):
        """Test filtering courses by search text in name"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Filter courses by search text in name
        filtered_courses = self.course_service.filter_courses(search_text="машинного")
        
        # Assert that only the course with "машинного" in the name is returned
        self.assertEqual(len(filtered_courses), 1)
        self.assertEqual(filtered_courses[0].name, "Вступ до машинного навчання")
    
    def test_filter_courses_by_search_text_in_description(self):
        """Test filtering courses by search text in description"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Filter courses by search text in description
        filtered_courses = self.course_service.filter_courses(search_text="нейронних")
        
        # Assert that only the course with "нейронних" in the description is returned
        self.assertEqual(len(filtered_courses), 1)
        self.assertEqual(filtered_courses[0].name, "Глибоке навчання")
    
    def test_filter_courses_by_search_text_in_tags(self):
        """Test filtering courses by search text in tags"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Filter courses by search text in tags
        filtered_courses = self.course_service.filter_courses(search_text="linear")
        
        # Assert that only the course with "Linear Algebra" in tags is returned
        self.assertEqual(len(filtered_courses), 1)
        self.assertEqual(filtered_courses[0].name, "Лінійна алгебра")
    
    def test_filter_courses_by_search_text_case_insensitive(self):
        """Test that search text filtering is case-insensitive"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Filter courses by search text with different case
        filtered_courses = self.course_service.filter_courses(search_text="МАШИННОГО")
        
        # Assert that the course is found despite case difference
        self.assertEqual(len(filtered_courses), 1)
        self.assertEqual(filtered_courses[0].name, "Вступ до машинного навчання")
    
    def test_filter_courses_by_search_text_with_whitespace(self):
        """Test that search text is properly trimmed"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Filter courses by search text with whitespace
        filtered_courses = self.course_service.filter_courses(search_text="  машинного  ")
        
        # Assert that the course is found despite whitespace
        self.assertEqual(len(filtered_courses), 1)
        self.assertEqual(filtered_courses[0].name, "Вступ до машинного навчання")
    
    def test_filter_courses_by_empty_search_text(self):
        """Test that empty search text returns all courses"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Filter courses by empty search text
        filtered_courses = self.course_service.filter_courses(search_text="")
        
        # Assert that all courses are returned
        self.assertEqual(len(filtered_courses), 3)
    
    def test_filter_courses_by_whitespace_search_text(self):
        """Test that whitespace-only search text returns all courses"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Filter courses by whitespace-only search text
        filtered_courses = self.course_service.filter_courses(search_text="   ")
        
        # Assert that all courses are returned
        self.assertEqual(len(filtered_courses), 3)
    
    def test_filter_courses_by_subject(self):
        """Test filtering courses by subject"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Filter courses by subject
        filtered_courses = self.course_service.filter_courses(subjects=["Math"])
        
        # Assert that only Math courses are returned
        self.assertEqual(len(filtered_courses), 1)
        self.assertEqual(filtered_courses[0].topic, "Math")
    
    def test_filter_courses_by_multiple_subjects(self):
        """Test filtering courses by multiple subjects"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Filter courses by multiple subjects
        filtered_courses = self.course_service.filter_courses(subjects=["Math", "Informatics"])
        
        # Assert that all courses are returned
        self.assertEqual(len(filtered_courses), 3)
    
    def test_filter_courses_by_level(self):
        """Test filtering courses by difficulty level"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Filter courses by difficulty level
        filtered_courses = self.course_service.filter_courses(levels=["Advanced"])
        
        # Assert that only Advanced courses are returned
        self.assertEqual(len(filtered_courses), 1)
        self.assertEqual(filtered_courses[0].metadata.get("difficulty_level"), "Advanced")
    
    def test_filter_courses_by_multiple_levels(self):
        """Test filtering courses by multiple difficulty levels"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Filter courses by multiple difficulty levels
        filtered_courses = self.course_service.filter_courses(levels=["Beginner", "Advanced"])
        
        # Assert that only Beginner and Advanced courses are returned
        self.assertEqual(len(filtered_courses), 2)
        self.assertIn(filtered_courses[0].metadata.get("difficulty_level"), ["Beginner", "Advanced"])
        self.assertIn(filtered_courses[1].metadata.get("difficulty_level"), ["Beginner", "Advanced"])
    
    def test_filter_courses_by_year_range(self):
        """Test filtering courses by year range"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Filter courses by year range
        filtered_courses = self.course_service.filter_courses(year_range=(2023, 2023))
        
        # Assert that only courses from 2023 are returned
        self.assertEqual(len(filtered_courses), 2)
        for course in filtered_courses:
            self.assertEqual(course.created_at.year, 2023)
    
    def test_filter_courses_by_multiple_criteria(self):
        """Test filtering courses by multiple criteria"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Filter courses by multiple criteria
        filtered_courses = self.course_service.filter_courses(
            search_text="навчання",
            subjects=["Informatics"],
            levels=["Advanced"],
            year_range=(2023, 2023)
        )
        
        # Assert that only the course matching all criteria is returned
        self.assertEqual(len(filtered_courses), 1)
        self.assertEqual(filtered_courses[0].name, "Глибоке навчання")
        self.assertEqual(filtered_courses[0].topic, "Informatics")
        self.assertEqual(filtered_courses[0].metadata.get("difficulty_level"), "Advanced")
        self.assertEqual(filtered_courses[0].created_at.year, 2023)
    
    def test_filter_courses_with_no_matches(self):
        """Test filtering courses with no matches"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Filter courses with criteria that don't match any course
        filtered_courses = self.course_service.filter_courses(search_text="nonexistent")
        
        # Assert that no courses are returned
        self.assertEqual(len(filtered_courses), 0)
    
    def test_filter_courses_with_active_status(self):
        """Test filtering courses with active status"""
        # Create a mock for get_active_courses
        active_courses = [self.sample_courses[0]]  # Only the first course is active
        self.course_service.get_active_courses = MagicMock(return_value=active_courses)
        
        # Filter active courses
        filtered_courses = self.course_service.filter_courses(status="active")
        
        # Assert that only active courses are returned
        self.assertEqual(len(filtered_courses), 1)
        self.assertEqual(filtered_courses[0].name, "Вступ до машинного навчання")
    
    def test_filter_courses_with_completed_status(self):
        """Test filtering courses with completed status"""
        # Create a mock for get_completed_courses
        completed_courses = [self.sample_courses[1]]  # Only the second course is completed
        self.course_service.get_completed_courses = MagicMock(return_value=completed_courses)
        
        # Filter completed courses
        filtered_courses = self.course_service.filter_courses(status="completed")
        
        # Assert that only completed courses are returned
        self.assertEqual(len(filtered_courses), 1)
        self.assertEqual(filtered_courses[0].name, "Лінійна алгебра")
    
    def test_filter_courses_handles_exception(self):
        """Test that filter_courses handles exceptions gracefully"""
        # Mock the get_all_courses method to raise an exception
        self.course_service.get_all_courses = MagicMock(side_effect=Exception("Test exception"))
        
        # Filter courses should handle the exception and return an empty list
        filtered_courses = self.course_service.filter_courses(search_text="test")
        
        # Assert that an empty list is returned
        self.assertEqual(filtered_courses, [])


if __name__ == '__main__':
    unittest.main() 