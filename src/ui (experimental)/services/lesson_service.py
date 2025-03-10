from typing import Optional, List
from src.db import get_db
from src.db.repositories import lesson_repo
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Lesson:
    """UI model for a lesson"""
    id: str
    title: str
    content: dict
    lesson_type: str
    difficulty_level: str
    lesson_order: int
    estimated_time: int
    points_reward: int
    prerequisites: dict
    learning_objectives: list


class LessonService:
    """Service for managing lessons in the UI"""
    
    def get_lesson_by_id(self, lesson_id: str) -> Optional[Lesson]:
        """Get a lesson by its ID"""
        try:
            db = next(get_db())
            db_lesson = lesson_repo.get_lesson(db, lesson_id)
            if not db_lesson:
                return None
            return self._convert_db_lesson_to_ui_lesson(db_lesson)
        except Exception as e:
            print(f"Error getting lesson: {str(e)}")
            return None

    def get_lessons_by_course_id(self, course_id: str) -> List[Lesson]:
        """Get all lessons for a course"""
        try:
            db = next(get_db())
            db_lessons = lesson_repo.get_lessons_by_course_id(db, course_id)
            return [self._convert_db_lesson_to_ui_lesson(lesson) for lesson in db_lessons]
        except Exception as e:
            print(f"Error getting lessons: {str(e)}")
            return []

    def _convert_db_lesson_to_ui_lesson(self, db_lesson) -> Lesson:
        """Convert a database lesson model to a UI lesson model"""
        try:
            return Lesson(
                id=str(db_lesson.id),
                title=db_lesson.title,
                content=db_lesson.content,
                lesson_type=db_lesson.lesson_type,
                difficulty_level=db_lesson.difficulty_level,
                lesson_order=db_lesson.lesson_order,
                estimated_time=db_lesson.estimated_time,
                points_reward=db_lesson.points_reward,
                prerequisites=db_lesson.prerequisites,
                learning_objectives=db_lesson.learning_objectives
            )
        except Exception as e:
            print(f"Error converting lesson: {str(e)}")
            # Return a default lesson as fallback
            return Lesson(
                id=str(db_lesson.id) if hasattr(db_lesson, 'id') else "unknown",
                title=db_lesson.title if hasattr(db_lesson, 'title') else "Unknown Lesson",
                content={},
                lesson_type="Theory",
                difficulty_level="Beginner",
                lesson_order=1,
                estimated_time=30,
                points_reward=10,
                prerequisites={},
                learning_objectives=[]
            ) 