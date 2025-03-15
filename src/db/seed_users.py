import uuid
import hashlib
import os
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from src.db import get_db
from src.db.models import User, Setting
from src.db.repositories.user_repo import create_user, get_user_by_email

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

def seed_users():
    """
    Seed the database with mock users for development and testing.
    """
    db = next(get_db())
    
    # Define mock users
    mock_users = [
        {
            "username": "student1",
            "email": "student1@example.com",
            "password": "password123",
            "age_group": "10-12",
        },
        {
            "username": "student2",
            "email": "student2@example.com",
            "password": "password123",
            "age_group": "13-14",
        },
        {
            "username": "student3",
            "email": "student3@example.com",
            "password": "password123",
            "age_group": "15-17",
        }
    ]
    
    # Create users if they don't exist
    for user_data in mock_users:
        if not get_user_by_email(db, user_data["email"]):
            user = User(
                id=uuid.uuid4(),
                username=user_data["username"],
                email=user_data["email"],
                password_hash=hash_password(user_data["password"]),
                age_group=user_data["age_group"],
                points=0,
                experience_level=1,
                total_study_time=0,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            
            # Create the user
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
            
            print(f"Created user: {user_data['username']}")
        else:
            print(f"User {user_data['email']} already exists")
    
    print("User seeding completed!")

if __name__ == "__main__":
    seed_users() 