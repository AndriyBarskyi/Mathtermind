"""
Lesson Service for Mathtermind application.

This module provides utilities for managing lesson-related operations
including retrieving lessons by ID or course, and converting lesson models.
"""

from typing import Optional, List, Dict, Any, Tuple
import uuid
from datetime import datetime
import logging
from sqlalchemy.orm import Session

# Import our logging and error handling framework
from src.core import get_logger
from src.core.error_handling import (
    handle_service_errors,
    ValidationError,
    ResourceNotFoundError,
    DatabaseError,
    BusinessLogicError,
    report_error
)
from src.services.base_service import BaseService

from src.db import get_db
from src.db.repositories import lesson_repo
from src.models.lesson import Lesson
from src.db.models import Lesson as DBLesson
from src.db.models.enums import LessonType, DifficultyLevel
from src.services.progress_service import ProgressService

# Set up logging
logger = get_logger(__name__)

class LessonService(BaseService):
    """Service for managing lessons in the UI"""
    
    def __init__(self, repo=None):
        super().__init__()
        # Connect to the database
        self.db = next(get_db())
        # Use the provided repository (for testing) or create a new one
        self.lesson_repo = repo if repo is not None else lesson_repo
        # Create an instance of the progress service for checking lesson completion
        self.progress_service = ProgressService()
    
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
            with self.transaction() as session:
                db_lesson = self.lesson_repo.get_lesson(session, lesson_uuid)

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
            with self.transaction() as session:
                db_lessons = self.lesson_repo.get_lessons_by_course_id(session, course_uuid)
                
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
    def create_lesson(self, course_id: str, title: str, 
                     difficulty_level: str, lesson_order: int, 
                     estimated_time: int, points_reward: int = 10,
                     prerequisites: Optional[Dict[str, Any]] = None,
                     learning_objectives: Optional[List[str]] = None,
                     content: Optional[Dict[str, Any]] = None) -> Lesson:
        """
        Create a new lesson for a course
        
        Args:
            course_id: ID of the course this lesson belongs to
            title: Title of the lesson
            difficulty_level: Difficulty level of the lesson
            lesson_order: Order of the lesson within the course
            estimated_time: Estimated time to complete the lesson (in minutes)
            points_reward: Points earned when completing the lesson
            prerequisites: Prerequisites for the lesson (optional)
            learning_objectives: Learning objectives for the lesson (optional)
            content: Initial content for the lesson (optional)
            
        Returns:
            The created lesson
            
        Raises:
            ValidationError: If any of the required fields are invalid
            DatabaseError: If there is an error accessing the database
            
        Note:
            Lessons don't have types. Only content items within lessons have types.
            Lessons are containers that organize different types of content.
        """
        logger.info(f"Creating new lesson for course {course_id}: {title}")
        
        # Validate required fields
        if not title or title.strip() == "":
            logger.warning("Attempted to create lesson with empty title")
            raise ValidationError(
                message="Lesson title cannot be empty",
                details={"field": "title"}
            )
            
        if not course_id:
            logger.warning("Attempted to create lesson with empty course ID")
            raise ValidationError(
                message="Course ID cannot be empty",
                details={"field": "course_id"}
            )
            
        # Set default values for optional fields
        if prerequisites is None:
            prerequisites = {}
            
        if learning_objectives is None:
            learning_objectives = []
            
        if content is None:
            content = {}
            
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
                
            # Create lesson in repository
            with self.transaction() as session:
                db_lesson = self.lesson_repo.create_lesson(
                    session,
                    course_id=course_uuid,
                    title=title,
                    difficulty_level=difficulty_level,
                    lesson_order=lesson_order,
                    estimated_time=estimated_time,
                    points_reward=points_reward,
                    prerequisites=prerequisites,
                    learning_objectives=learning_objectives,
                    content=content
                )
                
            # Convert to UI model
            ui_lesson = self._convert_db_lesson_to_ui_lesson(db_lesson)
            logger.info(f"Successfully created lesson: {str(db_lesson.id)} - {title}")
            return ui_lesson
            
        except Exception as e:
            logger.error(f"Error creating lesson: {str(e)}")
            report_error(e, context={
                "course_id": course_id,
                "title": title
            })
            raise DatabaseError(
                message="Failed to create lesson",
                details={"course_id": course_id, "title": title, "error": str(e)}
            ) from e
            
    @handle_service_errors(service_name="lesson")
    def update_lesson(self, lesson_id: str, **updates) -> Lesson:
        """
        Update an existing lesson
        
        Args:
            lesson_id: ID of the lesson to update
            **updates: Fields to update as keyword arguments
            
        Returns:
            The updated lesson
            
        Raises:
            ValidationError: If any of the fields are invalid
            ResourceNotFoundError: If the lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Updating lesson {lesson_id}")
        
        if not lesson_id:
            logger.warning("Attempted to update lesson with empty ID")
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
                
            # Get the lesson to ensure it exists
            with self.transaction() as session:
                db_lesson = self.lesson_repo.get_lesson(session, lesson_uuid)
                
            if not db_lesson:
                logger.warning(f"Lesson not found with ID: {lesson_id}")
                raise ResourceNotFoundError(
                    message="Lesson not found",
                    details={"lesson_id": lesson_id}
                )
                
            # Validate title if it's being updated
            if 'title' in updates and (not updates['title'] or updates['title'].strip() == ""):
                logger.warning("Attempted to update lesson with empty title")
                raise ValidationError(
                    message="Lesson title cannot be empty",
                    details={"field": "title"}
                )
                
            # Update lesson in repository
            with self.transaction() as session:
                updated_db_lesson = self.lesson_repo.update_lesson(
                    session,
                    lesson_id=lesson_uuid,
                    **updates
                )
                
            # Convert to UI model
            ui_lesson = self._convert_db_lesson_to_ui_lesson(updated_db_lesson)
            logger.info(f"Successfully updated lesson: {lesson_id}")
            return ui_lesson
            
        except (ValidationError, ResourceNotFoundError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error updating lesson: {str(e)}")
            report_error(e, context={"lesson_id": lesson_id, "updates": updates})
            raise DatabaseError(
                message="Failed to update lesson",
                details={"lesson_id": lesson_id, "error": str(e)}
            ) from e
            
    @handle_service_errors(service_name="lesson")
    def delete_lesson(self, lesson_id: str) -> bool:
        """
        Delete a lesson
        
        Args:
            lesson_id: ID of the lesson to delete
            
        Returns:
            True if the lesson was deleted, False otherwise
            
        Raises:
            ValidationError: If the lesson_id is invalid
            ResourceNotFoundError: If the lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Deleting lesson {lesson_id}")
        
        if not lesson_id:
            logger.warning("Attempted to delete lesson with empty ID")
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
                
            # Get the lesson to ensure it exists
            with self.transaction() as session:
                db_lesson = self.lesson_repo.get_lesson(session, lesson_uuid)
                
            if not db_lesson:
                logger.warning(f"Lesson not found with ID: {lesson_id}")
                raise ResourceNotFoundError(
                    message="Lesson not found",
                    details={"lesson_id": lesson_id}
                )
                
            # Delete lesson from repository
            with self.transaction() as session:
                result = self.lesson_repo.delete_lesson(session, lesson_uuid)
                
            logger.info(f"Successfully deleted lesson: {lesson_id}")
            return result is not None
            
        except (ValidationError, ResourceNotFoundError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error deleting lesson: {str(e)}")
            report_error(e, context={"lesson_id": lesson_id})
            raise DatabaseError(
                message="Failed to delete lesson",
                details={"lesson_id": lesson_id, "error": str(e)}
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
            
            # Note: lesson_type is intentionally not included - lessons don't have types,
            # only content items within them have types
            
            difficulty_level = db_lesson.difficulty_level
            if hasattr(difficulty_level, 'value'):
                difficulty_level = difficulty_level.value
            
            # Get course_id
            course_id = str(db_lesson.course_id) if hasattr(db_lesson, 'course_id') else "unknown"
            
            # Create the lesson model
            ui_lesson = Lesson(
                id=lesson_id,
                title=db_lesson.title,
                content=content,
                difficulty_level=difficulty_level,
                lesson_order=db_lesson.lesson_order,
                estimated_time=db_lesson.estimated_time,
                points_reward=db_lesson.points_reward,
                prerequisites=prerequisites,
                learning_objectives=learning_objectives,
                course_id=course_id
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
                difficulty_level="BEGINNER",
                lesson_order=1,
                estimated_time=30,
                points_reward=10,
                prerequisites={},
                learning_objectives=[],
                course_id=str(db_lesson.course_id) if hasattr(db_lesson, 'course_id') else "unknown"
            )

    @handle_service_errors(service_name="lesson")
    def update_lesson_order(self, lesson_id: str, new_order: int) -> bool:
        """
        Update the order of a lesson within its course
        
        Args:
            lesson_id: ID of the lesson to update
            new_order: New order for the lesson
            
        Returns:
            True if the order was updated, False otherwise
            
        Raises:
            ValidationError: If the lesson_id or new_order is invalid
            ResourceNotFoundError: If the lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Updating order for lesson {lesson_id} to {new_order}")
        
        if not lesson_id:
            logger.warning("Attempted to update lesson order with empty ID")
            raise ValidationError(
                message="Lesson ID cannot be empty",
                details={"field": "lesson_id"}
            )
            
        if new_order < 1:
            logger.warning(f"Attempted to set invalid lesson order: {new_order}")
            raise ValidationError(
                message="Lesson order must be greater than 0",
                details={"field": "new_order", "value": new_order}
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
                
            # Get the lesson to ensure it exists
            with self.transaction() as session:
                db_lesson = self.lesson_repo.get_lesson(session, lesson_uuid)
                
            if not db_lesson:
                logger.warning(f"Lesson not found with ID: {lesson_id}")
                raise ResourceNotFoundError(
                    message="Lesson not found",
                    details={"lesson_id": lesson_id}
                )
                
            # Update lesson order in repository
            with self.transaction() as session:
                success = self.lesson_repo.update_lesson_order(
                    session,
                    lesson_id=lesson_uuid,
                    new_order=new_order
                )
                
            logger.info(f"Successfully updated order for lesson: {lesson_id}")
            return success
            
        except (ValidationError, ResourceNotFoundError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error updating lesson order: {str(e)}")
            report_error(e, context={"lesson_id": lesson_id, "new_order": new_order})
            raise DatabaseError(
                message="Failed to update lesson order",
                details={"lesson_id": lesson_id, "error": str(e)}
            ) from e
            
    @handle_service_errors(service_name="lesson")
    def reorder_lessons(self, course_id: str, new_order: Dict[str, int]) -> bool:
        """
        Reorder multiple lessons within a course
        
        Args:
            course_id: ID of the course containing the lessons
            new_order: Dictionary mapping lesson IDs to their new order
            
        Returns:
            True if all lessons were reordered successfully, False otherwise
            
        Raises:
            ValidationError: If the course_id or new_order is invalid
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Reordering lessons for course {course_id}")
        
        if not course_id:
            logger.warning("Attempted to reorder lessons with empty course ID")
            raise ValidationError(
                message="Course ID cannot be empty",
                details={"field": "course_id"}
            )
            
        if not new_order:
            logger.warning("Attempted to reorder lessons with empty order mapping")
            raise ValidationError(
                message="New order mapping cannot be empty",
                details={"field": "new_order"}
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
                
            # Get all lessons for the course
            with self.transaction() as session:
                db_lessons = self.lesson_repo.get_lessons_by_course_id(session, course_uuid)
                
            # Create a mapping of current orders
            current_orders = {str(lesson.id): lesson.lesson_order for lesson in db_lessons}
            
            # Identify lessons that need updating
            changes_needed = {
                lesson_id: new_order[lesson_id]
                for lesson_id in new_order
                if lesson_id in current_orders and current_orders[lesson_id] != new_order[lesson_id]
            }
            
            if not changes_needed:
                logger.info("No order changes needed for lessons")
                return True
                
            # Update lesson orders
            success = True
            for lesson_id, order in changes_needed.items():
                try:
                    result = self.update_lesson_order(lesson_id, order)
                    if not result:
                        success = False
                except Exception as e:
                    logger.error(f"Error updating order for lesson {lesson_id}: {str(e)}")
                    report_error(e, context={"lesson_id": lesson_id, "new_order": order})
                    success = False
                    
            logger.info(f"Completed reordering lessons for course: {course_id}")
            return success
            
        except ValidationError:
            # Allow ValidationError to propagate
            raise
        except Exception as e:
            logger.error(f"Error reordering lessons: {str(e)}")
            report_error(e, context={"course_id": course_id})
            raise DatabaseError(
                message="Failed to reorder lessons",
                details={"course_id": course_id, "error": str(e)}
            ) from e
            
    @handle_service_errors(service_name="lesson")
    def get_prerequisite_lessons(self, lesson_id: str) -> List[Lesson]:
        """
        Get all prerequisite lessons for a given lesson
        
        Args:
            lesson_id: The ID of the lesson to get prerequisites for
            
        Returns:
            List of prerequisite lessons
            
        Raises:
            ValidationError: If the lesson_id is invalid
            ResourceNotFoundError: If the lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Getting prerequisite lessons for lesson: {lesson_id}")
        
        if not lesson_id:
            logger.warning("Attempted to get prerequisites with empty lesson ID")
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
            
            # Get the lesson first to verify it exists
            with self.transaction() as session:
                lesson = self.lesson_repo.get_lesson(session, lesson_uuid)
                
                if not lesson:
                    logger.warning(f"Lesson not found with ID: {lesson_id}")
                    raise ResourceNotFoundError(
                        message="Lesson not found",
                        details={"lesson_id": lesson_id}
                    )
                
                # Get prerequisite lessons
                prerequisite_lessons = self.lesson_repo.get_prerequisite_lessons(session, lesson_uuid)
                
                # Convert to UI models
                result = [self._convert_db_lesson_to_ui_lesson(prereq) for prereq in prerequisite_lessons]
                
                logger.info(f"Found {len(result)} prerequisite lessons for lesson {lesson_id}")
                return result
                
        except (ValidationError, ResourceNotFoundError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error getting prerequisite lessons: {str(e)}")
            report_error(e, context={"lesson_id": lesson_id})
            raise DatabaseError(
                message="Failed to retrieve prerequisite lessons",
                details={"lesson_id": lesson_id, "error": str(e)}
            ) from e
    
    @handle_service_errors(service_name="lesson")
    def get_dependent_lessons(self, lesson_id: str) -> List[Lesson]:
        """
        Get all lessons that have this lesson as a prerequisite
        
        Args:
            lesson_id: The ID of the lesson to get dependents for
            
        Returns:
            List of lessons that depend on this lesson
            
        Raises:
            ValidationError: If the lesson_id is invalid
            ResourceNotFoundError: If the lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Getting dependent lessons for lesson: {lesson_id}")
        
        if not lesson_id:
            logger.warning("Attempted to get dependents with empty lesson ID")
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
            
            # Get the lesson first to verify it exists
            with self.transaction() as session:
                lesson = self.lesson_repo.get_lesson(session, lesson_uuid)
                
                if not lesson:
                    logger.warning(f"Lesson not found with ID: {lesson_id}")
                    raise ResourceNotFoundError(
                        message="Lesson not found",
                        details={"lesson_id": lesson_id}
                    )
                
                # Get dependent lessons
                dependent_lessons = self.lesson_repo.get_dependent_lessons(session, lesson_uuid)
                
                # Convert to UI models
                result = [self._convert_db_lesson_to_ui_lesson(dependent) for dependent in dependent_lessons]
                
                logger.info(f"Found {len(result)} dependent lessons for lesson {lesson_id}")
                return result
                
        except (ValidationError, ResourceNotFoundError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error getting dependent lessons: {str(e)}")
            report_error(e, context={"lesson_id": lesson_id})
            raise DatabaseError(
                message="Failed to retrieve dependent lessons",
                details={"lesson_id": lesson_id, "error": str(e)}
            ) from e
    
    @handle_service_errors(service_name="lesson")
    def add_prerequisite(self, lesson_id: str, prerequisite_id: str) -> bool:
        """
        Add a prerequisite to a lesson
        
        Args:
            lesson_id: The ID of the lesson to add a prerequisite to
            prerequisite_id: The ID of the lesson to add as a prerequisite
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            ValidationError: If any of the IDs are invalid or the same
            ResourceNotFoundError: If either lesson does not exist
            BusinessLogicError: If adding would create a circular dependency
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Adding lesson {prerequisite_id} as prerequisite for lesson {lesson_id}")
        
        if not lesson_id or not prerequisite_id:
            logger.warning("Attempted to add prerequisite with empty IDs")
            raise ValidationError(
                message="Lesson IDs cannot be empty",
                details={"field": "lesson_id or prerequisite_id"}
            )
            
        if lesson_id == prerequisite_id:
            logger.warning("Attempted to add lesson as its own prerequisite")
            raise ValidationError(
                message="A lesson cannot be its own prerequisite",
                details={"field": "prerequisite_id"}
            )
            
        try:
            # Convert string IDs to UUIDs
            try:
                lesson_uuid = uuid.UUID(lesson_id)
                prerequisite_uuid = uuid.UUID(prerequisite_id)
            except ValueError as e:
                logger.warning(f"Invalid lesson ID format: {str(e)}")
                raise ValidationError(
                    message="Invalid lesson ID format",
                    details={"error": str(e)}
                ) from e
            
            # Get both lessons to verify they exist
            with self.transaction() as session:
                lesson = self.lesson_repo.get_lesson(session, lesson_uuid)
                prerequisite = self.lesson_repo.get_lesson(session, prerequisite_uuid)
                
                if not lesson:
                    logger.warning(f"Lesson not found with ID: {lesson_id}")
                    raise ResourceNotFoundError(
                        message="Lesson not found",
                        details={"lesson_id": lesson_id}
                    )
                    
                if not prerequisite:
                    logger.warning(f"Prerequisite lesson not found with ID: {prerequisite_id}")
                    raise ResourceNotFoundError(
                        message="Prerequisite lesson not found",
                        details={"prerequisite_id": prerequisite_id}
                    )
                
                # Check if this would create a circular dependency
                dependent_lessons = self.lesson_repo.get_dependent_lessons(session, lesson_uuid)
                
                # If the prerequisite depends on the lesson (directly or indirectly), this would create a cycle
                for dependent in dependent_lessons:
                    if dependent.id == prerequisite_uuid:
                        logger.warning(f"Adding prerequisite {prerequisite_id} to {lesson_id} would create a circular dependency")
                        raise BusinessLogicError(
                            message="Adding this prerequisite would create a circular dependency",
                            details={
                                "lesson_id": lesson_id,
                                "prerequisite_id": prerequisite_id
                            }
                        )
                
                # Check if the prerequisite is already in the list
                prereq_list = lesson.prerequisites.get("lessons", [])
                if prerequisite_id in prereq_list:
                    logger.info(f"Prerequisite {prerequisite_id} is already added to lesson {lesson_id}")
                    return True
                
                # Add the prerequisite
                if not lesson.prerequisites:
                    lesson.prerequisites = {}
                    
                if "lessons" not in lesson.prerequisites:
                    lesson.prerequisites["lessons"] = []
                    
                lesson.prerequisites["lessons"].append(prerequisite_id)
                
                # Update the lesson
                updated_lesson = self.lesson_repo.update_lesson(
                    session,
                    lesson_uuid,
                    prerequisites=lesson.prerequisites
                )
                
                if not updated_lesson:
                    logger.error(f"Failed to update lesson with new prerequisite: {lesson_id}")
                    raise DatabaseError(
                        message="Failed to update lesson with new prerequisite",
                        details={"lesson_id": lesson_id}
                    )
                
                logger.info(f"Successfully added prerequisite {prerequisite_id} to lesson {lesson_id}")
                return True
                
        except (ValidationError, ResourceNotFoundError, BusinessLogicError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error adding prerequisite: {str(e)}")
            report_error(e, context={"lesson_id": lesson_id, "prerequisite_id": prerequisite_id})
            raise DatabaseError(
                message="Failed to add prerequisite",
                details={"lesson_id": lesson_id, "prerequisite_id": prerequisite_id, "error": str(e)}
            ) from e
    
    @handle_service_errors(service_name="lesson")
    def remove_prerequisite(self, lesson_id: str, prerequisite_id: str) -> bool:
        """
        Remove a prerequisite from a lesson
        
        Args:
            lesson_id: The ID of the lesson to remove a prerequisite from
            prerequisite_id: The ID of the lesson to remove as a prerequisite
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            ValidationError: If any of the IDs are invalid
            ResourceNotFoundError: If the lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Removing lesson {prerequisite_id} as prerequisite for lesson {lesson_id}")
        
        if not lesson_id or not prerequisite_id:
            logger.warning("Attempted to remove prerequisite with empty IDs")
            raise ValidationError(
                message="Lesson IDs cannot be empty",
                details={"field": "lesson_id or prerequisite_id"}
            )
            
        try:
            # Convert string IDs to UUIDs
            try:
                lesson_uuid = uuid.UUID(lesson_id)
                prerequisite_uuid = uuid.UUID(prerequisite_id)  # Not used directly but validate format
            except ValueError as e:
                logger.warning(f"Invalid lesson ID format: {str(e)}")
                raise ValidationError(
                    message="Invalid lesson ID format",
                    details={"error": str(e)}
                ) from e
            
            # Get the lesson to verify it exists
            with self.transaction() as session:
                lesson = self.lesson_repo.get_lesson(session, lesson_uuid)
                
                if not lesson:
                    logger.warning(f"Lesson not found with ID: {lesson_id}")
                    raise ResourceNotFoundError(
                        message="Lesson not found",
                        details={"lesson_id": lesson_id}
                    )
                
                # Check if the prerequisite is in the list
                prereqs = lesson.prerequisites.get("lessons", [])
                if prerequisite_id not in prereqs:
                    logger.info(f"Prerequisite {prerequisite_id} is not in lesson {lesson_id}")
                    return True  # Already not there
                
                # Remove the prerequisite
                prereqs.remove(prerequisite_id)
                lesson.prerequisites["lessons"] = prereqs
                
                # Update the lesson
                updated_lesson = self.lesson_repo.update_lesson(
                    session,
                    lesson_uuid,
                    prerequisites=lesson.prerequisites
                )
                
                if not updated_lesson:
                    logger.error(f"Failed to update lesson after removing prerequisite: {lesson_id}")
                    raise DatabaseError(
                        message="Failed to update lesson after removing prerequisite",
                        details={"lesson_id": lesson_id}
                    )
                
                logger.info(f"Successfully removed prerequisite {prerequisite_id} from lesson {lesson_id}")
                return True
                
        except (ValidationError, ResourceNotFoundError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error removing prerequisite: {str(e)}")
            report_error(e, context={"lesson_id": lesson_id, "prerequisite_id": prerequisite_id})
            raise DatabaseError(
                message="Failed to remove prerequisite",
                details={"lesson_id": lesson_id, "prerequisite_id": prerequisite_id, "error": str(e)}
            ) from e
    
    @handle_service_errors(service_name="lesson")
    def check_prerequisites_satisfied(self, user_id: str, lesson_id: str) -> Tuple[bool, List[Lesson]]:
        """
        Check if a user has completed all prerequisites for a lesson
        
        Args:
            user_id: The ID of the user
            lesson_id: The ID of the lesson to check prerequisites for
            
        Returns:
            Tuple of (all_prerequisites_satisfied, list of unsatisfied prerequisite lessons)
            
        Raises:
            ValidationError: If the lesson_id is invalid
            ResourceNotFoundError: If the lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Checking prerequisites for user {user_id} on lesson {lesson_id}")
        
        if not user_id or not lesson_id:
            logger.warning("Attempted to check prerequisites with empty IDs")
            raise ValidationError(
                message="User ID and lesson ID cannot be empty",
                details={"field": "user_id or lesson_id"}
            )
            
        try:
            # Convert string IDs to UUIDs
            try:
                user_uuid = uuid.UUID(user_id)
                lesson_uuid = uuid.UUID(lesson_id)
            except ValueError as e:
                logger.warning(f"Invalid ID format: {str(e)}")
                raise ValidationError(
                    message="Invalid ID format",
                    details={"error": str(e)}
                ) from e
            
            # Get the lesson to verify it exists
            with self.transaction() as session:
                lesson = self.lesson_repo.get_lesson(session, lesson_uuid)
                
                if not lesson:
                    logger.warning(f"Lesson not found with ID: {lesson_id}")
                    raise ResourceNotFoundError(
                        message="Lesson not found",
                        details={"lesson_id": lesson_id}
                    )
                
                # If no prerequisites, all are satisfied
                prereq_ids = lesson.prerequisites.get("lessons", [])
                if not prereq_ids:
                    logger.info(f"No prerequisites for lesson {lesson_id}")
                    return True, []
                
                # Get all prerequisite lessons
                prereq_lessons = self.lesson_repo.get_prerequisite_lessons(session, lesson_uuid)
                
                # Check each prerequisite
                unsatisfied_prerequisites = []
                for prereq in prereq_lessons:
                    is_completed = self.progress_service.has_completed_lesson(user_id, str(prereq.id))
                    if not is_completed:
                        unsatisfied_prerequisites.append(self._convert_db_lesson_to_ui_lesson(prereq))
                
                all_satisfied = len(unsatisfied_prerequisites) == 0
                
                logger.info(f"Prerequisites check for user {user_id} on lesson {lesson_id}: {all_satisfied}")
                return all_satisfied, unsatisfied_prerequisites
                
        except (ValidationError, ResourceNotFoundError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error checking prerequisites: {str(e)}")
            report_error(e, context={"user_id": user_id, "lesson_id": lesson_id})
            raise DatabaseError(
                message="Failed to check prerequisites",
                details={"user_id": user_id, "lesson_id": lesson_id, "error": str(e)}
            ) from e
    
    @handle_service_errors(service_name="lesson")
    def validate_lesson_dependencies(self, course_id: str) -> Tuple[bool, List[str]]:
        """
        Validate that there are no circular dependencies in the lesson prerequisites for a course
        
        Args:
            course_id: The ID of the course to validate
            
        Returns:
            Tuple of (is_valid, list of error messages)
            
        Raises:
            ValidationError: If the course_id is invalid
            ResourceNotFoundError: If the course does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Validating lesson dependencies for course: {course_id}")
        
        if not course_id:
            logger.warning("Attempted to validate lessons with empty course ID")
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
            
            with self.transaction() as session:
                # Get all lessons for the course
                lessons = self.lesson_repo.get_lessons_by_course_id(session, course_uuid)
                
                if not lessons:
                    logger.info(f"No lessons found for course {course_id}")
                    return True, []
                
                # Build a dependency graph
                dependency_graph = {}
                lesson_map = {}
                
                for lesson in lessons:
                    lesson_id = str(lesson.id)
                    lesson_map[lesson_id] = lesson
                    dependency_graph[lesson_id] = lesson.prerequisites.get("lessons", [])
                
                # Check for cycles in the graph
                visited = set()
                temp_visited = set()
                errors = []
                
                def is_cyclic(node):
                    """Check if the graph has a cycle starting from node."""
                    if node in temp_visited:
                        return True
                    
                    if node in visited:
                        return False
                    
                    temp_visited.add(node)
                    
                    for prereq in dependency_graph.get(node, []):
                        if prereq in lesson_map and is_cyclic(prereq):
                            return True
                    
                    temp_visited.remove(node)
                    visited.add(node)
                    return False
                
                # Check each lesson for cycles
                for lesson_id in dependency_graph:
                    if lesson_id not in visited:
                        if is_cyclic(lesson_id):
                            errors.append(f"Circular dependency detected in lesson: {lesson_map[lesson_id].title}")
                
                # Check for invalid lesson references
                for lesson_id, prereqs in dependency_graph.items():
                    for prereq_id in prereqs:
                        if prereq_id not in lesson_map:
                            errors.append(f"Lesson {lesson_map[lesson_id].title} references non-existent prerequisite: {prereq_id}")
                
                # Check lesson ordering vs prerequisites
                for lesson in lessons:
                    lesson_id = str(lesson.id)
                    prereq_ids = dependency_graph.get(lesson_id, [])
                    
                    for prereq_id in prereq_ids:
                        if prereq_id in lesson_map:
                            prereq = lesson_map[prereq_id]
                            if prereq.lesson_order >= lesson.lesson_order:
                                errors.append(
                                    f"Lesson '{lesson.title}' (order {lesson.lesson_order}) has prerequisite "
                                    f"'{prereq.title}' with equal or higher order ({prereq.lesson_order})"
                                )
                
                is_valid = len(errors) == 0
                
                logger.info(f"Dependency validation for course {course_id}: {is_valid}")
                return is_valid, errors
                
        except (ValidationError, ResourceNotFoundError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error validating lesson dependencies: {str(e)}")
            report_error(e, context={"course_id": course_id})
            raise DatabaseError(
                message="Failed to validate lesson dependencies",
                details={"course_id": course_id, "error": str(e)}
            ) from e
    
    @handle_service_errors(service_name="lesson")
    def reorder_lessons(self, course_id: str, new_order: Dict[str, int]) -> bool:
        """
        Update the order of multiple lessons in a course at once
        
        Args:
            course_id: The ID of the course
            new_order: Dictionary mapping lesson IDs to their new order values
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            ValidationError: If the course_id is invalid or new_order is empty
            ResourceNotFoundError: If the course or any lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Reordering lessons for course {course_id}")
        
        if not course_id:
            logger.warning("Attempted to reorder lessons with empty course ID")
            raise ValidationError(
                message="Course ID cannot be empty",
                details={"field": "course_id"}
            )
            
        if not new_order:
            logger.warning("Attempted to reorder lessons with empty order mapping")
            raise ValidationError(
                message="New order mapping cannot be empty",
                details={"field": "new_order"}
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
            
            with self.transaction() as session:
                # Get all lessons for the course
                lessons = self.lesson_repo.get_lessons_by_course_id(session, course_uuid)
                
                if not lessons:
                    logger.warning(f"No lessons found for course {course_id}")
                    raise ResourceNotFoundError(
                        message="No lessons found for course",
                        details={"course_id": course_id}
                    )
                
                # Validate that all provided lesson IDs exist in the course
                lesson_ids = {str(lesson.id) for lesson in lessons}
                for lesson_id in new_order:
                    if lesson_id not in lesson_ids:
                        logger.warning(f"Lesson {lesson_id} not found in course {course_id}")
                        raise ResourceNotFoundError(
                            message="Lesson not found in course",
                            details={"lesson_id": lesson_id, "course_id": course_id}
                        )
                
                # Update the order of each lesson
                for lesson_id, order in new_order.items():
                    lesson_uuid = uuid.UUID(lesson_id)
                    success = self.lesson_repo.update_lesson_order(session, lesson_uuid, order)
                    
                    if not success:
                        logger.error(f"Failed to update order for lesson {lesson_id}")
                        raise DatabaseError(
                            message="Failed to update lesson order",
                            details={"lesson_id": lesson_id}
                        )
                
                # Validate dependencies after reordering
                is_valid, errors = self.validate_lesson_dependencies(course_id)
                
                if not is_valid:
                    logger.warning(f"Reordering created invalid dependencies: {errors}")
                    # Note: We're not rolling back or raising an error here,
                    # just logging a warning. This allows the client to make 
                    # decisions about whether to fix the ordering.
                
                logger.info(f"Successfully reordered lessons for course {course_id}")
                return True
                
        except (ValidationError, ResourceNotFoundError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error reordering lessons: {str(e)}")
            report_error(e, context={"course_id": course_id})
            raise DatabaseError(
                message="Failed to reorder lessons",
                details={"course_id": course_id, "error": str(e)}
            ) from e

    @handle_service_errors(service_name="lesson")
    def set_completion_criteria(self, lesson_id: str, completion_criteria: Dict[str, Any]) -> bool:
        """
        Set the completion criteria for a lesson
        
        Args:
            lesson_id: The ID of the lesson
            completion_criteria: Dictionary containing completion criteria
                Example: {
                    "required_content_ids": ["content-id-1", "content-id-2"],
                    "required_score": 80,
                    "required_time_spent": 30,  # minutes
                    "assessment_required": True,
                    "custom_rules": {
                        "rule_type": "value",
                        "data": {}
                    }
                }
            
        Returns:
            True if the criteria were successfully set, False otherwise
            
        Raises:
            ValidationError: If the completion criteria are invalid
            ResourceNotFoundError: If the lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Setting completion criteria for lesson: {lesson_id}")
        
        if not lesson_id:
            logger.warning("Attempted to set completion criteria with empty lesson ID")
            raise ValidationError(
                message="Lesson ID cannot be empty",
                details={"field": "lesson_id"}
            )
        
        if not completion_criteria:
            logger.warning("Attempted to set empty completion criteria")
            raise ValidationError(
                message="Completion criteria cannot be empty",
                details={"field": "completion_criteria"}
            )
        
        try:
            # Validate the completion criteria format
            self._validate_completion_criteria(completion_criteria)
            
            # Convert string ID to UUID
            try:
                lesson_uuid = uuid.UUID(lesson_id)
            except ValueError as e:
                logger.warning(f"Invalid lesson ID format: {lesson_id}")
                raise ValidationError(
                    message="Invalid lesson ID format",
                    details={"field": "lesson_id", "error": str(e)}
                ) from e
            
            # Get the lesson
            with self.transaction() as session:
                lesson = self.lesson_repo.get_lesson(session, lesson_uuid)
                
                if not lesson:
                    logger.warning(f"Lesson not found with ID: {lesson_id}")
                    raise ResourceNotFoundError(
                        message="Lesson not found",
                        details={"lesson_id": lesson_id}
                    )
                
                # Update the lesson metadata with completion criteria
                if not lesson.metadata:
                    lesson.metadata = {}
                
                lesson.metadata["completion_criteria"] = completion_criteria
                
                # Save the updated lesson
                updated_lesson = self.lesson_repo.update_lesson_metadata(
                    session, 
                    lesson_uuid, 
                    lesson.metadata
                )
                
                if not updated_lesson:
                    logger.error(f"Failed to update lesson metadata for lesson: {lesson_id}")
                    raise DatabaseError(
                        message="Failed to update completion criteria",
                        details={"lesson_id": lesson_id}
                    )
            
            logger.info(f"Successfully set completion criteria for lesson: {lesson_id}")
            return True
            
        except (ValidationError, ResourceNotFoundError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error setting completion criteria: {str(e)}")
            report_error(e, context={"lesson_id": lesson_id})
            raise DatabaseError(
                message="Failed to set completion criteria",
                details={"lesson_id": lesson_id, "error": str(e)}
            ) from e
    
    @handle_service_errors(service_name="lesson")
    def get_completion_criteria(self, lesson_id: str) -> Dict[str, Any]:
        """
        Get the completion criteria for a lesson
        
        Args:
            lesson_id: The ID of the lesson
            
        Returns:
            Dictionary containing completion criteria, empty dict if not set
            
        Raises:
            ValidationError: If the lesson_id is invalid
            ResourceNotFoundError: If the lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Getting completion criteria for lesson: {lesson_id}")
        
        if not lesson_id:
            logger.warning("Attempted to get completion criteria with empty lesson ID")
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
            
            # Get the lesson
            with self.transaction() as session:
                lesson = self.lesson_repo.get_lesson(session, lesson_uuid)
                
                if not lesson:
                    logger.warning(f"Lesson not found with ID: {lesson_id}")
                    raise ResourceNotFoundError(
                        message="Lesson not found",
                        details={"lesson_id": lesson_id}
                    )
                
                # Get the completion criteria from metadata
                if not lesson.metadata or "completion_criteria" not in lesson.metadata:
                    return {}
                
                return lesson.metadata.get("completion_criteria", {})
            
        except (ValidationError, ResourceNotFoundError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error getting completion criteria: {str(e)}")
            report_error(e, context={"lesson_id": lesson_id})
            raise DatabaseError(
                message="Failed to get completion criteria",
                details={"lesson_id": lesson_id, "error": str(e)}
            ) from e
    
    @handle_service_errors(service_name="lesson")
    def check_completion_criteria_met(self, user_id: str, lesson_id: str) -> Tuple[bool, List[str]]:
        """
        Check if a user has met all completion criteria for a lesson.
        
        Args:
            user_id: ID of the user
            lesson_id: ID of the lesson
            
        Returns:
            A tuple (criteria_met, unmet_criteria) where:
            - criteria_met is a boolean indicating if all criteria are met
            - unmet_criteria is a list of strings describing criteria that are not met
            
        Raises:
            ValidationError: If either user_id or lesson_id is invalid
            ResourceNotFoundError: If the lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Checking completion criteria for user {user_id} and lesson {lesson_id}")
        
        completion_criteria = self.get_completion_criteria(lesson_id)
        unmet_criteria = []
        
        # If no criteria are set, the lesson is considered complete
        if not completion_criteria:
            logger.info(f"No completion criteria set for lesson {lesson_id}, considering it complete")
            return True, []
        
        # Check content completion
        if "required_content_ids" in completion_criteria:
            content_ids = completion_criteria["required_content_ids"]
            for content_id in content_ids:
                if not self.progress_service.has_completed_content(user_id, content_id):
                    unmet_criteria.append(f"Content item {content_id} not completed")
        
        # Check assessment score
        if "required_score" in completion_criteria:
            required_score = completion_criteria["required_score"]
            actual_score = self.progress_service.get_assessment_score(user_id, lesson_id)
            
            if actual_score is None or actual_score < required_score:
                actual_score_str = "None" if actual_score is None else str(actual_score)
                unmet_criteria.append(f"Assessment score ({actual_score_str}) below required ({required_score})")
        
        # Check time spent
        if "required_time_spent" in completion_criteria:
            required_time = completion_criteria["required_time_spent"]
            actual_time = self.progress_service.get_time_spent(user_id, lesson_id)
            
            if actual_time is None or actual_time < required_time:
                actual_time_str = "None" if actual_time is None else str(actual_time)
                unmet_criteria.append(f"Time spent ({actual_time_str} min) below required ({required_time} min)")
        
        # Note about prerequisites: We check prerequisites for information only, but don't enforce them
        # as requirements for completion. Prerequisites are for organizational purposes only.
        if completion_criteria.get("prerequisites_required", False):
            satisfied, missing = self.check_prerequisites_satisfied(user_id, lesson_id)
            
            if not satisfied:
                missing_ids = [lesson.id for lesson in missing]
                unmet_criteria.append(f"Recommended prerequisites not completed: {', '.join(missing_ids)}")
                logger.info(f"Prerequisites not satisfied for user {user_id} and lesson {lesson_id}, but this is only informational")
        
        # Check custom rules
        if "custom_rules" in completion_criteria:
            rules_met, custom_unmet = self._check_custom_completion_rules(
                user_id, lesson_id, completion_criteria["custom_rules"]
            )
            if not rules_met:
                unmet_criteria.extend(custom_unmet)
        
        criteria_met = len(unmet_criteria) == 0
        log_msg = f"Completion criteria {'met' if criteria_met else 'not met'} for user {user_id} and lesson {lesson_id}"
        logger.info(log_msg)
        
        if not criteria_met:
            logger.info(f"Unmet criteria: {', '.join(unmet_criteria)}")
        
        return criteria_met, unmet_criteria
    
    @handle_service_errors(service_name="lesson")
    def mark_lesson_complete(self, user_id: str, lesson_id: str, override_criteria: bool = False) -> bool:
        """
        Mark a lesson as complete for a user
        
        Args:
            user_id: The ID of the user
            lesson_id: The ID of the lesson
            override_criteria: Whether to override completion criteria checks
            
        Returns:
            True if the lesson was marked complete, False otherwise
            
        Raises:
            ValidationError: If any of the IDs are invalid
            ResourceNotFoundError: If the lesson does not exist
            BusinessLogicError: If completion criteria are not met and override is False
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Marking lesson {lesson_id} as complete for user {user_id}")
        
        if not user_id:
            logger.warning("Attempted to mark lesson complete with empty user ID")
            raise ValidationError(
                message="User ID cannot be empty",
                details={"field": "user_id"}
            )
        
        if not lesson_id:
            logger.warning("Attempted to mark lesson complete with empty lesson ID")
            raise ValidationError(
                message="Lesson ID cannot be empty",
                details={"field": "lesson_id"}
            )
        
        try:
            # If not overriding, check if completion criteria are met
            if not override_criteria:
                criteria_met, unmet_criteria = self.check_completion_criteria_met(user_id, lesson_id)
                
                if not criteria_met:
                    logger.warning(f"User {user_id} has not met completion criteria for lesson {lesson_id}")
                    raise BusinessLogicError(
                        message="Completion criteria not met",
                        details={"unmet_criteria": unmet_criteria}
                    )
            
            # Get the lesson to make sure it exists
            lesson = self.get_lesson_by_id(lesson_id)
            
            # Mark the lesson as complete using progress service
            result = self.progress_service.complete_lesson(
                user_id=user_id,
                lesson_id=lesson_id,
                course_id=lesson.course_id
            )
            
            if not result:
                logger.error(f"Failed to mark lesson {lesson_id} as complete for user {user_id}")
                return False
            
            logger.info(f"Successfully marked lesson {lesson_id} as complete for user {user_id}")
            return True
            
        except (ValidationError, ResourceNotFoundError, BusinessLogicError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error marking lesson as complete: {str(e)}")
            report_error(e, context={"user_id": user_id, "lesson_id": lesson_id})
            raise DatabaseError(
                message="Failed to mark lesson as complete",
                details={"user_id": user_id, "lesson_id": lesson_id, "error": str(e)}
            ) from e

    def _validate_completion_criteria(self, criteria: Dict[str, Any]) -> None:
        """
        Validate lesson completion criteria format
        
        Args:
            criteria: Dictionary containing completion criteria
            
        Raises:
            ValidationError: If the criteria are invalid
        """
        if not isinstance(criteria, dict):
            raise ValidationError(
                message="Completion criteria must be a dictionary",
                details={"field": "completion_criteria"}
            )
        
        # Check required content IDs if present
        if "required_content_ids" in criteria:
            if not isinstance(criteria["required_content_ids"], list):
                raise ValidationError(
                    message="Required content IDs must be a list",
                    details={"field": "required_content_ids"}
                )
            
            # Validate each content ID format
            for content_id in criteria["required_content_ids"]:
                try:
                    uuid.UUID(content_id)
                except ValueError:
                    raise ValidationError(
                        message=f"Invalid content ID format: {content_id}",
                        details={"field": "required_content_ids"}
                    )
        
        # Check required score if present
        if "required_score" in criteria:
            if not isinstance(criteria["required_score"], (int, float)):
                raise ValidationError(
                    message="Required score must be a number",
                    details={"field": "required_score"}
                )
            
            if criteria["required_score"] < 0 or criteria["required_score"] > 100:
                raise ValidationError(
                    message="Required score must be between 0 and 100",
                    details={"field": "required_score"}
                )
        
        # Check required time if present
        if "required_time_spent" in criteria:
            if not isinstance(criteria["required_time_spent"], (int, float)):
                raise ValidationError(
                    message="Required time spent must be a number",
                    details={"field": "required_time_spent"}
                )
            
            if criteria["required_time_spent"] <= 0:
                raise ValidationError(
                    message="Required time spent must be positive",
                    details={"field": "required_time_spent"}
                )
        
        # Check custom rules if present
        if "custom_rules" in criteria:
            if not isinstance(criteria["custom_rules"], dict):
                raise ValidationError(
                    message="Custom rules must be a dictionary",
                    details={"field": "custom_rules"}
                )
            
            if "rule_type" not in criteria["custom_rules"]:
                raise ValidationError(
                    message="Custom rules must have a rule_type",
                    details={"field": "custom_rules.rule_type"}
                )
    
    def _check_custom_completion_rules(self, user_id: str, lesson_id: str, rules: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Check custom completion rules
        
        Args:
            user_id: The ID of the user
            lesson_id: The ID of the lesson
            rules: Dictionary containing custom rules
            
        Returns:
            Tuple of (rules_met, list of unmet rule messages)
        """
        rule_type = rules.get("rule_type")
        unmet_rules = []
        
        # All rules met by default
        if not rule_type:
            return True, []
        
        # Handle different rule types
        if rule_type == "activity_count":
            # Example: User needs to perform an activity X times
            activity = rules.get("activity", "")
            required_count = rules.get("count", 0)
            
            actual_count = self.progress_service.get_activity_count(user_id, lesson_id)
            
            if actual_count < required_count:
                unmet_rules.append(f"Activity count {actual_count} below required {required_count}")
        
        elif rule_type == "content_interaction":
            # Example: User needs to interact with specific content elements
            interactions = rules.get("interactions", [])
            
            for interaction in interactions:
                content_id = interaction.get("content_id", "")
                
                has_interaction = self.progress_service.has_content_interaction(
                    user_id, content_id
                )
                
                if not has_interaction:
                    unmet_rules.append(f"Missing interaction for content {content_id}")
        
        # Add more rule types as needed
        
        # Rules are met if no unmet rules
        rules_met = len(unmet_rules) == 0
        return rules_met, unmet_rules