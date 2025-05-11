"""
Services module for Mathtermind application.

This module provides service interfaces for various application functionalities.
"""

from src.services.base_service import BaseService
from src.services.auth_service import AuthService
from src.services.user_service import UserService
from src.services.course_service import CourseService
from src.services.lesson_service import LessonService
from src.services.content_service import ContentService
from src.services.progress_service import ProgressService
from src.services.settings_service import SettingsService
from src.services.permission_service import PermissionService
from src.services.content_type_registry import ContentTypeRegistry
from src.services.content_validation_service import ContentValidationService
from src.services.assessment_service import AssessmentService
from src.services.user_stats_service import UserStatsService
from src.services.tracking_service import TrackingService
from src.services.tag_service import TagService
from src.services.session_manager import SessionManager
from src.services.credentials_manager import CredentialsManager
from src.services.achievement_service import AchievementService
from src.services.goals_service import GoalsService
from src.services.math_tools_service import MathToolsService
from src.services.cs_tools_service import CSToolsService
from src.services.interactive_content_handler_service import InteractiveContentHandlerService
from src.services.password_utils import (
    hash_password, 
    verify_password, 
    validate_password_strength,
    generate_reset_token,
    generate_temporary_password
)

# Export all service classes
__all__ = [
    'BaseService',
    'AuthService',
    'UserService',
    'CourseService',
    'LessonService',
    'ContentService',
    'ProgressService',
    'SettingsService',
    'PermissionService',
    'ContentTypeRegistry',
    'ContentValidationService',
    'AssessmentService',
    'UserStatsService',
    'TrackingService',
    'TagService',
    'SessionManager',
    'CredentialsManager',
    'AchievementService',
    'GoalsService',
    'MathToolsService',
    'CSToolsService',
    'InteractiveContentHandlerService',
    # Password utilities
    'hash_password',
    'verify_password',
    'validate_password_strength',
    'generate_reset_token',
    'generate_temporary_password'
]

# Services registry to hold service instances
_services = {}

def init_services(config):
    """
    Initialize all application services.
    
    Args:
        config: Application configuration dictionary
    
    Returns:
        Dictionary of initialized service instances
    """
    # Initialize content type registry first
    content_registry = ContentTypeRegistry()
    _services['content_registry'] = content_registry
    
    # Initialize validation service
    validation_service = ContentValidationService()
    _services['validation_service'] = validation_service
    
    # Initialize core services
    _services['auth_service'] = AuthService(config)
    _services['user_service'] = UserService(config)
    _services['settings_service'] = SettingsService(config)
    _services['permission_service'] = PermissionService(config)
    
    # Initialize content services
    _services['content_service'] = ContentService(config)
    _services['course_service'] = CourseService(config)
    _services['lesson_service'] = LessonService(config)
    
    # Initialize tracking and progress services
    _services['progress_service'] = ProgressService(config)
    _services['tracking_service'] = TrackingService(config)
    _services['assessment_service'] = AssessmentService(config)
    _services['user_stats_service'] = UserStatsService(config)
    
    # Initialize security services
    _services['session_manager'] = SessionManager(config)
    _services['credentials_manager'] = CredentialsManager(config)
    
    # Initialize achievement and goals services
    _services['achievement_service'] = AchievementService(config)
    _services['goals_service'] = GoalsService(config)
    
    # Initialize tag service
    _services['tag_service'] = TagService(config)
    
    # Initialize tools services
    _services['math_tools_service'] = MathToolsService(config)
    _services['cs_tools_service'] = CSToolsService(config)
    
    # Initialize interactive content handler
    _services['interactive_content_handler'] = InteractiveContentHandlerService(config)
    
    return _services

def get_service(service_name):
    """
    Get a service instance by name.
    
    Args:
        service_name: Name of the service to retrieve
        
    Returns:
        Service instance if found, None otherwise
    """
    return _services.get(service_name)

#