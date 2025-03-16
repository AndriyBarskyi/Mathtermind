from typing import Optional, List
import uuid
import logging
from src.db import get_db
from src.db.repositories import lesson_repo
from src.models.lesson import Lesson
from src.db.models import Lesson as DBLesson

# Set up logging
logger = logging.getLogger(__name__)

class LessonService:
    """Service for managing lessons in the UI"""
    
    def __init__(self):
        # Connect to the database
        self.db = next(get_db())
    
    def get_lesson_by_id(self, lesson_id: str) -> Optional[Lesson]:
        """Get a lesson by its ID"""
        try:
            lesson_uuid = uuid.UUID(lesson_id)
            db_lesson = lesson_repo.get_lesson(self.db, lesson_uuid)
            if not db_lesson:
                return None
            return self._convert_db_lesson_to_ui_lesson(db_lesson)
        except Exception as e:
            logger.error(f"Error getting lesson by ID: {str(e)}")
            return None

    def get_lessons_by_course_id(self, course_id: str) -> List[Lesson]:
        """Get all lessons for a course"""
        try:
            # Convert string ID to UUID
            course_uuid = uuid.UUID(course_id)
            db_lessons = lesson_repo.get_lessons_by_course_id(self.db, course_uuid)
            return [self._convert_db_lesson_to_ui_lesson(lesson) for lesson in db_lessons]
        except Exception as e:
            logger.error(f"Error getting lessons by course ID: {str(e)}")
            return []

    def _convert_db_lesson_to_ui_lesson(self, db_lesson: DBLesson) -> Lesson:
        """Convert a database lesson model to a UI lesson model"""
        try:
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
            
            return Lesson(
                id=str(db_lesson.id),
                title=db_lesson.title,
                content=content,
                lesson_type=db_lesson.lesson_type.value if hasattr(db_lesson.lesson_type, 'value') else db_lesson.lesson_type,
                difficulty_level=db_lesson.difficulty_level.value if hasattr(db_lesson.difficulty_level, 'value') else db_lesson.difficulty_level,
                lesson_order=db_lesson.lesson_order,
                estimated_time=db_lesson.estimated_time,
                points_reward=db_lesson.points_reward,
                prerequisites=prerequisites,
                learning_objectives=learning_objectives
            )
        except Exception as e:
            logger.error(f"Error converting DB lesson to UI lesson: {str(e)}")
            # Return a default lesson as fallback
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