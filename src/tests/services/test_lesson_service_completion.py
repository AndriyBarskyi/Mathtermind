"""
Test module for the lesson completion management functionality in LessonService.

This module contains tests for setting completion criteria, checking if criteria are met,
and marking lessons as complete.
"""

import unittest
from unittest.mock import MagicMock, patch
import uuid
from datetime import datetime, timezone

from src.core.error_handling.exceptions import ValidationError, ResourceNotFoundError, BusinessLogicError
from src.models.lesson import Lesson
from src.db.models.enums import DifficultyLevel
from src.services.lesson_service import LessonService

class TestLessonServiceCompletion(unittest.TestCase):
    """Test cases for the lesson completion management functions in the LessonService class."""
    
    def setUp(self):
        """Set up test fixtures before each test method is called."""
        # Create sample data for tests
        self.user_id = "11111111-1111-1111-1111-111111111111"
        self.lesson_id = "22222222-2222-2222-2222-222222222222"
        self.course_id = "33333333-3333-3333-3333-333333333333"
        self.content_id1 = "44444444-4444-4444-4444-444444444444"
        self.content_id2 = "55555555-5555-5555-5555-555555555555"
        
        # Create mock DB lesson
        self.db_lesson = MagicMock(
            id=uuid.UUID(self.lesson_id),
            title="Test Lesson",
            description="Test lesson description",
            lesson_order=1,
            estimated_time=60,
            points_reward=10,
            # Note: lesson_type is intentionally removed - lessons don't have types
            difficulty_level="INTERMEDIATE",
            course_id=uuid.UUID(self.course_id),
            metadata={}
        )
        
        # Sample completion criteria for tests
        self.sample_criteria = {
            "required_content_ids": [self.content_id1, self.content_id2],
            "required_score": 80,
            "required_time_spent": 30,
            "assessment_required": True,
            "prerequisites_required": False  # Prerequisites are for information only, not requirements
        }
        
        # Create mock DB
        self.mock_db = MagicMock()
        
        # Create service instance
        self.lesson_service = LessonService()
        
        # Create and set up mock repositories
        self.lesson_repo_mock = MagicMock()
        self.progress_service_mock = MagicMock()
        
        # Set up lesson repo mock
        self.lesson_repo_mock.get_lesson.return_value = self.db_lesson
        
        # Set up progress service mock methods
        self.progress_service_mock.has_completed_content = MagicMock(return_value=True)
        self.progress_service_mock.get_assessment_score = MagicMock(return_value=90)
        self.progress_service_mock.get_time_spent = MagicMock(return_value=60)
        self.progress_service_mock.get_activity_count = MagicMock(return_value=5)
        self.progress_service_mock.has_content_interaction = MagicMock(return_value=True)
        
        # Create a mock for complete_lesson that returns a valid object
        completed_lesson_mock = MagicMock(id="comp-lesson-1")
        self.progress_service_mock.complete_lesson.return_value = completed_lesson_mock
        
        # Replace the service's repositories with our mocks
        self.lesson_service.lesson_repo = self.lesson_repo_mock
        self.lesson_service.progress_service = self.progress_service_mock
        self.lesson_service.db = self.mock_db
    
    def test_set_completion_criteria(self):
        """Test setting completion criteria for a lesson."""
        # Mock repository methods
        updated_lesson = MagicMock()
        updated_lesson.id = self.db_lesson.id
        updated_lesson.title = self.db_lesson.title
        updated_lesson.metadata = {"completion_criteria": self.sample_criteria}
        
        self.lesson_repo_mock.update_lesson_metadata.return_value = updated_lesson
        
        # Mock transaction context
        mock_transaction_context = MagicMock()
        mock_transaction_context.__enter__ = MagicMock(return_value=self.mock_db)
        mock_transaction_context.__exit__ = MagicMock(return_value=None)
        self.lesson_service.transaction = MagicMock(return_value=mock_transaction_context)
        
        # Call the method
        result = self.lesson_service.set_completion_criteria(
            lesson_id=self.lesson_id,
            completion_criteria=self.sample_criteria
        )
        
        # Assertions
        self.assertTrue(result)
        self.lesson_repo_mock.update_lesson_metadata.assert_called_once()
    
    def test_set_completion_criteria_validation_error(self):
        """Test validation error when setting invalid completion criteria."""
        # Invalid criteria - required_score out of range
        invalid_criteria = {
            "required_score": 110,  # Invalid: more than 100%
            "assessment_required": True
        }
        
        # Test
        with self.assertRaises(ValidationError):
            self.lesson_service.set_completion_criteria(
                lesson_id=self.lesson_id,
                completion_criteria=invalid_criteria
            )
    
    def test_get_completion_criteria(self):
        """Test getting completion criteria for a lesson."""
        # Mock repository methods
        self.db_lesson.metadata = {"completion_criteria": self.sample_criteria}
        self.lesson_repo_mock.get_lesson.return_value = self.db_lesson
        
        # Mock transaction context
        mock_transaction_context = MagicMock()
        mock_transaction_context.__enter__ = MagicMock(return_value=self.mock_db)
        mock_transaction_context.__exit__ = MagicMock(return_value=None)
        self.lesson_service.transaction = MagicMock(return_value=mock_transaction_context)
        
        # Call the method
        result = self.lesson_service.get_completion_criteria(lesson_id=self.lesson_id)
        
        # Assertions
        self.assertEqual(result, self.sample_criteria)
    
    def test_get_completion_criteria_not_set(self):
        """Test getting completion criteria when not set."""
        # Mock repository methods with no completion criteria
        self.db_lesson.metadata = {}
        self.lesson_repo_mock.get_lesson.return_value = self.db_lesson
        
        # Mock transaction context
        mock_transaction_context = MagicMock()
        mock_transaction_context.__enter__ = MagicMock(return_value=self.mock_db)
        mock_transaction_context.__exit__ = MagicMock(return_value=None)
        self.lesson_service.transaction = MagicMock(return_value=mock_transaction_context)
        
        # Call the method
        result = self.lesson_service.get_completion_criteria(lesson_id=self.lesson_id)
        
        # Assertions
        self.assertEqual(result, {})
    
    def test_check_completion_criteria_no_criteria_set(self):
        """Test checking completion criteria when none are set."""
        # Mock get_completion_criteria to return empty dict
        self.lesson_service.get_completion_criteria = MagicMock(return_value={})
        
        # Call the method
        result, unmet = self.lesson_service.check_completion_criteria_met(
            user_id=self.user_id,
            lesson_id=self.lesson_id
        )
        
        # Assertions - should be true if no criteria set
        self.assertTrue(result)
        self.assertEqual(len(unmet), 0)
        self.lesson_service.get_completion_criteria.assert_called_once_with(self.lesson_id)
    
    def test_check_completion_criteria_met_all_criteria_met(self):
        """Test checking if all completion criteria are met."""
        # Setup completion criteria
        self.db_lesson.metadata = {"completion_criteria": self.sample_criteria}
        
        # Mock progress service methods to indicate all criteria are met
        self.progress_service_mock.has_completed_content.return_value = True
        self.progress_service_mock.get_assessment_score.return_value = 85
        self.progress_service_mock.get_time_spent.return_value = 45
        
        # Mock check_prerequisites_satisfied and get_completion_criteria
        self.lesson_service.check_prerequisites_satisfied = MagicMock(return_value=(True, []))
        self.lesson_service.get_completion_criteria = MagicMock(return_value=self.sample_criteria)
        
        # Call the method
        result, unmet = self.lesson_service.check_completion_criteria_met(
            user_id=self.user_id,
            lesson_id=self.lesson_id
        )
        
        # Assertions
        self.assertTrue(result)
        self.assertEqual(len(unmet), 0)
    
    def test_check_completion_criteria_met_some_criteria_not_met(self):
        """Test checking when some completion criteria are not met."""
        # Mock progress service methods to indicate some criteria are not met
        self.progress_service_mock.has_completed_content.side_effect = lambda user_id, content_id: content_id == self.content_id1
        self.progress_service_mock.get_assessment_score.return_value = 70  # Below required 80
        self.progress_service_mock.get_time_spent.return_value = 45  # Above required 30
        
        # Mock check_prerequisites_satisfied and get_completion_criteria
        self.lesson_service.check_prerequisites_satisfied = MagicMock(return_value=(True, []))
        self.lesson_service.get_completion_criteria = MagicMock(return_value=self.sample_criteria)
        
        # Call the method
        result, unmet = self.lesson_service.check_completion_criteria_met(
            user_id=self.user_id,
            lesson_id=self.lesson_id
        )
        
        # Assertions
        self.assertFalse(result)
        self.assertGreater(len(unmet), 0)
    
    def test_mark_lesson_complete_criteria_met(self):
        """Test marking a lesson as complete when criteria are met."""
        # Mock check_completion_criteria_met to return True
        self.lesson_service.check_completion_criteria_met = MagicMock(return_value=(True, []))
        
        # Mock get_lesson_by_id to return a lesson
        ui_lesson = Lesson(
            id=self.lesson_id,
            title=self.db_lesson.title,
            difficulty_level=DifficultyLevel.INTERMEDIATE.value,
            lesson_order=self.db_lesson.lesson_order,
            estimated_time=self.db_lesson.estimated_time,
            points_reward=self.db_lesson.points_reward,
            # Note: lesson_type is not included as it's deprecated
            course_id=self.course_id
        )
        self.lesson_service.get_lesson_by_id = MagicMock(return_value=ui_lesson)
        
        # Call the method
        result = self.lesson_service.mark_lesson_complete(
            user_id=self.user_id,
            lesson_id=self.lesson_id
        )
        
        # Assertions
        self.assertTrue(result)
        self.lesson_service.check_completion_criteria_met.assert_called_once_with(
            self.user_id, self.lesson_id
        )
        self.lesson_service.get_lesson_by_id.assert_called_once_with(self.lesson_id)
        self.progress_service_mock.complete_lesson.assert_called_once_with(
            user_id=self.user_id,
            lesson_id=self.lesson_id,
            course_id=self.course_id
        )
    
    def test_mark_lesson_complete_criteria_not_met(self):
        """Test marking a lesson as complete when criteria are not met."""
        # Mock check_completion_criteria_met to return False
        unmet_criteria = ["Assessment score below required", "Content item not completed"]
        self.lesson_service.check_completion_criteria_met = MagicMock(return_value=(False, unmet_criteria))
        
        # Test
        with self.assertRaises(BusinessLogicError):
            self.lesson_service.mark_lesson_complete(
                user_id=self.user_id,
                lesson_id=self.lesson_id
            )
            
        # Assertions
        self.lesson_service.check_completion_criteria_met.assert_called_once_with(
            self.user_id, self.lesson_id
        )
        self.progress_service_mock.complete_lesson.assert_not_called()
    
    def test_mark_lesson_complete_override_criteria(self):
        """Test marking a lesson complete with override_criteria=True."""
        # Mock get_lesson_by_id to return a lesson
        ui_lesson = Lesson(
            id=self.lesson_id,
            title=self.db_lesson.title,
            difficulty_level=DifficultyLevel.INTERMEDIATE.value,
            lesson_order=self.db_lesson.lesson_order,
            estimated_time=self.db_lesson.estimated_time,
            points_reward=self.db_lesson.points_reward,
            # Note: lesson_type is not included as it's deprecated
            course_id=self.course_id
        )
        self.lesson_service.get_lesson_by_id = MagicMock(return_value=ui_lesson)
        
        # Mock check_completion_criteria_met (should not be called)
        self.lesson_service.check_completion_criteria_met = MagicMock()
        
        # Call the method with override
        result = self.lesson_service.mark_lesson_complete(
            user_id=self.user_id,
            lesson_id=self.lesson_id,
            override_criteria=True
        )
        
        # Assertions
        self.assertTrue(result)
        self.lesson_service.check_completion_criteria_met.assert_not_called()
        self.progress_service_mock.complete_lesson.assert_called_once_with(
            user_id=self.user_id,
            lesson_id=self.lesson_id,
            course_id=self.course_id
        )
    
    def test_validate_completion_criteria_valid(self):
        """Test validation of valid completion criteria."""
        # Valid criteria
        valid_criteria = {
            "required_content_ids": [self.content_id1, self.content_id2],
            "required_score": 80,
            "assessment_required": True,
            "required_time_spent": 30
        }
        
        # This should not raise an exception
        self.lesson_service._validate_completion_criteria(valid_criteria)
    
    def test_validate_completion_criteria_invalid_format(self):
        """Test validation error with invalid completion criteria format."""
        # Test with non-dictionary
        with self.assertRaises(ValidationError):
            self.lesson_service._validate_completion_criteria("not a dictionary")
        
        # Test with invalid score range
        with self.assertRaises(ValidationError):
            self.lesson_service._validate_completion_criteria({
                "required_score": 150  # Over 100%
            })
        
        # Test with negative time
        with self.assertRaises(ValidationError):
            self.lesson_service._validate_completion_criteria({
                "required_time_spent": -10  # Negative time
            })
        
        # Test with invalid content ID format
        with self.assertRaises(ValidationError):
            self.lesson_service._validate_completion_criteria({
                "required_content_ids": ["not-a-uuid"]
            })

if __name__ == '__main__':
    unittest.main() 