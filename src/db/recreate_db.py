"""
Script to recreate the database from scratch using the current models.
"""

import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.db.models import Base
from src.db import engine

def recreate_db():
    """
    Recreate the database from scratch using the current models.
    """
    # Delete the database file if it exists
    db_path = project_root / "mathtermind.db"
    if db_path.exists():
        os.remove(db_path)
        print(f"Deleted existing database file: {db_path}")
    
    # Create all tables
    Base.metadata.create_all(engine)
    print("Created all tables from current models")

if __name__ == "__main__":
    recreate_db() 