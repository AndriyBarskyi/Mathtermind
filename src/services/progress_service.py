"""
Progress service for Mathtermind.

This module provides service methods for tracking user progress in courses and lessons.
"""

from typing import List, Optional, Dict, Any, Union, Tuple
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
    CourseRepository,
    ContentRepository
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
        self.progress_repo = ProgressRepository()
        self.content_state_repo = ContentStateRepository()
        self.completed_lesson_repo = CompletedLessonRepository()
        self.completed_course_repo = CompletedCourseRepository()
        self.user_content_progress_repo = UserContentProgressRepository()
        self.lesson_repo = LessonRepository()
        self.course_repo = CourseRepository()
        self.content_repo = ContentRepository()
    
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
            if not user_id:
                logger.error("User ID is required to get progress data")
                return []
                
            user_uuid = uuid.UUID(user_id)
            
            # Get all progress records for the user
            db_progress_records = self.progress_repo.get_user_progress(user_uuid)
            
            # Convert to UI models
            return [self._convert_db_progress_to_ui_progress(record) for record in db_progress_records]
        except Exception as e:
            logger.error(f"Error getting user progress: {str(e)}")
            import traceback
            logger.debug(traceback.format_exc())
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
            if not user_id or not course_id:
                logger.error("Both user_id and course_id are required to get course progress")
                return None
                
            user_uuid = uuid.UUID(user_id)
            course_uuid = uuid.UUID(course_id)
            
            # Get the progress for the course
            db_progress = self.progress_repo.get_course_progress(self.db, user_uuid, course_uuid)
            
            if not db_progress:
                return None
                
            return self._convert_db_progress_to_ui_progress(db_progress)
        except Exception as e:
            logger.error(f"Error getting course progress: {str(e)}")
            import traceback
            logger.debug(traceback.format_exc())
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
            existing_progress = self.progress_repo.get_course_progress(self.db, user_uuid, course_uuid)
            if existing_progress:
                return self._convert_db_progress_to_ui_progress(existing_progress)
            
            # Get the first lesson of the course
            course = self.course_repo.get_by_id(self.db, course_uuid)
            if not course:
                logger.warning(f"Course not found: {course_id}")
                return None
                
            # Get all lessons and use the first one based on order
            lessons = self.lesson_repo.get_lessons_by_course_id(self.db, course_uuid)
            first_lesson_id = lessons[0].id if lessons else None
            
            # Create the progress
            db_progress = self.progress_repo.create_progress(
                self.db,
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
                     time_spent: int = 30) -> Optional[CompletedLesson]:
        """
        Mark a lesson as complete for a user.
        
        Args:
            user_id: The ID of the user
            lesson_id: The ID of the lesson
            course_id: The ID of the course the lesson belongs to
            score: Optional score achieved in the lesson
            time_spent: Time spent on the lesson in minutes (default: 30)
            
        Returns:
            The completed lesson record if successful, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            lesson_uuid = uuid.UUID(lesson_id)
            course_uuid = uuid.UUID(course_id)
            
            # Check if the lesson is already completed
            existing = self.completed_lesson_repo.is_lesson_completed(
                self.db,
                user_uuid, 
                lesson_uuid
            )
            
            if existing:
                logger.info(f"Lesson {lesson_id} already completed by user {user_id}")
                
                # Get the existing completed lesson
                completed_lesson = self.completed_lesson_repo.get_completed_lesson(
                    self.db,
                    user_uuid,
                    lesson_uuid
                )
                
                if completed_lesson:
                    return self._convert_db_completed_lesson_to_ui_completed_lesson(completed_lesson)
                return None
            
            # Create completed lesson record
            completed_lesson = self.completed_lesson_repo.complete_lesson(
                self.db,
                user_uuid,
                lesson_uuid,
                course_uuid,
                score,
                time_spent
            )
            
            if not completed_lesson:
                return None
                
            # Update course progress
            progress = self.progress_repo.get_course_progress(
                self.db,
                user_uuid,
                course_uuid
            )
            
            if progress:
                # Update progress details
                self.update_progress_percentage(
                    progress_id=str(progress.id),
                    percentage=self._calculate_course_completion_percentage(user_id, course_id)
                )
            
            # Convert to UI model and return
            return self._convert_db_completed_lesson_to_ui_completed_lesson(completed_lesson)
            
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
            A list of completed lessons
        """
        try:
            user_uuid = uuid.UUID(user_id)
            
            # Get all completed lessons for the user
            db_completed_lessons = self.completed_lesson_repo.get_user_completed_lessons(self.db, user_uuid)
            
            # Convert to UI models
            return [self._convert_db_completed_lesson_to_ui_completed_lesson(lesson) for lesson in db_completed_lessons]
        except Exception as e:
            logger.error(f"Error getting user completed lessons: {str(e)}")
            return []
    
    def has_completed_lesson(self, user_id: str, lesson_id: str) -> bool:
        """
        Check if a user has completed a specific lesson.
        
        Args:
            user_id: The ID of the user
            lesson_id: The ID of the lesson to check
            
        Returns:
            True if the user has completed the lesson, False otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            lesson_uuid = uuid.UUID(lesson_id)
            
            # Check if the lesson exists in the user's completed lessons
            is_completed = self.completed_lesson_repo.is_lesson_completed(
                self.db,
                user_uuid, 
                lesson_uuid
            )
            
            return is_completed
        except Exception as e:
            logger.error(f"Error checking if lesson is completed: {str(e)}")
            return False
    
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
                self.db, user_uuid, course_uuid
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

    def mark_lesson_complete(self, user_id: str, lesson_id: str) -> bool:
        """
        Mark a lesson as complete for a user.
        
        Args:
            user_id: The ID of the user
            lesson_id: The ID of the lesson
            
        Returns:
            True if the lesson was marked as complete, False otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            lesson_uuid = uuid.UUID(lesson_id)
            
            # Get the lesson to verify it exists
            lesson = self.lesson_repo.get_lesson(self.db, lesson_uuid)
            if not lesson:
                logger.warning(f"Lesson not found with ID: {lesson_id}")
                return False
                
            # Get the course ID from the lesson
            course_id = lesson.course_id
            
            # Complete the lesson
            return self.complete_lesson(user_id, str(course_id), lesson_id)
        except Exception as e:
            logger.error(f"Error marking lesson as complete: {str(e)}")
            return False

    def get_lesson_score(self, user_id: str, lesson_id: str) -> float:
        """
        Get the user's score for a lesson.
        
        Args:
            user_id: The ID of the user
            lesson_id: The ID of the lesson
            
        Returns:
            The user's score for the lesson (0-100)
        """
        try:
            user_uuid = uuid.UUID(user_id)
            lesson_uuid = uuid.UUID(lesson_id)
            
            # Check if the lesson is completed
            completed_lesson = self.completed_lesson_repo.get_by_user_and_lesson(
                self.db, user_uuid, lesson_uuid
            )
            
            if completed_lesson and completed_lesson.score is not None:
                return completed_lesson.score
                
            # If not completed, calculate average from content progress
            content_items = self.lesson_repo.get_lesson_content(self.db, lesson_uuid)
            if not content_items:
                return 0.0
                
            total_score = 0.0
            scored_items = 0
            
            for content in content_items:
                progress = self.user_content_progress_repo.get_progress(
                    self.db, user_uuid, content.id
                )
                if progress and progress.score is not None:
                    total_score += progress.score
                    scored_items += 1
                    
            if scored_items == 0:
                return 0.0
                
            return total_score / scored_items
        except Exception as e:
            logger.error(f"Error getting lesson score: {str(e)}")
            return 0.0

    def get_completed_content_ids(self, user_id: str, lesson_id: str) -> List[str]:
        """
        Get the IDs of content items the user has completed in a lesson.
        
        Args:
            user_id: The ID of the user
            lesson_id: The ID of the lesson
            
        Returns:
            List of content IDs the user has completed
        """
        try:
            user_uuid = uuid.UUID(user_id)
            lesson_uuid = uuid.UUID(lesson_id)
            
            # Check if the lesson is completed
            completed_lesson = self.completed_lesson_repo.get_by_user_and_lesson(
                self.db, user_uuid, lesson_uuid
            )
            
            if completed_lesson:
                # Get all content items for the lesson
                content_items = self.lesson_repo.get_lesson_content(self.db, lesson_uuid)
                return [str(item.id) for item in content_items]
                
            # If not, get individually completed content items
            content_items = self.lesson_repo.get_lesson_content(self.db, lesson_uuid)
            completed_ids = []
            
            for content in content_items:
                progress = self.user_content_progress_repo.get_progress(
                    self.db, user_uuid, content.id
                )
                if progress and progress.is_completed:
                    completed_ids.append(str(content.id))
                    
            return completed_ids
        except Exception as e:
            logger.error(f"Error getting completed content IDs: {str(e)}")
            return []

    def get_time_spent_on_lesson(self, user_id: str, lesson_id: str) -> int:
        """
        Get the total time spent on a lesson by the user.
        
        Args:
            user_id: The ID of the user
            lesson_id: The ID of the lesson
            
        Returns:
            Time spent in minutes
        """
        try:
            user_uuid = uuid.UUID(user_id)
            lesson_uuid = uuid.UUID(lesson_id)
            
            # Check if the lesson is completed
            completed_lesson = self.completed_lesson_repo.get_by_user_and_lesson(
                self.db, user_uuid, lesson_uuid
            )
            
            if completed_lesson and completed_lesson.time_spent is not None:
                return completed_lesson.time_spent
                
            # If not, sum up time from content progress
            content_items = self.lesson_repo.get_lesson_content(self.db, lesson_uuid)
            total_time = 0
            
            for content in content_items:
                progress = self.user_content_progress_repo.get_progress(
                    self.db, user_uuid, content.id
                )
                if progress and progress.time_spent is not None:
                    total_time += progress.time_spent
                    
            return total_time
        except Exception as e:
            logger.error(f"Error getting time spent on lesson: {str(e)}")
            return 0

    def has_completed_content(self, user_id: str, content_id: str) -> bool:
        """
        Check if a user has completed a specific content item.
        
        Args:
            user_id: The ID of the user
            content_id: The ID of the content item
            
        Returns:
            True if the user has completed the content, False otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            content_uuid = uuid.UUID(content_id)
            
            progress = self.user_content_progress_repo.get_progress(
                self.db, user_uuid, content_uuid
            )
            
            return progress is not None and progress.is_completed
        except Exception as e:
            logger.error(f"Error checking if content is completed: {str(e)}")
            return False
    
    def get_assessment_score(self, user_id: str, lesson_id: str) -> Optional[float]:
        """
        Get the user's assessment score for a lesson.
        
        Args:
            user_id: The ID of the user
            lesson_id: The ID of the lesson
            
        Returns:
            The assessment score or None if not available
        """
        try:
            user_uuid = uuid.UUID(user_id)
            lesson_uuid = uuid.UUID(lesson_id)
            
            # First check if there's a score in the completed lesson
            completed_lesson = self.completed_lesson_repo.get_by_user_and_lesson(
                self.db, user_uuid, lesson_uuid
            )
            
            if completed_lesson and completed_lesson.score is not None:
                return completed_lesson.score
            
            # Otherwise, look for assessment content in the lesson
            content_items = self.lesson_repo.get_lesson_content(self.db, lesson_uuid)
            
            for content in content_items:
                # Check if content is assessment type
                if content.content_type.lower() in ['assessment', 'quiz', 'test', 'exam']:
                    progress = self.user_content_progress_repo.get_progress(
                        self.db, user_uuid, content.id
                    )
                    if progress and progress.score is not None:
                        return progress.score
            
            return None
        except Exception as e:
            logger.error(f"Error getting assessment score: {str(e)}")
            return None
    
    def get_time_spent(self, user_id: str, lesson_id: str) -> Optional[int]:
        """
        Get the total time spent on a lesson.
        
        Args:
            user_id: The ID of the user
            lesson_id: The ID of the lesson
            
        Returns:
            Time spent in minutes or None if not available
        """
        try:
            # Reuse existing method
            return self.get_time_spent_on_lesson(user_id, lesson_id)
        except Exception as e:
            logger.error(f"Error getting time spent: {str(e)}")
            return None
    
    def get_activity_count(self, user_id: str, lesson_id: str) -> int:
        """
        Get the count of user activities in a lesson.
        
        Args:
            user_id: The ID of the user
            lesson_id: The ID of the lesson
            
        Returns:
            The number of activities recorded
        """
        try:
            user_uuid = uuid.UUID(user_id)
            lesson_uuid = uuid.UUID(lesson_id)
            
            # Get all content items for the lesson
            content_items = self.lesson_repo.get_lesson_content(self.db, lesson_uuid)
            
            activity_count = 0
            
            for content in content_items:
                progress = self.user_content_progress_repo.get_progress(
                    self.db, user_uuid, content.id
                )
                if progress:
                    # If there's any interaction data, count it as an activity
                    activity_count += 1
            
            return activity_count
        except Exception as e:
            logger.error(f"Error getting activity count: {str(e)}")
            return 0
    
    def has_content_interaction(self, user_id: str, content_id: str) -> bool:
        """
        Check if a user has interacted with a specific content item.
        
        Args:
            user_id: The ID of the user
            content_id: The ID of the content item
            
        Returns:
            True if the user has interacted with the content, False otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            content_uuid = uuid.UUID(content_id)
            
            progress = self.user_content_progress_repo.get_progress(
                self.db, user_uuid, content_uuid
            )
            
            return progress is not None
        except Exception as e:
            logger.error(f"Error checking content interaction: {str(e)}")
            return False

    def get_all_user_completed_content_items(self, user_id: str) -> List[UserContentProgress]:
        """
        Get all content items marked as 'completed' for a user.

        Args:
            user_id: The ID of the user.

        Returns:
            A list of UserContentProgress objects.
        """
        try:
            user_uuid = uuid.UUID(user_id)
            db_items = self.user_content_progress_repo.get_all_completed_by_user(self.db, user_uuid)
            return [self._convert_db_user_content_progress_to_ui_user_content_progress(item) for item in db_items]
        except Exception as e:
            logger.error(f"Error getting all completed content items for user {user_id}: {str(e)}")
            return []

    def calculate_weighted_course_progress(self, user_id: str, course_id: str) -> Tuple[float, Dict[str, Any]]:
        """
        Calculate a weighted progress percentage based on content difficulty and importance.
        
        This method implements a more sophisticated progress calculation algorithm that
        considers each content item's difficulty level and assigned importance when
        calculating overall course progress. Content with higher difficulty or importance
        contributes more to the overall progress percentage.
        
        Args:
            user_id: The ID of the user
            course_id: The ID of the course
            
        Returns:
            A tuple containing:
            - The weighted progress percentage (0-100)
            - A dictionary with detailed progress metrics
        """
        try:
            user_uuid = uuid.UUID(user_id)
            course_uuid = uuid.UUID(course_id)
            
            # Get all lessons in the course
            lessons = self.lesson_repo.get_lessons_by_course_id(self.db, course_uuid)
            if not lessons:
                logger.warning(f"No lessons found for course ID: {course_id}")
                return 0.0, {"status": "no_lessons", "details": {}}

            # Collect all content items across all lessons
            all_content = []
            lesson_weights = {}
            for lesson in lessons:
                # Get lesson content items
                lesson_obj, content_items = self.lesson_repo.get_lesson_with_content(self.db, lesson.id)
                all_content.extend(content_items)
                
                # Calculate lesson weight based on its position in the course and difficulty
                # Earlier lessons typically have lower weights as they are foundational
                order_factor = lesson.lesson_order / len(lessons)  # Normalized to 0-1
                difficulty_factor = lesson.difficulty_level.value / 5.0  # Assuming 5 levels, normalized to 0-1
                
                # Combine factors: later lessons and higher difficulty increase weight
                lesson_weights[str(lesson.id)] = 0.5 + ((order_factor + difficulty_factor) / 2) * 0.5
            
            if not all_content:
                logger.warning(f"No content items found for course ID: {course_id}")
                return 0.0, {"status": "no_content", "details": {}}
            
            # Calculate the weight of each content item
            content_weights = {}
            total_weight = 0.0
            
            for content in all_content:
                # Base weight considering content type importance
                base_weight = 1.0
                if content.content_type.lower() in ['assessment', 'quiz', 'exam']:
                    base_weight = 2.0  # Assessments count twice as much
                elif content.content_type.lower() in ['exercise', 'practice']:
                    base_weight = 1.5  # Exercises count 1.5 times as much
                
                # Adjust weight by content metadata if available
                if hasattr(content, 'metadata') and content.metadata:
                    # Consider importance if specified in metadata
                    importance = content.metadata.get('importance', 1.0)
                    base_weight *= importance
                    
                    # Consider points value if specified
                    points = content.metadata.get('points', 1.0)
                    base_weight *= points
                
                # Factor in the lesson weight
                lesson_id = str(content.lesson_id) if hasattr(content, 'lesson_id') else None
                if lesson_id and lesson_id in lesson_weights:
                    base_weight *= lesson_weights[lesson_id]
                
                content_weights[str(content.id)] = base_weight
                total_weight += base_weight
            
            # Normalize weights so they sum to 1.0
            if total_weight > 0:
                for content_id in content_weights:
                    content_weights[content_id] /= total_weight
            
            # Get all completed content for this user and course
            completed_content_ids = set()
            partial_content_progress = {}
            
            # Check which content items the user has completed
            for content in all_content:
                content_id = str(content.id)
                
                # Get progress for this content
                progress = self.user_content_progress_repo.get_progress(
                    self.db, user_uuid, content.id
                )
                
                if progress:
                    if progress.status.lower() == 'completed':
                        completed_content_ids.add(content_id)
                    elif hasattr(progress, 'percentage') and progress.percentage is not None:
                        # Store partial progress if available
                        partial_content_progress[content_id] = progress.percentage / 100.0
                    elif hasattr(progress, 'score') and progress.score is not None:
                        # Use score as percentage if available
                        partial_content_progress[content_id] = progress.score / 100.0
            
            # Calculate weighted progress
            weighted_progress = 0.0
            
            # Add up weights for completed content
            for content_id in completed_content_ids:
                weighted_progress += content_weights.get(content_id, 0.0)
            
            # Add partial progress for in-progress content
            for content_id, partial in partial_content_progress.items():
                if content_id not in completed_content_ids:  # Don't double count
                    weighted_progress += content_weights.get(content_id, 0.0) * partial
            
            # Convert to percentage (0-100)
            weighted_percentage = float(weighted_progress * 100.0)
            
            # Prepare detailed metrics
            details = {
                "completed_count": len(completed_content_ids),
                "total_count": len(all_content),
                "completion_ratio": len(completed_content_ids) / len(all_content),
                "partial_progress_count": len(partial_content_progress),
                "content_weights": content_weights,
                "lesson_weights": lesson_weights,
            }
            
            # Update the progress record in the database
            progress_record = self.progress_repo.get_course_progress(self.db, user_uuid, course_uuid)
            if progress_record:
                self.progress_repo.update_progress_percentage(
                    self.db, progress_record.id, weighted_percentage
                )
                
                # Update progress_data with detailed metrics
                self.progress_repo.update_progress_data(
                    self.db, progress_record.id, 
                    {
                        "weighted_calculation": details,
                        "last_calculation": datetime.utcnow().isoformat()
                    }
                )
            
            return weighted_percentage, {"status": "success", "details": details}
        except Exception as e:
            logger.error(f"Error calculating weighted progress: {str(e)}")
            return 0.0, {"status": "error", "message": str(e)}

    def update_course_progress_with_weighting(self, user_id: str, course_id: str) -> Optional[Progress]:
        """
        Update course progress using the weighted calculation algorithm.
        
        This method applies the weighted progress calculation and updates the progress record
        in the database, returning the updated Progress model.
        
        Args:
            user_id: The ID of the user
            course_id: The ID of the course
            
        Returns:
            The updated progress record if successful, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            course_uuid = uuid.UUID(course_id)
            
            # Get existing progress or create new
            progress_record = self.progress_repo.get_course_progress(self.db, user_uuid, course_uuid)
            if not progress_record:
                # Create a new progress record if one doesn't exist
                progress_record = self.create_course_progress(user_id, course_id)
                if not progress_record:
                    return None
            
            # Calculate weighted progress
            weighted_percentage, details = self.calculate_weighted_course_progress(user_id, course_id)
            
            # If calculation was successful, return the updated progress
            if details.get("status") == "success":
                # Fetch the latest progress record
                updated_record = self.progress_repo.get_course_progress(self.db, user_uuid, course_uuid)
                if updated_record:
                    return self._convert_db_progress_to_ui_progress(updated_record)
            
            return None
        except Exception as e:
            logger.error(f"Error updating course progress with weighting: {str(e)}")
            return None
            
    def sync_progress_data(self, user_id: str, course_id: str) -> bool:
        """
        Synchronize progress data between related repositories.
        
        This method ensures that progress data is consistent across different repositories,
        such as updating progress percentages when lessons are completed or ensuring
        that completed lesson counts match the course progress.
        
        Args:
            user_id: The ID of the user
            course_id: The ID of the course
            
        Returns:
            True if synchronization was successful, False otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            course_uuid = uuid.UUID(course_id)
            
            # Get the progress record
            progress = self.progress_repo.get_course_progress(self.db, user_uuid, course_uuid)
            if not progress:
                logger.warning(f"No progress record found for user {user_id} in course {course_id}")
                return False
            
            # Get all lessons in the course
            lessons = self.lesson_repo.get_lessons_by_course_id(self.db, course_uuid)
            if not lessons:
                logger.warning(f"No lessons found for course {course_id}")
                return False
            
            # Get completed lessons
            completed_lessons = self.completed_lesson_repo.get_course_completed_lessons(
                self.db, user_uuid, course_uuid
            )
            completed_lesson_ids = {str(lesson.lesson_id) for lesson in completed_lessons}
            
            # Count total lessons and calculate simple percentage
            total_lessons = len(lessons)
            completed_count = len(completed_lesson_ids)
            simple_percentage = (completed_count / total_lessons * 100) if total_lessons > 0 else 0
            
            # Get the course completion record if it exists
            course_completion = self.completed_course_repo.get_course_completion(
                self.db, user_uuid, course_uuid
            )
            
            # Gather all content progress
            content_progress = []
            for lesson in lessons:
                # Get all content for the lesson
                lesson_obj, content_items = self.lesson_repo.get_lesson_with_content(self.db, lesson.id)
                for content in content_items:
                    progress_item = self.user_content_progress_repo.get_progress(
                        self.db, user_uuid, content.id
                    )
                    if progress_item:
                        content_progress.append(progress_item)
            
            # Calculate total time spent
            total_time_spent = sum(item.time_spent for item in content_progress if item.time_spent is not None)
            
            # Calculate average score
            scores = [item.score for item in content_progress if item.score is not None]
            avg_score = sum(scores) / len(scores) if scores else None
            
            # Update the progress record with synchronized data
            updates = {
                "time_spent": total_time_spent,
                "progress_data": {
                    "completed_lesson_count": completed_count,
                    "total_lesson_count": total_lessons,
                    "simple_percentage": simple_percentage,
                    "average_score": avg_score,
                    "content_progress_count": len(content_progress),
                    "last_sync": datetime.utcnow().isoformat()
                }
            }
            
            # Update the progress record
            self.progress_repo.update_progress_data(
                self.db, progress.id, updates["progress_data"]
            )
            
            # If all lessons are completed but course is not marked as completed, update it
            if completed_count == total_lessons and total_lessons > 0 and not progress.is_completed:
                self.progress_repo.complete_progress(
                    self.db, progress.id
                )
                
                # Create course completion record if it doesn't exist
                if not course_completion:
                    self.completed_course_repo.create_completed_course(
                        self.db,
                        user_id=user_uuid,
                        course_id=course_uuid,
                        final_score=avg_score,
                        total_time_spent=total_time_spent,
                        completed_lessons_count=completed_count
                    )
            
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Error synchronizing progress data: {str(e)}")
            self.db.rollback()
            return False

    def _calculate_course_completion_percentage(self, user_id: str, course_id: str) -> float:
        """
        Calculate the percentage of completion for a course.
        
        Args:
            user_id: The ID of the user
            course_id: The ID of the course
            
        Returns:
            The completion percentage (0-100)
        """
        try:
            user_uuid = uuid.UUID(user_id)
            course_uuid = uuid.UUID(course_id)
            
            # Get all lessons in the course
            lessons = self.lesson_repo.get_lessons_by_course_id(self.db, course_uuid)
            if not lessons:
                logger.warning(f"No lessons found for course ID: {course_id}")
                return 0.0
                
            # Count total lessons
            total_lessons = len(lessons)
            
            # Count completed lessons
            completed_count = self.completed_lesson_repo.count_completed_lessons(
                self.db, user_uuid, course_uuid
            )
            
            # Calculate percentage
            if total_lessons > 0:
                percentage = (completed_count / total_lessons) * 100
            else:
                percentage = 0.0
                
            logger.info(f"Course completion: {completed_count}/{total_lessons} = {percentage:.2f}%")
            return percentage
            
        except Exception as e:
            logger.error(f"Error calculating course completion percentage: {str(e)}")
            return 0.0 