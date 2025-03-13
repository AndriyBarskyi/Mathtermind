#!/usr/bin/env python3
"""
Simplified test suite for the search functionality in the Mathtermind application.
This test suite focuses on the core search functionality in the CourseService class.
"""

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
import uuid
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ui.services.course_service import CourseService
from src.ui.models.course import Course


class TestSearchFunctionality(unittest.TestCase):
    """Test cases for the search functionality in the CourseService class"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create a mock database session
        self.mock_db = MagicMock()
        
        # Create a patcher for the get_db function
        self.get_db_patcher = patch('src.ui.services.course_service.get_db')
        self.mock_get_db = self.get_db_patcher.start()
        self.mock_get_db.return_value.__next__.return_value = self.mock_db
        
        # Create the CourseService instance with the mocked database
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
    
    def test_search_by_name(self):
        """Test searching courses by name"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Search for courses with "машинного" in the name
        result = self.course_service.filter_courses(search_text="машинного")
        
        # Assert that only the course with "машинного" in the name is returned
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Вступ до машинного навчання")
    
    def test_search_by_description(self):
        """Test searching courses by description"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Search for courses with "нейронних" in the description
        result = self.course_service.filter_courses(search_text="нейронних")
        
        # Assert that only the course with "нейронних" in the description is returned
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Глибоке навчання")
    
    def test_search_by_tags(self):
        """Test searching courses by tags"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Search for courses with "linear" in the tags
        result = self.course_service.filter_courses(search_text="linear")
        
        # Assert that only the course with "Linear Algebra" in tags is returned
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Лінійна алгебра")
    
    def test_search_case_insensitive(self):
        """Test that search is case-insensitive"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Search for courses with "МАШИННОГО" in uppercase
        result = self.course_service.filter_courses(search_text="МАШИННОГО")
        
        # Assert that the course is found despite case difference
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Вступ до машинного навчання")
    
    def test_search_with_whitespace(self):
        """Test that search text is properly trimmed"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Search for courses with whitespace around the search term
        result = self.course_service.filter_courses(search_text="  машинного  ")
        
        # Assert that the course is found despite whitespace
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Вступ до машинного навчання")
    
    def test_search_empty_text(self):
        """Test that empty search text returns all courses"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Search with empty text
        result = self.course_service.filter_courses(search_text="")
        
        # Assert that all courses are returned
        self.assertEqual(len(result), 3)
    
    def test_search_no_matches(self):
        """Test that search with no matches returns empty list"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Search for a term that doesn't exist in any course
        result = self.course_service.filter_courses(search_text="nonexistent")
        
        # Assert that no courses are returned
        self.assertEqual(len(result), 0)
    
    def test_search_with_filters(self):
        """Test that search works with other filters"""
        # Mock the get_all_courses method to return sample courses
        self.course_service.get_all_courses = MagicMock(return_value=self.sample_courses)
        
        # Search for "навчання" in Informatics courses with Advanced difficulty
        result = self.course_service.filter_courses(
            search_text="навчання",
            subjects=["Informatics"],
            levels=["Advanced"]
        )
        
        # Assert that only the matching course is returned
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Глибоке навчання")
        self.assertEqual(result[0].topic, "Informatics")
        self.assertEqual(result[0].metadata.get("difficulty_level"), "Advanced")
    
    def test_search_handles_exception(self):
        """Test that search handles exceptions gracefully"""
        # Mock the get_all_courses method to raise an exception
        self.course_service.get_all_courses = MagicMock(side_effect=Exception("Test exception"))
        
        # Search should handle the exception and return an empty list
        result = self.course_service.filter_courses(search_text="test")
        
        # Assert that an empty list is returned
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main() 