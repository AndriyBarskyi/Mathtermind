from typing import List, Optional
from datetime import datetime, timezone
import uuid
import json
import logging

from src.ui.models.course import Course
from src.db import get_db
from src.db.repositories import course_repo
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
        """Get active courses"""
        # In a real implementation, this would filter by user progress
        # For now, we'll just return all courses as active
        return self.get_all_courses()
    
    def get_completed_courses(self) -> List[Course]:
        """Get completed courses"""
        # In a real implementation, this would filter by user progress
        # For now, we'll return an empty list
        return []
    
    def get_course_by_id(self, course_id: str) -> Optional[Course]:
        """Get a course by its ID"""
        try:
            course_uuid = uuid.UUID(course_id)
            db_course = course_repo.get_course(self.db, course_uuid)
            if db_course:
                return self._convert_db_course_to_ui_course(db_course)
        except ValueError:
            # Invalid UUID format
            logger.warning(f"Invalid UUID format: {course_id}")
        except Exception as e:
            logger.error(f"Error fetching course by ID {course_id}: {str(e)}")
        return None
    
    def filter_courses(self, 
                      search_text: str = "", 
                      subjects: List[str] = None,
                      levels: List[str] = None,
                      year_range: tuple = None,
                      status: str = "all") -> List[Course]:
        """
        Filter courses based on various criteria
        
        Args:
            search_text: Text to search in title and description
            subjects: List of subject IDs to include
            levels: List of level IDs to include
            year_range: Tuple of (min_year, max_year) for updated date
            status: Filter by status ('all', 'active', 'completed')
            
        Returns:
            List of filtered courses
        """
        try:
            # Start with all courses or filtered by status
            if status == "active":
                filtered_courses = self.get_active_courses()
            elif status == "completed":
                filtered_courses = self.get_completed_courses()
            else:
                filtered_courses = self.get_all_courses()
            
            # Apply text search filter
            if search_text:
                search_text = search_text.lower()
                filtered_courses = [
                    course for course in filtered_courses
                    if search_text in course.title.lower() or search_text in course.description.lower()
                ]
            
            # Apply subject filter
            if subjects:
                filtered_courses = [
                    course for course in filtered_courses
                    if course.subject in subjects
                ]
            
            # Apply level filter
            if levels:
                filtered_courses = [
                    course for course in filtered_courses
                    if course.level in levels
                ]
            
            # Apply year range filter
            if year_range:
                min_year, max_year = year_range
                filtered_courses = [
                    course for course in filtered_courses
                    if min_year <= course.updated_date.year <= max_year
                ]
            
            return filtered_courses
        except Exception as e:
            logger.error(f"Error filtering courses: {str(e)}")
            return []
    
    def _convert_db_course_to_ui_course(self, db_course: DBCourse) -> Course:
        """
        Convert a database Course model to a UI Course model
        
        Args:
            db_course: Database Course model
            
        Returns:
            UI Course model
        """
        try:
            # Get metadata or use empty dict if None
            metadata = db_course.course_metadata or {}
            
            # Extract tags from the metadata or use an empty list
            tags = metadata.get("tags", [])
            
            # Get difficulty level from metadata or use default
            difficulty_level = metadata.get("difficulty_level", "Beginner")
            
            # Map difficulty level to UI level
            level_mapping = {
                "Beginner": "basic",
                "Intermediate": "intermediate",
                "Advanced": "advanced"
            }
            level = level_mapping.get(difficulty_level, "basic")
            
            # Map topic to UI subject
            subject_mapping = {
                "Math": "math",
                "Informatics": "info"
            }
            subject = subject_mapping.get(db_course.topic, "info")
            
            # Get estimated time from metadata or use default
            estimated_time = metadata.get("estimated_time", 300)
            
            # Parse updated_at from metadata or use created_at
            try:
                updated_at_str = metadata.get("updated_at")
                if updated_at_str:
                    updated_date = datetime.fromisoformat(updated_at_str)
                else:
                    updated_date = db_course.created_at or datetime.now(timezone.utc)
            except (ValueError, TypeError):
                updated_date = db_course.created_at or datetime.now(timezone.utc)
            
            # Create and return a UI Course model
            return Course(
                id=str(db_course.id),
                title=db_course.name,
                description=db_course.description,
                tags=tags,
                updated_date=updated_date,
                duration_hours=estimated_time / 60,  # Convert minutes to hours
                level=level,
                subject=subject,
                is_active=True,  # Default to active for now
                is_completed=False  # Default to not completed
            )
        except Exception as e:
            logger.error(f"Error converting DB course to UI course: {str(e)}")
            # Return a default course as fallback
            return Course(
                id=str(db_course.id) if db_course.id else str(uuid.uuid4()),
                title=db_course.name if hasattr(db_course, 'name') and db_course.name else "Unknown Course",
                description=db_course.description if hasattr(db_course, 'description') and db_course.description else "No description available",
                tags=[],
                updated_date=datetime.now(timezone.utc),
                duration_hours=5.0,  # Default duration
                level="basic",
                subject="info",
                is_active=True,
                is_completed=False
            ) 