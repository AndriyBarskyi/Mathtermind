"""
Repository module for ContentState model in the Mathtermind application.
"""

from typing import List, Optional, Dict, Any, Union
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from src.db.models import ContentState
from .base_repository import BaseRepository


class ContentStateRepository(BaseRepository[ContentState]):
    """Repository for ContentState model."""
    
    def __init__(self):
        """Initialize the repository with the ContentState model."""
        super().__init__(ContentState)
    
    def create_content_state(self, db: Session, 
                           user_id: uuid.UUID, 
                           progress_id: uuid.UUID,
                           content_id: uuid.UUID,
                           state_type: str,
                           value: Union[float, Dict[str, Any], str] = None) -> ContentState:
        """
        Create a new content state record.
        
        Args:
            db: Database session
            user_id: User ID
            progress_id: Progress record ID
            content_id: Content ID
            state_type: Type of state (e.g., "scroll_position", "video_timestamp", "exercise_state")
            value: The state value - can be numeric, JSON, or text
            
        Returns:
            Created content state record
        """
        content_state = ContentState(
            user_id=user_id,
            progress_id=progress_id,
            content_id=content_id,
            state_type=state_type,
            updated_at=datetime.now(timezone.utc)
        )
        
        # Determine which field to use based on value type
        if isinstance(value, (int, float)):
            content_state.numeric_value = float(value)
        elif isinstance(value, dict):
            content_state.json_value = value
        elif isinstance(value, str):
            content_state.text_value = value
        
        db.add(content_state)
        db.commit()
        db.refresh(content_state)
        return content_state
    
    def get_content_state(self, db: Session, 
                        user_id: uuid.UUID, 
                        content_id: uuid.UUID,
                        state_type: str) -> Optional[ContentState]:
        """
        Get a specific content state record.
        
        Args:
            db: Database session
            user_id: User ID
            content_id: Content ID
            state_type: Type of state
            
        Returns:
            Content state record or None if not found
        """
        return db.query(ContentState).filter(
            ContentState.user_id == user_id,
            ContentState.content_id == content_id,
            ContentState.state_type == state_type
        ).first()
    
    def get_all_content_states(self, db: Session, 
                             user_id: uuid.UUID, 
                             content_id: uuid.UUID) -> List[ContentState]:
        """
        Get all state records for a specific content item.
        
        Args:
            db: Database session
            user_id: User ID
            content_id: Content ID
            
        Returns:
            List of content state records
        """
        return db.query(ContentState).filter(
            ContentState.user_id == user_id,
            ContentState.content_id == content_id
        ).all()
    
    def get_progress_content_states(self, db: Session, progress_id: uuid.UUID) -> List[ContentState]:
        """
        Get all state records for a specific progress record.
        
        Args:
            db: Database session
            progress_id: Progress record ID
            
        Returns:
            List of content state records
        """
        return db.query(ContentState).filter(
            ContentState.progress_id == progress_id
        ).all()
    
    def update_numeric_state(self, db: Session, 
                           state_id: uuid.UUID, 
                           value: float) -> Optional[ContentState]:
        """
        Update a numeric state value.
        
        Args:
            db: Database session
            state_id: Content state record ID
            value: New numeric value
            
        Returns:
            Updated content state record or None if not found
        """
        state = self.get_by_id(db, state_id)
        if state:
            state.numeric_value = value
            state.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(state)
        return state
    
    def update_json_state(self, db: Session, 
                        state_id: uuid.UUID, 
                        value: Dict[str, Any]) -> Optional[ContentState]:
        """
        Update a JSON state value.
        
        Args:
            db: Database session
            state_id: Content state record ID
            value: New JSON value
            
        Returns:
            Updated content state record or None if not found
        """
        state = self.get_by_id(db, state_id)
        if state:
            state.json_value = value
            state.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(state)
        return state
    
    def update_text_state(self, db: Session, 
                        state_id: uuid.UUID, 
                        value: str) -> Optional[ContentState]:
        """
        Update a text state value.
        
        Args:
            db: Database session
            state_id: Content state record ID
            value: New text value
            
        Returns:
            Updated content state record or None if not found
        """
        state = self.get_by_id(db, state_id)
        if state:
            state.text_value = value
            state.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(state)
        return state
    
    def update_or_create_state(self, db: Session, 
                             user_id: uuid.UUID, 
                             progress_id: uuid.UUID,
                             content_id: uuid.UUID,
                             state_type: str,
                             value: Union[float, Dict[str, Any], str]) -> ContentState:
        """
        Update an existing state or create a new one if it doesn't exist.
        
        Args:
            db: Database session
            user_id: User ID
            progress_id: Progress record ID
            content_id: Content ID
            state_type: Type of state
            value: The state value - can be numeric, JSON, or text
            
        Returns:
            Updated or created content state record
        """
        state = self.get_content_state(db, user_id, content_id, state_type)
        
        if state:
            # Update existing state
            if isinstance(value, (int, float)):
                state.numeric_value = float(value)
                state.json_value = None
                state.text_value = None
            elif isinstance(value, dict):
                state.numeric_value = None
                state.json_value = value
                state.text_value = None
            elif isinstance(value, str):
                state.numeric_value = None
                state.json_value = None
                state.text_value = value
                
            state.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(state)
            return state
        else:
            # Create new state
            return self.create_content_state(db, user_id, progress_id, content_id, state_type, value) 