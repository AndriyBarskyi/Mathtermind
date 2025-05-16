"""
Test suite for the GoalsService class.

This module contains unit tests for the GoalsService class, which manages
learning goals and personal bests in the Mathtermind application.
"""

import uuid
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
import pytest
from src.tests.base_test_classes import BaseServiceTest
from src.services.goals_service import GoalsService
from src.db.models import LearningGoal as DBLearningGoal, PersonalBest as DBPersonalBest
from src.models.goals import LearningGoal, PersonalBest


class TestGoalsService(BaseServiceTest):
    """Test class for GoalsService."""
    
    def setUp(self):
        """Set up test environment before each test."""
        super().setUp()
        
        # Create test data
        self.test_user_id = str(uuid.uuid4())
        self.test_goal_id = str(uuid.uuid4())
        self.test_best_id = str(uuid.uuid4())
        
        # Create mock DB objects
        self.mock_db_goal = MagicMock(spec=DBLearningGoal)
        self.mock_db_goal.id = uuid.UUID(self.test_goal_id)
        self.mock_db_goal.user_id = uuid.UUID(self.test_user_id)
        self.mock_db_goal.goal_type = "Daily"
        self.mock_db_goal.title = "Complete 5 exercises"
        self.mock_db_goal.description = "Daily practice goal"
        self.mock_db_goal.target = 5
        self.mock_db_goal.target_unit = "Exercises"
        self.mock_db_goal.current_progress = 2
        self.mock_db_goal.start_date = datetime.now() - timedelta(days=1)
        self.mock_db_goal.end_date = datetime.now() + timedelta(days=1)
        self.mock_db_goal.is_completed = False
        self.mock_db_goal.is_recurring = True
        self.mock_db_goal.created_at = datetime.now() - timedelta(days=1)
        self.mock_db_goal.updated_at = datetime.now() - timedelta(hours=1)
        
        self.mock_db_best = MagicMock(spec=DBPersonalBest)
        self.mock_db_best.id = uuid.UUID(self.test_best_id)
        self.mock_db_best.user_id = uuid.UUID(self.test_user_id)
        self.mock_db_best.metric_type = "Score"
        self.mock_db_best.value = 95.5
        self.mock_db_best.context_id = uuid.uuid4()
        self.mock_db_best.context_type = "Quiz"
        self.mock_db_best.achieved_at = datetime.now() - timedelta(hours=2)
        self.mock_db_best.previous_best = 90.0
        self.mock_db_best.improvement = 5.5
        self.mock_db_best.created_at = datetime.now() - timedelta(hours=2)
        self.mock_db_best.updated_at = datetime.now() - timedelta(hours=2)
        
        # Expected UI models
        self.expected_goal = LearningGoal(
            id=self.test_goal_id,
            user_id=self.test_user_id,
            goal_type="Daily",
            title="Complete 5 exercises",
            description="Daily practice goal",
            target=5,
            target_unit="Exercises",
            current_progress=2,
            start_date=self.mock_db_goal.start_date,
            end_date=self.mock_db_goal.end_date,
            is_completed=False,
            is_recurring=True,
            created_at=self.mock_db_goal.created_at,
            updated_at=self.mock_db_goal.updated_at
        )
        
        self.expected_best = PersonalBest(
            id=self.test_best_id,
            user_id=self.test_user_id,
            metric_type="Score",
            value=95.5,
            context_id=str(self.mock_db_best.context_id),
            context_type="Quiz",
            achieved_at=self.mock_db_best.achieved_at,
            previous_best=90.0,
            improvement=5.5,
            created_at=self.mock_db_best.created_at,
            updated_at=self.mock_db_best.updated_at
        )
        
        # Important: Initialize the service with patch
        with patch('src.services.goals_service.get_db'):
            self.goals_service = GoalsService()
            # Override the db with our mock
            self.goals_service.db = self.mock_db
        
        # Mock the conversion methods to return our pre-defined models
        self.goals_service._convert_db_goal_to_ui_goal = MagicMock(return_value=self.expected_goal)
        self.goals_service._convert_db_best_to_ui_best = MagicMock(return_value=self.expected_best)
    
    def test_get_user_goals_success(self):
        """Test getting all goals for a user successfully."""
        # Setup database mock
        self.mock_db.reset_mock()
        query_mock = MagicMock()
        self.mock_db.query.return_value = query_mock
        
        filter_mock = MagicMock()
        query_mock.filter.return_value = filter_mock
        
        order_by_mock = MagicMock()
        filter_mock.order_by.return_value = order_by_mock
        order_by_mock.all.return_value = [self.mock_db_goal]
        
        # Call the method
        result = self.goals_service.get_user_goals(self.test_user_id)
        
        # Verify the result
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, self.test_goal_id)
        self.assertEqual(result[0].title, "Complete 5 exercises")
        
        # Verify the mock was called correctly
        self.mock_db.query.assert_called_with(DBLearningGoal)
    
    def test_get_user_goals_exception(self):
        """Test handling of exceptions when getting user goals."""
        # Mock the database query to raise an exception
        self.mock_db.query.side_effect = Exception("Database error")
        
        # Call the method
        result = self.goals_service.get_user_goals(self.test_user_id)
        
        # Verify an empty list is returned
        self.assertEqual(result, [])
    
    def test_get_active_goals_success(self):
        """Test getting active goals for a user successfully."""
        # Setup database mock
        self.mock_db.reset_mock()
        query_mock = MagicMock()
        self.mock_db.query.return_value = query_mock
        
        filter_mock = MagicMock()
        query_mock.filter.return_value = filter_mock
        
        order_by_mock = MagicMock()
        filter_mock.order_by.return_value = order_by_mock
        order_by_mock.all.return_value = [self.mock_db_goal]
        
        # Call the method
        result = self.goals_service.get_active_goals(self.test_user_id)
        
        # Verify the result
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, self.test_goal_id)
        self.assertEqual(result[0].is_completed, False)
        
        # Verify the mock was called correctly
        self.mock_db.query.assert_called_with(DBLearningGoal)
    
    def test_get_active_goals_exception(self):
        """Test handling of exceptions when getting active goals."""
        # Mock the database query to raise an exception
        self.mock_db.query.side_effect = Exception("Database error")
        
        # Call the method
        result = self.goals_service.get_active_goals(self.test_user_id)
        
        # Verify an empty list is returned
        self.assertEqual(result, [])
    
    def test_create_goal_success(self):
        """Test creating a goal successfully."""
        # Mock the database operations
        self.mock_db.reset_mock()
        self.mock_db.add = MagicMock()
        self.mock_db.commit = MagicMock()
        self.mock_db.refresh = MagicMock()
        
        # Mock uuid.uuid4 to return our test ID
        with patch('uuid.uuid4', return_value=uuid.UUID(self.test_goal_id)):
            # Make sure we capture what's passed to db.add for verification
            def side_effect(arg):
                self.created_goal = arg
            self.mock_db.add.side_effect = side_effect
            
            # Call the method
            result = self.goals_service.create_goal(
                user_id=self.test_user_id,
                goal_type="Daily",
                title="Complete 5 exercises",
                target=5,
                target_unit="Exercises",
                description="Daily practice goal",
                end_date=datetime.now() + timedelta(days=1),
                is_recurring=True
            )
            
            # Verify mocking was done correctly - the service should convert the 
            # database goal to our expected goal
            self.goals_service._convert_db_goal_to_ui_goal.assert_called_once()
            
            # Verify the result matches our expected goal
            self.assertEqual(result, self.expected_goal)
            
            # Verify database operations were called
            self.mock_db.add.assert_called_once()
            self.mock_db.commit.assert_called_once()
            self.mock_db.refresh.assert_called_once()
    
    def test_create_goal_exception(self):
        """Test handling of exceptions when creating a goal."""
        # Mock the database to raise an exception
        self.mock_db.reset_mock()
        self.mock_db.add.side_effect = Exception("Database error")
        
        # Call the method
        result = self.goals_service.create_goal(
            user_id=self.test_user_id,
            goal_type="Daily",
            title="Complete 5 exercises",
            target=5,
            target_unit="Exercises"
        )
        
        # Verify None is returned
        self.assertIsNone(result)
        
        # Verify rollback was called
        self.mock_db.rollback.assert_called_once()
    
    def test_update_goal_progress_success(self):
        """Test updating goal progress successfully."""
        # Setup database mock
        self.mock_db.reset_mock()
        query_mock = MagicMock()
        self.mock_db.query.return_value = query_mock
        
        filter_mock = MagicMock()
        query_mock.filter.return_value = filter_mock
        filter_mock.first.return_value = self.mock_db_goal
        
        # Original progress before update
        initial_progress = self.mock_db_goal.current_progress
        
        # Call the method to update progress
        result = self.goals_service.update_goal_progress(
            goal_id=self.test_goal_id,
            progress=2
        )
        
        # Verify the result
        self.assertEqual(result, self.expected_goal)
        
        # Verify goal progress was updated
        self.assertEqual(self.mock_db_goal.current_progress, initial_progress + 2)
        
        # Verify mocks were called correctly
        self.mock_db.query.assert_called_with(DBLearningGoal)
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()
    
    def test_update_goal_progress_complete(self):
        """Test updating goal progress that results in completion."""
        # Set up a goal that will be completed with the update
        self.mock_db.reset_mock()
        query_mock = MagicMock()
        self.mock_db.query.return_value = query_mock
        
        filter_mock = MagicMock()
        query_mock.filter.return_value = filter_mock
        
        # Create a local copy of the mock_db_goal with specific values for this test
        test_goal = MagicMock(spec=DBLearningGoal)
        test_goal.id = uuid.UUID(self.test_goal_id)
        test_goal.user_id = uuid.UUID(self.test_user_id)
        test_goal.current_progress = 3
        test_goal.target = 5
        test_goal.is_completed = False
        
        filter_mock.first.return_value = test_goal
        
        # Call the method to update progress
        result = self.goals_service.update_goal_progress(
            goal_id=self.test_goal_id,
            progress=2
        )
        
        # Verify the goal is marked as completed
        self.assertTrue(test_goal.is_completed)
        self.assertEqual(test_goal.current_progress, 5)  # 3 (initial) + 2 (added)
    
    def test_update_goal_progress_not_found(self):
        """Test updating progress for a non-existent goal."""
        # Mock the database query to return None
        self.mock_db.reset_mock()
        query_mock = MagicMock()
        self.mock_db.query.return_value = query_mock
        
        filter_mock = MagicMock()
        query_mock.filter.return_value = filter_mock
        filter_mock.first.return_value = None
        
        # Call the method
        result = self.goals_service.update_goal_progress(
            goal_id=self.test_goal_id,
            progress=2
        )
        
        # Verify None is returned
        self.assertIsNone(result)
    
    def test_update_goal_progress_exception(self):
        """Test handling of exceptions when updating goal progress."""
        # Mock the database query to raise an exception
        self.mock_db.reset_mock()
        self.mock_db.query.side_effect = Exception("Database error")
        
        # Call the method
        result = self.goals_service.update_goal_progress(
            goal_id=self.test_goal_id,
            progress=2
        )
        
        # Verify None is returned
        self.assertIsNone(result)
        
        # Verify rollback was called
        self.mock_db.rollback.assert_called_once()
    
    def test_complete_goal_success(self):
        """Test completing a goal successfully."""
        # Setup database mock
        self.mock_db.reset_mock()
        query_mock = MagicMock()
        self.mock_db.query.return_value = query_mock
        
        filter_mock = MagicMock()
        query_mock.filter.return_value = filter_mock
        filter_mock.first.return_value = self.mock_db_goal
        
        # Call the method
        result = self.goals_service.complete_goal(goal_id=self.test_goal_id)
        
        # Verify the result
        self.assertEqual(result, self.expected_goal)
        
        # Verify goal was updated
        self.assertTrue(self.mock_db_goal.is_completed)
        self.assertEqual(self.mock_db_goal.current_progress, self.mock_db_goal.target)
        
        # Verify mocks were called correctly
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()
    
    def test_complete_goal_not_found(self):
        """Test completing a non-existent goal."""
        # Mock the database query to return None
        self.mock_db.reset_mock()
        query_mock = MagicMock()
        self.mock_db.query.return_value = query_mock
        
        filter_mock = MagicMock()
        query_mock.filter.return_value = filter_mock
        filter_mock.first.return_value = None
        
        # Call the method
        result = self.goals_service.complete_goal(goal_id=self.test_goal_id)
        
        # Verify None is returned
        self.assertIsNone(result)
    
    def test_complete_goal_exception(self):
        """Test handling of exceptions when completing a goal."""
        # Mock the database query to raise an exception
        self.mock_db.reset_mock()
        self.mock_db.query.side_effect = Exception("Database error")
        
        # Call the method
        result = self.goals_service.complete_goal(goal_id=self.test_goal_id)
        
        # Verify None is returned
        self.assertIsNone(result)
        
        # Verify rollback was called
        self.mock_db.rollback.assert_called_once()
    
    def test_get_personal_bests_success(self):
        """Test getting personal bests for a user successfully."""
        # Setup database mock
        self.mock_db.reset_mock()
        query_mock = MagicMock()
        self.mock_db.query.return_value = query_mock
        
        filter_mock = MagicMock()
        query_mock.filter.return_value = filter_mock
        
        order_by_mock = MagicMock()
        filter_mock.order_by.return_value = order_by_mock
        order_by_mock.all.return_value = [self.mock_db_best]
        
        # Call the method
        result = self.goals_service.get_personal_bests(self.test_user_id)
        
        # Verify the result
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, self.test_best_id)
        self.assertEqual(result[0].value, 95.5)
        
        # Verify the mock was called correctly
        self.mock_db.query.assert_called_with(DBPersonalBest)
    
    def test_get_personal_bests_exception(self):
        """Test handling of exceptions when getting personal bests."""
        # Mock the database query to raise an exception
        self.mock_db.query.side_effect = Exception("Database error")
        
        # Call the method
        result = self.goals_service.get_personal_bests(self.test_user_id)
        
        # Verify an empty list is returned
        self.assertEqual(result, [])
    
    def test_record_personal_best_success(self):
        """Test recording a personal best successfully."""
        # Mock the database operations
        self.mock_db.reset_mock()
        self.mock_db.add = MagicMock()
        self.mock_db.commit = MagicMock()
        self.mock_db.refresh = MagicMock()
        
        # Mock uuid.uuid4 to return our test ID
        with patch('uuid.uuid4', return_value=uuid.UUID(self.test_best_id)):
            # Make sure we capture what's passed to db.add for verification
            def side_effect(arg):
                self.created_best = arg
            self.mock_db.add.side_effect = side_effect
            
            # Call the method
            result = self.goals_service.record_personal_best(
                user_id=self.test_user_id,
                metric_type="Score",
                value=95.5,
                context_id=str(self.mock_db_best.context_id),
                context_type="Quiz",
                previous_best=90.0
            )
            
            # Verify mocking was done correctly - the service should convert the 
            # database personal best to our expected personal best
            self.goals_service._convert_db_best_to_ui_best.assert_called_once()
            
            # Verify the result matches our expected personal best
            self.assertEqual(result, self.expected_best)
            
            # Verify database operations were called
            self.mock_db.add.assert_called_once()
            self.mock_db.commit.assert_called_once()
            self.mock_db.refresh.assert_called_once()
    
    def test_record_personal_best_time_metric(self):
        """Test recording a time-based personal best (where lower is better)."""
        # Mock the database operations
        self.mock_db.reset_mock()
        self.mock_db.add = MagicMock()
        self.mock_db.commit = MagicMock()
        self.mock_db.refresh = MagicMock()
        
        # Call the method
        with patch('uuid.uuid4', return_value=uuid.UUID(self.test_best_id)):
            result = self.goals_service.record_personal_best(
                user_id=self.test_user_id,
                metric_type="Time",
                value=60.0,  # 60 seconds
                previous_best=75.0  # 75 seconds
            )
        
        # Verify the result - we expect our mocked PersonalBest
        self.assertEqual(result, self.expected_best)
        
        # Verify database operations
        self.mock_db.add.assert_called_once()
        
        # Check the improvement calculation in the created object
        # Get the personal best that was added to the database
        created_best = self.mock_db.add.call_args[0][0]
        self.assertEqual(created_best.metric_type, "Time")
        self.assertEqual(created_best.value, 60.0)
        # For time metrics, improvement is previous - current (since lower is better)
        self.assertEqual(created_best.improvement, 15.0)  # 75.0 - 60.0
    
    def test_record_personal_best_exception(self):
        """Test handling of exceptions when recording a personal best."""
        # Mock the database to raise an exception
        self.mock_db.reset_mock()
        self.mock_db.add.side_effect = Exception("Database error")
        
        # Call the method
        result = self.goals_service.record_personal_best(
            user_id=self.test_user_id,
            metric_type="Score",
            value=95.5
        )
        
        # Verify None is returned
        self.assertIsNone(result)
        
        # Verify rollback was called
        self.mock_db.rollback.assert_called_once()
    
    def test_convert_db_goal_to_ui_goal(self):
        """Test conversion from database goal to UI goal model."""
        # Restore the original method for this test
        original_convert = GoalsService._convert_db_goal_to_ui_goal.__get__(self.goals_service, GoalsService)
        self.goals_service._convert_db_goal_to_ui_goal = original_convert
        
        # Call the method directly
        result = self.goals_service._convert_db_goal_to_ui_goal(self.mock_db_goal)
        
        # Verify the result
        self.assertEqual(result.id, self.test_goal_id)
        self.assertEqual(result.user_id, self.test_user_id)
        self.assertEqual(result.goal_type, "Daily")
        self.assertEqual(result.title, "Complete 5 exercises")
        self.assertEqual(result.description, "Daily practice goal")
        self.assertEqual(result.target, 5)
        self.assertEqual(result.target_unit, "Exercises")
        self.assertEqual(result.current_progress, 2)
        self.assertEqual(result.start_date, self.mock_db_goal.start_date)
        self.assertEqual(result.end_date, self.mock_db_goal.end_date)
        self.assertEqual(result.is_completed, False)
        self.assertEqual(result.is_recurring, True)
        self.assertEqual(result.created_at, self.mock_db_goal.created_at)
        self.assertEqual(result.updated_at, self.mock_db_goal.updated_at)
    
    def test_convert_db_best_to_ui_best(self):
        """Test conversion from database personal best to UI personal best model."""
        # Restore the original method for this test
        original_convert = GoalsService._convert_db_best_to_ui_best.__get__(self.goals_service, GoalsService)
        self.goals_service._convert_db_best_to_ui_best = original_convert
        
        # Call the method directly
        result = self.goals_service._convert_db_best_to_ui_best(self.mock_db_best)
        
        # Verify the result
        self.assertEqual(result.id, self.test_best_id)
        self.assertEqual(result.user_id, self.test_user_id)
        self.assertEqual(result.metric_type, "Score")
        self.assertEqual(result.value, 95.5)
        self.assertEqual(result.context_id, str(self.mock_db_best.context_id))
        self.assertEqual(result.context_type, "Quiz")
        self.assertEqual(result.achieved_at, self.mock_db_best.achieved_at)
        self.assertEqual(result.previous_best, 90.0)
        self.assertEqual(result.improvement, 5.5)
        self.assertEqual(result.created_at, self.mock_db_best.created_at)
        self.assertEqual(result.updated_at, self.mock_db_best.updated_at) 