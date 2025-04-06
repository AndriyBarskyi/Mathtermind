"""
Settings service for Mathtermind.

This module provides a service for managing user settings,
including retrieving, updating, and applying default settings.
"""

from sqlalchemy.orm import Session
import uuid
from typing import Dict, Any, Optional
from src.db import get_db
from src.db.models import UserSetting, User
from src.services.base_service import BaseService

# Import our logging and error handling framework
from src.core import get_logger
from src.core.error_handling import (
    handle_service_errors,
    ServiceError,
    ValidationError,
    ResourceNotFoundError,
    DatabaseError,
    create_error_boundary,
    report_error
)

# Set up logging
logger = get_logger(__name__)


class SettingsService(BaseService):
    """Service for managing user settings."""
    
    def __init__(self):
        """Initialize the settings service."""
        super().__init__()
        logger.debug("SettingsService initialized")
    
    @handle_service_errors(service_name="settings")
    def get_user_settings(self, user_id=None) -> Dict[str, Any]:
        """
        Get settings for a user.
        
        Args:
            user_id: The UUID of the user. If None, returns default settings.
            
        Returns:
            The user's settings or default settings.
            
        Raises:
            ResourceNotFoundError: If the user does not exist.
            DatabaseError: If there is an error retrieving settings.
        """
        if not user_id:
            logger.debug("No user ID provided, returning default settings")
            return self._get_default_settings()
        
        logger.info(f"Fetching settings for user: {user_id}")
        
        try:
            # Convert string ID to UUID if it's a string
            if isinstance(user_id, str):
                try:
                    user_id = uuid.UUID(user_id)
                    logger.debug(f"Converted string ID to UUID: {user_id}")
                except ValueError:
                    logger.error(f"Invalid UUID format: {user_id}")
                    raise ValidationError(
                        message=f"Invalid user ID format: {user_id}",
                        field="user_id",
                        value=user_id
                    )
                
            # Check if user exists
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                logger.warning(f"User not found: {user_id}")
                raise ResourceNotFoundError(
                    message=f"User with ID {user_id} not found",
                    resource_type="user",
                    resource_id=str(user_id)
                )
                
            # Query the database for user settings
            with create_error_boundary("fetch_user_settings"):
                settings = self.db.query(UserSetting).filter(UserSetting.user_id == user_id).first()
                
                if not settings:
                    logger.info(f"No settings found for user {user_id}, returning defaults")
                    return self._get_default_settings()
            
            # Convert the ORM model to a dictionary
            user_settings = {
                "theme": settings.theme.value if hasattr(settings, 'theme') and settings.theme else "light",
                "notifications": {
                    "daily_reminder": settings.notification_daily_reminder,
                    "achievement_alerts": settings.notification_achievement_alerts,
                    "study_time": settings.notification_study_time
                },
                "accessibility": {
                    "font_size": settings.accessibility_font_size.value if hasattr(settings, 'accessibility_font_size') and settings.accessibility_font_size else "medium",
                    "high_contrast": settings.accessibility_high_contrast
                },
                "study_preferences": {
                    "daily_goal_minutes": settings.study_daily_goal_minutes,
                    "preferred_subject": settings.study_preferred_subject.value if hasattr(settings, 'study_preferred_subject') and settings.study_preferred_subject else "Math"
                }
            }
            
            logger.debug(f"Retrieved settings for user {user_id}")
            return user_settings
            
        except (ValidationError, ResourceNotFoundError):
            # Let these errors propagate up
            raise
        except Exception as e:
            logger.error(f"Error getting user settings: {str(e)}")
            report_error(e, operation="get_user_settings", user_id=str(user_id))
            raise DatabaseError(
                message=f"Failed to retrieve settings for user {user_id}",
                details={"error": str(e), "user_id": str(user_id)}
            ) from e
    
    @handle_service_errors(service_name="settings")
    def save_user_settings(self, settings_data: Dict[str, Any], user_id=None) -> bool:
        """
        Save settings for a user.
        
        Args:
            settings_data: Dictionary containing the settings to save.
            user_id: The UUID of the user. If None, settings are not saved.
            
        Returns:
            True if settings were saved successfully.
            
        Raises:
            ValidationError: If settings data is invalid.
            ResourceNotFoundError: If the user does not exist.
            DatabaseError: If there is an error saving settings.
        """
        if not user_id:
            # In a real app, we would get the current user's ID
            # For now, just log the settings that would be saved
            logger.info(f"No user ID provided, settings not saved: {settings_data}")
            return True
            
        logger.info(f"Saving settings for user: {user_id}")
        
        if not settings_data:
            logger.warning(f"Empty settings data for user {user_id}")
            raise ValidationError(
                message="Settings data cannot be empty",
                field="settings_data",
                value=settings_data
            )
            
        try:
            # Convert string ID to UUID if it's a string
            if isinstance(user_id, str):
                try:
                    user_id = uuid.UUID(user_id)
                    logger.debug(f"Converted string ID to UUID: {user_id}")
                except ValueError:
                    logger.error(f"Invalid UUID format: {user_id}")
                    raise ValidationError(
                        message=f"Invalid user ID format: {user_id}",
                        field="user_id",
                        value=user_id
                    )
            
            # Check if user exists
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                logger.warning(f"User not found: {user_id}")
                raise ResourceNotFoundError(
                    message=f"User with ID {user_id} not found",
                    resource_type="user",
                    resource_id=str(user_id)
                )
                
            # Extract values from settings_data
            theme = settings_data.get("theme", "light")
            notifications = settings_data.get("notifications", {})
            accessibility = settings_data.get("accessibility", {})
            study_preferences = settings_data.get("study_preferences", {})
            
            # Validate settings before saving
            self._validate_settings(theme, notifications, accessibility, study_preferences)
            
            # Begin transaction
            with self.transaction():
                logger.debug(f"Beginning transaction to save settings for user {user_id}")
                
                # Check if settings already exist for this user
                existing_settings = self.db.query(UserSetting).filter(UserSetting.user_id == user_id).first()
                
                if existing_settings:
                    logger.debug(f"Updating existing settings for user {user_id}")
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
                    logger.debug(f"Creating new settings for user {user_id}")
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
            
            logger.info(f"Settings saved successfully for user {user_id}")
            return True
            
        except (ValidationError, ResourceNotFoundError):
            # Let these errors propagate up
            raise
        except Exception as e:
            logger.error(f"Error saving settings: {str(e)}")
            report_error(e, operation="save_user_settings", user_id=str(user_id))
            raise DatabaseError(
                message=f"Failed to save settings for user {user_id}",
                details={"error": str(e), "user_id": str(user_id)}
            ) from e
    
    @handle_service_errors(service_name="settings")
    def _validate_settings(self, theme, notifications, accessibility, study_preferences):
        """
        Validate settings data.
        
        Args:
            theme: The theme setting.
            notifications: Notification settings.
            accessibility: Accessibility settings.
            study_preferences: Study preference settings.
            
        Raises:
            ValidationError: If settings data is invalid.
        """
        logger.debug("Validating settings data")
        
        # Validate theme
        valid_themes = ["light", "dark", "system"]
        if theme not in valid_themes:
            logger.warning(f"Invalid theme: {theme}")
            raise ValidationError(
                message=f"Invalid theme: {theme}. Must be one of {valid_themes}",
                field="theme",
                value=theme
            )
        
        # Validate notification study time format (HH:MM)
        study_time = notifications.get("study_time", "18:00")
        try:
            hours, minutes = study_time.split(":")
            if not (0 <= int(hours) <= 23 and 0 <= int(minutes) <= 59):
                raise ValueError("Invalid time format")
        except ValueError:
            logger.warning(f"Invalid study time format: {study_time}")
            raise ValidationError(
                message=f"Invalid study time format: {study_time}. Must be in HH:MM format",
                field="notifications.study_time",
                value=study_time
            )
        
        # Validate font size
        valid_font_sizes = ["small", "medium", "large", "extra-large"]
        font_size = accessibility.get("font_size", "medium")
        if font_size not in valid_font_sizes:
            logger.warning(f"Invalid font size: {font_size}")
            raise ValidationError(
                message=f"Invalid font size: {font_size}. Must be one of {valid_font_sizes}",
                field="accessibility.font_size",
                value=font_size
            )
        
        # Validate daily goal minutes (must be positive)
        daily_goal_minutes = study_preferences.get("daily_goal_minutes", 30)
        if not isinstance(daily_goal_minutes, int) or daily_goal_minutes <= 0:
            logger.warning(f"Invalid daily goal minutes: {daily_goal_minutes}")
            raise ValidationError(
                message=f"Daily goal minutes must be a positive integer, got: {daily_goal_minutes}",
                field="study_preferences.daily_goal_minutes",
                value=daily_goal_minutes
            )
        
        logger.debug("Settings validation successful")
    
    @handle_service_errors(service_name="settings")
    def _get_default_settings(self) -> Dict[str, Any]:
        """
        Get default settings.
        
        Returns:
            Default settings dictionary.
        """
        logger.debug("Getting default settings")
        
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