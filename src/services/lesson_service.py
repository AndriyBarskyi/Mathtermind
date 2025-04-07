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
    def create_lesson(self, course_id: str, title: str, lesson_type: str,
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
            lesson_type: Type of lesson (e.g., THEORY, PRACTICE, ASSESSMENT)
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
                    lesson_type=lesson_type,
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
                "title": title,
                "lesson_type": lesson_type
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
            
            lesson_type = db_lesson.lesson_type
            if hasattr(lesson_type, 'value'):
                lesson_type = lesson_type.value
                
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
                lesson_type=lesson_type,
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
                lesson_type="THEORY",
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
        Get all prerequisite lessons for a lesson
        
        Args:
            lesson_id: ID of the lesson to get prerequisites for
            
        Returns:
            List of prerequisite lessons
            
        Raises:
            ValidationError: If the lesson_id is invalid
            ResourceNotFoundError: If the lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Getting prerequisite lessons for lesson {lesson_id}")
        
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
                
            # Get the lesson to ensure it exists
            with self.transaction() as session:
                db_lesson = self.lesson_repo.get_lesson(session, lesson_uuid)
                
            if not db_lesson:
                logger.warning(f"Lesson not found with ID: {lesson_id}")
                raise ResourceNotFoundError(
                    message="Lesson not found",
                    details={"lesson_id": lesson_id}
                )
                
            # Get prerequisite lessons from repository
            with self.transaction() as session:
                db_prereqs = self.lesson_repo.get_prerequisite_lessons(session, lesson_uuid)
                
            # Convert to UI models
            ui_prereqs = [
                self._convert_db_lesson_to_ui_lesson(lesson)
                for lesson in db_prereqs
            ]
            
            logger.info(f"Found {len(ui_prereqs)} prerequisite lessons for lesson: {lesson_id}")
            return ui_prereqs
            
        except (ValidationError, ResourceNotFoundError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error getting prerequisite lessons: {str(e)}")
            report_error(e, context={"lesson_id": lesson_id})
            raise DatabaseError(
                message="Failed to get prerequisite lessons",
                details={"lesson_id": lesson_id, "error": str(e)}
            ) from e
            
    @handle_service_errors(service_name="lesson")
    def get_dependent_lessons(self, lesson_id: str) -> List[Lesson]:
        """
        Get all lessons that depend on a specific lesson
        
        Args:
            lesson_id: ID of the prerequisite lesson
            
        Returns:
            List of lessons that have this lesson as a prerequisite
            
        Raises:
            ValidationError: If the lesson_id is invalid
            ResourceNotFoundError: If the lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Getting dependent lessons for lesson {lesson_id}")
        
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
                
            # Get the lesson to ensure it exists
            with self.transaction() as session:
                db_lesson = self.lesson_repo.get_lesson(session, lesson_uuid)
                
            if not db_lesson:
                logger.warning(f"Lesson not found with ID: {lesson_id}")
                raise ResourceNotFoundError(
                    message="Lesson not found",
                    details={"lesson_id": lesson_id}
                )
                
            # Get dependent lessons from repository
            with self.transaction() as session:
                db_dependents = self.lesson_repo.get_dependent_lessons(session, lesson_uuid)
                
            # Convert to UI models
            ui_dependents = [
                self._convert_db_lesson_to_ui_lesson(lesson)
                for lesson in db_dependents
            ]
            
            logger.info(f"Found {len(ui_dependents)} dependent lessons for lesson: {lesson_id}")
            return ui_dependents
            
        except (ValidationError, ResourceNotFoundError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error getting dependent lessons: {str(e)}")
            report_error(e, context={"lesson_id": lesson_id})
            raise DatabaseError(
                message="Failed to get dependent lessons",
                details={"lesson_id": lesson_id, "error": str(e)}
            ) from e
            
    @handle_service_errors(service_name="lesson")
    def add_prerequisite(self, lesson_id: str, prerequisite_id: str) -> bool:
        """
        Add a prerequisite to a lesson
        
        Args:
            lesson_id: ID of the lesson to add the prerequisite to
            prerequisite_id: ID of the lesson to add as a prerequisite
            
        Returns:
            True if the prerequisite was added successfully, False otherwise
            
        Raises:
            ValidationError: If any of the IDs are invalid
            ResourceNotFoundError: If either lesson does not exist
            BusinessLogicError: If adding the prerequisite would create a circular dependency
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Adding prerequisite {prerequisite_id} to lesson {lesson_id}")
        
        if not lesson_id or not prerequisite_id:
            logger.warning("Attempted to add prerequisite with empty IDs")
            raise ValidationError(
                message="Lesson ID and prerequisite ID cannot be empty",
                details={"field": "lesson_id or prerequisite_id"}
            )
            
        if lesson_id == prerequisite_id:
            logger.warning("Attempted to add lesson as its own prerequisite")
            raise ValidationError(
                message="A lesson cannot be its own prerequisite",
                details={"lesson_id": lesson_id}
            )
            
        try:
            # Convert string IDs to UUIDs
            try:
                lesson_uuid = uuid.UUID(lesson_id)
                prereq_uuid = uuid.UUID(prerequisite_id)
            except ValueError as e:
                logger.warning(f"Invalid ID format: {str(e)}")
                raise ValidationError(
                    message="Invalid ID format",
                    details={"error": str(e)}
                ) from e
                
            # Get both lessons to ensure they exist
            with self.transaction() as session:
                db_lesson = self.lesson_repo.get_lesson(session, lesson_uuid)
                db_prereq = self.lesson_repo.get_lesson(session, prereq_uuid)
                
            if not db_lesson:
                logger.warning(f"Lesson not found with ID: {lesson_id}")
                raise ResourceNotFoundError(
                    message="Lesson not found",
                    details={"lesson_id": lesson_id}
                )
                
            if not db_prereq:
                logger.warning(f"Prerequisite lesson not found with ID: {prerequisite_id}")
                raise ResourceNotFoundError(
                    message="Prerequisite lesson not found",
                    details={"prerequisite_id": prerequisite_id}
                )
                
            # Check for circular dependencies
            with self.transaction() as session:
                dependent_lessons = self.lesson_repo.get_dependent_lessons(session, lesson_uuid)
            
            dependent_ids = [str(lesson.id) for lesson in dependent_lessons]
            if prerequisite_id in dependent_ids:
                logger.warning(f"Circular dependency detected: {prerequisite_id} already depends on {lesson_id}")
                raise BusinessLogicError(
                    message="Adding this prerequisite would create a circular dependency",
                    details={
                        "lesson_id": lesson_id,
                        "prerequisite_id": prerequisite_id
                    }
                )
                
            # Get current prerequisites
            prereqs = db_lesson.prerequisites or {}
            lesson_prereqs = prereqs.get("lessons", [])
            
            # Check if prerequisite already exists
            if prerequisite_id in lesson_prereqs:
                logger.info(f"Prerequisite {prerequisite_id} already exists for lesson {lesson_id}")
                return True
                
            # Add prerequisite
            if not isinstance(lesson_prereqs, list):
                lesson_prereqs = []
            
            lesson_prereqs.append(prerequisite_id)
            prereqs["lessons"] = lesson_prereqs
            
            # Update lesson in repository
            with self.transaction() as session:
                updated_lesson = self.lesson_repo.update_lesson(
                    session,
                    lesson_id=lesson_uuid,
                    prerequisites=prereqs
                )
                
            logger.info(f"Successfully added prerequisite {prerequisite_id} to lesson {lesson_id}")
            return updated_lesson is not None
            
        except (ValidationError, ResourceNotFoundError, BusinessLogicError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error adding prerequisite: {str(e)}")
            report_error(e, context={"lesson_id": lesson_id, "prerequisite_id": prerequisite_id})
            raise DatabaseError(
                message="Failed to add prerequisite",
                details={
                    "lesson_id": lesson_id,
                    "prerequisite_id": prerequisite_id,
                    "error": str(e)
                }
            ) from e
            
    @handle_service_errors(service_name="lesson")
    def remove_prerequisite(self, lesson_id: str, prerequisite_id: str) -> bool:
        """
        Remove a prerequisite from a lesson
        
        Args:
            lesson_id: ID of the lesson to remove the prerequisite from
            prerequisite_id: ID of the prerequisite to remove
            
        Returns:
            True if the prerequisite was removed successfully, False otherwise
            
        Raises:
            ValidationError: If any of the IDs are invalid
            ResourceNotFoundError: If the lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Removing prerequisite {prerequisite_id} from lesson {lesson_id}")
        
        if not lesson_id or not prerequisite_id:
            logger.warning("Attempted to remove prerequisite with empty IDs")
            raise ValidationError(
                message="Lesson ID and prerequisite ID cannot be empty",
                details={"field": "lesson_id or prerequisite_id"}
            )
            
        try:
            # Convert string IDs to UUIDs
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
                
            # Get current prerequisites
            prereqs = db_lesson.prerequisites or {}
            lesson_prereqs = prereqs.get("lessons", [])
            
            # Check if prerequisite exists
            if prerequisite_id not in lesson_prereqs:
                logger.info(f"Prerequisite {prerequisite_id} not found for lesson {lesson_id}")
                return True
                
            # Remove prerequisite
            lesson_prereqs.remove(prerequisite_id)
            prereqs["lessons"] = lesson_prereqs
            
            # Update lesson in repository
            with self.transaction() as session:
                updated_lesson = self.lesson_repo.update_lesson(
                    session,
                    lesson_id=lesson_uuid,
                    prerequisites=prereqs
                )
                
            logger.info(f"Successfully removed prerequisite {prerequisite_id} from lesson {lesson_id}")
            return updated_lesson is not None
            
        except (ValidationError, ResourceNotFoundError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error removing prerequisite: {str(e)}")
            report_error(e, context={"lesson_id": lesson_id, "prerequisite_id": prerequisite_id})
            raise DatabaseError(
                message="Failed to remove prerequisite",
                details={
                    "lesson_id": lesson_id,
                    "prerequisite_id": prerequisite_id,
                    "error": str(e)
                }
            ) from e
            
    @handle_service_errors(service_name="lesson")
    def check_prerequisites_satisfied(self, user_id: str, lesson_id: str) -> Tuple[bool, List[Lesson]]:
        """
        Check if a user has satisfied all prerequisites for a lesson
        
        Args:
            user_id: ID of the user
            lesson_id: ID of the lesson to check prerequisites for
            
        Returns:
            Tuple containing:
                - Boolean indicating if all prerequisites are satisfied
                - List of lessons that are not completed (empty if all are satisfied)
            
        Raises:
            ValidationError: If any of the IDs are invalid
            ResourceNotFoundError: If the lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Checking prerequisites for user {user_id}, lesson {lesson_id}")
        
        if not user_id or not lesson_id:
            logger.warning("Attempted to check prerequisites with empty IDs")
            raise ValidationError(
                message="User ID and lesson ID cannot be empty",
                details={"field": "user_id or lesson_id"}
            )
            
        try:
            # Convert string IDs to UUIDs
            try:
                lesson_uuid = uuid.UUID(lesson_id)
                user_uuid = uuid.UUID(user_id)
            except ValueError as e:
                logger.warning(f"Invalid ID format: {str(e)}")
                raise ValidationError(
                    message="Invalid ID format",
                    details={"error": str(e)}
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
                
            # Get prerequisite lessons
            prerequisite_lessons = self.get_prerequisite_lessons(lesson_id)
            
            if not prerequisite_lessons:
                logger.info(f"No prerequisites found for lesson {lesson_id}")
                return True, []
                
            # Import here to avoid circular imports
            from src.services.progress_service import ProgressService
            progress_service = ProgressService()
            
            # Check if user has completed each prerequisite
            missing_prerequisites = []
            for prereq_lesson in prerequisite_lessons:
                if not progress_service.has_completed_lesson(user_id, prereq_lesson.id):
                    missing_prerequisites.append(prereq_lesson)
                    
            logger.info(f"Found {len(missing_prerequisites)} missing prerequisites for user {user_id}, lesson {lesson_id}")
            return len(missing_prerequisites) == 0, missing_prerequisites
            
        except (ValidationError, ResourceNotFoundError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error checking prerequisites: {str(e)}")
            report_error(e, context={"user_id": user_id, "lesson_id": lesson_id})
            raise DatabaseError(
                message="Failed to check prerequisites",
                details={
                    "user_id": user_id,
                    "lesson_id": lesson_id,
                    "error": str(e)
                }
            ) from e
            
    @handle_service_errors(service_name="lesson")
    def validate_lesson_dependencies(self, course_id: str) -> Tuple[bool, List[str]]:
        """
        Validate that lesson dependencies make sense with lesson order
        
        Args:
            course_id: ID of the course to validate
            
        Returns:
            Tuple containing:
                - Boolean indicating if all dependencies are valid
                - List of error messages describing issues (empty if all are valid)
            
        Raises:
            ValidationError: If the course_id is invalid
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Validating lesson dependencies for course {course_id}")
        
        if not course_id:
            logger.warning("Attempted to validate dependencies with empty course ID")
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
                
            # Get all lessons for the course
            with self.transaction() as session:
                db_lessons = self.lesson_repo.get_lessons_by_course_id(session, course_uuid)
                
            if not db_lessons:
                logger.info(f"No lessons found for course {course_id}")
                return True, []
                
            # Create a mapping of lesson ID to lesson order
            lesson_orders = {str(lesson.id): lesson.lesson_order for lesson in db_lessons}
            
            # Check for dependencies that violate order
            issues = []
            for lesson in db_lessons:
                lesson_id = str(lesson.id)
                lesson_order = lesson.lesson_order
                
                prereqs = lesson.prerequisites or {}
                prereq_ids = prereqs.get("lessons", [])
                
                for prereq_id in prereq_ids:
                    if prereq_id not in lesson_orders:
                        # Prerequisite not in this course, skip
                        continue
                        
                    prereq_order = lesson_orders[prereq_id]
                    
                    # Find prerequisite lesson name
                    prereq_name = "Unknown"
                    for db_lesson in db_lessons:
                        if str(db_lesson.id) == prereq_id:
                            prereq_name = db_lesson.title
                            break
                    
                    if prereq_order >= lesson_order:
                        issue = (
                            f"Lesson '{lesson.title}' (order {lesson_order}) "
                            f"depends on '{prereq_name}' (order {prereq_order}), "
                            f"but the prerequisite should come before the dependent lesson."
                        )
                        issues.append(issue)
                        
            valid = len(issues) == 0
            logger.info(f"Validation completed for course {course_id}. Valid: {valid}, Issues: {len(issues)}")
            return valid, issues
            
        except ValidationError:
            # Allow ValidationError to propagate
            raise
        except Exception as e:
            logger.error(f"Error validating lesson dependencies: {str(e)}")
            report_error(e, context={"course_id": course_id})
            raise DatabaseError(
                message="Failed to validate lesson dependencies",
                details={"course_id": course_id, "error": str(e)}
            ) from e
            
    @handle_service_errors(service_name="lesson")
    def set_completion_criteria(self, lesson_id: str, completion_criteria: Dict[str, Any]) -> bool:
        """
        Set completion criteria for a lesson
        
        Args:
            lesson_id: ID of the lesson to set criteria for
            completion_criteria: Dictionary containing criteria (min_score, required_content_ids, time_requirement, etc.)
            
        Returns:
            True if the criteria were set successfully, False otherwise
            
        Raises:
            ValidationError: If the lesson_id or criteria are invalid
            ResourceNotFoundError: If the lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Setting completion criteria for lesson {lesson_id}")
        
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
                
            # Validate criteria
            if "min_score" in completion_criteria and (
                not isinstance(completion_criteria["min_score"], (int, float)) or 
                completion_criteria["min_score"] < 0 or 
                completion_criteria["min_score"] > 100
            ):
                logger.warning(f"Invalid min_score in completion criteria: {completion_criteria['min_score']}")
                raise ValidationError(
                    message="min_score must be a number between 0 and 100",
                    details={"field": "completion_criteria.min_score"}
                )
                
            if "time_requirement" in completion_criteria and (
                not isinstance(completion_criteria["time_requirement"], int) or 
                completion_criteria["time_requirement"] < 0
            ):
                logger.warning(f"Invalid time_requirement in completion criteria: {completion_criteria['time_requirement']}")
                raise ValidationError(
                    message="time_requirement must be a positive integer",
                    details={"field": "completion_criteria.time_requirement"}
                )
                
            # Update lesson metadata in repository
            with self.transaction() as session:
                # Call update_lesson_metadata with the completion criteria
                metadata = {"completion_criteria": completion_criteria}
                updated_lesson = self.lesson_repo.update_lesson_metadata(
                    session,
                    lesson_uuid,
                    metadata
                )
                
            logger.info(f"Successfully set completion criteria for lesson {lesson_id}")
            return updated_lesson is not None
            
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
        Get completion criteria for a lesson
        
        Args:
            lesson_id: ID of the lesson to get criteria for
            
        Returns:
            Dictionary containing completion criteria
            
        Raises:
            ValidationError: If the lesson_id is invalid
            ResourceNotFoundError: If the lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Getting completion criteria for lesson {lesson_id}")
        
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
                
            # Get the lesson to ensure it exists
            with self.transaction() as session:
                db_lesson = self.lesson_repo.get_lesson(session, lesson_uuid)
                
            if not db_lesson:
                logger.warning(f"Lesson not found with ID: {lesson_id}")
                raise ResourceNotFoundError(
                    message="Lesson not found",
                    details={"lesson_id": lesson_id}
                )
                
            # Get completion criteria from lesson
            # Return the completion_criteria directly from the db_lesson object
            completion_criteria = db_lesson.completion_criteria
            if completion_criteria is None:
                completion_criteria = {}
            
            logger.info(f"Successfully retrieved completion criteria for lesson {lesson_id}")
            return completion_criteria
            
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
        Check if a user has met all completion criteria for a lesson
        
        Args:
            user_id: ID of the user
            lesson_id: ID of the lesson to check criteria for
            
        Returns:
            Tuple containing:
                - Boolean indicating if all criteria are met
                - List of messages describing unmet criteria (empty if all are met)
            
        Raises:
            ValidationError: If any of the IDs are invalid
            ResourceNotFoundError: If the lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Checking completion criteria for user {user_id}, lesson {lesson_id}")
        
        if not user_id or not lesson_id:
            logger.warning("Attempted to check completion criteria with empty IDs")
            raise ValidationError(
                message="User ID and lesson ID cannot be empty",
                details={"field": "user_id or lesson_id"}
            )
            
        try:
            # Convert string IDs to UUIDs
            try:
                lesson_uuid = uuid.UUID(lesson_id)
                user_uuid = uuid.UUID(user_id)
            except ValueError as e:
                logger.warning(f"Invalid ID format: {str(e)}")
                raise ValidationError(
                    message="Invalid ID format",
                    details={"error": str(e)}
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
                
            # Get completion criteria
            completion_criteria = db_lesson.completion_criteria
            if not completion_criteria:
                logger.info(f"No completion criteria found for lesson {lesson_id}")
                return True, []
                
            # Import here to avoid circular imports
            from src.services.progress_service import ProgressService
            progress_service = ProgressService()
            
            # Check each criterion
            unmet_criteria = []
            
            # Check minimum score
            if "min_score" in completion_criteria:
                min_score = completion_criteria["min_score"]
                user_score = progress_service.get_lesson_score(user_id, lesson_id)
                
                if user_score < min_score:
                    unmet_criteria.append(f"Score ({user_score}) is below the required minimum ({min_score})")
                    
            # Check required content
            if "required_content_ids" in completion_criteria and completion_criteria["required_content_ids"]:
                required_ids = completion_criteria["required_content_ids"]
                completed_ids = progress_service.get_completed_content_ids(user_id, lesson_id)
                
                missing_ids = [content_id for content_id in required_ids if content_id not in completed_ids]
                if missing_ids:
                    unmet_criteria.append(f"Not all required content has been completed ({len(missing_ids)} items remaining)")
                    
            # Check time requirement
            if "time_requirement" in completion_criteria:
                time_required = completion_criteria["time_requirement"]
                time_spent = progress_service.get_time_spent_on_lesson(user_id, lesson_id)
                
                if time_spent < time_required:
                    unmet_criteria.append(f"Time spent ({time_spent} min) is less than required ({time_required} min)")
                    
            criteria_met = len(unmet_criteria) == 0
            logger.info(f"Completion criteria check for user {user_id}, lesson {lesson_id}. Met: {criteria_met}")
            return criteria_met, unmet_criteria
            
        except (ValidationError, ResourceNotFoundError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error checking completion criteria: {str(e)}")
            report_error(e, context={"user_id": user_id, "lesson_id": lesson_id})
            raise DatabaseError(
                message="Failed to check completion criteria",
                details={
                    "user_id": user_id,
                    "lesson_id": lesson_id,
                    "error": str(e)
                }
            ) from e
            
    @handle_service_errors(service_name="lesson")
    def mark_lesson_complete(self, user_id: str, lesson_id: str, override_criteria: bool = False) -> bool:
        """
        Mark a lesson as complete for a user
        
        Args:
            user_id: ID of the user
            lesson_id: ID of the lesson to mark as complete
            override_criteria: If True, mark as complete even if completion criteria aren't met
            
        Returns:
            True if the lesson was marked as complete, False otherwise
            
        Raises:
            ValidationError: If any of the IDs are invalid
            ResourceNotFoundError: If the lesson does not exist
            DatabaseError: If there is an error accessing the database
        """
        logger.info(f"Marking lesson {lesson_id} as complete for user {user_id}")
        
        if not user_id or not lesson_id:
            logger.warning("Attempted to mark lesson complete with empty IDs")
            raise ValidationError(
                message="User ID and lesson ID cannot be empty",
                details={"field": "user_id or lesson_id"}
            )
            
        try:
            # Convert string IDs to UUIDs
            try:
                lesson_uuid = uuid.UUID(lesson_id)
                user_uuid = uuid.UUID(user_id)
            except ValueError as e:
                logger.warning(f"Invalid ID format: {str(e)}")
                raise ValidationError(
                    message="Invalid ID format",
                    details={"error": str(e)}
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
                
            # Check if completion criteria are met (if not overriding)
            if not override_criteria:
                criteria_met, unmet_criteria = self.check_completion_criteria_met(user_id, lesson_id)
                
                if not criteria_met:
                    logger.warning(f"Completion criteria not met for user {user_id}, lesson {lesson_id}")
                    logger.debug(f"Unmet criteria: {unmet_criteria}")
                    return False
                    
            # Mark lesson as complete
            from src.services.progress_service import ProgressService
            progress_service = ProgressService()
            
            result = progress_service.mark_lesson_complete(user_id=user_id, lesson_id=lesson_id)
            
            logger.info(f"Lesson {lesson_id} marked as complete for user {user_id}. Result: {result}")
            return result
            
        except (ValidationError, ResourceNotFoundError):
            # Allow these to propagate
            raise
        except Exception as e:
            logger.error(f"Error marking lesson as complete: {str(e)}")
            report_error(e, context={"user_id": user_id, "lesson_id": lesson_id})
            raise DatabaseError(
                message="Failed to mark lesson as complete",
                details={
                    "user_id": user_id,
                    "lesson_id": lesson_id,
                    "error": str(e)
                }
            ) from e

    @staticmethod
    def _validate_lesson_data(title: str = None, lesson_type: str = None, difficulty_level: str = None, **kwargs) -> None:
        """
        Validate lesson data
        
        Args:
            title: Title of the lesson
            lesson_type: Type of lesson (e.g., THEORY, PRACTICE, ASSESSMENT)
            difficulty_level: Difficulty level of the lesson
            **kwargs: Additional fields to validate
            
        Raises:
            ValidationError: If any of the fields are invalid
        """
        if title is not None and (not title or title.strip() == ""):
            logger.warning("Validation failed: Empty lesson title")
            raise ValidationError(
                message="Lesson title cannot be empty",
                details={"field": "title"}
            )
            
        if lesson_type is not None:
            try:
                # Check if the lesson_type is a valid key in the LessonType enum
                if lesson_type not in LessonType.__members__:
                    raise ValueError(f"{lesson_type} is not a valid LessonType key")
            except (ValueError, TypeError) as e:
                logger.warning(f"Validation failed: Invalid lesson type: {lesson_type}")
                raise ValidationError(
                    message="Invalid lesson type",
                    details={"field": "lesson_type", "error": str(e)}
                ) from e
                
        if difficulty_level is not None:
            try:
                # Check if the difficulty_level is a valid key in the DifficultyLevel enum
                if difficulty_level not in DifficultyLevel.__members__:
                    raise ValueError(f"{difficulty_level} is not a valid DifficultyLevel key")
            except (ValueError, TypeError) as e:
                logger.warning(f"Validation failed: Invalid difficulty level: {difficulty_level}")
                raise ValidationError(
                    message="Invalid difficulty level",
                    details={"field": "difficulty_level", "error": str(e)}
                ) from e 