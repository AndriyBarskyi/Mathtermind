from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid

from src.models.course import Course
from src.db import get_db
from src.db.repositories import course_repo, progress_repo
from src.db.models import Course as DBCourse
from src.services.base_service import BaseService

# Import our new logging and error handling framework
from src.core import get_logger
from src.core.error_handling import (
    handle_service_errors,
    ServiceError,
    ResourceNotFoundError,
    DatabaseError,
    create_error_boundary,
    report_error
)

# Set up logging using our new framework
logger = get_logger(__name__)


class CourseService(BaseService):
    """
    Service class for handling course data operations.
    This class provides methods for fetching, filtering, and managing courses.
    """
    
    def __init__(self):
        """Initialize the course service with a database connection."""
        super().__init__(repository=course_repo)
        logger.debug("CourseService initialized")
    
    @handle_service_errors(service_name="course")
    def get_all_courses(self) -> List[Course]:
        """
        Get all available courses from the database.
        
        Returns:
            A list of all courses.
        """
        logger.info("Fetching all courses")
        
        db_courses = course_repo.get_all_courses(self.db)
        course_count = len(db_courses)
        logger.debug(f"Found {course_count} courses")
        
        return [self._convert_db_course_to_ui_course(course) for course in db_courses]
    
    @handle_service_errors(service_name="course")
    def get_active_courses(self) -> List[Course]:
        """
        Get courses that the user is currently enrolled in.
        
        Returns:
            A list of active courses for the current user.
        """
        logger.info("Fetching active courses for user")
        
        # TODO: Replace with actual user ID from authentication
        # Use a valid UUID string instead of "1"
        user_id = "00000000-0000-0000-0000-000000000001"  # Placeholder user ID
        logger.debug(f"Using placeholder user ID: {user_id}")
        
        with create_error_boundary("fetch_user_progress"):
            # Convert string ID to UUID
            user_uuid = uuid.UUID(user_id)
            
            # Get courses the user is enrolled in
            user_progress = progress_repo.get_user_progress(self.db, user_uuid)
            
            # Get course IDs from progress
            course_ids = [progress.course_id for progress in user_progress]
            logger.debug(f"User enrolled in {len(course_ids)} courses")
            
            # Get courses by IDs
            active_courses = []
            for course_id in course_ids:
                course = course_repo.get_course(self.db, course_id)
                if course:
                    ui_course = self._convert_db_course_to_ui_course(course)
                    ui_course.is_active = True
                    active_courses.append(ui_course)
            
            logger.info(f"Found {len(active_courses)} active courses for user")
            return active_courses
            
        # For development, return all courses if there's an error
        logger.warning("Error in fetching user progress. Returning all courses as active (development fallback).")
        courses = self.get_all_courses()
        for course in courses:
            course.is_active = True
        return courses
    
    @handle_service_errors(service_name="course")
    def get_completed_courses(self) -> List[Course]:
        """
        Get courses that the user has completed.
        
        Returns:
            A list of completed courses for the current user.
        """
        logger.info("Fetching completed courses for user")
        
        # TODO: Replace with actual user ID from authentication
        user_id = "00000000-0000-0000-0000-000000000001"  # Placeholder user ID
        logger.debug(f"Using placeholder user ID: {user_id}")
        
        with create_error_boundary("fetch_completed_courses"):
            # Convert string ID to UUID
            user_uuid = uuid.UUID(user_id)
            
            # Get courses the user has completed
            # This is a placeholder - in a real app, we would check if all lessons are completed
            completed_courses = []
            
            logger.info(f"Found {len(completed_courses)} completed courses for user")
            return completed_courses
    
    @handle_service_errors(service_name="course")
    def get_course_by_id(self, course_id: str) -> Optional[Course]:
        """
        Get a course by its ID.
        
        Args:
            course_id: The ID of the course to retrieve.
            
        Returns:
            The course if found, None otherwise.
            
        Raises:
            ResourceNotFoundError: If the course with the given ID is not found.
        """
        logger.info(f"Fetching course with ID: {course_id}")
        
        try:
            course_uuid = uuid.UUID(course_id)
            db_course = course_repo.get_course(self.db, course_uuid)
            
            if not db_course:
                logger.warning(f"Course with ID {course_id} not found")
                raise ResourceNotFoundError(
                    message=f"Course with ID {course_id} not found",
                    resource_type="course",
                    resource_id=course_id
                )
                
            logger.debug(f"Course found: {db_course.name}")
            return self._convert_db_course_to_ui_course(db_course)
            
        except ValueError:
            logger.error(f"Invalid course ID format: {course_id}")
            raise ServiceError(
                message=f"Invalid course ID format: {course_id}",
                service_name="course",
                details={"course_id": course_id}
            )
    
    @handle_service_errors(service_name="course")
    def get_courses_by_difficulty(self, difficulty_level: str) -> List[Course]:
        """
        Get courses filtered by difficulty level.
        
        Args:
            difficulty_level: The difficulty level to filter by.
            
        Returns:
            A list of courses with the specified difficulty level.
        """
        logger.info(f"Fetching courses with difficulty level: {difficulty_level}")
        
        db_courses = course_repo.get_courses_by_difficulty(self.db, difficulty_level)
        course_count = len(db_courses)
        logger.debug(f"Found {course_count} courses with difficulty level {difficulty_level}")
        
        return [self._convert_db_course_to_ui_course(course) for course in db_courses]
    
    @handle_service_errors(service_name="course")
    def get_courses_by_age_group(self, age_group: str) -> List[Course]:
        """
        Get courses filtered by target age group.
        
        Args:
            age_group: The age group to filter by.
            
        Returns:
            A list of courses for the specified age group.
        """
        logger.info(f"Fetching courses for age group: {age_group}")
        
        db_courses = course_repo.get_courses_by_age_group(self.db, age_group)
        course_count = len(db_courses)
        logger.debug(f"Found {course_count} courses for age group {age_group}")
        
        return [self._convert_db_course_to_ui_course(course) for course in db_courses]
    
    @handle_service_errors(service_name="course")
    def search_courses(self, query: str) -> List[Course]:
        """
        Search for courses by name or description.
        
        Args:
            query: The search query.
            
        Returns:
            A list of courses matching the search query.
        """
        logger.info(f"Searching courses with query: {query}")
        
        db_courses = course_repo.search_courses(self.db, query)
        course_count = len(db_courses)
        logger.debug(f"Found {course_count} courses matching search query '{query}'")
        
        return [self._convert_db_course_to_ui_course(course) for course in db_courses]
    
    @handle_service_errors(service_name="course")
    def _convert_db_course_to_ui_course(self, db_course: DBCourse) -> Course:
        """
        Convert a database course model to a UI course model.
        
        Args:
            db_course: The database course model.
            
        Returns:
            The UI course model.
        """
        logger.debug(f"Converting DB course to UI course: {db_course.id}")
        
        try:
            # Create metadata dictionary with default values
            metadata = {
                "difficulty_level": "Beginner",
                "target_age_group": "13-14",
                "estimated_time": 60,  # Default 60 minutes
                "points_reward": 10,
                "prerequisites": {},
                "tags": [],
                "updated_at": datetime.now(timezone.utc)
            }
            
            # Extract tags from the course
            tags = [tag.name for tag in db_course.tags] if hasattr(db_course, 'tags') and db_course.tags else []
            metadata["tags"] = tags
            
            return Course(
                id=str(db_course.id),
                topic=db_course.topic.value if hasattr(db_course.topic, 'value') else db_course.topic,
                name=db_course.name,
                description=db_course.description,
                created_at=db_course.created_at,
                tags=tags,
                metadata=metadata
            )
        except Exception as e:
            logger.error(f"Error converting DB course to UI course: {str(e)}")
            report_error(e, operation="convert_db_course", course_id=str(db_course.id))
            
            # Return a default course as fallback
            return Course(
                id=str(db_course.id) if hasattr(db_course, 'id') else "unknown",
                topic="Informatics",
                name=db_course.name if hasattr(db_course, 'name') else "Unknown Course",
                description=db_course.description if hasattr(db_course, 'description') else "No description available",
                created_at=datetime.now(timezone.utc),
                tags=[],
                metadata={}
            ) 