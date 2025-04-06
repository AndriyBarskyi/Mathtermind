"""
Lesson Service for Mathtermind application.

This module provides utilities for managing lesson-related operations
including retrieving lessons by ID or course, and converting lesson models.
"""

from typing import Optional, List
import uuid

# Import our logging and error handling framework
from src.core import get_logger
from src.core.error_handling import (
    handle_service_errors,
    ValidationError,
    ResourceNotFoundError,
    DatabaseError,
    report_error
)
from src.services.base_service import BaseService

from src.db import get_db
from src.db.repositories import lesson_repo
from src.models.lesson import Lesson
from src.db.models import Lesson as DBLesson

# Set up logging
logger = get_logger(__name__)

class LessonService(BaseService):
    """Service for managing lessons in the UI"""
    
    def __init__(self):
        super().__init__()
        # Connect to the database
        self.db = next(get_db())
    
    @handle_service_errors(service_name="lesson")
    def get_lesson_by_id(self, lesson_id: str) -> Optional[Lesson]:
        """
        Get a lesson by its ID
        
        Args:
            lesson_id: The ID of the lesson to retrieve
            
        Returns:
            The lesson if found, None otherwise
            
        Raises:
            ValidationError: If the lesson_id is invalid
            ResourceNotFoundError: If the lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Getting lesson by ID: {lesson_id}")
        
        if not lesson_id:
            logger.warning("Attempted to get lesson with empty ID")
            raise ValidationError(
                message="Lesson ID cannot be empty",
                details={"field": "lesson_id"}
            )
            
        try:
            # Convert string ID to UUID
            try:
                lesson_uuid = uuid.UUID(lesson_id)
            except ValueError as e:
                logger.warning(f"Invalid lesson ID format: {lesson_id}")
                raise ValidationError(
                    message="Invalid lesson ID format",
                    details={"field": "lesson_id", "error": str(e)}
                ) from e
                
            # Get lesson from repository
            with self.transaction(self.db) as session:
                db_lesson = lesson_repo.get_lesson(session, lesson_uuid)
                
            if not db_lesson:
                logger.warning(f"Lesson not found with ID: {lesson_id}")
                raise ResourceNotFoundError(
                    message="Lesson not found",
                    details={"lesson_id": lesson_id}
                )
                
            # Convert to UI model
            ui_lesson = self._convert_db_lesson_to_ui_lesson(db_lesson)
            logger.info(f"Successfully retrieved lesson: {lesson_id} - {ui_lesson.title}")
            return ui_lesson
            
        except (ValidationError, ResourceNotFoundError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error getting lesson by ID: {str(e)}")
            report_error(e, context={"lesson_id": lesson_id})
            raise DatabaseError(
                message="Failed to retrieve lesson",
                details={"lesson_id": lesson_id, "error": str(e)}
            ) from e

    @handle_service_errors(service_name="lesson")
    def get_lessons_by_course_id(self, course_id: str) -> List[Lesson]:
        """
        Get all lessons for a course
        
        Args:
            course_id: The ID of the course to get lessons for
            
        Returns:
            List of lessons for the course
            
        Raises:
            ValidationError: If the course_id is invalid
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Getting lessons for course: {course_id}")
        
        if not course_id:
            logger.warning("Attempted to get lessons with empty course ID")
            raise ValidationError(
                message="Course ID cannot be empty",
                details={"field": "course_id"}
            )
            
        try:
            # Convert string ID to UUID
            try:
                course_uuid = uuid.UUID(course_id)
            except ValueError as e:
                logger.warning(f"Invalid course ID format: {course_id}")
                raise ValidationError(
                    message="Invalid course ID format",
                    details={"field": "course_id", "error": str(e)}
                ) from e
                
            # Get lessons from repository
            with self.transaction(self.db) as session:
                db_lessons = lesson_repo.get_lessons_by_course_id(session, course_uuid)
                
            # Convert to UI models
            ui_lessons = [
                self._convert_db_lesson_to_ui_lesson(lesson) 
                for lesson in db_lessons
            ]
            
            logger.info(f"Successfully retrieved {len(ui_lessons)} lessons for course: {course_id}")
            return ui_lessons
            
        except ValidationError:
            # Allow ValidationError to propagate
            raise
        except Exception as e:
            logger.error(f"Error getting lessons by course ID: {str(e)}")
            report_error(e, context={"course_id": course_id})
            raise DatabaseError(
                message="Failed to retrieve lessons for course",
                details={"course_id": course_id, "error": str(e)}
            ) from e

    @handle_service_errors(service_name="lesson")
    def _convert_db_lesson_to_ui_lesson(self, db_lesson: DBLesson) -> Lesson:
        """
        Convert a database lesson model to a UI lesson model
        
        Args:
            db_lesson: The database lesson model to convert
            
        Returns:
            The converted UI lesson model
            
        Raises:
            ValidationError: If the database lesson is invalid
        """
        if not db_lesson:
            logger.warning("Attempted to convert null lesson")
            raise ValidationError(
                message="Cannot convert null lesson",
                details={"error": "db_lesson is None"}
            )
            
        try:
            lesson_id = str(db_lesson.id) if hasattr(db_lesson, 'id') else "unknown"
            logger.debug(f"Converting DB lesson to UI lesson: {lesson_id}")
            
            # Create default prerequisites and learning objectives if they don't exist
            prerequisites = getattr(db_lesson, 'prerequisites', {})
            if prerequisites is None:
                prerequisites = {}
                
            learning_objectives = getattr(db_lesson, 'learning_objectives', [])
            if learning_objectives is None:
                learning_objectives = []
            
            # Create content if it doesn't exist
            content = getattr(db_lesson, 'content', {})
            if content is None:
                content = {}
            
            lesson_type = db_lesson.lesson_type
            if hasattr(lesson_type, 'value'):
                lesson_type = lesson_type.value
                
            difficulty_level = db_lesson.difficulty_level
            if hasattr(difficulty_level, 'value'):
                difficulty_level = difficulty_level.value
            
            # Create the lesson model
            ui_lesson = Lesson(
                id=lesson_id,
                title=db_lesson.title,
                content=content,
                lesson_type=lesson_type,
                difficulty_level=difficulty_level,
                lesson_order=db_lesson.lesson_order,
                estimated_time=db_lesson.estimated_time,
                points_reward=db_lesson.points_reward,
                prerequisites=prerequisites,
                learning_objectives=learning_objectives
            )
            
            logger.debug(f"Successfully converted lesson: {lesson_id}")
            return ui_lesson
            
        except Exception as e:
            logger.error(f"Error converting DB lesson to UI lesson: {str(e)}")
            report_error(e, context={"lesson_id": getattr(db_lesson, 'id', 'unknown')})
            
            # Return a default lesson as fallback
            logger.warning("Creating fallback lesson model due to conversion error")
            return Lesson(
                id=str(db_lesson.id) if hasattr(db_lesson, 'id') else "unknown",
                title=db_lesson.title if hasattr(db_lesson, 'title') else "Unknown Lesson",
                content={},
                lesson_type="THEORY",
                difficulty_level="BEGINNER",
                lesson_order=1,
                estimated_time=30,
                points_reward=10,
                prerequisites={},
                learning_objectives=[]
            ) 