import unittest
from unittest.mock import patch, MagicMock
import uuid
from datetime import datetime, timezone

from src.services.course_service import CourseService
from src.db.models import Course as DBCourse


class TestCourseService(unittest.TestCase):
    """Unit tests for the CourseService class."""

    def setUp(self):
        """Set up test environment before each test."""
        self.course_service = CourseService()
        
        # Create mock course data
        self.mock_courses = [
            self._create_mock_course(
                id=uuid.uuid4(),
                name="Introduction to Python",
                description="Learn the basics of Python programming",
                topic="Informatics",
                difficulty_level="Beginner",
                estimated_duration=120,
                prerequisites=["Basic computer skills"]
            ),
            self._create_mock_course(
                id=uuid.uuid4(),
                name="Advanced Algebra",
                description="Explore advanced algebraic concepts",
                topic="Math",
                difficulty_level="Intermediate",
                estimated_duration=180,
                prerequisites=["Basic Algebra"]
            ),
            self._create_mock_course(
                id=uuid.uuid4(),
                name="Data Structures",
                description="Learn about common data structures",
                topic="Informatics",
                difficulty_level="Advanced",
                estimated_duration=240,
                prerequisites=["Introduction to Programming", "Basic Algorithms"]
            )
        ]

    def _create_mock_course(self, id, name, description, topic, difficulty_level, estimated_duration, prerequisites):
        """Helper method to create a mock course object."""
        mock_course = MagicMock(spec=DBCourse)
        mock_course.id = id
        mock_course.name = name
        mock_course.description = description
        mock_course.topic = topic
        mock_course.difficulty_level = difficulty_level
        mock_course.estimated_time = estimated_duration
        mock_course.prerequisites = prerequisites
        mock_course.created_at = datetime.now(timezone.utc)
        mock_course.updated_at = datetime.now(timezone.utc)
        return mock_course

    @patch('src.services.course_service.course_repo.get_all_courses')
    @patch('src.services.course_service.get_db')
    def test_get_all_courses_success(self, mock_get_db, mock_get_all_courses):
        """Test getting all courses successfully."""
        # Set up mocks
        mock_db = MagicMock()
        mock_get_db.return_value.__next__.return_value = mock_db
        mock_get_all_courses.return_value = self.mock_courses
        
        # Call the method
        result = self.course_service.get_all_courses()
        
        # Verify the result
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].name, "Introduction to Python")
        self.assertEqual(result[1].name, "Advanced Algebra")
        self.assertEqual(result[2].name, "Data Structures")
        
        # Verify the mocks were called correctly
        mock_get_db.return_value.__next__.assert_called_once()
        mock_get_all_courses.assert_called_once_with(mock_db)
        mock_db.close.assert_called_once()

    @patch('src.services.course_service.course_repo.get_all_courses')
    @patch('src.services.course_service.get_db')
    def test_get_all_courses_empty(self, mock_get_db, mock_get_all_courses):
        """Test getting all courses when there are no courses."""
        # Set up mocks
        mock_db = MagicMock()
        mock_get_db.return_value.__next__.return_value = mock_db
        mock_get_all_courses.return_value = []
        
        # Call the method
        result = self.course_service.get_all_courses()
        
        # Verify the result
        self.assertEqual(len(result), 0)
        
        # Verify the mocks were called correctly
        mock_get_db.return_value.__next__.assert_called_once()
        mock_get_all_courses.assert_called_once_with(mock_db)
        mock_db.close.assert_called_once()

    @patch('src.services.course_service.course_repo.get_all_courses')
    @patch('src.services.course_service.get_db')
    def test_get_all_courses_exception(self, mock_get_db, mock_get_all_courses):
        """Test getting all courses when an exception occurs."""
        # Set up mocks
        mock_db = MagicMock()
        mock_get_db.return_value.__next__.return_value = mock_db
        mock_get_all_courses.side_effect = Exception("Database error")
        
        # Call the method
        result = self.course_service.get_all_courses()
        
        # Verify the result
        self.assertEqual(len(result), 0)
        
        # Verify the mocks were called correctly
        mock_get_db.return_value.__next__.assert_called_once()
        mock_get_all_courses.assert_called_once_with(mock_db)
        # Note: db.close() might not be called if an exception occurs, depending on the implementation
