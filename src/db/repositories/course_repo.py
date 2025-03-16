from sqlalchemy.orm import Session
from src.db.models import Course
import uuid
from typing import List, Optional, Dict, Any
import json
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)


def create_course(db: Session, 
                 topic: str,
                 name: str, 
                 description: str,
                 difficulty_level: str = "Beginner",
                 target_age_group: str = "15-17",
                 estimated_time: int = 300,
                 points_reward: int = 100,
                 prerequisites: Optional[Dict[str, Any]] = None,
                 tags: Optional[List[str]] = None) -> Course:
    """
    Create a new course in the database
    
    Args:
        db: Database session
        topic: Course topic ("Informatics" or "Math")
        name: Course name
        description: Course description
        difficulty_level: Course difficulty level ("Beginner", "Intermediate", or "Advanced")
        target_age_group: Target age group ("10-12", "13-14", or "15-17")
        estimated_time: Estimated time to complete the course in minutes
        points_reward: Points reward for completing the course
        prerequisites: Optional prerequisites for the course
        tags: Optional tags for the course
        
    Returns:
        Created course
    """
    # Create the course with the basic fields
    course = Course(
        id=uuid.uuid4(),
        topic=topic,
        name=name,
        description=description,
        created_at=datetime.now(timezone.utc)
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def delete_course(db: Session, course_id: uuid.UUID) -> Optional[Course]:
    """
    Delete a course from the database
    
    Args:
        db: Database session
        course_id: Course ID
        
    Returns:
        Deleted course or None if not found
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        return None
    db.delete(course)
    db.commit()
    return course


def get_course(db: Session, course_id: uuid.UUID) -> Optional[Course]:
    """
    Get a course by ID
    
    Args:
        db: Database session
        course_id: Course ID
        
    Returns:
        Course or None if not found
    """
    return db.query(Course).filter(Course.id == course_id).first()


def update_course(db: Session, 
                 course_id: uuid.UUID, 
                 **kwargs) -> Optional[Course]:
    """
    Update a course in the database
    
    Args:
        db: Database session
        course_id: Course ID
        **kwargs: Fields to update
        
    Returns:
        Updated course or None if not found
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        return None
    
    # Update basic fields
    basic_fields = ["name", "description", "topic"]
    for field in basic_fields:
        if field in kwargs:
            setattr(course, field, kwargs[field])
    
    db.commit()
    db.refresh(course)
    return course


def get_all_courses(db: Session) -> List[Course]:
    """
    Get all courses from the database
    
    Args:
        db: Database session
        
    Returns:
        List of all courses
    """
    return db.query(Course).all()


def get_courses_by_topic(db: Session, topic: str) -> List[Course]:
    """
    Get courses by topic
    
    Args:
        db: Database session
        topic: Course topic ("Informatics" or "Math")
        
    Returns:
        List of courses with the specified topic
    """
    return db.query(Course).filter(Course.topic == topic).all()


def get_courses_by_difficulty(db: Session, difficulty_level: str) -> List[Course]:
    """
    Get courses by difficulty level
    
    Args:
        db: Database session
        difficulty_level: Course difficulty level ("Beginner", "Intermediate", or "Advanced")
        
    Returns:
        List of courses with the specified difficulty level
    """
    # Since course_metadata no longer exists, we can't filter by difficulty level
    # Return all courses instead
    logger.warning("get_courses_by_difficulty: course_metadata no longer exists, returning all courses")
    return get_all_courses(db)


def get_courses_by_age_group(db: Session, target_age_group: str) -> List[Course]:
    """
    Get courses by target age group
    
    Args:
        db: Database session
        target_age_group: Target age group ("10-12", "13-14", or "15-17")
        
    Returns:
        List of courses with the specified target age group
    """
    # Since course_metadata no longer exists, we can't filter by age group
    # Return all courses instead
    logger.warning("get_courses_by_age_group: course_metadata no longer exists, returning all courses")
    return get_all_courses(db)
