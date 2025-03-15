"""
Script to reset the database and recreate it with the correct schema.
"""

import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.db.models.base import Base
from src.db import engine

def reset_database():
    """
    Drop all tables and recreate them.
    """
    print("Dropping all tables...")
    Base.metadata.drop_all(engine)
    print("Creating all tables...")
    Base.metadata.create_all(engine)
    print("Database reset complete.")

if __name__ == "__main__":
    # Confirm with the user
    confirm = input("This will delete all data in the database. Are you sure? (y/n): ")
    if confirm.lower() == 'y':
        reset_database()
    else:
        print("Database reset cancelled.") 