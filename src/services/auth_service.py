"""
Authentication service for Mathtermind.

This module provides a comprehensive authentication service
with features including login, registration, password management,
session handling, and role-based access control.
"""

import logging
import re
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union

from src.db import get_db
from src.db.models import User
from src.db.repositories import user_repo
from src.services.base_service import BaseService, EntityNotFoundError, ValidationError
from src.services.password_utils import (
    hash_password, 
    verify_password, 
    validate_password_strength,
    generate_reset_token,
    generate_temporary_password
)
from src.services.session_manager import SessionManager
from src.services.permission_service import PermissionService, Permission, Role

# Set up logging
logger = logging.getLogger(__name__)

# Constants
PASSWORD_RESET_EXPIRY = 24 * 60 * 60  # 24 hours in seconds
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


class AuthService(BaseService):
    """
    Authentication service for user management and access control.
    
    This service handles user authentication, session management,
    password management, and access control.
    """
    
    def __init__(self):
        """Initialize the authentication service."""
        super().__init__(repository=user_repo)
        self.session_manager = SessionManager()
        self.permission_service = PermissionService()
        
        # Store password reset tokens with expiry
        self._reset_tokens = {}  # token: {"user_id": id, "expires_at": timestamp}
    
    def login(self, username_or_email: str, password: str) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Authenticate a user and create a session.
        
        Args:
            username_or_email: The username or email address
            password: The plaintext password
            
        Returns:
            A tuple with (success, session_token, user_data)
        """
        try:
            # Determine if input is email or username
            if re.match(EMAIL_REGEX, username_or_email):
                user = user_repo.get_user_by_email(self.db, username_or_email)
            else:
                user = user_repo.get_user_by_username(self.db, username_or_email)
                
            if not user:
                logger.warning(f"Login failed: User {username_or_email} not found")
                return (False, None, None)
                
            # Check if user is active
            if not getattr(user, 'is_active', True):
                logger.warning(f"Login failed: User {username_or_email} is inactive")
                return (False, None, None)
                
            # Verify password
            if not verify_password(password, user.password_hash):
                logger.warning(f"Login failed: Invalid password for {username_or_email}")
                return (False, None, None)
                
            # Create session
            user_data = {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin,
                # Add role if available, otherwise default to student
                'role': getattr(user, 'role', Role.STUDENT.value),
                'last_login': datetime.now().isoformat()
            }
            
            session_token = self.session_manager.create_session(str(user.id), user_data)
            
            # Update last login timestamp
            if hasattr(user, 'last_login'):
                user_repo.update(self.db, user.id, last_login=datetime.now())
            
            logger.info(f"User {username_or_email} logged in successfully")
            return (True, session_token, user_data)
            
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return (False, None, None)
    
    def register(self, username: str, email: str, password: str, 
                first_name: Optional[str] = None, 
                last_name: Optional[str] = None,
                age_group: Optional[str] = None) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Register a new user.
        
        Args:
            username: The username
            email: The email address
            password: The plaintext password
            first_name: The user's first name (optional)
            last_name: The user's last name (optional)
            age_group: The user's age group (optional)
            
        Returns:
            A tuple with (success, user_id, error_message)
        """
        try:
            # Validate email format
            if not re.match(EMAIL_REGEX, email):
                return (False, None, "Invalid email format")
                
            # Validate password strength
            is_valid, errors = validate_password_strength(password)
            if not is_valid:
                return (False, None, "\n".join(errors))
                
            # Check if username or email already exists
            if user_repo.get_user_by_username(self.db, username):
                return (False, None, f"Username '{username}' is already taken")
                
            if user_repo.get_user_by_email(self.db, email):
                return (False, None, f"Email '{email}' is already registered")
                
            # Hash the password
            hashed_password = hash_password(password)
            
            # Create the user
            with self.transaction():
                new_user = user_repo.create_user(
                    self.db,
                    username=username,
                    email=email,
                    hashed_password=hashed_password,
                    first_name=first_name,
                    last_name=last_name,
                    age_group=age_group,
                    is_active=True,
                    is_admin=False,
                )
                
            logger.info(f"New user registered: {username} ({email})")
            return (True, str(new_user.id), None)
            
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return (False, None, f"Registration failed: {str(e)}")
    
    def logout(self, session_token: str) -> bool:
        """
        Log out a user by destroying their session.
        
        Args:
            session_token: The session token
            
        Returns:
            True if successful, False otherwise
        """
        return self.session_manager.destroy_session(session_token)
    
    def validate_session(self, session_token: str) -> Optional[Dict[str, Any]]:
        """
        Validate a session and return user data.
        
        Args:
            session_token: The session token
            
        Returns:
            The session data if valid, None otherwise
        """
        return self.session_manager.get_session(session_token)
    
    def get_current_user(self, session_token: str) -> Optional[Dict[str, Any]]:
        """
        Get the current user from a session token.
        
        Args:
            session_token: The session token
            
        Returns:
            User data if session is valid, None otherwise
        """
        session_data = self.session_manager.get_session(session_token)
        if not session_data:
            return None
            
        return session_data.get("data", {})
    
    def change_password(self, user_id: str, current_password: str, 
                        new_password: str) -> Tuple[bool, Optional[str]]:
        """
        Change a user's password.
        
        Args:
            user_id: The user ID
            current_password: The current password
            new_password: The new password
            
        Returns:
            A tuple with (success, error_message)
        """
        try:
            # Convert string ID to UUID
            if isinstance(user_id, str):
                user_id = uuid.UUID(user_id)
                
            # Get the user
            user = user_repo.get_by_id(self.db, user_id)
            if not user:
                return (False, "User not found")
                
            # Verify current password
            if not verify_password(current_password, user.password_hash):
                return (False, "Current password is incorrect")
                
            # Validate new password strength
            is_valid, errors = validate_password_strength(new_password)
            if not is_valid:
                return (False, "\n".join(errors))
                
            # Hash the new password
            hashed_password = hash_password(new_password)
            
            # Update the password
            with self.transaction():
                user_repo.update_user(
                    self.db,
                    user_id,
                    hashed_password=hashed_password
                )
                
            # Log out all sessions for security
            self.session_manager.destroy_all_user_sessions(str(user_id))
                
            logger.info(f"Password changed for user {user.username}")
            return (True, None)
            
        except Exception as e:
            logger.error(f"Password change error: {str(e)}")
            return (False, f"Password change failed: {str(e)}")
    
    def request_password_reset(self, email: str) -> Tuple[bool, Optional[str]]:
        """
        Request a password reset token.
        
        Args:
            email: The user's email address
            
        Returns:
            A tuple with (success, reset_token)
        """
        try:
            # Get the user
            user = user_repo.get_user_by_email(self.db, email)
            if not user:
                # Don't reveal if the email exists for security reasons
                logger.info(f"Password reset requested for non-existent email: {email}")
                return (True, None)
                
            # Generate a reset token
            token = generate_reset_token()
            
            # Store the token with expiry
            self._reset_tokens[token] = {
                "user_id": str(user.id),
                "expires_at": datetime.now() + timedelta(seconds=PASSWORD_RESET_EXPIRY)
            }
            
            logger.info(f"Password reset token generated for {email}")
            return (True, token)
            
        except Exception as e:
            logger.error(f"Password reset request error: {str(e)}")
            return (False, None)
    
    def reset_password(self, token: str, new_password: str) -> Tuple[bool, Optional[str]]:
        """
        Reset a password using a token.
        
        Args:
            token: The reset token
            new_password: The new password
            
        Returns:
            A tuple with (success, error_message)
        """
        try:
            # Check if token exists and is valid
            token_data = self._reset_tokens.get(token)
            if not token_data:
                return (False, "Invalid or expired reset token")
                
            # Check if token is expired
            if token_data["expires_at"] < datetime.now():
                self._reset_tokens.pop(token, None)
                return (False, "Reset token has expired")
                
            # Validate new password strength
            is_valid, errors = validate_password_strength(new_password)
            if not is_valid:
                return (False, "\n".join(errors))
                
            # Get the user
            user_id = token_data["user_id"]
            if isinstance(user_id, str):
                user_id = uuid.UUID(user_id)
                
            user = user_repo.get_by_id(self.db, user_id)
            if not user:
                return (False, "User not found")
                
            # Hash the new password
            hashed_password = hash_password(new_password)
            
            # Update the password
            with self.transaction():
                user_repo.update_user(
                    self.db,
                    user_id,
                    hashed_password=hashed_password
                )
                
            # Remove the used token
            self._reset_tokens.pop(token, None)
            
            # Log out all sessions for security
            self.session_manager.destroy_all_user_sessions(str(user_id))
                
            logger.info(f"Password reset successful for user {user.username}")
            return (True, None)
            
        except Exception as e:
            logger.error(f"Password reset error: {str(e)}")
            return (False, f"Password reset failed: {str(e)}")
    
    def check_permission(self, session_token: str, 
                        permission: Union[Permission, str]) -> bool:
        """
        Check if the current user has a specific permission.
        
        Args:
            session_token: The session token
            permission: The permission to check
            
        Returns:
            True if the user has the permission, False otherwise
        """
        user_data = self.get_current_user(session_token)
        if not user_data:
            return False
            
        return self.permission_service.user_has_permission(user_data, permission)
    
    def generate_temp_password(self, user_id: str) -> Tuple[bool, Optional[str]]:
        """
        Generate a temporary password for a user.
        
        Args:
            user_id: The user ID
            
        Returns:
            A tuple with (success, temporary_password)
        """
        try:
            # Convert string ID to UUID
            if isinstance(user_id, str):
                user_id = uuid.UUID(user_id)
                
            # Get the user
            user = user_repo.get_by_id(self.db, user_id)
            if not user:
                return (False, None)
                
            # Generate a temporary password
            temp_password = generate_temporary_password()
            
            # Hash the temporary password
            hashed_password = hash_password(temp_password)
            
            # Update the password
            with self.transaction():
                user_repo.update_user(
                    self.db,
                    user_id,
                    hashed_password=hashed_password
                )
                
            # Log out all sessions for security
            self.session_manager.destroy_all_user_sessions(str(user_id))
                
            logger.info(f"Temporary password generated for user {user.username}")
            return (True, temp_password)
            
        except Exception as e:
            logger.error(f"Temporary password generation error: {str(e)}")
            return (False, None)
            
    def require_password_change(self, user_id: str, required: bool = True) -> bool:
        """
        Set whether a user is required to change their password on next login.
        
        Args:
            user_id: The user ID
            required: Whether password change is required
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert string ID to UUID
            if isinstance(user_id, str):
                user_id = uuid.UUID(user_id)
                
            # Get the user
            user = user_repo.get_by_id(self.db, user_id)
            if not user:
                return False
                
            # Set the flag in user metadata
            metadata = getattr(user, 'metadata', {}) or {}
            metadata['require_password_change'] = required
            
            # Update the user
            with self.transaction():
                user_repo.update_user(
                    self.db,
                    user_id,
                    metadata=metadata
                )
                
            logger.info(f"Password change requirement set to {required} for user {user.username}")
            return True
            
        except Exception as e:
            logger.error(f"Set password change requirement error: {str(e)}")
            return False 