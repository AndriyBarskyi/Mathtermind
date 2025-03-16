from sqlalchemy.orm import Session
import uuid
import json
import logging
from src.db import get_db
from src.db.models import Setting, User

# Set up logging
logger = logging.getLogger(__name__)

class SettingsService:
    """Service for managing user settings."""
    
    def __init__(self):
        """Initialize the settings service."""
        self.db = next(get_db())
        
    def get_user_settings(self, user_id=None):
        """
        Get settings for a user.
        
        Args:
            user_id: The UUID of the user. If None, returns default settings.
            
        Returns:
            dict: The user's settings or default settings.
        """
        if not user_id:
            return self._get_default_settings()
        
        try:
            # Convert string ID to UUID if it's a string
            if isinstance(user_id, str):
                user_id = uuid.UUID(user_id)
                
            # Query the database for user settings
            settings = self.db.query(Setting).filter(Setting.user_id == user_id).first()
            
            if not settings:
                return self._get_default_settings()
                
            return settings.preferences
        except Exception as e:
            logger.error(f"Error getting user settings: {str(e)}")
            return self._get_default_settings()
        
    def save_user_settings(self, settings_data, user_id=None):
        """
        Save settings for a user.
        
        Args:
            settings_data: Dictionary containing the settings to save.
            user_id: The UUID of the user. If None, settings are not saved.
            
        Returns:
            bool: True if settings were saved successfully, False otherwise.
        """
        if not user_id:
            # In a real app, we would get the current user's ID
            # For now, just log the settings that would be saved
            logger.info(f"Would save settings: {settings_data}")
            return True
            
        try:
            # Convert string ID to UUID if it's a string
            if isinstance(user_id, str):
                user_id = uuid.UUID(user_id)
                
            # Check if settings already exist for this user
            existing_settings = self.db.query(Setting).filter(Setting.user_id == user_id).first()
            
            if existing_settings:
                # Update existing settings
                existing_settings.preferences = settings_data
            else:
                # Create new settings
                new_settings = Setting(
                    id=uuid.uuid4(),
                    user_id=user_id,
                    preferences=settings_data
                )
                self.db.add(new_settings)
                
            # Commit changes
            self.db.commit()
            return True
            
        except Exception as e:
            # Log the error
            logger.error(f"Error saving settings: {e}")
            self.db.rollback()
            return False
            
    def _get_default_settings(self):
        """
        Get default settings.
        
        Returns:
            dict: Default settings.
        """
        return {
            "theme": "light",
            "notifications": {
                "daily_reminder": True,
                "achievement_alerts": True,
                "study_time": "18:00"
            },
            "accessibility": {
                "font_size": "medium",
                "high_contrast": False
            },
            "study_preferences": {
                "daily_goal_minutes": 30,
                "preferred_subject": "Math"
            }
        } 