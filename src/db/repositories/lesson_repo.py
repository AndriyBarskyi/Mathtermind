from sqlalchemy.orm import Session
from src.db.models import Lesson
import uuid
from typing import List, Optional


def create_lesson(db: Session, course_id: uuid.UUID, title: str, content: dict, 
                 lesson_type: str, difficulty_level: str, lesson_order: int,
                 estimated_time: int, points_reward: int, prerequisites: dict,
                 learning_objectives: list) -> Lesson:
    """
    Create a new lesson in the database
    
    Args:
        db: Database session
        course_id: Course ID
        title: Lesson title
        content: Lesson content
        lesson_type: Lesson type
        difficulty_level: Lesson difficulty level
        lesson_order: Lesson order
        estimated_time: Estimated time to complete the lesson in minutes
        points_reward: Points reward for completing the lesson
        prerequisites: Prerequisites for the lesson
        learning_objectives: Learning objectives for the lesson
        
    Returns:
        Created lesson
    """
    lesson = Lesson(
        id=uuid.uuid4(),
        course_id=course_id,
        title=title,
        content=content,
        lesson_type=lesson_type,
        difficulty_level=difficulty_level,
        lesson_order=lesson_order,
        estimated_time=estimated_time,
        points_reward=points_reward,
        prerequisites=prerequisites,
        learning_objectives=learning_objectives
    )
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


def delete_lesson(db: Session, lesson_id: uuid.UUID) -> Optional[Lesson]:
    """
    Delete a lesson from the database
    
    Args:
        db: Database session
        lesson_id: Lesson ID
        
    Returns:
        Deleted lesson or None if not found
    """
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson is None:
        return None
    db.delete(lesson)
    db.commit()
    return lesson


def get_lesson(db: Session, lesson_id: str) -> Optional[Lesson]:
    """
    Get a lesson by ID
    
    Args:
        db: Database session
        lesson_id: Lesson ID
        
    Returns:
        Lesson or None if not found
    """
    try:
        lesson_uuid = uuid.UUID(lesson_id)
        return db.query(Lesson).filter(Lesson.id == lesson_uuid).first()
    except ValueError:
        # Invalid UUID format
        return None


def update_lesson(db: Session, lesson_id: uuid.UUID, **kwargs) -> Optional[Lesson]:
    """
    Update a lesson in the database
    
    Args:
        db: Database session
        lesson_id: Lesson ID
        **kwargs: Fields to update
        
    Returns:
        Updated lesson or None if not found
    """
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson is None:
        return None
    
    # Update fields
    for key, value in kwargs.items():
        if hasattr(lesson, key):
            setattr(lesson, key, value)
    
    db.commit()
    db.refresh(lesson)
    return lesson


def get_all_lessons(db: Session) -> List[Lesson]:
    """
    Get all lessons from the database
    
    Args:
        db: Database session
        
    Returns:
        List of all lessons
    """
    return db.query(Lesson).all()


def get_lessons_by_course_id(db: Session, course_id: str) -> List[Lesson]:
    """
    Get lessons by course ID
    
    Args:
        db: Database session
        course_id: Course ID
        
    Returns:
        List of lessons for the specified course
    """
    try:
        course_uuid = uuid.UUID(course_id)
        return db.query(Lesson).filter(Lesson.course_id == course_uuid).all()
    except ValueError:
        # Invalid UUID format
        return []
