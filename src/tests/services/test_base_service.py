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
from src.tests.utils.test_factories import UserFactory


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
        
        # Create a test user using the factory
        self.test_user = UserFactory.create(
            id=self.test_user_id,
            username="testuser",
            email="testuser@example.com"
        )
    
    def test_get_by_id(self):
        """Test getting an entity by ID."""
        # Arrange
        self.mock_repository.get_by_id.return_value = self.test_user
        
        # Act
        result = self.service.get_by_id(self.test_user_id)
        
        # Assert
        assert result == self.test_user
        self.mock_repository.get_by_id.assert_called_once_with(self.mock_db, self.test_user_id)
    
    def test_get_by_id_exception(self):
        """Test getting an entity by ID when an exception occurs."""
        # Arrange
        self.mock_repository.get_by_id.side_effect = Exception("Database error")
        
        # Act
        result = self.service.get_by_id(self.test_user_id)
        
        # Assert
        assert result is None
        self.mock_repository.get_by_id.assert_called_once_with(self.mock_db, self.test_user_id)
    
    def test_get_all(self):
        """Test getting all entities."""
        # Arrange
        # Create multiple users using the factory
        users = UserFactory.create_batch(3)
        self.mock_repository.get_all.return_value = users
        
        # Act
        result = self.service.get_all()
        
        # Assert
        assert result == users
        self.mock_repository.get_all.assert_called_once_with(self.mock_db)
    
    def test_get_all_exception(self):
        """Test getting all entities when an exception occurs."""
        # Arrange
        self.mock_repository.get_all.side_effect = Exception("Database error")
        
        # Act
        result = self.service.get_all()
        
        # Assert
        assert result == []
        self.mock_repository.get_all.assert_called_once_with(self.mock_db)
    
    def test_create(self):
        """Test creating an entity."""
        # Arrange
        # Use the factory to generate user data
        user_data = UserFactory._get_defaults()
        user_data['id'] = self.test_user_id
        
        self.mock_repository.create.return_value = self.test_user
        
        # Act
        result = self.service.create(**user_data)
        
        # Assert
        assert result == self.test_user
        self.mock_repository.create.assert_called_once_with(self.mock_db, **user_data)
    
    def test_create_exception(self):
        """Test creating an entity when an exception occurs."""
        # Arrange
        # Use the factory to generate user data
        user_data = UserFactory._get_defaults()
        user_data['id'] = self.test_user_id
        
        self.mock_repository.create.side_effect = Exception("Database error")
        
        # Act
        result = self.service.create(**user_data)
        
        # Assert
        assert result is None
        self.mock_repository.create.assert_called_once_with(self.mock_db, **user_data)
    
    def test_update(self):
        """Test updating an entity."""
        # Arrange
        update_data = {"username": "updateduser"}
        self.mock_repository.update.return_value = True
        
        # Act
        result = self.service.update(self.test_user_id, **update_data)
        
        # Assert
        assert result is True
        self.mock_repository.update.assert_called_once_with(self.mock_db, self.test_user_id, **update_data)
    
    def test_update_exception(self):
        """Test updating an entity when an exception occurs."""
        # Arrange
        update_data = {"username": "updateduser"}
        self.mock_repository.update.side_effect = Exception("Database error")
        
        # Act
        result = self.service.update(self.test_user_id, **update_data)
        
        # Assert
        assert result is None
        self.mock_repository.update.assert_called_once_with(self.mock_db, self.test_user_id, **update_data)
    
    def test_delete(self):
        """Test deleting an entity."""
        # Arrange
        self.mock_repository.delete.return_value = True
        
        # Act
        result = self.service.delete(self.test_user_id)
        
        # Assert
        assert result is True
        self.mock_repository.delete.assert_called_once_with(self.mock_db, self.test_user_id)
    
    def test_delete_exception(self):
        """Test deleting an entity when an exception occurs."""
        # Arrange
        self.mock_repository.delete.side_effect = Exception("Database error")
        
        # Act
        result = self.service.delete(self.test_user_id)
        
        # Assert
        assert result is False
        self.mock_repository.delete.assert_called_once_with(self.mock_db, self.test_user_id)
    
    def test_filter_by(self):
        """Test filtering entities by criteria."""
        # Arrange
        # Create multiple users with different attributes using the factory
        users = [
            UserFactory.create(username=f"filteruser{i}", points=i*100)
            for i in range(1, 4)
        ]
        
        filter_criteria = {"username": "filteruser1"}
        self.mock_repository.filter_by.return_value = [users[0]]
        
        # Act
        result = self.service.filter_by(**filter_criteria)
        
        # Assert
        assert result == [users[0]]
        self.mock_repository.filter_by.assert_called_once_with(self.mock_db, **filter_criteria)
    
    def test_filter_by_exception(self):
        """Test filtering entities when an exception occurs."""
        # Arrange
        filter_criteria = {"username": "filteruser1"}
        self.mock_repository.filter_by.side_effect = Exception("Database error")
        
        # Act
        result = self.service.filter_by(**filter_criteria)
        
        # Assert
        assert result == []
        self.mock_repository.filter_by.assert_called_once_with(self.mock_db, **filter_criteria)
    
    def test_count(self):
        """Test counting entities."""
        # Arrange
        self.mock_repository.count.return_value = 5
        
        # Act
        result = self.service.count()
        
        # Assert
        assert result == 5
        self.mock_repository.count.assert_called_once_with(self.mock_db)
    
    def test_count_exception(self):
        """Test counting entities when an exception occurs."""
        # Arrange
        self.mock_repository.count.side_effect = Exception("Database error")
        
        # Act
        result = self.service.count()
        
        # Assert
        assert result == 0
        self.mock_repository.count.assert_called_once_with(self.mock_db) 