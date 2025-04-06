"""
Progress service for Mathtermind.

This module provides service methods for tracking user progress in courses and lessons.
"""

from typing import List, Optional, Dict, Any, Union
import uuid
import logging
from datetime import datetime

from src.db import get_db
from src.db.models import (
    Progress as DBProgress,
    ContentState as DBContentState,
    CompletedLesson as DBCompletedLesson,
    CompletedCourse as DBCompletedCourse,
    UserContentProgress as DBUserContentProgress
)
from src.db.repositories import (
    ProgressRepository,
    ContentStateRepository,
    CompletedLessonRepository,
    CompletedCourseRepository,
    UserContentProgressRepository,
    LessonRepository,
    CourseRepository
)
from src.models.progress import (
    Progress, 
    ContentState, 
    CompletedLesson, 
    CompletedCourse, 
    UserContentProgress
)

# Set up logging
logger = logging.getLogger(__name__)


class ProgressService:
    """Service for managing user progress."""
    
    def __init__(self):
        """Initialize the progress service."""
        self.db = next(get_db())
        self.progress_repo = ProgressRepository(self.db)
        self.content_state_repo = ContentStateRepository(self.db)
        self.completed_lesson_repo = CompletedLessonRepository(self.db)
        self.completed_course_repo = CompletedCourseRepository(self.db)
        self.user_content_progress_repo = UserContentProgressRepository(self.db)
        self.lesson_repo = LessonRepository(self.db)
        self.course_repo = CourseRepository(self.db)
    
    # Progress Methods
    
    def get_user_progress(self, user_id: str) -> List[Progress]:
        """
        Get all progress records for a user.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            A list of progress records
        """
        try:
            user_uuid = uuid.UUID(user_id)
            
            # Get all progress records for the user
            db_progress_records = self.progress_repo.get_user_progress(user_uuid)
            
            # Convert to UI models
            return [self._convert_db_progress_to_ui_progress(record) for record in db_progress_records]
        except Exception as e:
            logger.error(f"Error getting user progress: {str(e)}")
            return []
    
    def get_course_progress(self, user_id: str, course_id: str) -> Optional[Progress]:
        """
        Get progress for a specific course.
        
        Args:
            user_id: The ID of the user
            course_id: The ID of the course
            
        Returns:
            The progress record if found, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            course_uuid = uuid.UUID(course_id)
            
            # Get the progress for the course
            db_progress = self.progress_repo.get_course_progress(user_uuid, course_uuid)
            
            if not db_progress:
                return None
                
            return self._convert_db_progress_to_ui_progress(db_progress)
        except Exception as e:
            logger.error(f"Error getting course progress: {str(e)}")
            return None
    
    def create_course_progress(self, user_id: str, course_id: str) -> Optional[Progress]:
        """
        Create a new progress record for a course.
        
        Args:
            user_id: The ID of the user
            course_id: The ID of the course
            
        Returns:
            The created progress record if successful, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            course_uuid = uuid.UUID(course_id)
            
            # Check if progress already exists
            existing_progress = self.progress_repo.get_course_progress(user_uuid, course_uuid)
            if existing_progress:
                return self._convert_db_progress_to_ui_progress(existing_progress)
            
            # Get the first lesson of the course
            course = self.course_repo.get_by_id(course_uuid)
            if not course:
                logger.warning(f"Course not found: {course_id}")
                return None
                
            # Get all lessons and use the first one based on order
            lessons = self.lesson_repo.get_lessons_by_course_id(course_uuid)
            first_lesson_id = lessons[0].id if lessons else None
            
            # Create the progress
            db_progress = self.progress_repo.create_progress(
                user_id=user_uuid,
                course_id=course_uuid,
                current_lesson_id=first_lesson_id
            )
            
            if not db_progress:
                return None
                
            return self._convert_db_progress_to_ui_progress(db_progress)
        except Exception as e:
            logger.error(f"Error creating course progress: {str(e)}")
            self.db.rollback()
            return None
    
    def update_progress_percentage(self, progress_id: str, percentage: float) -> Optional[Progress]:
        """
        Update the progress percentage.
        
        Args:
            progress_id: The ID of the progress record
            percentage: The new progress percentage
            
        Returns:
            The updated progress record if successful, None otherwise
        """
        try:
            progress_uuid = uuid.UUID(progress_id)
            
            # Update the progress percentage
            db_progress = self.progress_repo.update_progress_percentage(
                progress_id=progress_uuid,
                percentage=percentage
            )
            
            if not db_progress:
                return None
                
            return self._convert_db_progress_to_ui_progress(db_progress)
        except Exception as e:
            logger.error(f"Error updating progress percentage: {str(e)}")
            self.db.rollback()
            return None
    
    def update_current_lesson(self, progress_id: str, lesson_id: str) -> Optional[Progress]:
        """
        Update the current lesson.
        
        Args:
            progress_id: The ID of the progress record
            lesson_id: The ID of the new current lesson
            
        Returns:
            The updated progress record if successful, None otherwise
        """
        try:
            progress_uuid = uuid.UUID(progress_id)
            lesson_uuid = uuid.UUID(lesson_id)
            
            # Update the current lesson
            db_progress = self.progress_repo.update_current_lesson(
                progress_id=progress_uuid,
                lesson_id=lesson_uuid
            )
            
            if not db_progress:
                return None
                
            return self._convert_db_progress_to_ui_progress(db_progress)
        except Exception as e:
            logger.error(f"Error updating current lesson: {str(e)}")
            self.db.rollback()
            return None
    
    def add_points(self, progress_id: str, points: int) -> Optional[Progress]:
        """
        Add points to the progress.
        
        Args:
            progress_id: The ID of the progress record
            points: The points to add
            
        Returns:
            The updated progress record if successful, None otherwise
        """
        try:
            progress_uuid = uuid.UUID(progress_id)
            
            # Add points to the progress
            db_progress = self.progress_repo.add_points(
                progress_id=progress_uuid,
                points=points
            )
            
            if not db_progress:
                return None
                
            return self._convert_db_progress_to_ui_progress(db_progress)
        except Exception as e:
            logger.error(f"Error adding points: {str(e)}")
            self.db.rollback()
            return None
    
    def add_time_spent(self, progress_id: str, minutes: int) -> Optional[Progress]:
        """
        Add time spent to the progress.
        
        Args:
            progress_id: The ID of the progress record
            minutes: The minutes to add
            
        Returns:
            The updated progress record if successful, None otherwise
        """
        try:
            progress_uuid = uuid.UUID(progress_id)
            
            # Add time spent to the progress
            db_progress = self.progress_repo.add_time_spent(
                progress_id=progress_uuid,
                minutes=minutes
            )
            
            if not db_progress:
                return None
                
            return self._convert_db_progress_to_ui_progress(db_progress)
        except Exception as e:
            logger.error(f"Error adding time spent: {str(e)}")
            self.db.rollback()
            return None
    
    def complete_progress(self, user_id: str, progress_id: str) -> None:
        """
        Mark progress as completed.
        
        Args:
            user_id: The ID of the user
            progress_id: The ID of the progress record
        """
        progress_uuid = uuid.UUID(progress_id)
            
        # Mark progress as completed
        self.progress_repo.mark_as_completed(progress_uuid)
    
    # Completed Lesson Methods
    
    def complete_lesson(self, 
                     user_id: str, 
                     lesson_id: str, 
                     course_id: str, 
                     score: Optional[int] = None,
                     time_spent: Optional[int] = None) -> Optional[CompletedLesson]:
        """
        Mark a lesson as completed.
        
        Args:
            user_id: The ID of the user
            lesson_id: The ID of the lesson
            course_id: The ID of the course
            score: Optional score for the lesson
            time_spent: Optional time spent on the lesson in minutes
            
        Returns:
            The completed lesson record if successful, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            lesson_uuid = uuid.UUID(lesson_id)
            course_uuid = uuid.UUID(course_id)
            
            # Check if already completed
            is_completed = self.completed_lesson_repo.is_lesson_completed(user_uuid, lesson_uuid)
            if is_completed:
                # Get the completion record
                db_completed = self.completed_lesson_repo.get_lesson_completion(user_uuid, lesson_uuid)
                return self._convert_db_completed_lesson_to_ui_completed_lesson(db_completed)
            
            # Create completed lesson
            db_completed = self.completed_lesson_repo.create_completed_lesson(
                user_id=user_uuid,
                lesson_id=lesson_uuid,
                course_id=course_uuid,
                score=score,
                time_spent=time_spent
            )
            
            if not db_completed:
                return None
            
            # Update course progress
            progress = self.progress_repo.get_course_progress(user_uuid, course_uuid)
            if progress:
                # Calculate new progress percentage
                lessons = self.lesson_repo.get_lessons_by_course_id(course_uuid)
                total_lessons = len(lessons)
                completed_lessons = self.completed_lesson_repo.count_completed_lessons(user_uuid, course_uuid)
                
                if total_lessons > 0:
                    new_percentage = (completed_lessons / total_lessons) * 100
                    self.progress_repo.update_progress_percentage(progress.id, new_percentage)
                
                # Check if all lessons are completed
                if completed_lessons == total_lessons:
                    self.progress_repo.mark_as_completed(progress.id)
                    
                    # Create completed course record
                    self.completed_course_repo.create_completed_course(
                        user_id=user_uuid,
                        course_id=course_uuid
                    )
            
            return self._convert_db_completed_lesson_to_ui_completed_lesson(db_completed)
        except Exception as e:
            logger.error(f"Error completing lesson: {str(e)}")
            self.db.rollback()
            return None
    
    def get_user_completed_lessons(self, user_id: str) -> List[CompletedLesson]:
        """
        Get all completed lessons for a user.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            A list of completed lesson records
        """
        try:
            user_uuid = uuid.UUID(user_id)
            
            # Get all completed lessons for the user
            db_completed_lessons = self.completed_lesson_repo.get_user_completed_lessons(user_uuid)
            
            # Convert to UI models
            return [self._convert_db_completed_lesson_to_ui_completed_lesson(record) for record in db_completed_lessons]
        except Exception as e:
            logger.error(f"Error getting user completed lessons: {str(e)}")
            return []
    
    def get_course_completed_lessons(self, user_id: str, course_id: str) -> List[CompletedLesson]:
        """
        Get all completed lessons for a user in a course.
        
        Args:
            user_id: The ID of the user
            course_id: The ID of the course
            
        Returns:
            A list of completed lesson records
        """
        try:
            user_uuid = uuid.UUID(user_id)
            course_uuid = uuid.UUID(course_id)
            
            # Get all completed lessons for the user in the course
            db_completed_lessons = self.completed_lesson_repo.get_course_completed_lessons(
                user_id=user_uuid,
                course_id=course_uuid
            )
            
            # Convert to UI models
            return [self._convert_db_completed_lesson_to_ui_completed_lesson(record) for record in db_completed_lessons]
        except Exception as e:
            logger.error(f"Error getting course completed lessons: {str(e)}")
            return []
    
    # Completed Course Methods
    
    def get_user_completed_courses(self, user_id: str) -> List[CompletedCourse]:
        """
        Get all completed courses for a user.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            A list of completed course records
        """
        try:
            user_uuid = uuid.UUID(user_id)
            
            # Get all completed courses for the user
            db_completed_courses = self.completed_course_repo.get_user_completed_courses(user_uuid)
            
            # Convert to UI models
            return [self._convert_db_completed_course_to_ui_completed_course(record) for record in db_completed_courses]
        except Exception as e:
            logger.error(f"Error getting user completed courses: {str(e)}")
            return []
    
    def get_course_completion(self, user_id: str, course_id: str) -> Optional[CompletedCourse]:
        """
        Get the completion record for a course.
        
        Args:
            user_id: The ID of the user
            course_id: The ID of the course
            
        Returns:
            The completed course record if found, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            course_uuid = uuid.UUID(course_id)
            
            # Get the completion record for the course
            db_completion = self.completed_course_repo.get_course_completion(
                user_id=user_uuid,
                course_id=course_uuid
            )
            
            if not db_completion:
                return None
                
            return self._convert_db_completed_course_to_ui_completed_course(db_completion)
        except Exception as e:
            logger.error(f"Error getting course completion: {str(e)}")
            return None
    
    # User Content Progress Methods
    
    def get_content_progress(self, 
                         user_id: str, 
                         content_id: str) -> Optional[UserContentProgress]:
        """
        Get user progress for a specific content item.
        
        Args:
            user_id: The ID of the user
            content_id: The ID of the content
            
        Returns:
            The user content progress record if found, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            content_uuid = uuid.UUID(content_id)
            
            # Get the content progress
            db_content_progress = self.user_content_progress_repo.get_content_progress(
                user_id=user_uuid,
                content_id=content_uuid
            )
            
            if not db_content_progress:
                return None
                
            return self._convert_db_user_content_progress_to_ui_user_content_progress(db_content_progress)
        except Exception as e:
            logger.error(f"Error getting content progress: {str(e)}")
            return None
    
    def update_content_progress(self, 
                             user_id: str, 
                             content_id: str, 
                             status: str, 
                             score: Optional[int] = None,
                             time_spent: Optional[int] = None,
                             custom_data: Optional[Dict[str, Any]] = None) -> Optional[UserContentProgress]:
        """
        Update or create user progress for a content item.
        
        Args:
            user_id: The ID of the user
            content_id: The ID of the content
            status: The status of the content progress
            score: Optional score for the content
            time_spent: Optional time spent on the content in minutes
            custom_data: Optional custom data
            
        Returns:
            The updated or created user content progress record if successful, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            content_uuid = uuid.UUID(content_id)
            
            # Get existing progress or create new
            db_content_progress = self.user_content_progress_repo.get_content_progress(
                user_id=user_uuid,
                content_id=content_uuid
            )
            
            if db_content_progress:
                # Update existing progress
                updates = {}
                if status:
                    updates["status"] = status
                if score is not None:
                    updates["score"] = score
                if time_spent is not None:
                    updates["time_spent"] = db_content_progress.time_spent + time_spent
                if custom_data is not None:
                    existing_data = db_content_progress.custom_data or {}
                    existing_data.update(custom_data)
                    updates["custom_data"] = existing_data
                
                db_content_progress = self.user_content_progress_repo.update_content_progress(
                    progress_id=db_content_progress.id,
                    updates=updates
                )
            else:
                # Create new progress
                db_content_progress = self.user_content_progress_repo.create_content_progress(
                    user_id=user_uuid,
                    content_id=content_uuid,
                    status=status,
                    score=score,
                    time_spent=time_spent,
                    custom_data=custom_data
                )
            
            if not db_content_progress:
                return None
                
            return self._convert_db_user_content_progress_to_ui_user_content_progress(db_content_progress)
        except Exception as e:
            logger.error(f"Error updating content progress: {str(e)}")
            self.db.rollback()
            return None
    
    # Conversion Methods
    
    def _convert_db_progress_to_ui_progress(self, db_progress: DBProgress) -> Progress:
        """
        Convert a database progress to a UI progress.
        
        Args:
            db_progress: The database progress
            
        Returns:
            The corresponding UI progress
        """
        return Progress(
            id=str(db_progress.id),
            user_id=str(db_progress.user_id),
            course_id=str(db_progress.course_id),
            current_lesson_id=str(db_progress.current_lesson_id) if db_progress.current_lesson_id else None,
            total_points_earned=db_progress.total_points_earned,
            time_spent=db_progress.time_spent,
            progress_percentage=db_progress.progress_percentage,
            progress_data=db_progress.progress_data,
            last_accessed=db_progress.last_accessed,
            is_completed=db_progress.is_completed,
            created_at=db_progress.created_at,
            updated_at=db_progress.updated_at
        )
    
    def _convert_db_completed_lesson_to_ui_completed_lesson(self, db_completed_lesson: DBCompletedLesson) -> CompletedLesson:
        """
        Convert a database completed lesson to a UI completed lesson.
        
        Args:
            db_completed_lesson: The database completed lesson
            
        Returns:
            The corresponding UI completed lesson
        """
        return CompletedLesson(
            id=str(db_completed_lesson.id),
            user_id=str(db_completed_lesson.user_id),
            lesson_id=str(db_completed_lesson.lesson_id),
            course_id=str(db_completed_lesson.course_id),
            completed_at=db_completed_lesson.completed_at,
            score=db_completed_lesson.score,
            time_spent=db_completed_lesson.time_spent,
            created_at=db_completed_lesson.created_at,
            updated_at=db_completed_lesson.updated_at
        )
    
    def _convert_db_completed_course_to_ui_completed_course(self, db_completed_course: DBCompletedCourse) -> CompletedCourse:
        """
        Convert a database completed course to a UI completed course.
        
        Args:
            db_completed_course: The database completed course
            
        Returns:
            The corresponding UI completed course
        """
        return CompletedCourse(
            id=str(db_completed_course.id),
            user_id=str(db_completed_course.user_id),
            course_id=str(db_completed_course.course_id),
            completed_at=db_completed_course.completed_at,
            final_score=db_completed_course.final_score,
            total_time_spent=db_completed_course.total_time_spent,
            completed_lessons_count=db_completed_course.completed_lessons_count,
            achievements_earned=db_completed_course.achievements_earned,
            certificate_id=db_completed_course.certificate_id,
            created_at=db_completed_course.created_at,
            updated_at=db_completed_course.updated_at
        )
    
    def _convert_db_user_content_progress_to_ui_user_content_progress(self, db_content_progress: DBUserContentProgress) -> UserContentProgress:
        """
        Convert a database user content progress to a UI user content progress.
        
        Args:
            db_content_progress: The database user content progress
            
        Returns:
            The corresponding UI user content progress
        """
        return UserContentProgress(
            id=str(db_content_progress.id),
            user_id=str(db_content_progress.user_id),
            content_id=str(db_content_progress.content_id),
            lesson_id=str(db_content_progress.lesson_id) if db_content_progress.lesson_id else None,
            progress_id=str(db_content_progress.progress_id) if db_content_progress.progress_id else None,
            status=db_content_progress.status,
            score=db_content_progress.score,
            time_spent=db_content_progress.time_spent,
            last_interaction=db_content_progress.last_interaction,
            custom_data=db_content_progress.custom_data,
            created_at=db_content_progress.created_at,
            updated_at=db_content_progress.updated_at
        ) 