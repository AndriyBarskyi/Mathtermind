"""
Services module for Mathtermind application.

This module provides service interfaces for various application functionalities.
"""

from src.services.achievement_service import AchievementService
from src.services.auth_service import AuthService
from src.services.content_service import ContentService
from src.services.goals_service import GoalsService
from src.services.permission_service import PermissionService
from src.services.progress_service import ProgressService
from src.services.session_manager import SessionManager
from src.services.tracking_service import TrackingService
from src.services.user_service import UserService
from src.services.course_service import CourseService
from src.services.lesson_service import LessonService
from src.services.settings_service import SettingsService
from src.services.credentials_manager import CredentialsManager
from src.services.user_stats_service import UserStatsService
from src.services.password_utils import (
    hash_password, 
    verify_password, 
    validate_password_strength,
    generate_reset_token,
    generate_temporary_password
)

# Export all service classes
__all__ = [
    'AchievementService',
    'AuthService',
    'ContentService',
    'CourseService',
    'CredentialsManager',
    'GoalsService',
    'LessonService',
    'PermissionService',
    'ProgressService',
    'SessionManager',
    'SettingsService',
    'TrackingService',
    'UserService',
    'UserStatsService',
    # Password utilities
    'hash_password',
    'verify_password',
    'validate_password_strength',
    'generate_reset_token',
    'generate_temporary_password'
]
