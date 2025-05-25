"""
Seed script for populating the database with initial data.
"""

from typing import Dict, Any
from src.db.seed_users import seed_users
from src.db.seed_courses import seed_courses
from src.db.seed_lessons import seed_lesson_content
from .seed_progress import seed_progress
from src.core import get_logger
from src.core.error_handling import handle_db_errors

logger = get_logger(__name__)

@handle_db_errors(operation="seed_database")
def seed_database(options: Dict[str, Any] = None) -> None:
    """
    Seed the database with initial data.
    
    Args:
        options: Options for controlling the seeding process
    """
    logger.info("Seeding database...")
    
    # Seed users first
    seed_users()
    
    # Then seed courses, which also handles lessons and their basic content structure
    seed_courses()

    # Seed detailed lesson content
    seed_lesson_content()
    
    # Then seed progress for users
    seed_progress()

    # Seed other data as needed
    
    logger.info("Database seeding completed successfully.")

if __name__ == "__main__":
    seed_database() 