from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid
import json
import logging

from src.models.course import Course
from src.db import get_db
from src.db.repositories import course_repo, progress_repo
from src.db.models import Course as DBCourse

# Set up logging
logger = logging.getLogger(__name__)

class CourseService:
    """
    Service class for handling course data operations.
    This class provides methods for fetching, filtering, and managing courses.
    """
    
    def __init__(self):
        # Connect to the database
        self.db = next(get_db())
    
    def get_all_courses(self) -> List[Course]:
        """Get all available courses from the database"""
        try:
            db_courses = course_repo.get_all_courses(self.db)
            return [self._convert_db_course_to_ui_course(course) for course in db_courses]
        except Exception as e:
            logger.error(f"Error fetching all courses: {str(e)}")
            return []
    
    def get_active_courses(self) -> List[Course]:
        """Get courses that the user is currently enrolled in"""
        try:
            # TODO: Replace with actual user ID from authentication
            # Use a valid UUID string instead of "1"
            user_id = "00000000-0000-0000-0000-000000000001"  # Placeholder user ID
            
            try:
                # Convert string ID to UUID
                user_uuid = uuid.UUID(user_id)
                # Get courses the user is enrolled in
                user_progress = progress_repo.get_user_progress(self.db, user_uuid)
                
                # Get course IDs from progress
                course_ids = [progress.course_id for progress in user_progress]
                
                # Get courses by IDs
                active_courses = []
                for course_id in course_ids:
                    course = course_repo.get_course(self.db, course_id)
                    if course:
                        ui_course = self._convert_db_course_to_ui_course(course)
                        ui_course.is_active = True
                        active_courses.append(ui_course)
                
                return active_courses
            except Exception as e:
                logger.error(f"Error getting active courses: {str(e)}")
                # For development, return all courses if there's an error
                courses = self.get_all_courses()
                for course in courses:
                    course.is_active = True
                return courses
        except Exception as e:
            logger.error(f"Error in get_active_courses: {str(e)}")
            return []
    
    def get_completed_courses(self) -> List[Course]:
        """Get courses that the user has completed"""
        try:
            # TODO: Replace with actual user ID from authentication
            user_id = "00000000-0000-0000-0000-000000000001"  # Placeholder user ID
            
            try:
                # Convert string ID to UUID
                user_uuid = uuid.UUID(user_id)
                # Get courses the user has completed
                # This is a placeholder - in a real app, we would check if all lessons are completed
                completed_courses = []
                
                return completed_courses
            except Exception as e:
                logger.error(f"Error getting completed courses: {str(e)}")
                # For development, return an empty list
                return []
        except Exception as e:
            logger.error(f"Error in get_completed_courses: {str(e)}")
            return []
    
    def get_course_by_id(self, course_id: str) -> Optional[Course]:
        """Get a course by its ID"""
        try:
            course_uuid = uuid.UUID(course_id)
            db_course = course_repo.get_course(self.db, course_uuid)
            if not db_course:
                return None
            return self._convert_db_course_to_ui_course(db_course)
        except Exception as e:
            logger.error(f"Error getting course by ID: {str(e)}")
            return None
    
    def get_courses_by_difficulty(self, difficulty_level: str) -> List[Course]:
        """Get courses filtered by difficulty level"""
        try:
            db_courses = course_repo.get_courses_by_difficulty(self.db, difficulty_level)
            return [self._convert_db_course_to_ui_course(course) for course in db_courses]
        except Exception as e:
            logger.error(f"Error getting courses by difficulty: {str(e)}")
            return []
    
    def get_courses_by_age_group(self, age_group: str) -> List[Course]:
        """Get courses filtered by target age group"""
        try:
            db_courses = course_repo.get_courses_by_age_group(self.db, age_group)
            return [self._convert_db_course_to_ui_course(course) for course in db_courses]
        except Exception as e:
            logger.error(f"Error getting courses by age group: {str(e)}")
            return []
    
    def search_courses(self, query: str) -> List[Course]:
        """Search for courses by name or description"""
        try:
            db_courses = course_repo.search_courses(self.db, query)
            return [self._convert_db_course_to_ui_course(course) for course in db_courses]
        except Exception as e:
            logger.error(f"Error searching courses: {str(e)}")
            return []
    
    def _convert_db_course_to_ui_course(self, db_course: DBCourse) -> Course:
        """Convert a database course model to a UI course model"""
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