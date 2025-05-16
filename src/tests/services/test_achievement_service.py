"""
Tests for the Achievement Service.

This module contains tests for achievement service methods.
"""

import uuid
from unittest.mock import patch, MagicMock, ANY
from datetime import datetime, timedelta

import pytest
from src.tests.base_test_classes import BaseServiceTest
from src.services.achievement_service import AchievementService
from src.models.achievement import Achievement, UserAchievement
from src.db.models import Achievement as DBAchievement, UserAchievement as DBUserAchievement


class TestAchievementService(BaseServiceTest):
    """Test class for AchievementService."""
    
    def setUp(self):
        """Set up test environment before each test."""
        super().setUp()
        
        # Create mocks for repositories
        self.achievement_repo_mock = MagicMock()
        self.user_repo_mock = MagicMock()
        self.progress_repo_mock = MagicMock()
        
        # Patch the repository classes
        self.repo_patches = [
            patch('src.services.achievement_service.AchievementRepository', return_value=self.achievement_repo_mock),
            patch('src.services.achievement_service.UserRepository', return_value=self.user_repo_mock),
            patch('src.services.achievement_service.ProgressRepository', return_value=self.progress_repo_mock)
        ]
        
        # Start all patches
        for p in self.repo_patches:
            p.start()
            self.addCleanup(p.stop)
        
        # Create the service instance
        self.achievement_service = AchievementService()
        
        # Create test data
        self.test_achievement_id = str(uuid.uuid4())
        self.test_user_id = str(uuid.uuid4())
        self.test_progress_id = str(uuid.uuid4())
        
        # Create mock achievement
        self.mock_db_achievement = MagicMock(spec=DBAchievement)
        self.mock_db_achievement.id = uuid.UUID(self.test_achievement_id)
        self.mock_db_achievement.name = "Test Achievement"
        self.mock_db_achievement.description = "This is a test achievement"
        self.mock_db_achievement.criteria = {"type": "test", "requirements": {}}
        self.mock_db_achievement.category = "test"
        self.mock_db_achievement.icon = "test-icon.png"
        self.mock_db_achievement.icon_url = "test-icon.png"
        self.mock_db_achievement.points = 10
        self.mock_db_achievement.points_value = 10
        self.mock_db_achievement.display_order = 1
        self.mock_db_achievement.is_hidden = False
        self.mock_db_achievement.tier = "bronze"
        self.mock_db_achievement.metadata = {}
        self.mock_db_achievement.created_at = datetime.now()
        self.mock_db_achievement.updated_at = datetime.now()
        
        # Create mock user achievement
        self.mock_db_user_achievement = MagicMock(spec=DBUserAchievement)
        self.mock_db_user_achievement.id = uuid.uuid4()
        self.mock_db_user_achievement.user_id = uuid.UUID(self.test_user_id)
        self.mock_db_user_achievement.achievement_id = uuid.UUID(self.test_achievement_id)
        self.mock_db_user_achievement.earned_at = datetime.now()
        self.mock_db_user_achievement.awarded_at = datetime.now()
        self.mock_db_user_achievement.progress_data = {"progress": 100}
        self.mock_db_user_achievement.created_at = datetime.now()
        self.mock_db_user_achievement.updated_at = datetime.now()
        
        # Mock the achievement relationship
        self.mock_db_user_achievement.achievement = self.mock_db_achievement
        
        # Create mock UI models
        self.mock_achievement = Achievement(
            id=self.test_achievement_id,
            name="Test Achievement",
            description="This is a test achievement",
            criteria={"type": "test", "requirements": {}},
            category="test",
            icon="test-icon.png",
            points=10
        )
        
        self.mock_user_achievement = UserAchievement(
            id=str(self.mock_db_user_achievement.id),
            user_id=self.test_user_id,
            achievement_id=self.test_achievement_id,
            achievement=self.mock_achievement,
            earned_at=datetime.now(),
            progress_data={"progress": 100}
        )
    
    def test_get_all_achievements(self):
        """Test getting all achievements."""
        # Set up mock
        self.achievement_repo_mock.get_all.return_value = [self.mock_db_achievement]
        
        # Mock the conversion method
        with patch.object(
            self.achievement_service, 
            '_convert_db_achievement_to_ui_achievement', 
            return_value=self.mock_achievement
        ):
            # Call the method
            result = self.achievement_service.get_all_achievements()
            
            # Verify the result
            self.assertEqual(len(result), 1)
            self.assertIsInstance(result[0], Achievement)
            self.assertEqual(result[0].id, self.test_achievement_id)
            self.assertEqual(result[0].name, "Test Achievement")
            
            # Verify mock was called
            self.achievement_repo_mock.get_all.assert_called_once()
    
    def test_get_achievement_by_id(self):
        """Test getting an achievement by ID."""
        # Set up mock
        self.achievement_repo_mock.get_by_id.return_value = self.mock_db_achievement
        
        # Mock the conversion method
        with patch.object(
            self.achievement_service, 
            '_convert_db_achievement_to_ui_achievement', 
            return_value=self.mock_achievement
        ):
            # Call the method
            result = self.achievement_service.get_achievement_by_id(self.test_achievement_id)
            
            # Verify the result
            self.assertIsNotNone(result)
            self.assertIsInstance(result, Achievement)
            self.assertEqual(result.id, self.test_achievement_id)
            self.assertEqual(result.name, "Test Achievement")
            
            # Verify mock was called
            self.achievement_repo_mock.get_by_id.assert_called_once()
    
    def test_get_achievement_by_id_not_found(self):
        """Test getting an achievement by ID when not found."""
        # Set up mock
        self.achievement_repo_mock.get_by_id.return_value = None
        
        # Call the method
        result = self.achievement_service.get_achievement_by_id(self.test_achievement_id)
        
        # Verify the result
        self.assertIsNone(result)
        
        # Verify mock was called
        self.achievement_repo_mock.get_by_id.assert_called_once()
    
    def test_get_achievements_by_category(self):
        """Test getting achievements by category."""
        # Set up mock
        self.achievement_repo_mock.get_by_category.return_value = [self.mock_db_achievement]
        
        # Mock the conversion method
        with patch.object(
            self.achievement_service, 
            '_convert_db_achievement_to_ui_achievement', 
            return_value=self.mock_achievement
        ):
            # Call the method
            result = self.achievement_service.get_achievements_by_category("test")
            
            # Verify the result
            self.assertEqual(len(result), 1)
            self.assertIsInstance(result[0], Achievement)
            self.assertEqual(result[0].id, self.test_achievement_id)
            self.assertEqual(result[0].category, "test")
            
            # Verify mock was called
            self.achievement_repo_mock.get_by_category.assert_called_once_with("test")
    
    def test_get_user_achievements(self):
        """Test getting achievements for a user."""
        # Set up mock
        self.achievement_repo_mock.get_user_achievements.return_value = [self.mock_db_user_achievement]
        
        # Mock the conversion method
        with patch.object(
            self.achievement_service, 
            '_convert_db_user_achievement_to_ui_user_achievement', 
            return_value=self.mock_user_achievement
        ):
            # Call the method
            result = self.achievement_service.get_user_achievements(self.test_user_id)
            
            # Verify the result
            self.assertEqual(len(result), 1)
            self.assertIsInstance(result[0], UserAchievement)
            self.assertEqual(result[0].user_id, self.test_user_id)
            self.assertEqual(result[0].achievement_id, self.test_achievement_id)
            
            # Verify mock was called
            self.achievement_repo_mock.get_user_achievements.assert_called_once()
    
    def test_award_achievement(self):
        """Test awarding an achievement to a user."""
        # Set up mocks
        self.achievement_repo_mock.get_user_achievement.return_value = None
        self.achievement_repo_mock.get_by_id.return_value = self.mock_db_achievement
        self.achievement_repo_mock.award_achievement.return_value = self.mock_db_user_achievement
        
        # Mock user
        mock_user = MagicMock()
        mock_user.points = 0
        self.user_repo_mock.get_by_id.return_value = mock_user
        
        # Mock the conversion method
        with patch.object(
            self.achievement_service, 
            '_convert_db_user_achievement_to_ui_user_achievement', 
            return_value=self.mock_user_achievement
        ):
            # Call the method
            result = self.achievement_service.award_achievement(
                self.test_user_id, 
                self.test_achievement_id,
                {"progress": 100}
            )
            
            # Verify the result
            self.assertIsNotNone(result)
            self.assertIsInstance(result, UserAchievement)
            self.assertEqual(result.user_id, self.test_user_id)
            self.assertEqual(result.achievement_id, self.test_achievement_id)
            
            # Verify mocks were called
            self.achievement_repo_mock.get_user_achievement.assert_called_once()
            self.achievement_repo_mock.get_by_id.assert_called_once()
            self.achievement_repo_mock.award_achievement.assert_called_once()
            self.user_repo_mock.get_by_id.assert_called_once()
            self.user_repo_mock.update.assert_called_once()
            
            # Verify points were awarded
            self.assertEqual(mock_user.points, 10)
    
    def test_award_achievement_already_earned(self):
        """Test awarding an achievement that was already earned."""
        # Set up mock
        self.achievement_repo_mock.get_user_achievement.return_value = self.mock_db_user_achievement
        
        # Mock the conversion method
        with patch.object(
            self.achievement_service, 
            '_convert_db_user_achievement_to_ui_user_achievement', 
            return_value=self.mock_user_achievement
        ):
            # Call the method
            result = self.achievement_service.award_achievement(
                self.test_user_id, 
                self.test_achievement_id
            )
            
            # Verify the result
            self.assertIsNotNone(result)
            self.assertIsInstance(result, UserAchievement)
            
            # Verify mock was called
            self.achievement_repo_mock.get_user_achievement.assert_called_once()
            self.achievement_repo_mock.award_achievement.assert_not_called()
    
    def test_award_achievement_not_found(self):
        """Test awarding a non-existent achievement."""
        # Set up mock
        self.achievement_repo_mock.get_user_achievement.return_value = None
        self.achievement_repo_mock.get_by_id.return_value = None
        
        # Call the method
        result = self.achievement_service.award_achievement(
            self.test_user_id, 
            self.test_achievement_id
        )
        
        # Verify the result
        self.assertIsNone(result)
        
        # Verify mock was called
        self.achievement_repo_mock.get_user_achievement.assert_called_once()
        self.achievement_repo_mock.get_by_id.assert_called_once()
        self.achievement_repo_mock.award_achievement.assert_not_called()
    
    def test_create_achievement(self):
        """Test creating a new achievement."""
        # Set up mock
        self.achievement_repo_mock.create.return_value = self.mock_db_achievement
        
        # Mock the conversion method
        with patch.object(
            self.achievement_service,
            '_convert_db_achievement_to_ui_achievement',
            return_value=self.mock_achievement
        ):
            # Call the method
            result = self.achievement_service.create_achievement(
                name="Test Achievement",
                description="This is a test achievement",
                category="test",
                criteria={"type": "test", "requirements": {}},
                icon_url="test-icon.png",
                points_value=10,
                is_hidden=False
            )
            
            # Verify the result
            self.assertIsNotNone(result)
            self.assertIsInstance(result, Achievement)
            self.assertEqual(result.name, "Test Achievement")
            
            # Verify mock was called
            self.achievement_repo_mock.create.assert_called_once()
    
    def test_check_progress_achievements(self):
        """Test checking and awarding achievements based on progress."""
        # Set up mocks
        mock_progress = MagicMock()
        mock_progress.id = uuid.UUID(self.test_progress_id)
        mock_progress.user_id = uuid.UUID(self.test_user_id)
        mock_progress.is_completed = True
        mock_progress.course_id = uuid.uuid4()
        mock_progress.progress_percentage = 100
        
        self.progress_repo_mock.get_by_id.return_value = mock_progress
        
        # Set up achievement mocks
        course_completion_achievement = MagicMock(spec=DBAchievement)
        course_completion_achievement.id = uuid.uuid4()
        course_completion_achievement.criteria = {"type": "course_completion"}
        
        progress_percentage_achievement = MagicMock(spec=DBAchievement)
        progress_percentage_achievement.id = uuid.uuid4()
        progress_percentage_achievement.criteria = {"type": "progress_percentage", "min_percentage": 90}
        
        # Mock repository methods
        self.achievement_repo_mock.get_by_category.return_value = [
            course_completion_achievement,
            progress_percentage_achievement
        ]
        self.achievement_repo_mock.get_user_achievement.side_effect = [None, None]
        
        # Create a return value list for award_achievement calls
        with patch.object(
            self.achievement_service,
            'award_achievement',
            side_effect=[self.mock_user_achievement, self.mock_user_achievement]
        ):
            # Call the method
            result = self.achievement_service.check_progress_achievements(
                self.test_user_id,
                self.test_progress_id
            )
            
            # Verify the result
            self.assertEqual(len(result), 2)
            self.assertIsInstance(result[0], UserAchievement)
            
            # Verify mocks were called correctly
            self.progress_repo_mock.get_by_id.assert_called_once()
            self.achievement_repo_mock.get_by_category.assert_called_once()
            self.assertEqual(self.achievement_repo_mock.get_user_achievement.call_count, 2)
            self.assertEqual(self.achievement_service.award_achievement.call_count, 2)
    
    def test_check_user_achievements(self):
        """Test checking and awarding general user achievements."""
        # Set up user mock
        mock_user = MagicMock()
        mock_user.id = uuid.UUID(self.test_user_id)
        mock_user.points = 1000
        mock_user.created_at = datetime.now() - timedelta(days=100)
        mock_user.total_study_time = 3000  # 50 hours
        
        self.user_repo_mock.get_by_id.return_value = mock_user
        
        # Set up achievement mocks
        points_achievement = MagicMock(spec=DBAchievement)
        points_achievement.id = uuid.uuid4()
        points_achievement.criteria = {"type": "total_points", "min_points": 500}
        
        account_age_achievement = MagicMock(spec=DBAchievement)
        account_age_achievement.id = uuid.uuid4()
        account_age_achievement.criteria = {"type": "account_age", "min_days": 30}
        
        study_time_achievement = MagicMock(spec=DBAchievement)
        study_time_achievement.id = uuid.uuid4()
        study_time_achievement.criteria = {"type": "study_time", "min_minutes": 1500}
        
        # Mock repository methods
        self.achievement_repo_mock.get_by_category.return_value = [
            points_achievement,
            account_age_achievement,
            study_time_achievement
        ]
        self.achievement_repo_mock.get_user_achievement.side_effect = [None, None, None]
        
        # Create return values for award_achievement calls
        with patch.object(
            self.achievement_service,
            'award_achievement',
            side_effect=[self.mock_user_achievement, self.mock_user_achievement, self.mock_user_achievement]
        ):
            # Call the method
            result = self.achievement_service.check_user_achievements(self.test_user_id)
            
            # Verify the result
            self.assertEqual(len(result), 3)
            self.assertIsInstance(result[0], UserAchievement)
            
            # Verify mocks were called correctly
            self.user_repo_mock.get_by_id.assert_called_once()
            self.achievement_repo_mock.get_by_category.assert_called_once()
            self.assertEqual(self.achievement_repo_mock.get_user_achievement.call_count, 3)
            self.assertEqual(self.achievement_service.award_achievement.call_count, 3) 