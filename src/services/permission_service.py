"""
Permission service for role-based access control in Mathtermind.

This module provides utilities for role-based access control,
including defining roles, permissions, and validation.
"""

import enum
from typing import Dict, List, Set, Optional, Any, Union

# Define permission levels as an enum
class Permission(enum.Enum):
    """Permissions available in the system."""
    
    # Content management
    VIEW_CONTENT = "view_content"
    CREATE_CONTENT = "create_content"
    EDIT_CONTENT = "edit_content"
    DELETE_CONTENT = "delete_content"
    
    # User management
    VIEW_USERS = "view_users"
    CREATE_USERS = "create_users"
    EDIT_USERS = "edit_users"
    DELETE_USERS = "delete_users"
    
    # Course management
    VIEW_COURSES = "view_courses"
    CREATE_COURSES = "create_courses"
    EDIT_COURSES = "edit_courses"
    DELETE_COURSES = "delete_courses"
    
    # Progress management
    VIEW_OWN_PROGRESS = "view_own_progress"
    VIEW_ALL_PROGRESS = "view_all_progress"
    
    # Statistics management
    VIEW_OWN_STATS = "view_own_stats"
    VIEW_ALL_STATS = "view_all_stats"
    
    # Settings management
    MANAGE_OWN_SETTINGS = "manage_own_settings"
    MANAGE_APP_SETTINGS = "manage_app_settings"


# Define roles
class Role(enum.Enum):
    """User roles in the system."""
    
    STUDENT = "student"
    ADMIN = "admin"


# Define role-permission mappings
ROLE_PERMISSIONS = {
    Role.STUDENT: {
        # Basic content and course viewing for studying
        Permission.VIEW_CONTENT,
        Permission.VIEW_COURSES,
        
        # Students can see their own progress and stats
        Permission.VIEW_OWN_PROGRESS,
        Permission.VIEW_OWN_STATS,
        Permission.MANAGE_OWN_SETTINGS,
    },
    Role.ADMIN: {
        permission for permission in Permission
    }  # Admins have all permissions
}


class PermissionService:
    """
    Service for handling permissions and access control.
    
    This service provides utilities for checking user permissions
    and validating access rights.
    """
    
    @staticmethod
    def get_role_permissions(role: Union[Role, str]) -> Set[Permission]:
        """
        Get all permissions for a role.
        
        Args:
            role: The role to get permissions for
            
        Returns:
            A set of permissions
        """
        if isinstance(role, str):
            try:
                role = Role(role)
            except ValueError:
                return set()
                
        return ROLE_PERMISSIONS.get(role, set())
    
    @staticmethod
    def user_has_permission(user: Dict[str, Any], permission: Union[Permission, str]) -> bool:
        """
        Check if a user has a specific permission.
        
        Args:
            user: The user object with 'is_admin' and 'role' fields
            permission: The permission to check
            
        Returns:
            True if the user has the permission, False otherwise
        """
        # Convert string permission to enum if needed
        if isinstance(permission, str):
            try:
                permission = Permission(permission)
            except ValueError:
                return False
        
        # Admins have all permissions
        if user.get('is_admin', False):
            return True
            
        # Get the user's role
        user_role = user.get('role')
        if not user_role:
            return False
            
        # Check if the permission is included in the role's permissions
        try:
            if isinstance(user_role, str):
                user_role = Role(user_role)
            return permission in ROLE_PERMISSIONS.get(user_role, set())
        except ValueError:
            return False
    
    @staticmethod
    def user_has_permissions(user: Dict[str, Any], permissions: List[Union[Permission, str]]) -> bool:
        """
        Check if a user has all specified permissions.
        
        Args:
            user: The user object with 'is_admin' and 'role' fields
            permissions: The permissions to check
            
        Returns:
            True if the user has all permissions, False otherwise
        """
        return all(PermissionService.user_has_permission(user, perm) for perm in permissions)
    
    @staticmethod
    def user_has_any_permission(user: Dict[str, Any], permissions: List[Union[Permission, str]]) -> bool:
        """
        Check if a user has any of the specified permissions.
        
        Args:
            user: The user object with 'is_admin' and 'role' fields
            permissions: The permissions to check
            
        Returns:
            True if the user has any of the permissions, False otherwise
        """
        return any(PermissionService.user_has_permission(user, perm) for perm in permissions)
    
    @staticmethod
    def is_resource_owner(user: Dict[str, Any], resource: Dict[str, Any]) -> bool:
        """
        Check if a user is the owner of a resource.
        
        Args:
            user: The user object with 'id' field
            resource: The resource with 'user_id' or 'author_id' field
            
        Returns:
            True if the user is the owner, False otherwise
        """
        user_id = str(user.get('id'))
        if not user_id:
            return False
            
        # Check common owner fields
        for field in ['user_id', 'author_id', 'owner_id', 'created_by']:
            if str(resource.get(field, '')) == user_id:
                return True
                
        return False
        
    @staticmethod
    def has_access_to_resource(user: Dict[str, Any], resource: Dict[str, Any], 
                             required_permission: Union[Permission, str]) -> bool:
        """
        Check if a user has access to a resource.
        
        This combines permission checks with ownership checks. Users can access
        a resource if they have the required permission or if they own the resource.
        
        Args:
            user: The user object
            resource: The resource object
            required_permission: The permission required to access the resource
            
        Returns:
            True if the user has access, False otherwise
        """
        # Always allow if the user has the permission
        if PermissionService.user_has_permission(user, required_permission):
            return True
            
        # Allow if the user is the owner (for their own resources)
        return PermissionService.is_resource_owner(user, resource)
        
    @staticmethod
    def get_user_role(user: Dict[str, Any]) -> Optional[Role]:
        """
        Get a user's role.
        
        Args:
            user: The user object
            
        Returns:
            The user's role or None if not found
        """
        # If user is admin, return admin role
        if user.get('is_admin', False):
            return Role.ADMIN
            
        # Get the role from the user object
        user_role = user.get('role')
        if not user_role:
            return None
            
        try:
            if isinstance(user_role, str):
                return Role(user_role)
            return user_role
        except ValueError:
            return None 