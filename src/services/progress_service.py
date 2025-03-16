from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid
import logging

from src.db import get_db
from src.db.repositories import progress_repo
from src.db.models import Progress as DBProgress

# Set up logging
logger = logging.getLogger(__name__)

class Progress:
    """Model for user progress in a course"""
    def __init__(
        self,
        id: str,
        user_id: str,
        course_id: str,
        current_lesson_id: Optional[str],
        completed_lessons: List[Dict[str, Any]],
        current_difficulty: str,
        progress_percentage: float,
        total_points_earned: int,
        time_spent: int,
        strengths: List[Dict[str, Any]],
        weaknesses: List[Dict[str, Any]],
        learning_path: Dict[str, Any],
        progress_data: Dict[str, Any],
        last_accessed: datetime
    ):
        self.id = id
        self.user_id = user_id
        self.course_id = course_id
        self.current_lesson_id = current_lesson_id
        self.completed_lessons = completed_lessons
        self.current_difficulty = current_difficulty
        self.progress_percentage = progress_percentage
        self.total_points_earned = total_points_earned
        self.time_spent = time_spent
        self.strengths = strengths
        self.weaknesses = weaknesses
        self.learning_path = learning_path
        self.progress_data = progress_data
        self.last_accessed = last_accessed


class ProgressService:
    """
    Service class for handling user progress operations.
    This class provides methods for tracking, updating, and analyzing user progress.
    """
    
    def get_user_progress(self, user_id: str) -> List[Progress]:
        """
        Get all progress records for a user
        
        Args:
            user_id: The ID of the user
            
        Returns:
            List of progress records for the user
        """
        try:
            db = next(get_db())
            db_progress_records = progress_repo.get_progress_by_user(db, user_id)
            progress_records = [self._convert_db_progress_to_progress(record) for record in db_progress_records]
            db.close()
            return progress_records
        except Exception as e:
            logger.error(f"Error fetching user progress: {str(e)}")
            return []
    
    def get_course_progress(self, user_id: str, course_id: str) -> Optional[Progress]:
        """
        Get progress record for a specific course and user
        
        Args:
            user_id: The ID of the user
            course_id: The ID of the course
            
        Returns:
            Progress record if found, None otherwise
        """
        try:
            db = next(get_db())
            db_progress = progress_repo.get_progress_by_user_and_course(db, user_id, course_id)
            if db_progress:
                progress = self._convert_db_progress_to_progress(db_progress)
                db.close()
                return progress
            db.close()
            return None
        except Exception as e:
            logger.error(f"Error fetching course progress: {str(e)}")
            return None
    
    def update_current_lesson(self, user_id: str, course_id: str, lesson_id: str) -> bool:
        """
        Update the current lesson for a user's course progress
        
        Args:
            user_id: The ID of the user
            course_id: The ID of the course
            lesson_id: The ID of the new current lesson
            
        Returns:
            True if successful, False otherwise
        """
        try:
            db = next(get_db())
            progress = progress_repo.get_progress_by_user_and_course(db, user_id, course_id)
            
            if not progress:
                db.close()
                return False
            
            # Update current lesson and last accessed time
            progress.current_lesson_id = lesson_id
            progress.last_accessed = datetime.now(timezone.utc)
            
            db.commit()
            db.close()
            return True
        except Exception as e:
            logger.error(f"Error updating current lesson: {str(e)}")
            return False
    
    def complete_lesson(self, user_id: str, course_id: str, lesson_id: str, score: float, time_spent: int) -> bool:
        """
        Mark a lesson as completed and update progress
        
        Args:
            user_id: The ID of the user
            course_id: The ID of the course
            lesson_id: The ID of the completed lesson
            score: The score achieved (0-100)
            time_spent: Time spent on the lesson in minutes
            
        Returns:
            True if successful, False otherwise
        """
        try:
            db = next(get_db())
            progress = progress_repo.get_progress_by_user_and_course(db, user_id, course_id)
            
            if not progress:
                db.close()
                return False
            
            # Create completed lesson record
            completed_lesson = {
                "lesson_id": lesson_id,
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "score": score,
                "time_spent": time_spent
            }
            
            # Check if lesson is already completed
            lesson_already_completed = False
            for i, lesson in enumerate(progress.completed_lessons):
                if lesson.get("lesson_id") == lesson_id:
                    # Update existing record
                    progress.completed_lessons[i] = completed_lesson
                    lesson_already_completed = True
                    break
            
            # Add to completed lessons if not already there
            if not lesson_already_completed:
                progress.completed_lessons.append(completed_lesson)
            
            # Update total time spent
            progress.time_spent += time_spent
            
            # Update last accessed time
            progress.last_accessed = datetime.now(timezone.utc)
            
            # Update progress percentage (this would need to know total lessons in course)
            # For now, we'll just estimate based on completed lessons
            # In a real implementation, you'd query the course for total lessons
            progress.progress_percentage = min(100.0, len(progress.completed_lessons) * 10.0)
            
            db.commit()
            db.close()
            return True
        except Exception as e:
            logger.error(f"Error completing lesson: {str(e)}")
            return False
    
    def add_points(self, user_id: str, course_id: str, points: int) -> bool:
        """
        Add points to a user's course progress
        
        Args:
            user_id: The ID of the user
            course_id: The ID of the course
            points: The number of points to add
            
        Returns:
            True if successful, False otherwise
        """
        try:
            db = next(get_db())
            progress = progress_repo.get_progress_by_user_and_course(db, user_id, course_id)
            
            if not progress:
                db.close()
                return False
            
            # Add points
            progress.total_points_earned += points
            
            # Update last accessed time
            progress.last_accessed = datetime.now(timezone.utc)
            
            db.commit()
            db.close()
            return True
        except Exception as e:
            logger.error(f"Error adding points: {str(e)}")
            return False
    
    def update_difficulty(self, user_id: str, course_id: str, new_difficulty: str) -> bool:
        """
        Update the difficulty level for a user's course progress
        
        Args:
            user_id: The ID of the user
            course_id: The ID of the course
            new_difficulty: The new difficulty level ("Beginner", "Intermediate", or "Advanced")
            
        Returns:
            True if successful, False otherwise
        """
        try:
            db = next(get_db())
            progress = progress_repo.get_progress_by_user_and_course(db, user_id, course_id)
            
            if not progress:
                db.close()
                return False
            
            # Validate difficulty level
            if new_difficulty not in ["Beginner", "Intermediate", "Advanced"]:
                db.close()
                return False
            
            # Update difficulty
            progress.current_difficulty = new_difficulty
            
            # Update last accessed time
            progress.last_accessed = datetime.now(timezone.utc)
            
            db.commit()
            db.close()
            return True
        except Exception as e:
            logger.error(f"Error updating difficulty: {str(e)}")
            return False
    
    def _convert_db_progress_to_progress(self, db_progress: DBProgress) -> Progress:
        """Convert a database progress model to a Progress model"""
        try:
            return Progress(
                id=str(db_progress.id),
                user_id=str(db_progress.user_id),
                course_id=str(db_progress.course_id),
                current_lesson_id=str(db_progress.current_lesson_id) if db_progress.current_lesson_id else None,
                completed_lessons=db_progress.completed_lessons,
                current_difficulty=db_progress.current_difficulty,
                progress_percentage=db_progress.progress_percentage,
                total_points_earned=db_progress.total_points_earned,
                time_spent=db_progress.time_spent,
                strengths=db_progress.strengths,
                weaknesses=db_progress.weaknesses,
                learning_path=db_progress.learning_path,
                progress_data=db_progress.progress_data,
                last_accessed=db_progress.last_accessed
            )
        except Exception as e:
            logger.error(f"Error converting progress: {str(e)}")
            # Return a default progress as fallback
            return Progress(
                id=str(db_progress.id) if hasattr(db_progress, 'id') else "unknown",
                user_id=str(db_progress.user_id) if hasattr(db_progress, 'user_id') else "unknown",
                course_id=str(db_progress.course_id) if hasattr(db_progress, 'course_id') else "unknown",
                current_lesson_id=None,
                completed_lessons=[],
                current_difficulty="Beginner",
                progress_percentage=0.0,
                total_points_earned=0,
                time_spent=0,
                strengths=[],
                weaknesses=[],
                learning_path={},
                progress_data={},
                last_accessed=datetime.now(timezone.utc)
            ) 