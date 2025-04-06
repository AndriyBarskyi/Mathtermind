from sqlalchemy.orm import Session
import uuid
import json
import logging
from src.db import get_db
from src.db.models import UserSetting, User

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
            settings = self.db.query(UserSetting).filter(UserSetting.user_id == user_id).first()
            
            if not settings:
                return self._get_default_settings()
                
            # Convert the ORM model to a dictionary
            return {
                "theme": settings.theme.value if settings.theme else "light",
                "notifications": {
                    "daily_reminder": settings.notification_daily_reminder,
                    "achievement_alerts": settings.notification_achievement_alerts,
                    "study_time": settings.notification_study_time
                },
                "accessibility": {
                    "font_size": settings.accessibility_font_size.value if settings.accessibility_font_size else "medium",
                    "high_contrast": settings.accessibility_high_contrast
                },
                "study_preferences": {
                    "daily_goal_minutes": settings.study_daily_goal_minutes,
                    "preferred_subject": settings.study_preferred_subject.value if settings.study_preferred_subject else "Math"
                }
            }
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
            existing_settings = self.db.query(UserSetting).filter(UserSetting.user_id == user_id).first()
            
            # Extract values from settings_data
            theme = settings_data.get("theme", "light")
            notifications = settings_data.get("notifications", {})
            accessibility = settings_data.get("accessibility", {})
            study_preferences = settings_data.get("study_preferences", {})
            
            if existing_settings:
                # Update existing settings
                existing_settings.theme = theme
                existing_settings.notification_daily_reminder = notifications.get("daily_reminder", True)
                existing_settings.notification_achievement_alerts = notifications.get("achievement_alerts", True)
                existing_settings.notification_study_time = notifications.get("study_time", "18:00")
                existing_settings.accessibility_font_size = accessibility.get("font_size", "medium")
                existing_settings.accessibility_high_contrast = accessibility.get("high_contrast", False)
                existing_settings.study_daily_goal_minutes = study_preferences.get("daily_goal_minutes", 30)
                existing_settings.study_preferred_subject = study_preferences.get("preferred_subject", "Math")
            else:
                # Create new settings
                new_settings = UserSetting(
                    id=uuid.uuid4(),
                    user_id=user_id,
                    theme=theme,
                    notification_daily_reminder=notifications.get("daily_reminder", True),
                    notification_achievement_alerts=notifications.get("achievement_alerts", True),
                    notification_study_time=notifications.get("study_time", "18:00"),
                    accessibility_font_size=accessibility.get("font_size", "medium"),
                    accessibility_high_contrast=accessibility.get("high_contrast", False),
                    study_daily_goal_minutes=study_preferences.get("daily_goal_minutes", 30),
                    study_preferred_subject=study_preferences.get("preferred_subject", "Math")
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