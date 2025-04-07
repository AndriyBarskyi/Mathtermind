"""
Test module for the lesson completion criteria management in LessonService.

This module contains tests for setting, getting, and evaluating completion criteria
for lessons in the LessonService.
"""

import unittest
from unittest.mock import MagicMock, patch
import uuid
from datetime import datetime, timezone

from src.services.lesson_service import LessonService
from src.db.models.enums import DifficultyLevel
from src.models.lesson import Lesson
from src.core.error_handling import ValidationError, ResourceNotFoundError

# Create a module level patch for lesson_repo
lesson_repo_mock = MagicMock()
lesson_repo_patch = patch('src.db.repositories.lesson_repo', lesson_repo_mock)

class TestLessonCompletion(unittest.TestCase):
    """Tests for the lesson completion criteria management functionality."""
    
    def setUp(self):
        """Set up the test environment."""
        # Start the module patch
        lesson_repo_patch.start()
        
        # Create an instance of LessonService
        self.lesson_service = LessonService()
        
        # Create a mock for the LessonRepository and assign it to the service
        self.lesson_service.lesson_repo = lesson_repo_mock
        
        # Mock the database session and repository methods
        self.mock_db = MagicMock()
        self.lesson_service.db = self.mock_db
        
        # Configure the transaction method to return a context manager
        # that yields the mock session
        transaction_cm = MagicMock()
        transaction_cm.__enter__ = MagicMock(return_value=self.mock_db)
        transaction_cm.__exit__ = MagicMock(return_value=None)
        self.lesson_service.transaction = MagicMock(return_value=transaction_cm)
        
        # Create sample data for tests
        self.course_id = str(uuid.uuid4())
        self.lesson_id = str(uuid.uuid4())
        self.user_id = str(uuid.uuid4())
        
        # Create mock DB lesson
        self.db_lesson = MagicMock()
        self.db_lesson.id = uuid.UUID(self.lesson_id)
        self.db_lesson.title = "Test Lesson"
        self.db_lesson.difficulty_level = DifficultyLevel.BEGINNER
        self.db_lesson.lesson_order = 1
        self.db_lesson.estimated_time = 30
        self.db_lesson.points_reward = 10
        self.db_lesson.prerequisites = {}
        self.db_lesson.learning_objectives = ["Basic concepts"]
        self.db_lesson.completion_criteria = {
            "min_score": 70,
            "required_content_ids": [str(uuid.uuid4()), str(uuid.uuid4())],
            "time_requirement": 15  # minutes
        }
        
        # Reset all mocks
        lesson_repo_mock.reset_mock()
    
    def tearDown(self):
        """Clean up after each test."""
        lesson_repo_patch.stop()
    
    def test_set_completion_criteria(self):
        """Test setting completion criteria for a lesson."""
        # Setup
        completion_criteria = {
            "min_score": 80,
            "required_content_ids": [str(uuid.uuid4())],
            "time_requirement": 20
        }
        
        # Mock repository methods
        lesson_repo_mock.get_lesson.return_value = self.db_lesson
        
        updated_lesson = MagicMock()
        updated_lesson.id = self.db_lesson.id
        updated_lesson.completion_criteria = completion_criteria
        lesson_repo_mock.update_lesson_metadata.return_value = updated_lesson
        
        # Call the method
        result = self.lesson_service.set_completion_criteria(
            lesson_id=self.lesson_id,
            completion_criteria=completion_criteria
        )
        
        # Assertions
        self.assertTrue(result)
        lesson_repo_mock.update_lesson_metadata.assert_called_once()
        call_args = lesson_repo_mock.update_lesson_metadata.call_args[0]
        self.assertEqual(call_args[1], uuid.UUID(self.lesson_id))
        self.assertEqual(call_args[2], {"completion_criteria": completion_criteria})
    
    def test_get_completion_criteria(self):
        """Test getting completion criteria for a lesson."""
        # Mock repository methods
        lesson_repo_mock.get_lesson.return_value = self.db_lesson
        
        # Call the method
        result = self.lesson_service.get_completion_criteria(lesson_id=self.lesson_id)
        
        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result["min_score"], 70)
        self.assertEqual(len(result["required_content_ids"]), 2)
        self.assertEqual(result["time_requirement"], 15)
    
    def test_get_completion_criteria_not_found(self):
        """Test getting completion criteria for a lesson that doesn't exist."""
        # Mock repository methods
        lesson_repo_mock.get_lesson.return_value = None
        
        # Test
        with self.assertRaises(ResourceNotFoundError):
            self.lesson_service.get_completion_criteria(lesson_id=self.lesson_id)
    
    def test_check_lesson_completion_criteria_met(self):
        """Test checking if a user has met a lesson's completion criteria."""
        # Mock repository and service methods
        lesson_repo_mock.get_lesson.return_value = self.db_lesson
        
        with patch('src.services.progress_service.ProgressService.get_lesson_score') as mock_get_score, \
             patch('src.services.progress_service.ProgressService.get_completed_content_ids') as mock_completed_content, \
             patch('src.services.progress_service.ProgressService.get_time_spent_on_lesson') as mock_time_spent:
            
            # User has satisfied all criteria
            mock_get_score.return_value = 85  # Above min_score of 70
            mock_completed_content.return_value = self.db_lesson.completion_criteria["required_content_ids"]
            mock_time_spent.return_value = 20  # Above time_requirement of 15
            
            # Call the method
            result, missing = self.lesson_service.check_completion_criteria_met(
                user_id=self.user_id,
                lesson_id=self.lesson_id
            )
            
            # Assertions
            self.assertTrue(result)
            self.assertEqual(len(missing), 0)
    
    def test_check_lesson_completion_criteria_not_met(self):
        """Test checking if a user has not met a lesson's completion criteria."""
        # Mock repository and service methods
        lesson_repo_mock.get_lesson.return_value = self.db_lesson
        
        with patch('src.services.progress_service.ProgressService.get_lesson_score') as mock_get_score, \
             patch('src.services.progress_service.ProgressService.get_completed_content_ids') as mock_completed_content, \
             patch('src.services.progress_service.ProgressService.get_time_spent_on_lesson') as mock_time_spent:
            
            # User has not satisfied all criteria
            mock_get_score.return_value = 65  # Below min_score of 70
            mock_completed_content.return_value = [self.db_lesson.completion_criteria["required_content_ids"][0]]  # Missing one content
            mock_time_spent.return_value = 10  # Below time_requirement of 15
            
            # Call the method
            result, missing = self.lesson_service.check_completion_criteria_met(
                user_id=self.user_id,
                lesson_id=self.lesson_id
            )
            
            # Assertions
            self.assertFalse(result)
            self.assertEqual(len(missing), 3)  # Missing score, content, and time
            self.assertIn("score", missing[0].lower())
            self.assertIn("content", missing[1].lower())
            self.assertIn("time", missing[2].lower())
    
    def test_mark_lesson_complete(self):
        """Test marking a lesson as complete for a user."""
        # Mock repository and service methods
        lesson_repo_mock.get_lesson.return_value = self.db_lesson
        
        with patch('src.services.progress_service.ProgressService.mark_lesson_complete') as mock_mark_complete, \
             patch.object(LessonService, 'check_completion_criteria_met') as mock_check_criteria:
            
            # User has met all criteria
            mock_check_criteria.return_value = (True, [])
            mock_mark_complete.return_value = True
            
            # Call the method
            result = self.lesson_service.mark_lesson_complete(
                user_id=self.user_id,
                lesson_id=self.lesson_id
            )
            
            # Assertions
            self.assertTrue(result)
            mock_mark_complete.assert_called_once_with(
                user_id=self.user_id,
                lesson_id=self.lesson_id
            )
    
    def test_mark_lesson_complete_criteria_not_met(self):
        """Test attempting to mark a lesson complete when criteria aren't met."""
        # Mock repository and service methods
        lesson_repo_mock.get_lesson.return_value = self.db_lesson
        
        with patch('src.services.progress_service.ProgressService.mark_lesson_complete') as mock_mark_complete, \
             patch.object(LessonService, 'check_completion_criteria_met') as mock_check_criteria:
            
            # User has not met all criteria
            mock_check_criteria.return_value = (False, ["Score below required minimum"])
            
            # Call the method
            result = self.lesson_service.mark_lesson_complete(
                user_id=self.user_id,
                lesson_id=self.lesson_id,
                override_criteria=False
            )
            
            # Assertions
            self.assertFalse(result)
            mock_mark_complete.assert_not_called()
    
    def test_mark_lesson_complete_with_override(self):
        """Test marking a lesson complete with criteria override."""
        # Mock repository and service methods
        lesson_repo_mock.get_lesson.return_value = self.db_lesson
        
        with patch('src.services.progress_service.ProgressService.mark_lesson_complete') as mock_mark_complete, \
             patch.object(LessonService, 'check_completion_criteria_met') as mock_check_criteria:
            
            # User has not met all criteria
            mock_check_criteria.return_value = (False, ["Score below required minimum"])
            mock_mark_complete.return_value = True
            
            # Call the method with override
            result = self.lesson_service.mark_lesson_complete(
                user_id=self.user_id,
                lesson_id=self.lesson_id,
                override_criteria=True
            )
            
            # Assertions
            self.assertTrue(result)
            mock_mark_complete.assert_called_once_with(
                user_id=self.user_id,
                lesson_id=self.lesson_id
            )

if __name__ == '__main__':
    unittest.main() 