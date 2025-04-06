"""
Tests for the enhanced base service implementation.

This module contains tests for the enhanced BaseService class to ensure that
it provides the expected functionality for all service implementations.
This includes tests for transaction management, caching, and validation.
"""

import pytest
import uuid
import time
from unittest.mock import patch, MagicMock, call
from datetime import timedelta

from src.services.base_service import (
    BaseService, 
    EntityNotFoundError, 
    ValidationError, 
    DatabaseError,
    ServiceError
)
from src.db.models import User
from src.tests.base_test_classes import BaseServiceTest
from src.tests.utils.test_factories import UserFactory
from sqlalchemy.exc import IntegrityError, DataError


@pytest.mark.service
@pytest.mark.unit
class TestEnhancedBaseService(BaseServiceTest):
    """Tests for the enhanced BaseService class."""
    
    def setUp(self):
        """Set up the test environment before each test."""
        super().setUp()
        
        # Create a mock repository
        self.mock_repository = MagicMock()
        
        # Create the service with the mock repository
        self.service = BaseService(repository=self.mock_repository, test_mode=True)
        
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

    # Transaction Management Tests
    
    def test_transaction_context_manager_success(self):
        """Test that the transaction context manager commits on success."""
        # Act
        with self.service.transaction():
            pass  # Do something that succeeds
        
        # Assert
        self.mock_db.commit.assert_called_once()
        self.mock_db.rollback.assert_not_called()
    
    def test_transaction_context_manager_exception(self):
        """Test that the transaction context manager rolls back on exception."""
        # Act/Assert
        with pytest.raises(Exception):
            with self.service.transaction():
                raise Exception("Test exception")
        
        # Assert
        self.mock_db.rollback.assert_called_once()
        self.mock_db.commit.assert_not_called()
    
    def test_transaction_context_manager_sqlalchemy_error(self):
        """Test that the transaction context manager handles SQLAlchemy errors."""
        # Act/Assert
        with pytest.raises(DatabaseError):
            with self.service.transaction():
                raise IntegrityError("statement", "params", "orig")
        
        # Assert
        self.mock_db.rollback.assert_called_once()
        self.mock_db.commit.assert_not_called()
    
    def test_execute_in_transaction(self):
        """Test executing a function in a transaction."""
        # Arrange
        mock_func = MagicMock()
        mock_func.return_value = "result"
        
        # Act
        result = self.service.execute_in_transaction(mock_func, "arg1", kwarg1="value")
        
        # Assert
        assert result == "result"
        mock_func.assert_called_once_with("arg1", kwarg1="value")
        self.mock_db.commit.assert_called_once()
    
    def test_batch_operation(self):
        """Test batch operation functionality."""
        # Arrange
        items = ["item1", "item2", "item3", "item4", "item5"]
        operation = MagicMock()
        
        # Act
        self.service.batch_operation(items, operation, batch_size=2)
        
        # Assert
        assert operation.call_count == 5
        assert self.mock_db.commit.call_count == 3  # 3 batches with size 2
    
    # Caching Tests
    
    def test_cache_decorator(self):
        """Test that the cache decorator caches function results."""
        # Arrange
        test_func = MagicMock()
        test_func.return_value = "cached_result"
        
        cached_func = self.service.cache("test_key")(test_func)
        
        # Act - First call should execute the function
        result1 = cached_func("arg1", kwarg1="value")
        
        # Act - Second call with same args should use cache
        result2 = cached_func("arg1", kwarg1="value")
        
        # Assert
        assert result1 == "cached_result"
        assert result2 == "cached_result"
        test_func.assert_called_once()  # Function should only be called once
    
    def test_cache_with_different_args(self):
        """Test that the cache uses different keys for different args."""
        # Arrange
        test_func = MagicMock()
        test_func.side_effect = ["result1", "result2"]
        
        cached_func = self.service.cache("test_key")(test_func)
        
        # Act - Call with different args
        result1 = cached_func("arg1")
        result2 = cached_func("arg2")
        
        # Assert
        assert result1 == "result1"
        assert result2 == "result2"
        assert test_func.call_count == 2  # Function should be called twice
    
    def test_cache_ttl_expiration(self):
        """Test that cached items expire after TTL."""
        # Arrange
        test_func = MagicMock()
        test_func.side_effect = ["result1", "result2"]
        
        # Use a very short TTL
        cached_func = self.service.cache("test_key", ttl=timedelta(milliseconds=1))(test_func)
        
        # Act - First call
        result1 = cached_func("arg")
        
        # Wait for TTL to expire
        time.sleep(0.01)
        
        # Act - Second call after expiration
        result2 = cached_func("arg")
        
        # Assert
        assert result1 == "result1"
        assert result2 == "result2"
        assert test_func.call_count == 2
    
    def test_invalidate_cache(self):
        """Test that invalidate_cache removes cache entries."""
        # Arrange
        test_func1 = MagicMock(return_value="result1")
        test_func2 = MagicMock(return_value="result2")
        
        cached_func1 = self.service.cache("key1")(test_func1)
        cached_func2 = self.service.cache("key2")(test_func2)
        
        # Call functions to populate cache
        cached_func1()
        cached_func2()
        
        # Act - Invalidate cache for key1
        self.service.invalidate_cache("key1")
        
        # Call functions again
        cached_func1()
        cached_func2()
        
        # Assert
        assert test_func1.call_count == 2  # Function should be called again
        assert test_func2.call_count == 1  # Function should not be called again
    
    def test_invalidate_all_cache(self):
        """Test that invalidate_cache without a key prefix clears all cache."""
        # Arrange
        test_func1 = MagicMock(return_value="result1")
        test_func2 = MagicMock(return_value="result2")
        
        cached_func1 = self.service.cache("key1")(test_func1)
        cached_func2 = self.service.cache("key2")(test_func2)
        
        # Call functions to populate cache
        cached_func1()
        cached_func2()
        
        # Act - Invalidate all cache
        self.service.invalidate_cache()
        
        # Call functions again
        cached_func1()
        cached_func2()
        
        # Assert
        assert test_func1.call_count == 2
        assert test_func2.call_count == 2
    
    def test_manage_cache_size(self):
        """Test that cache size is managed correctly."""
        # Arrange - Set a small max cache size
        self.service._max_cache_size = 2
        
        test_func = MagicMock()
        test_func.side_effect = ["result1", "result2", "result3"]
        
        cached_func = self.service.cache("test_key")(test_func)
        
        # Act - Fill cache beyond max size
        cached_func("arg1")
        cached_func("arg2")
        cached_func("arg3")
        
        # Force a cache management check
        self.service._manage_cache_size()
        
        # Assert
        assert len(self.service._cache) <= 2
    
    # Validation Tests
    
    def test_validate_success(self):
        """Test validation with valid data."""
        # Arrange
        data = {"name": "Valid Name", "age": 25}
        validators = {
            "name": lambda x: isinstance(x, str) and len(x) > 0,
            "age": lambda x: isinstance(x, int) and x > 0
        }
        
        # Act
        try:
            self.service.validate(data, validators)
            validation_passed = True
        except ValidationError:
            validation_passed = False
        
        # Assert
        assert validation_passed
    
    def test_validate_failure(self):
        """Test validation with invalid data."""
        # Arrange
        data = {"name": "", "age": -5}
        validators = {
            "name": lambda x: isinstance(x, str) and len(x) > 0,
            "age": lambda x: isinstance(x, int) and x > 0
        }
        
        # Act/Assert
        with pytest.raises(ValidationError):
            self.service.validate(data, validators)
    
    # Enhanced Error Handling Tests
    
    def test_get_by_id_not_found(self):
        """Test getting an entity by ID when it doesn't exist."""
        # Arrange
        self.mock_repository.get_by_id.return_value = None
        
        # Act/Assert
        with pytest.raises(EntityNotFoundError):
            self.service.get_by_id(self.test_user_id)
    
    def test_update_entity_not_found(self):
        """Test updating an entity when it doesn't exist."""
        # Arrange
        self.mock_repository.get_by_id.return_value = None
        
        # Act/Assert
        with pytest.raises(EntityNotFoundError):
            self.service.update(self.test_user_id, username="newname")
    
    def test_delete_entity_not_found(self):
        """Test deleting an entity when it doesn't exist."""
        # Arrange
        self.mock_repository.get_by_id.return_value = None
        
        # Act/Assert
        with pytest.raises(EntityNotFoundError):
            self.service.delete(self.test_user_id)
    
    def test_exists(self):
        """Test the exists method."""
        # Arrange
        self.mock_repository.exists.return_value = True
        
        # Act
        result = self.service.exists(self.test_user_id)
        
        # Assert
        assert result is True
        self.mock_repository.exists.assert_called_once_with(self.mock_db, self.test_user_id)
    
    def test_exists_exception(self):
        """Test the exists method when an exception occurs."""
        # Arrange
        self.mock_repository.exists.side_effect = Exception("Database error")
        
        # Act/Assert
        with pytest.raises(Exception):
            self.service.exists(self.test_user_id)
        
        # Verify the call was made
        self.mock_repository.exists.assert_called_once_with(self.mock_db, self.test_user_id) 