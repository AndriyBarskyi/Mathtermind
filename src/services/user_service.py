"""
User service for Mathtermind.

This module provides service methods for managing users.
"""

from typing import List, Optional, Dict, Any
import uuid
import logging
from datetime import datetime

from src.db import get_db
from src.db.models import User as DBUser
from src.db.repositories import UserRepository
from src.models.user import User

# Set up logging
logger = logging.getLogger(__name__)


class UserService:
    """Service for managing users."""

    def __init__(self):
        """Initialize the user service."""
        self.db = next(get_db())
        self.user_repo = UserRepository(self.db)

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get a user by ID.

        Args:
            user_id: The ID of the user

        Returns:
            The user if found, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)

            # Get the user from the repository
            db_user = self.user_repo.get_by_id(user_uuid)

            if not db_user:
                return None

            return self._convert_db_user_to_ui_user(db_user)
        except Exception as e:
            logger.error(f"Error getting user by ID: {str(e)}")
            return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get a user by username.

        Args:
            username: The username of the user

        Returns:
            The user if found, None otherwise
        """
        try:
            # Get the user from the repository
            db_user = self.user_repo.get_user_by_username(username)

            if not db_user:
                return None

            return self._convert_db_user_to_ui_user(db_user)
        except Exception as e:
            logger.error(f"Error getting user by username: {str(e)}")
            return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email.

        Args:
            email: The email of the user

        Returns:
            The user if found, None otherwise
        """
        try:
            # Get the user from the repository
            db_user = self.user_repo.get_user_by_email(email)

            if not db_user:
                return None

            return self._convert_db_user_to_ui_user(db_user)
        except Exception as e:
            logger.error(f"Error getting user by email: {str(e)}")
            return None

    def get_all_users(self) -> List[User]:
        """
        Get all users.

        Returns:
            A list of users
        """
        try:
            # Get all users from the repository
            db_users = self.user_repo.get_all()

            # Convert to UI models
            return [self._convert_db_user_to_ui_user(user) for user in db_users]
        except Exception as e:
            logger.error(f"Error getting all users: {str(e)}")
            return []

    def get_active_users(self) -> List[User]:
        """
        Get all active users.

        Returns:
            A list of active users
        """
        try:
            # Get active users from the repository
            db_users = self.user_repo.get_active_users()

            # Convert to UI models
            return [self._convert_db_user_to_ui_user(user) for user in db_users]
        except Exception as e:
            logger.error(f"Error getting active users: {str(e)}")
            return []

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
    ) -> Optional[User]:
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
            The created user if successful, None otherwise
        """
        try:
            # Check if username or email already exists
            if self.user_repo.get_user_by_username(username):
                logger.warning(f"Username already exists: {username}")
                return None

            if self.user_repo.get_user_by_email(email):
                logger.warning(f"Email already exists: {email}")
                return None

            # Create the user
            db_user = self.user_repo.create(
                username=username,
                email=email,
                hashed_password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                age_group=age_group,
                is_admin=is_admin,
                avatar_url=avatar_url,
                metadata=metadata or {},
            )

            if not db_user:
                return None

            return self._convert_db_user_to_ui_user(db_user)
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            self.db.rollback()
            return None

    def update_user(self, user_id: str, updates: Dict[str, Any]) -> Optional[User]:
        """
        Update a user.

        Args:
            user_id: The ID of the user
            updates: The updates to apply

        Returns:
            The updated user if successful, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)

            # Get the user
            db_user = self.user_repo.get_by_id(user_uuid)
            if not db_user:
                logger.warning(f"User not found: {user_id}")
                return None

            # Update the user
            for key, value in updates.items():
                if hasattr(db_user, key):
                    setattr(db_user, key, value)

            # Save the updates
            updated_user = self.user_repo.update(db_user)

            if not updated_user:
                return None

            return self._convert_db_user_to_ui_user(updated_user)
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            self.db.rollback()
            return None

    def update_user_metadata(
        self, user_id: str, metadata_updates: Dict[str, Any]
    ) -> Optional[User]:
        """
        Update user metadata.

        Args:
            user_id: The ID of the user
            metadata_updates: The updates to apply to the metadata

        Returns:
            The updated user if successful, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)

            # Get the user
            db_user = self.user_repo.get_by_id(user_uuid)
            if not db_user:
                logger.warning(f"User not found: {user_id}")
                return None

            # Update metadata
            metadata = db_user.metadata or {}
            metadata.update(metadata_updates)

            # Save the updates
            db_user.metadata = metadata
            updated_user = self.user_repo.update(db_user)

            if not updated_user:
                return None

            return self._convert_db_user_to_ui_user(updated_user)
        except Exception as e:
            logger.error(f"Error updating user metadata: {str(e)}")
            self.db.rollback()
            return None

    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user.

        Args:
            user_id: The ID of the user

        Returns:
            True if successful, False otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)

            # Delete the user
            return self.user_repo.delete(user_uuid)
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            self.db.rollback()
            return False

    def activate_user(self, user_id: str) -> Optional[User]:
        """
        Activate a user.

        Args:
            user_id: The ID of the user

        Returns:
            The updated user if successful, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)

            # Activate the user
            db_user = self.user_repo.activate_user(user_uuid)

            if not db_user:
                return None

            return self._convert_db_user_to_ui_user(db_user)
        except Exception as e:
            logger.error(f"Error activating user: {str(e)}")
            self.db.rollback()
            return None

    def deactivate_user(self, user_id: str) -> Optional[User]:
        """
        Deactivate a user.

        Args:
            user_id: The ID of the user

        Returns:
            The updated user if successful, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)

            # Deactivate the user
            db_user = self.user_repo.deactivate_user(user_uuid)

            if not db_user:
                return None

            return self._convert_db_user_to_ui_user(db_user)
        except Exception as e:
            logger.error(f"Error deactivating user: {str(e)}")
            self.db.rollback()
            return None

    def add_points(self, user_id: str, points: int) -> Optional[User]:
        """
        Add points to a user.

        Args:
            user_id: The ID of the user
            points: The points to add

        Returns:
            The updated user if successful, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)

            # Get the user
            db_user = self.user_repo.get_by_id(user_uuid)
            if not db_user:
                logger.warning(f"User not found: {user_id}")
                return None

            # Add points
            db_user.points = (db_user.points or 0) + points

            # Save the updates
            updated_user = self.user_repo.update(db_user)

            if not updated_user:
                return None

            return self._convert_db_user_to_ui_user(updated_user)
        except Exception as e:
            logger.error(f"Error adding points to user: {str(e)}")
            self.db.rollback()
            return None

    def update_study_time(self, user_id: str, minutes: int) -> Optional[User]:
        """
        Update the study time for a user.

        Args:
            user_id: The ID of the user
            minutes: The minutes to add

        Returns:
            The updated user if successful, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)

            # Get the user
            db_user = self.user_repo.get_by_id(user_uuid)
            if not db_user:
                logger.warning(f"User not found: {user_id}")
                return None

            # Update study time
            db_user.total_study_time = (db_user.total_study_time or 0) + minutes

            # Save the updates
            updated_user = self.user_repo.update(db_user)

            if not updated_user:
                return None

            return self._convert_db_user_to_ui_user(updated_user)
        except Exception as e:
            logger.error(f"Error updating user study time: {str(e)}")
            self.db.rollback()
            return None

    def search_users(self, query: str, limit: int = 10) -> List[User]:
        """
        Search for users.

        Args:
            query: The search query
            limit: Maximum number of results to return

        Returns:
            A list of matching users
        """
        try:
            # Search for users
            db_users = self.user_repo.search_users(query, limit)

            # Convert to UI models
            return [self._convert_db_user_to_ui_user(user) for user in db_users]
        except Exception as e:
            logger.error(f"Error searching users: {str(e)}")
            return []

    # Conversion Methods

    def _convert_db_user_to_ui_user(self, db_user: DBUser) -> User:
        """
        Convert a database user to a UI user.

        Args:
            db_user: The database user

        Returns:
            The corresponding UI user
        """
        return User(
            id=str(db_user.id),
            username=db_user.username,
            email=db_user.email,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            age_group=db_user.age_group,
            is_active=db_user.is_active,
            is_admin=db_user.is_admin,
            points=db_user.points,
            experience_level=db_user.experience_level,
            total_study_time=db_user.total_study_time,
            avatar_url=db_user.avatar_url,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            metadata=db_user.metadata,
        )
