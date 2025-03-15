import uuid
import hashlib
import os
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.orm import Session
import bcrypt

from src.db import get_db
from src.db.models import User, Setting
from src.db.repositories.user_repo import (
    create_user,
    get_user_by_id,
    get_user_by_email,
    update_user,
    delete_user
)

class UserService:
    """Service for handling user-related operations."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password for storing using SHA-256 with salt."""
        # Generate a random salt
        salt = os.urandom(32)
        # Hash the password with the salt
        hash_obj = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000  # Number of iterations
        )
        # Return the salt and hash as a single string
        return salt.hex() + ':' + hash_obj.hex()
    
    @staticmethod
    def verify_password(plain_password: str, stored_password: str) -> bool:
        """Verify a password against a hash."""
        try:
            # Check if the stored password is in bcrypt format
            if stored_password.startswith('$2b$') or stored_password.startswith('$2a$') or stored_password.startswith('$2y$'):
                # Use bcrypt to verify the password
                return bcrypt.checkpw(plain_password.encode('utf-8'), stored_password.encode('utf-8'))
            
            # Otherwise, assume it's in our PBKDF2 format
            # Split the stored password into salt and hash
            salt_hex, hash_hex = stored_password.split(':')
            salt = bytes.fromhex(salt_hex)
            stored_hash = bytes.fromhex(hash_hex)
            
            # Hash the provided password with the same salt
            hash_obj = hashlib.pbkdf2_hmac(
                'sha256',
                plain_password.encode('utf-8'),
                salt,
                100000  # Same number of iterations as in hash_password
            )
            
            # Compare the hashes
            return hash_obj == stored_hash
        except Exception as e:
            # If there's any error, log it and return False
            print(f"Password verification error: {str(e)}")
            return False
    
    @staticmethod
    def get_user(user_id: uuid.UUID) -> Optional[User]:
        """Get a user by ID."""
        db = next(get_db())
        return get_user_by_id(db, user_id)
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """Get a user by email."""
        db = next(get_db())
        return get_user_by_email(db, email)
    
    @staticmethod
    def create_new_user(
        username: str,
        email: str,
        password: str,
        age_group: str
    ) -> User:
        """Create a new user."""
        db = next(get_db())
        
        # Check if user already exists
        existing_user = get_user_by_email(db, email)
        if existing_user:
            raise ValueError(f"User with email {email} already exists")
        
        # Create new user
        user = User(
            id=uuid.uuid4(),
            username=username,
            email=email,
            password_hash=UserService.hash_password(password),
            age_group=age_group,
            points=0,
            experience_level=1,
            total_study_time=0,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        created_user = create_user(db, user)
        
        # Create default settings for the user
        default_preferences = {
            "theme": "light",
            "notifications": {
                "daily_reminder": True,
                "achievement_alerts": True,
                "study_time": "16:00"
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
        
        setting = Setting(
            id=uuid.uuid4(),
            user_id=created_user.id,
            preferences=default_preferences
        )
        
        db.add(setting)
        db.commit()
        
        return created_user
    
    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password."""
        user = UserService.get_user_by_email(email)
        if not user:
            return None
        
        if not UserService.verify_password(password, user.password_hash):
            return None
        
        return user
    
    @staticmethod
    def update_user_info(
        user_id: uuid.UUID,
        username: Optional[str] = None,
        email: Optional[str] = None,
        age_group: Optional[str] = None
    ) -> Optional[User]:
        """Update user information."""
        db = next(get_db())
        user = get_user_by_id(db, user_id)
        
        if not user:
            return None
        
        if username:
            user.username = username
        
        if email:
            user.email = email
        
        if age_group:
            user.age_group = age_group
        
        user.updated_at = datetime.now(timezone.utc)
        
        return update_user(db, user)
    
    @staticmethod
    def change_password(user_id: uuid.UUID, new_password: str) -> Optional[User]:
        """Change a user's password."""
        db = next(get_db())
        user = get_user_by_id(db, user_id)
        
        if not user:
            return None
        
        user.password_hash = UserService.hash_password(new_password)
        user.updated_at = datetime.now(timezone.utc)
        
        return update_user(db, user)
    
    @staticmethod
    def add_points(user_id: uuid.UUID, points: int) -> Optional[User]:
        """Add points to a user's account."""
        db = next(get_db())
        user = get_user_by_id(db, user_id)
        
        if not user:
            return None
        
        user.points += points
        
        # Check if user should level up (simple algorithm: level up every 100 points)
        if user.points >= (user.experience_level * 100):
            user.experience_level += 1
        
        user.updated_at = datetime.now(timezone.utc)
        
        return update_user(db, user)
    
    @staticmethod
    def add_study_time(user_id: uuid.UUID, minutes: int) -> Optional[User]:
        """Add study time to a user's account."""
        db = next(get_db())
        user = get_user_by_id(db, user_id)
        
        if not user:
            return None
        
        user.total_study_time += minutes
        user.updated_at = datetime.now(timezone.utc)
        
        return update_user(db, user)
    
    @staticmethod
    def delete_user_account(user_id: uuid.UUID) -> bool:
        """Delete a user account."""
        db = next(get_db())
        user = get_user_by_id(db, user_id)
        
        if not user:
            return False
        
        delete_user(db, user)
        return True 