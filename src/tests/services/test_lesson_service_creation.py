"""
Test module for the lesson creation and modification functionality in LessonService.

This module contains tests for the lesson creation, modification, sequencing, and 
prerequisite management functions of the LessonService.
"""

import unittest
from unittest.mock import MagicMock, patch
import uuid
from datetime import datetime, timezone
import contextlib
from unittest import TestCase

from src.services.lesson_service import LessonService
from src.db.repositories import lesson_repo
from src.db.models.enums import LessonType, DifficultyLevel
from src.models.lesson import Lesson
from src.core.error_handling.exceptions import ValidationError, ResourceNotFoundError

class TestLessonServiceCreation(unittest.TestCase):
    """Test cases for lesson service creation functionality."""

    def setUp(self):
        """Set up test resources."""
        # Create mock database session
        self.mock_db = MagicMock()
        
        # Create the lesson service instance
        self.lesson_service = LessonService()
        
        # Create sample lesson for testing
        self.lesson_id = str(uuid.uuid4())
        
        # Create Sample lesson
        self.sample_lesson = Lesson(
            id=uuid.UUID(self.lesson_id),
            title="Test Lesson",
            lesson_type=LessonType.THEORY,
            difficulty_level=DifficultyLevel.BEGINNER,
            estimated_time=30,
            points_reward=10,
            lesson_order=1,
            prerequisites=["Basic Math"],
            learning_objectives=["Learn Something"],
            content={"blocks": []},
            course_id=uuid.uuid4()  # Added course_id
        )
        
        # Create a mock lesson as it would be stored in the database
        self.db_lesson = MagicMock()
        self.db_lesson.id = uuid.UUID(self.lesson_id)
        self.db_lesson.title = "Test Lesson"
        self.db_lesson.lesson_type = LessonType.THEORY
        self.db_lesson.difficulty_level = DifficultyLevel.BEGINNER
        self.db_lesson.estimated_time = 30
        self.db_lesson.points_reward = 10
        self.db_lesson.lesson_order = 1
        self.db_lesson.prerequisites = ["Basic Math"]
        self.db_lesson.learning_objectives = ["Learn Something"]
        self.db_lesson.content = {"blocks": []}
        self.db_lesson.course_id = uuid.uuid4()  # Added course_id
        
        # Create a mock transaction context manager
        self.mock_transaction_context = MagicMock()
        self.mock_transaction_context.__enter__ = MagicMock(return_value=self.mock_db)
        self.mock_transaction_context.__exit__ = MagicMock(return_value=None)
        
        # Mock the transaction method in LessonService
        self.lesson_service.transaction = MagicMock(return_value=self.mock_transaction_context)
    
    def test_create_lesson(self):
        """Test creating a new lesson."""
        # Setup
        lesson_data = {
            "title": "New Lesson",
            "lesson_type": "THEORY",
            "course_id": str(uuid.uuid4()),
            "difficulty_level": "BEGINNER",
            "estimated_time": 30,
            "points_reward": 10,
            "lesson_order": 1,
            "prerequisites": ["Basic Math"],
            "learning_objectives": ["Learn Something"],
            "content": {"blocks": []}
        }
        
        # Mock repository method
        with patch.object(lesson_repo, 'create_lesson') as mock_create:
            # Create a mock lesson with the same title as in lesson_data
            mock_db_lesson = MagicMock()
            mock_db_lesson.id = self.db_lesson.id
            mock_db_lesson.title = "New Lesson"  # Match the title in lesson_data
            mock_db_lesson.lesson_type = LessonType.THEORY
            mock_db_lesson.difficulty_level = DifficultyLevel.BEGINNER
            mock_db_lesson.course_id = self.db_lesson.course_id
            mock_db_lesson.lesson_order = 1
            mock_db_lesson.estimated_time = 30
            mock_db_lesson.points_reward = 10
            mock_db_lesson.prerequisites = ["Basic Math"]
            mock_db_lesson.learning_objectives = ["Learn Something"]
            mock_db_lesson.content = {"blocks": []}
            
            mock_create.return_value = mock_db_lesson
            
            # Call the method
            result = self.lesson_service.create_lesson(**lesson_data)
            
            # Assertions
            self.assertEqual(str(result.id), str(self.sample_lesson.id))
            self.assertEqual(result.title, lesson_data["title"])
            
            # Verify the method was called with correct parameters
            mock_create.assert_called_once()
    
    def test_create_lesson_validation_error(self):
        """Test validation error when creating a lesson with invalid data."""
        # Setup
        lesson_data = {
            "title": "",  # Empty title
            "lesson_type": "THEORY",
            "difficulty_level": "BEGINNER",
            "lesson_order": 1,
            "estimated_time": 30,
            "points_reward": 10
        }
        
        # Test
        with self.assertRaises(ValidationError):
            self.lesson_service.create_lesson(
                course_id=self.sample_lesson.course_id,
                **lesson_data
            )
    
    def test_update_lesson(self):
        """Test updating an existing lesson."""
        # Setup
        update_data = {
            "title": "Updated Lesson",
            "difficulty_level": "INTERMEDIATE",
            "estimated_time": 45
        }
        
        # Mock repository methods
        with patch.object(lesson_repo, 'get_lesson') as mock_get, \
             patch.object(lesson_repo, 'update_lesson') as mock_update:
            mock_get.return_value = self.db_lesson
            updated_lesson = MagicMock()
            updated_lesson.id = uuid.UUID(self.lesson_id)
            updated_lesson.title = "Updated Lesson"
            updated_lesson.difficulty_level = DifficultyLevel.INTERMEDIATE
            updated_lesson.estimated_time = 45
            updated_lesson.lesson_type = self.db_lesson.lesson_type
            updated_lesson.lesson_order = self.db_lesson.lesson_order
            updated_lesson.points_reward = self.db_lesson.points_reward
            updated_lesson.prerequisites = self.db_lesson.prerequisites
            updated_lesson.learning_objectives = self.db_lesson.learning_objectives
            mock_update.return_value = updated_lesson
            
            # Call the method
            result = self.lesson_service.update_lesson(
                lesson_id=self.lesson_id,
                **update_data
            )
            
            # Assertions
            self.assertEqual(str(result.id), str(self.sample_lesson.id))
            self.assertEqual(result.title, "Updated Lesson")
            # Expecting Ukrainian translation due to the enum value
            self.assertEqual(result.difficulty_level, DifficultyLevel.INTERMEDIATE.value)
            self.assertEqual(result.estimated_time, 45)
            mock_update.assert_called_once()
    
    def test_update_lesson_not_found(self):
        """Test updating a lesson that doesn't exist."""
        # Setup
        update_data = {
            "title": "Updated Lesson"
        }
        
        # Mock repository method
        with patch.object(lesson_repo, 'get_lesson') as mock_get:
            mock_get.return_value = None
            
            # Test
            with self.assertRaises(ResourceNotFoundError):
                self.lesson_service.update_lesson(
                    lesson_id=self.lesson_id,
                    **update_data
                )
    
    def test_delete_lesson(self):
        """Test deleting a lesson."""
        # Mock repository methods
        with patch.object(lesson_repo, 'get_lesson') as mock_get, \
             patch.object(lesson_repo, 'delete_lesson') as mock_delete:
            mock_get.return_value = self.db_lesson
            mock_delete.return_value = self.db_lesson
            
            # Call the method
            result = self.lesson_service.delete_lesson(lesson_id=self.lesson_id)
            
            # Assertions
            self.assertTrue(result)
            mock_delete.assert_called_once()
    
    def test_update_lesson_order(self):
        """Test updating lesson order."""
        # Setup
        # Mock repository methods
        with patch.object(lesson_repo, 'get_lesson') as mock_get, \
             patch.object(lesson_repo, 'update_lesson_order') as mock_update_order:
            mock_get.return_value = self.db_lesson
            mock_update_order.return_value = True
            
            # Call the method
            result = self.lesson_service.update_lesson_order(
                lesson_id=self.lesson_id,
                new_order=2
            )
            
            # Assertions
            self.assertTrue(result)
            mock_update_order.assert_called_once()
    
    def test_validate_lesson_data(self):
        """Test validation of lesson data."""
        # Test valid data
        valid_data = {
            "title": "Valid Lesson",
            "lesson_type": "THEORY",
            "difficulty_level": "BEGINNER"
        }
        
        # This should not raise an exception
        LessonService._validate_lesson_data(**valid_data)
        
        # Test invalid title
        invalid_title_data = {
            "title": "",  # Empty title
            "lesson_type": "THEORY",
            "difficulty_level": "BEGINNER"
        }
        
        with self.assertRaises(ValidationError):
            LessonService._validate_lesson_data(**invalid_title_data)

if __name__ == '__main__':
    unittest.main() 