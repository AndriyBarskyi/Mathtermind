"""
Seed script for populating the database with sample user data.

This script creates sample users in the database for development
and testing purposes.
"""

import uuid
from datetime import datetime, timezone

from src.db import get_db
from src.db.models import User
from src.db.models.enums import AgeGroup
from src.core import get_logger
from src.core.error_handling import handle_db_errors
from src.services.password_utils import hash_password

logger = get_logger(__name__)

@handle_db_errors(operation="seed_users")
def seed_users():
    """
    Seed the database with sample user data.
    """
    logger.info("Seeding users...")
    
    # Get database session
    db = next(get_db())
    
    # Check if users already exist
    existing_users = db.query(User).count()
    if existing_users > 0:
        logger.info(f"Found {existing_users} existing users. Skipping seeding.")
        return
    
    # Create sample users
    users = [
        {
            "id": uuid.uuid4(),
            "username": "admin",
            "email": "admin@example.com",
            "password_hash": hash_password("admin123"),
            "age_group": AgeGroup.FIFTEEN_TO_SEVENTEEN.value,
            "points": 1000,
            "experience_level": 5,
            "total_study_time": 3600,  # 1 hour in seconds
            "created_at": datetime.now(timezone.utc),
        },
        {
            "id": uuid.uuid4(),
            "username": "student",
            "email": "student@example.com",
            "password_hash": hash_password("student123"),
            "age_group": AgeGroup.THIRTEEN_TO_FOURTEEN.value,
            "points": 500,
            "experience_level": 3,
            "total_study_time": 1800,  # 30 minutes in seconds
            "created_at": datetime.now(timezone.utc),
        },
        {
            "id": uuid.uuid4(),
            "username": "teacher",
            "email": "teacher@example.com",
            "password_hash": hash_password("teacher123"),
            "age_group": AgeGroup.FIFTEEN_TO_SEVENTEEN.value,
            "points": 800,
            "experience_level": 4,
            "total_study_time": 2700,  # 45 minutes in seconds
            "created_at": datetime.now(timezone.utc),
        },
    ]
    
    # Create and save user objects
    for user_data in users:
        user = User(**user_data)
        db.add(user)
    
    # Commit to database
    db.commit()
    logger.info(f"Created {len(users)} sample users") 