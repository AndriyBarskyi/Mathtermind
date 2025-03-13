from typing import List, Optional
from datetime import datetime, timezone
import uuid
import json
import logging

from src.ui.models.course import Course
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
            user_id = "1"  # Placeholder user ID
            
            # Get courses the user is enrolled in
            user_progress = progress_repo.get_user_progress(self.db, user_id)
            
            # If no progress records, return empty list
            if not user_progress:
                # For development, return all courses if no progress exists
                return self.get_all_courses()
            
            # Extract course IDs from progress records
            course_ids = [progress.course_id for progress in user_progress]
            
            # Get course details for each course ID
            active_courses = []
            for course_id in course_ids:
                course = course_repo.get_course(self.db, str(course_id))
                if course:
                    active_courses.append(self._convert_db_course_to_ui_course(course))
            
            # Sort by last accessed (most recent first)
            active_courses.sort(
                key=lambda c: next(
                    (p.last_accessed for p in user_progress if str(p.course_id) == c.id), 
                    datetime.min
                ),
                reverse=True
            )
            
            return active_courses
        except Exception as e:
            logger.error(f"Error fetching active courses: {str(e)}")
            # For development, return all courses if there's an error
            return self.get_all_courses()
    
    def get_completed_courses(self) -> List[Course]:
        """Get courses that the user has completed"""
        try:
            # TODO: Replace with actual user ID from authentication
            user_id = "1"  # Placeholder user ID
            
            # Get completed courses (progress >= 100%)
            user_progress = progress_repo.get_completed_progress(self.db, user_id)
            
            # Extract course IDs from progress records
            course_ids = [progress.course_id for progress in user_progress]
            
            # Get course details for each course ID
            completed_courses = []
            for course_id in course_ids:
                course = course_repo.get_course(self.db, str(course_id))
                if course:
                    completed_courses.append(self._convert_db_course_to_ui_course(course))
            
            return completed_courses
        except Exception as e:
            logger.error(f"Error fetching completed courses: {str(e)}")
            return []
    
    def get_course_by_id(self, course_id: str) -> Optional[Course]:
        """Get a specific course by ID"""
        try:
            db_course = course_repo.get_course(self.db, course_id)
            if not db_course:
                return None
            return self._convert_db_course_to_ui_course(db_course)
        except Exception as e:
            logger.error(f"Error fetching course by ID: {str(e)}")
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
            search_text: Text to search in course title and description
            subjects: List of subjects to include
            levels: List of difficulty levels to include
            year_range: Tuple of (min_year, max_year) for course creation date
            status: Filter by status ("all", "active", "completed")
            
        Returns:
            List of filtered courses
        """
        try:
            # Get the appropriate base list of courses
            if status == "active":
                courses = self.get_active_courses()
            elif status == "completed":
                courses = self.get_completed_courses()
            else:
                courses = self.get_all_courses()
            
            # Apply text search filter
            if search_text and search_text.strip():
                search_text = search_text.lower().strip()
                logger.info(f"Filtering courses by search text: '{search_text}'")
                filtered_courses = []
                for course in courses:
                    if (search_text in course.name.lower() or 
                        search_text in course.description.lower()):
                        filtered_courses.append(course)
                    else:
                        # Check in metadata tags if available
                        tags = course.metadata.get("tags", [])
                        if any(search_text in tag.lower() for tag in tags):
                            filtered_courses.append(course)
                
                courses = filtered_courses
                logger.info(f"Found {len(courses)} courses matching search text")
            
            # Apply subject filter
            if subjects:
                logger.info(f"Filtering courses by subjects: {subjects}")
                courses = [
                    course for course in courses
                    if course.topic.lower() in [s.lower() for s in subjects]
                ]
            
            # Apply level filter
            if levels:
                logger.info(f"Filtering courses by levels: {levels}")
                courses = [
                    course for course in courses
                    if course.metadata.get("difficulty_level", "").lower() in [l.lower() for l in levels]
                ]
            
            # Apply year range filter
            if year_range:
                min_year, max_year = year_range
                logger.info(f"Filtering courses by year range: {min_year}-{max_year}")
                courses = [
                    course for course in courses
                    if course.created_at and min_year <= course.created_at.year <= max_year
                ]
            
            logger.info(f"Returning {len(courses)} courses after all filters")
            return courses
        except Exception as e:
            logger.error(f"Error filtering courses: {str(e)}")
            return []
    
    def _convert_db_course_to_ui_course(self, db_course: DBCourse) -> Course:
        """Convert a database course model to a UI course model"""
        try:
            return Course(
                id=str(db_course.id),
                topic=db_course.topic,
                name=db_course.name,
                description=db_course.description,
                metadata=db_course.course_metadata or {},
                created_at=db_course.created_at
            )
        except Exception as e:
            logger.error(f"Error converting course: {str(e)}")
            # Return a default course as fallback
            return Course(
                id=str(db_course.id) if hasattr(db_course, 'id') else "unknown",
                topic="Informatics",
                name=db_course.name if hasattr(db_course, 'name') else "Unknown Course",
                description=db_course.description if hasattr(db_course, 'description') else "",
                metadata={},
                created_at=datetime.now(timezone.utc)
            ) 