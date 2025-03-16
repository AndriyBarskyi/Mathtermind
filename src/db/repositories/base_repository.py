"""
Base repository interface for Mathtermind.

This module provides a base repository interface that defines the standard
operations to be supported by all repository implementations.
"""

from typing import Generic, TypeVar, List, Optional, Any, Dict, Type
from sqlalchemy.orm import Session
from src.db.models import Base

# Define a type variable for the model
T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T]):
    """Base repository interface for database operations.
    
    This class defines the standard operations to be supported by all
    repository implementations. It is generic over the model type.
    """
    
    def __init__(self, model: Type[T]):
        """Initialize the repository with the model class.
        
        Args:
            model: The SQLAlchemy model class.
        """
        self.model = model
    
    def get_by_id(self, db: Session, id: Any) -> Optional[T]:
        """Get an entity by its ID.
        
        Args:
            db: The database session.
            id: The ID of the entity.
            
        Returns:
            The entity if found, None otherwise.
        """
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, db: Session) -> List[T]:
        """Get all entities.
        
        Args:
            db: The database session.
            
        Returns:
            A list of all entities.
        """
        return db.query(self.model).all()
    
    def create(self, db: Session, **kwargs) -> T:
        """Create a new entity.
        
        Args:
            db: The database session.
            **kwargs: The attributes of the entity.
            
        Returns:
            The created entity.
        """
        entity = self.model(**kwargs)
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity
    
    def update(self, db: Session, id: Any, **kwargs) -> Optional[T]:
        """Update an entity.
        
        Args:
            db: The database session.
            id: The ID of the entity.
            **kwargs: The attributes to update.
            
        Returns:
            The updated entity if found, None otherwise.
        """
        entity = self.get_by_id(db, id)
        if entity:
            for key, value in kwargs.items():
                setattr(entity, key, value)
            db.commit()
            db.refresh(entity)
        return entity
    
    def delete(self, db: Session, id: Any) -> bool:
        """Delete an entity.
        
        Args:
            db: The database session.
            id: The ID of the entity.
            
        Returns:
            True if the entity was deleted, False otherwise.
        """
        entity = self.get_by_id(db, id)
        if entity:
            db.delete(entity)
            db.commit()
            return True
        return False
    
    def filter_by(self, db: Session, **kwargs) -> List[T]:
        """Filter entities by attributes.
        
        Args:
            db: The database session.
            **kwargs: The attributes to filter by.
            
        Returns:
            A list of entities matching the filter.
        """
        return db.query(self.model).filter_by(**kwargs).all()
    
    def count(self, db: Session) -> int:
        """Count the number of entities.
        
        Args:
            db: The database session.
            
        Returns:
            The number of entities.
        """
        return db.query(self.model).count() 