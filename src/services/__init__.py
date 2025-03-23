"""
Services module for Mathtermind application.

This module provides service interfaces for various application functionalities.
"""

from src.services.achievement_service import AchievementService
from src.services.content_service import ContentService
from src.services.goals_service import GoalsService
from src.services.progress_service import ProgressService
from src.services.tracking_service import TrackingService
from src.services.user_service import UserService
from src.services.course_service import CourseService
from src.services.lesson_service import LessonService
from src.services.settings_service import SettingsService
from src.services.credentials_manager import CredentialsManager

# Export all service classes
__all__ = [
    'AchievementService',
    'ContentService',
    'CourseService',
    'CredentialsManager',
    'GoalsService',
    'LessonService',
    'ProgressService',
    'SettingsService',
    'TrackingService',
    'UserService',
]
