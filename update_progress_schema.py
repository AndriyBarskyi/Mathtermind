import sqlite3
import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.db.models import Base, Progress
import uuid
from datetime import datetime, timezone
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_progress_table_schema():
    """Update the progress table schema to match the Progress model in the code."""
    logger.info("Updating progress table schema...")
    
    # Connect to the SQLite database
    conn = sqlite3.connect('mathtermind.db')
    cursor = conn.cursor()
    
    try:
        # Backup existing progress data
        logger.info("Backing up existing progress data...")
        cursor.execute("SELECT * FROM progress")
        progress_data = cursor.fetchall()
        
        # Get column names
        cursor.execute("PRAGMA table_info(progress)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Create a dictionary to map old data to new schema
        progress_backup = []
        for row in progress_data:
            progress_dict = {}
            for i, column in enumerate(columns):
                progress_dict[column] = row[i]
            progress_backup.append(progress_dict)
        
        # Drop the existing progress table
        logger.info("Dropping existing progress table...")
        cursor.execute("DROP TABLE progress")
        conn.commit()
        
        # Create SQLAlchemy engine and recreate the progress table with the correct schema
        logger.info("Recreating progress table with correct schema...")
        engine = create_engine('sqlite:///mathtermind.db')
        Base.metadata.create_all(engine, tables=[Progress.__table__])
        
        # Restore progress data if possible
        if progress_backup:
            logger.info(f"Restoring {len(progress_backup)} progress records...")
            Session = sessionmaker(bind=engine)
            session = Session()
            
            for old_progress in progress_backup:
                try:
                    # Create a new Progress object with the correct schema
                    new_progress = Progress(
                        id=uuid.UUID(old_progress['id']) if isinstance(old_progress['id'], str) else old_progress['id'],
                        user_id=uuid.UUID(old_progress['user_id']) if isinstance(old_progress['user_id'], str) else old_progress['user_id'],
                        course_id=uuid.UUID(old_progress['course_id']) if isinstance(old_progress['course_id'], str) else old_progress['course_id'],
                        current_lesson_id=None,  # New field
                        completed_lessons=[],  # New field
                        current_difficulty="Beginner",  # New field
                        progress_percentage=0.0,  # New field
                        total_points_earned=0,  # New field
                        time_spent=0,  # New field
                        strengths=[],  # New field
                        weaknesses=[],  # New field
                        learning_path={},  # New field
                        progress_data=old_progress.get('progress_data', {}),
                        last_accessed=old_progress.get('last_accessed', datetime.now(timezone.utc))
                    )
                    session.add(new_progress)
                except Exception as e:
                    logger.error(f"Error restoring progress record: {str(e)}")
                    continue
            
            session.commit()
            session.close()
        
        logger.info("Progress table schema updated successfully!")
    except Exception as e:
        logger.error(f"Error updating progress table schema: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    update_progress_table_schema() 