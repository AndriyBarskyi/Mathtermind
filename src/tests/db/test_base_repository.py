"""
Tests for the base repository implementation.

This module contains tests for the BaseRepository class to ensure that
it provides the expected functionality for all repository implementations.
"""

import pytest
import uuid
from datetime import datetime, timezone
from src.db.repositories.base_repository import BaseRepository
from src.db.models import User


@pytest.mark.repository
@pytest.mark.unit
class TestBaseRepository:
    """Tests for the BaseRepository class."""
    
    def setup_method(self):
        """Set up the test environment before each test."""
        self.user_repo = BaseRepository(User)
    
    def test_get_by_id(self, test_db, test_user):
        """Test getting an entity by ID."""
        # Arrange
        user_id = test_user.id
        
        # Act
        result = self.user_repo.get_by_id(test_db, user_id)
        
        # Assert
        assert result is not None
        assert result.id == user_id
        assert result.username == "testuser"
        assert result.email == "testuser@example.com"
    
    def test_get_all(self, test_db, test_user):
        """Test getting all entities."""
        # Arrange
        # Create another user
        self.user_repo.create(
            test_db,
            id=uuid.uuid4(),
            username="anotheruser",
            email="another@example.com",
            password_hash="hashed_password",
            age_group="15-17",
            points=0,
            experience_level=1,
            total_study_time=0,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        # Act
        result = self.user_repo.get_all(test_db)
        
        # Assert
        assert len(result) == 2
        assert any(user.username == "testuser" for user in result)
        assert any(user.username == "anotheruser" for user in result)
    
    def test_create(self, test_db):
        """Test creating a new entity."""
        # Arrange
        user_id = uuid.uuid4()
        user_data = {
            "id": user_id,
            "username": "newuser",
            "email": "newuser@example.com",
            "password_hash": "hashed_password",
            "age_group": "15-17",
            "points": 0,
            "experience_level": 1,
            "total_study_time": 0,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        
        # Act
        result = self.user_repo.create(test_db, **user_data)
        
        # Assert
        assert result is not None
        assert result.id == user_id
        assert result.username == "newuser"
        assert result.email == "newuser@example.com"
        
        # Verify the user was added to the database
        db_user = test_db.query(User).filter(User.id == user_id).first()
        assert db_user is not None
        assert db_user.username == "newuser"
    
    def test_update(self, test_db, test_user):
        """Test updating an entity."""
        # Arrange
        user_id = test_user.id
        update_data = {
            "username": "updateduser",
            "email": "updated@example.com"
        }
        
        # Act
        result = self.user_repo.update(test_db, user_id, **update_data)
        
        # Assert
        assert result is not None
        assert result.id == user_id
        assert result.username == "updateduser"
        assert result.email == "updated@example.com"
        
        # Verify the user was updated in the database
        db_user = test_db.query(User).filter(User.id == user_id).first()
        assert db_user is not None
        assert db_user.username == "updateduser"
        assert db_user.email == "updated@example.com"
    
    def test_delete(self, test_db, test_user):
        """Test deleting an entity."""
        # Arrange
        user_id = test_user.id
        
        # Act
        result = self.user_repo.delete(test_db, user_id)
        
        # Assert
        assert result is True
        
        # Verify the user was deleted from the database
        db_user = test_db.query(User).filter(User.id == user_id).first()
        assert db_user is None
    
    def test_filter_by(self, test_db, test_user):
        """Test filtering entities by attributes."""
        # Arrange
        # Create another user
        self.user_repo.create(
            test_db,
            id=uuid.uuid4(),
            username="anotheruser",
            email="another@example.com",
            password_hash="hashed_password",
            age_group="13-14",  # Different age group
            points=0,
            experience_level=1,
            total_study_time=0,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        # Act
        result = self.user_repo.filter_by(test_db, age_group="15-17")
        
        # Assert
        assert len(result) == 1
        assert result[0].username == "testuser"
        assert result[0].age_group == "15-17"
    
    def test_count(self, test_db, test_user):
        """Test counting entities."""
        # Arrange
        # Create another user
        self.user_repo.create(
            test_db,
            id=uuid.uuid4(),
            username="anotheruser",
            email="another@example.com",
            password_hash="hashed_password",
            age_group="15-17",
            points=0,
            experience_level=1,
            total_study_time=0,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        # Act
        result = self.user_repo.count(test_db)
        
        # Assert
        assert result == 2 