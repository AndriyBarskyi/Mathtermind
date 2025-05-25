"""
User service for Mathtermind.

This module provides service methods for managing users.
"""

from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

from src.db import get_db
from src.db.models import User as DBUser
from src.db.repositories import UserRepository
from src.models.user import User
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


class UserService(BaseService):
    """Service for managing users."""

    def __init__(self):
        """Initialize the user service."""
        super().__init__()
        self.user_repo = UserRepository()
        logger.debug("UserService initialized")

    @handle_service_errors(service_name="user")
    def get_user_by_id(self, user_id: str) -> User:
        """
        Get a user by ID.

        Args:
            user_id: The ID of the user

        Returns:
            The user object

        Raises:
            ValidationError: If the user ID format is invalid
            ResourceNotFoundError: If the user is not found
        """
        logger.info(f"Getting user by ID: {user_id}")
        
        try:
            user_uuid = uuid.UUID(user_id)
            logger.debug(f"Converted string ID to UUID: {user_uuid}")
            
        except ValueError:
            logger.error(f"Invalid user ID format: {user_id}")
            raise ValidationError(
                message=f"Invalid user ID format: {user_id}",
                field="user_id",
                value=user_id
            )

        # Get the user from the repository
        with create_error_boundary("fetch_user"):
            db_user = self.user_repo.get_by_id(self.db, user_uuid)

        if not db_user:
            logger.warning(f"User not found with ID: {user_id}")
            raise ResourceNotFoundError(
                message=f"User with ID {user_id} not found",
                resource_type="user",
                resource_id=user_id
            )
            
        logger.debug(f"Found user with ID {user_id}: {db_user.username}")
        return self._convert_db_user_to_ui_user(db_user)

    @handle_service_errors(service_name="user")
    def get_user_by_username(self, username: str) -> User:
        """
        Get a user by username.

        Args:
            username: The username of the user

        Returns:
            The user object

        Raises:
            ValidationError: If the username is invalid
            ResourceNotFoundError: If the user is not found
        """
        logger.info(f"Getting user by username: {username}")
        
        if not username:
            logger.error("Username cannot be empty")
            raise ValidationError(
                message="Username cannot be empty",
                field="username",
                value=username
            )

        # Get the user from the repository
        with create_error_boundary("fetch_user_by_username"):
            db_user = self.user_repo.get_user_by_username(self.db, username)

        if not db_user:
            logger.warning(f"User not found with username: {username}")
            raise ResourceNotFoundError(
                message=f"User with username '{username}' not found",
                resource_type="user",
                resource_id=username
            )

        logger.debug(f"Found user with username '{username}': {db_user.id}")
        return self._convert_db_user_to_ui_user(db_user)

    @handle_service_errors(service_name="user")
    def get_user_by_email(self, email: str) -> User:
        """
        Get a user by email.

        Args:
            email: The email of the user

        Returns:
            The user object

        Raises:
            ValidationError: If the email is invalid
            ResourceNotFoundError: If the user is not found
        """
        logger.info(f"Getting user by email: {email}")
        
        if not email:
            logger.error("Email cannot be empty")
            raise ValidationError(
                message="Email cannot be empty",
                field="email",
                value=email
            )

        # Get the user from the repository
        with create_error_boundary("fetch_user_by_email"):
            db_user = self.user_repo.get_user_by_email(self.db, email)

        if not db_user:
            logger.warning(f"User not found with email: {email}")
            raise ResourceNotFoundError(
                message=f"User with email '{email}' not found",
                resource_type="user",
                resource_id=email
            )

        logger.debug(f"Found user with email '{email}': {db_user.id}")
        return self._convert_db_user_to_ui_user(db_user)

    @handle_service_errors(service_name="user")
    def get_all_users(self) -> List[User]:
        """
        Get all users.

        Returns:
            A list of users
        """
        logger.info("Getting all users")

        # Get all users from the repository
        with create_error_boundary("fetch_all_users"):
            db_users = self.user_repo.get_all(self.db)

        user_count = len(db_users)
        logger.debug(f"Found {user_count} users")

        # Convert to UI models
        return [self._convert_db_user_to_ui_user(user) for user in db_users]

    @handle_service_errors(service_name="user")
    def get_active_users(self) -> List[User]:
        """
        Get all active users.

        Returns:
            A list of active users
        """
        logger.info("Getting active users")

        # Get active users from the repository
        with create_error_boundary("fetch_active_users"):
            db_users = self.user_repo.get_active_users(self.db)

        user_count = len(db_users)
        logger.debug(f"Found {user_count} active users")

        # Convert to UI models
        return [self._convert_db_user_to_ui_user(user) for user in db_users]

    @handle_service_errors(service_name="user")
    def create_user(
        self,
        username: str,
        email: str,
        hashed_password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        age_group: Optional[str] = None,
        is_admin: bool = False,
        avatar_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> User:
        """
        Create a new user.

        Args:
            username: The username of the user
            email: The email of the user
            hashed_password: The hashed password of the user
            first_name: Optional first name of the user
            last_name: Optional last name of the user
            age_group: Optional age group of the user
            is_admin: Whether the user is an admin
            avatar_url: Optional URL to the user's avatar
            metadata: Additional metadata

        Returns:
            The created user

        Raises:
            ValidationError: If the user data is invalid or user already exists
            DatabaseError: If there's an error creating the user
        """
        logger.info(f"Creating new user with username: {username}, email: {email}")
        
        # Validate required fields
        if not username:
            logger.error("Username cannot be empty")
            raise ValidationError(
                message="Username cannot be empty",
                field="username",
                value=username
            )
            
        if not email:
            logger.error("Email cannot be empty")
            raise ValidationError(
                message="Email cannot be empty",
                field="email",
                value=email
            )
            
        if not hashed_password:
            logger.error("Password cannot be empty")
            raise ValidationError(
                message="Password cannot be empty",
                field="password",
                value="[redacted]"
            )

        # Check if username or email already exists
        with create_error_boundary("check_existing_user_on_create"):
            if self.user_repo.get_user_by_username(self.db, username):
                logger.warning(f"Username already exists: {username}")
                raise ValidationError(
                    message=f"Username '{username}' already exists",
                    field="username",
                    value=username
                )
            if self.user_repo.get_user_by_email(self.db, email):
                logger.warning(f"Email already registered: {email}")
                raise ValidationError(
                    message=f"Email '{email}' is already registered",
                    field="email",
                    value=email
                )

        # Create the user with transaction
        with self.transaction() as session:
            logger.debug(f"Creating user in database: {username}")
            db_user = self.user_repo.create(session, {
                "username": username,
                "email": email,
                "hashed_password": hashed_password,
                "first_name": first_name,
                "last_name": last_name,
                "age_group": age_group,
                "is_admin": is_admin,
                "avatar_url": avatar_url,
                "profile_data": metadata or {},
            })

        if not db_user:
            logger.error(f"Failed to create user: {username}")
            raise DatabaseError(
                message=f"Failed to create user '{username}'",
                details={"username": username, "email": email}
            )

        logger.info(f"User created successfully: {username} (ID: {db_user.id})")
        return self._convert_db_user_to_ui_user(db_user)

    @handle_service_errors(service_name="user")
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> User:
        """
        Update a user.

        Args:
            user_id: The ID of the user
            updates: The updates to apply

        Returns:
            The updated user

        Raises:
            ValidationError: If the user ID or updates are invalid
            ResourceNotFoundError: If the user is not found
            DatabaseError: If there's an error updating the user
        """
        logger.info(f"Updating user with ID: {user_id}")
        
        if not updates:
            logger.warning(f"No updates provided for user: {user_id}")
            raise ValidationError(
                message="No updates provided",
                field="updates",
                value=updates
            )

        # Validate user ID
        try:
            user_uuid = uuid.UUID(user_id)
            logger.debug(f"Converted string ID to UUID: {user_uuid}")
        except ValueError:
            logger.error(f"Invalid user ID format: {user_id}")
            raise ValidationError(
                message=f"Invalid user ID format: {user_id}",
                field="user_id",
                value=user_id
            )

        # Get the user to ensure it exists
        with create_error_boundary("fetch_user_for_update"):
            db_user = self.user_repo.get_by_id(self.db, user_uuid)

        if not db_user:
            logger.warning(f"User not found for update: {user_id}")
            raise ResourceNotFoundError(
                message=f"User with ID {user_id} not found",
                resource_type="user",
                resource_id=user_id
            )

        # Check uniqueness constraints if updating username or email
        if "username" in updates and updates["username"] != db_user.username:
            existing_user = self.user_repo.get_user_by_username(self.db, updates["username"])
            if existing_user and existing_user.id != user_uuid:
                logger.warning(f"Username already exists: {updates['username']}")
                raise ValidationError(
                    message=f"Username '{updates['username']}' is already taken",
                    field="username",
                    value=updates["username"]
                )

        if "email" in updates and updates["email"] != db_user.email:
            existing_user = self.user_repo.get_user_by_email(self.db, updates["email"])
            if existing_user and existing_user.id != user_uuid:
                logger.warning(f"Email already registered: {updates['email']}")
                raise ValidationError(
                    message=f"Email '{updates['email']}' is already registered",
                    field="email",
                    value=updates["email"]
                )

        # Apply the updates with transaction
        with self.transaction() as session:
            logger.debug(f"Updating user in database: {user_id}")
            updated_user = self.user_repo.update(session, user_uuid, **updates)

        if not updated_user:
            logger.error(f"Failed to update user: {user_id}")
            raise DatabaseError(
                message=f"Failed to update user with ID {user_id}",
                details={"user_id": user_id, "updates": updates}
            )

        logger.info(f"User updated successfully: {user_id}")
        return self._convert_db_user_to_ui_user(updated_user)

    @handle_service_errors(service_name="user")
    def update_user_metadata(
        self, user_id: str, metadata_updates: Dict[str, Any]
    ) -> User:
        """
        Update a user's metadata.

        Args:
            user_id: The ID of the user
            metadata_updates: The metadata updates to apply

        Returns:
            The updated user

        Raises:
            ValidationError: If the user ID or metadata updates are invalid
            ResourceNotFoundError: If the user is not found
            DatabaseError: If there's an error updating the user's metadata
        """
        logger.info(f"Updating metadata for user with ID: {user_id}")
        
        if not metadata_updates:
            logger.warning(f"No metadata updates provided for user: {user_id}")
            raise ValidationError(
                message="No metadata updates provided",
                field="metadata_updates",
                value=metadata_updates
            )

        # Validate user ID
        try:
            user_uuid = uuid.UUID(user_id)
            logger.debug(f"Converted string ID to UUID: {user_uuid}")
        except ValueError:
            logger.error(f"Invalid user ID format: {user_id}")
            raise ValidationError(
                message=f"Invalid user ID format: {user_id}",
                field="user_id",
                value=user_id
            )

        # Get the user to check existence and current metadata
        with create_error_boundary("fetch_user_for_metadata_update"):
            db_user = self.user_repo.get_by_id(self.db, user_uuid)

        if not db_user:
            logger.warning(f"User not found for metadata update: {user_id}")
            raise ResourceNotFoundError(
                message=f"User with ID {user_id} not found",
                resource_type="user",
                resource_id=user_id
            )

        # Merge existing metadata with updates
        current_metadata = db_user.profile_data or {}
        updated_metadata = {**current_metadata, **metadata_updates}
        
        # Apply the updates with transaction
        with self.transaction() as session:
            logger.debug(f"Updating metadata for user: {user_id}")
            updated_user = self.user_repo.update(session, user_uuid, profile_data=updated_metadata)

        if not updated_user:
            logger.error(f"Failed to update metadata for user: {user_id}")
            raise DatabaseError(
                message=f"Failed to update metadata for user with ID {user_id}",
                details={"user_id": user_id, "metadata_updates": metadata_updates}
            )

        logger.info(f"Metadata updated successfully for user: {user_id}")
        return self._convert_db_user_to_ui_user(updated_user)

    @handle_service_errors(service_name="user")
    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user.

        Args:
            user_id: The ID of the user

        Returns:
            True if the user was deleted successfully

        Raises:
            ValidationError: If the user ID format is invalid
            ResourceNotFoundError: If the user is not found
            DatabaseError: If there's an error deleting the user
        """
        logger.info(f"Deleting user with ID: {user_id}")

        # Validate user ID
        try:
            user_uuid = uuid.UUID(user_id)
            logger.debug(f"Converted string ID to UUID: {user_uuid}")
        except ValueError:
            logger.error(f"Invalid user ID format: {user_id}")
            raise ValidationError(
                message=f"Invalid user ID format: {user_id}",
                field="user_id",
                value=user_id
            )

        # Check if the user exists
        with create_error_boundary("fetch_user_for_deletion"):
            db_user = self.user_repo.get_by_id(self.db, user_uuid)

        if not db_user:
            logger.warning(f"User not found for deletion: {user_id}")
            raise ResourceNotFoundError(
                message=f"User with ID {user_id} not found",
                resource_type="user",
                resource_id=user_id
            )

        # Delete the user with transaction
        with self.transaction() as session:
            logger.debug(f"Deleting user from database: {user_id}")
            success = self.user_repo.delete(session, user_uuid)

        if not success:
            logger.error(f"Failed to delete user: {user_id}")
            raise DatabaseError(
                message=f"Failed to delete user with ID {user_id}",
                details={"user_id": user_id}
            )

        logger.info(f"User deleted successfully: {user_id}")
        return True

    @handle_service_errors(service_name="user")
    def _convert_db_user_to_ui_user(self, db_user: DBUser) -> User:
        """
        Convert a database user model to a UI user model.

        Args:
            db_user: The database user model

        Returns:
            The UI user model
        """
        logger.debug(f"Converting DB user to UI user: {db_user.id}")
        
        try:
            # Attributes guaranteed on DBUser: id, username, email, age_group, created_at, points, total_study_time
            # Attributes for UI User that might be missing on DBUser: first_name, last_name, is_active, is_admin, avatar_url, profile_data (for metadata)
            
            raw_profile_data = getattr(db_user, "profile_data", None)
            processed_metadata = {}
            if isinstance(raw_profile_data, dict):
                processed_metadata = raw_profile_data
            elif raw_profile_data is not None:
                logger.warning(f"DBUser profile_data attribute was of unexpected type: {type(raw_profile_data)}. Using empty dict for UI User metadata.")

            user = User(
                id=str(db_user.id),
                username=db_user.username,
                email=db_user.email,
                first_name=getattr(db_user, "first_name", None),
                last_name=getattr(db_user, "last_name", None),
                is_active=getattr(db_user, "is_active", True),  # Default to True if not on DB model
                is_admin=getattr(db_user, "is_admin", False), # Default to False if not on DB model
                created_at=db_user.created_at, # This exists on DBUser via TimestampMixin
                age_group=db_user.age_group, # This exists on DBUser
                avatar_url=getattr(db_user, "avatar_url", None),
                points=getattr(db_user, "points", 0), # points exists on DBUser
                total_study_time=getattr(db_user, "total_study_time", 0), # total_study_time exists on DBUser
                metadata=processed_metadata, # Use the explicitly processed dictionary
            )
            return user
        except Exception as e:
            logger.error(f"Error converting DB user to UI user: {str(e)}")
            report_error(e, operation="_convert_db_user_to_ui_user", user_id=str(db_user.id))
            
            # Fallback with minimal data that is known to exist on DBUser
            return User(
                id=str(db_user.id),
                username=db_user.username,
                email=db_user.email,
                age_group=db_user.age_group,
                created_at=db_user.created_at,
                points=getattr(db_user, "points", 0),
                total_study_time=getattr(db_user, "total_study_time", 0),
                # For other fields, UI model's defaults will apply (e.g., is_active=True, is_admin=False, metadata={})
            )
