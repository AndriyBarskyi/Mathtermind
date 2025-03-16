"""
Tests for the base service implementation.

This module contains tests for the BaseService class to ensure that
it provides the expected functionality for all service implementations.
"""

import pytest
import uuid
from unittest.mock import patch, MagicMock
from src.services.base_service import BaseService
from src.db.models import User
from src.tests.base_test_classes import BaseServiceTest


@pytest.mark.service
@pytest.mark.unit
class TestBaseService(BaseServiceTest):
    """Tests for the BaseService class."""
    
    def setUp(self):
        """Set up the test environment before each test."""
        super().setUp()
        
        # Create a mock repository
        self.mock_repository = MagicMock()
        
        # Create the service with the mock repository
        self.service = BaseService(repository=self.mock_repository)
        
        # Replace the service's db with our mock db
        self.service.db = self.mock_db
        
        # Create a test user ID
        self.test_user_id = uuid.uuid4()
        
        # Create a test user
        self.test_user = User(
            id=self.test_user_id,
            username="testuser",
            email="testuser@example.com",
            password_hash="hashed_password",
            age_group="15-17",
            points=0,
            experience_level=1,
            total_study_time=0
        )
    
    def test_get_by_id(self):
        """Test getting an entity by ID."""
        # Arrange
        self.mock_repository.get_by_id.return_value = self.test_user
        
        # Act
        result = self.service.get_by_id(self.test_user_id)
        
        # Assert
        self.mock_repository.get_by_id.assert_called_once_with(self.mock_db, self.test_user_id)
        assert result is self.test_user
    
    def test_get_by_id_exception(self):
        """Test getting an entity by ID when an exception occurs."""
        # Arrange
        self.mock_repository.get_by_id.side_effect = Exception("Test exception")
        
        # Act
        result = self.service.get_by_id(self.test_user_id)
        
        # Assert
        self.mock_repository.get_by_id.assert_called_once_with(self.mock_db, self.test_user_id)
        assert result is None
    
    def test_get_all(self):
        """Test getting all entities."""
        # Arrange
        self.mock_repository.get_all.return_value = [self.test_user]
        
        # Act
        result = self.service.get_all()
        
        # Assert
        self.mock_repository.get_all.assert_called_once_with(self.mock_db)
        assert result == [self.test_user]
    
    def test_get_all_exception(self):
        """Test getting all entities when an exception occurs."""
        # Arrange
        self.mock_repository.get_all.side_effect = Exception("Test exception")
        
        # Act
        result = self.service.get_all()
        
        # Assert
        self.mock_repository.get_all.assert_called_once_with(self.mock_db)
        assert result == []
    
    def test_create(self):
        """Test creating a new entity."""
        # Arrange
        self.mock_repository.create.return_value = self.test_user
        user_data = {
            "id": self.test_user_id,
            "username": "testuser",
            "email": "testuser@example.com",
            "password_hash": "hashed_password",
            "age_group": "15-17",
            "points": 0,
            "experience_level": 1,
            "total_study_time": 0
        }
        
        # Act
        result = self.service.create(**user_data)
        
        # Assert
        self.mock_repository.create.assert_called_once_with(self.mock_db, **user_data)
        assert result is self.test_user
    
    def test_create_exception(self):
        """Test creating a new entity when an exception occurs."""
        # Arrange
        self.mock_repository.create.side_effect = Exception("Test exception")
        user_data = {
            "id": self.test_user_id,
            "username": "testuser",
            "email": "testuser@example.com",
            "password_hash": "hashed_password",
            "age_group": "15-17",
            "points": 0,
            "experience_level": 1,
            "total_study_time": 0
        }
        
        # Act
        result = self.service.create(**user_data)
        
        # Assert
        self.mock_repository.create.assert_called_once_with(self.mock_db, **user_data)
        self.mock_db.rollback.assert_called_once()
        assert result is None
    
    def test_update(self):
        """Test updating an entity."""
        # Arrange
        self.mock_repository.update.return_value = self.test_user
        update_data = {
            "username": "updateduser",
            "email": "updated@example.com"
        }
        
        # Act
        result = self.service.update(self.test_user_id, **update_data)
        
        # Assert
        self.mock_repository.update.assert_called_once_with(self.mock_db, self.test_user_id, **update_data)
        assert result is self.test_user
    
    def test_update_exception(self):
        """Test updating an entity when an exception occurs."""
        # Arrange
        self.mock_repository.update.side_effect = Exception("Test exception")
        update_data = {
            "username": "updateduser",
            "email": "updated@example.com"
        }
        
        # Act
        result = self.service.update(self.test_user_id, **update_data)
        
        # Assert
        self.mock_repository.update.assert_called_once_with(self.mock_db, self.test_user_id, **update_data)
        self.mock_db.rollback.assert_called_once()
        assert result is None
    
    def test_delete(self):
        """Test deleting an entity."""
        # Arrange
        self.mock_repository.delete.return_value = True
        
        # Act
        result = self.service.delete(self.test_user_id)
        
        # Assert
        self.mock_repository.delete.assert_called_once_with(self.mock_db, self.test_user_id)
        assert result is True
    
    def test_delete_exception(self):
        """Test deleting an entity when an exception occurs."""
        # Arrange
        self.mock_repository.delete.side_effect = Exception("Test exception")
        
        # Act
        result = self.service.delete(self.test_user_id)
        
        # Assert
        self.mock_repository.delete.assert_called_once_with(self.mock_db, self.test_user_id)
        self.mock_db.rollback.assert_called_once()
        assert result is False
    
    def test_filter_by(self):
        """Test filtering entities by attributes."""
        # Arrange
        self.mock_repository.filter_by.return_value = [self.test_user]
        filter_data = {
            "age_group": "15-17"
        }
        
        # Act
        result = self.service.filter_by(**filter_data)
        
        # Assert
        self.mock_repository.filter_by.assert_called_once_with(self.mock_db, **filter_data)
        assert result == [self.test_user]
    
    def test_filter_by_exception(self):
        """Test filtering entities by attributes when an exception occurs."""
        # Arrange
        self.mock_repository.filter_by.side_effect = Exception("Test exception")
        filter_data = {
            "age_group": "15-17"
        }
        
        # Act
        result = self.service.filter_by(**filter_data)
        
        # Assert
        self.mock_repository.filter_by.assert_called_once_with(self.mock_db, **filter_data)
        assert result == []
    
    def test_count(self):
        """Test counting entities."""
        # Arrange
        self.mock_repository.count.return_value = 2
        
        # Act
        result = self.service.count()
        
        # Assert
        self.mock_repository.count.assert_called_once_with(self.mock_db)
        assert result == 2
    
    def test_count_exception(self):
        """Test counting entities when an exception occurs."""
        # Arrange
        self.mock_repository.count.side_effect = Exception("Test exception")
        
        # Act
        result = self.service.count()
        
        # Assert
        self.mock_repository.count.assert_called_once_with(self.mock_db)
        assert result == 0 