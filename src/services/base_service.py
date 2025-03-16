"""
Base service class for Mathtermind.

This module provides a base service class that defines the standard
operations and patterns to be used by all service implementations.
"""

import logging
from typing import Generic, TypeVar, List, Optional, Any, Dict, Type
from src.db import get_db
from src.db.models import Base

# Define a type variable for the model
T = TypeVar('T', bound=Base)


class BaseService(Generic[T]):
    """Base service class for business logic operations.
    
    This class defines the standard operations and patterns to be used by all
    service implementations. It is generic over the model type.
    """
    
    def __init__(self, repository=None):
        """Initialize the service with a repository.
        
        Args:
            repository: The repository to use for database operations.
        """
        self.repository = repository
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db = next(get_db())
    
    def get_by_id(self, id: Any) -> Optional[T]:
        """Get an entity by its ID.
        
        Args:
            id: The ID of the entity.
            
        Returns:
            The entity if found, None otherwise.
        """
        try:
            return self.repository.get_by_id(self.db, id)
        except Exception as e:
            self.logger.error(f"Error getting entity by ID: {str(e)}")
            return None
    
    def get_all(self) -> List[T]:
        """Get all entities.
        
        Returns:
            A list of all entities.
        """
        try:
            return self.repository.get_all(self.db)
        except Exception as e:
            self.logger.error(f"Error getting all entities: {str(e)}")
            return []
    
    def create(self, **kwargs) -> Optional[T]:
        """Create a new entity.
        
        Args:
            **kwargs: The attributes of the entity.
            
        Returns:
            The created entity if successful, None otherwise.
        """
        try:
            return self.repository.create(self.db, **kwargs)
        except Exception as e:
            self.logger.error(f"Error creating entity: {str(e)}")
            self.db.rollback()
            return None
    
    def update(self, id: Any, **kwargs) -> Optional[T]:
        """Update an entity.
        
        Args:
            id: The ID of the entity.
            **kwargs: The attributes to update.
            
        Returns:
            The updated entity if successful, None otherwise.
        """
        try:
            return self.repository.update(self.db, id, **kwargs)
        except Exception as e:
            self.logger.error(f"Error updating entity: {str(e)}")
            self.db.rollback()
            return None
    
    def delete(self, id: Any) -> bool:
        """Delete an entity.
        
        Args:
            id: The ID of the entity.
            
        Returns:
            True if the entity was deleted, False otherwise.
        """
        try:
            return self.repository.delete(self.db, id)
        except Exception as e:
            self.logger.error(f"Error deleting entity: {str(e)}")
            self.db.rollback()
            return False
    
    def filter_by(self, **kwargs) -> List[T]:
        """Filter entities by attributes.
        
        Args:
            **kwargs: The attributes to filter by.
            
        Returns:
            A list of entities matching the filter.
        """
        try:
            return self.repository.filter_by(self.db, **kwargs)
        except Exception as e:
            self.logger.error(f"Error filtering entities: {str(e)}")
            return []
    
    def count(self) -> int:
        """Count the number of entities.
        
        Returns:
            The number of entities.
        """
        try:
            return self.repository.count(self.db)
        except Exception as e:
            self.logger.error(f"Error counting entities: {str(e)}")
            return 0 