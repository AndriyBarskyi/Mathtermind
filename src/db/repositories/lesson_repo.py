"""
Repository module for Lesson model in the Mathtermind application.
"""

from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from src.db.models import Lesson, Content
from .base_repository import BaseRepository


class LessonRepository(BaseRepository[Lesson]):
    """Repository for Lesson model."""
    
    def __init__(self):
        """Initialize the repository with the Lesson model."""
        super().__init__(Lesson)
    
    def get_lesson(self, db: Session, lesson_id: uuid.UUID) -> Optional[Lesson]:
        """
        Get a lesson by its ID. Alias for get_by_id.
        
        Args:
            db: Database session
            lesson_id: Lesson ID
            
        Returns:
            Lesson if found, None otherwise
        """
        return self.get_by_id(db, lesson_id)
    
    def create_lesson(self, db: Session, 
                    course_id: uuid.UUID,
                    title: str, 
                    difficulty_level: str,
                    lesson_order: int,
                    estimated_time: int = 0,
                    points_reward: int = 10,
                    prerequisites: Optional[Dict[str, Any]] = None,
                    learning_objectives: Optional[List[str]] = None,
                    content: Optional[Dict[str, Any]] = None,
                    is_required: bool = True,
                    metadata: Optional[Dict[str, Any]] = None,
                    lesson_type: str = "") -> Lesson:
        """
        Create a new lesson.
        
        Args:
            db: Database session
            course_id: Course ID
            title: Lesson title
            difficulty_level: Difficulty level
            lesson_order: Display order in the course
            estimated_time: Estimated time to complete in minutes
            points_reward: Points reward for completing the lesson
            prerequisites: Dictionary of prerequisite lessons
            learning_objectives: List of learning objectives
            content: Content of the lesson
            is_required: Whether this lesson is required to complete the course
            metadata: Additional metadata
            lesson_type: Deprecated parameter, kept for database compatibility
            
        Returns:
            Created lesson
            
        Note:
            lesson_type is deprecated. Lessons are containers for content items.
            Content items have types, not lessons.
        """
        lesson = Lesson(
            course_id=course_id,
            title=title,
            lesson_type=lesson_type,  # Kept for database compatibility but deprecated
            difficulty_level=difficulty_level,
            lesson_order=lesson_order,
            estimated_time=estimated_time,
            points_reward=points_reward,
            prerequisites=prerequisites or {},
            learning_objectives=learning_objectives or [],
            content=content or {},
            is_required=is_required,
            metadata=metadata or {}
        )
        
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        return lesson
    
    def update_lesson(self, db: Session, 
                    lesson_id: uuid.UUID,
                    title: Optional[str] = None,
                    lesson_order: Optional[int] = None,
                    prerequisites: Optional[Dict[str, Any]] = None,
                    estimated_time: Optional[int] = None,
                    difficulty_level: Optional[str] = None,
                    points_reward: Optional[int] = None,
                    learning_objectives: Optional[List[str]] = None,
                    content: Optional[Dict[str, Any]] = None,
                    is_required: Optional[bool] = None,
                    metadata: Optional[Dict[str, Any]] = None,
                    lesson_type: Optional[str] = None) -> Optional[Lesson]:
        """
        Update a lesson.
        
        Args:
            db: Database session
            lesson_id: Lesson ID
            title: New lesson title
            lesson_order: New display order
            prerequisites: New dictionary of prerequisite lessons
            estimated_time: New estimated time to complete
            difficulty_level: New difficulty level
            points_reward: New points reward
            learning_objectives: New learning objectives
            content: New content
            is_required: New required status
            metadata: New metadata to merge with existing
            lesson_type: Deprecated parameter, kept for database compatibility
            
        Returns:
            Updated lesson or None if not found
            
        Note:
            lesson_type is deprecated. Lessons are containers for content items.
            Content items have types, not lessons.
        """
        lesson = self.get_by_id(db, lesson_id)
        if lesson:
            if title is not None:
                lesson.title = title
                
            if lesson_type is not None:
                # This is kept for database compatibility but is deprecated
                lesson.lesson_type = lesson_type
                
            if lesson_order is not None:
                lesson.lesson_order = lesson_order
                
            if prerequisites is not None:
                lesson.prerequisites = prerequisites
                
            if estimated_time is not None:
                lesson.estimated_time = estimated_time
                
            if difficulty_level is not None:
                lesson.difficulty_level = difficulty_level
                
            if points_reward is not None:
                lesson.points_reward = points_reward
                
            if learning_objectives is not None:
                lesson.learning_objectives = learning_objectives
                
            if content is not None:
                lesson.content = content
                
            if is_required is not None:
                lesson.is_required = is_required
                
            if metadata is not None:
                if not lesson.metadata:
                    lesson.metadata = {}
                lesson.metadata.update(metadata)
                
            db.commit()
            db.refresh(lesson)
        return lesson
    
    def delete_lesson(self, db: Session, lesson_id: uuid.UUID) -> Optional[Lesson]:
        """
        Delete a lesson.
        
        Args:
            db: Database session
            lesson_id: Lesson ID
            
        Returns:
            Deleted lesson or None if not found
        """
        lesson = self.get_by_id(db, lesson_id)
        if lesson:
            db.delete(lesson)
            db.commit()
        return lesson
    
    def get_lessons_by_course_id(self, db: Session, course_id: uuid.UUID) -> List[Lesson]:
        """
        Get all lessons for a course.
        
        Args:
            db: Database session
            course_id: Course ID
            
        Returns:
            List of lessons
        """
        return db.query(Lesson).filter(
            Lesson.course_id == course_id
        ).order_by(Lesson.lesson_order).all()
    
    def get_required_lessons(self, db: Session, course_id: uuid.UUID) -> List[Lesson]:
        """
        Get all required lessons for a course.
        
        Args:
            db: Database session
            course_id: Course ID
            
        Returns:
            List of required lessons
        """
        return db.query(Lesson).filter(
            Lesson.course_id == course_id,
            Lesson.is_required == True
        ).order_by(Lesson.lesson_order).all()
    
    def get_lesson_with_content(self, db: Session, lesson_id: uuid.UUID) -> Dict[str, Any]:
        """
        Get a lesson with all its content items.
        
        Args:
            db: Database session
            lesson_id: Lesson ID
            
        Returns:
            Dictionary with lesson and content items
        """
        lesson = self.get_by_id(db, lesson_id)
        if not lesson:
            return None
            
        content_items = db.query(Content).filter(
            Content.lesson_id == lesson_id
        ).order_by(Content.order).all()
        
        return {
            "lesson": lesson,
            "content": content_items
        }
    
    def update_lesson_order(self, db: Session, 
                          lesson_id: uuid.UUID, 
                          new_order: int) -> Optional[Lesson]:
        """
        Update the order of a lesson.
        
        Args:
            db: Database session
            lesson_id: Lesson ID
            new_order: New display order
            
        Returns:
            Updated lesson or None if not found
        """
        return self.update_lesson(db, lesson_id, lesson_order=new_order)
    
    def get_prerequisite_lessons(self, db: Session, lesson_id: uuid.UUID) -> List[Lesson]:
        """
        Get all prerequisite lessons for a lesson.
        
        Args:
            db: Database session
            lesson_id: Lesson ID
            
        Returns:
            List of prerequisite lessons
        """
        lesson = self.get_by_id(db, lesson_id)
        if not lesson or not lesson.prerequisites:
            return []
            
        return db.query(Lesson).filter(
            Lesson.id.in_(lesson.prerequisites)
        ).all()
    
    def get_dependent_lessons(self, db: Session, lesson_id: uuid.UUID) -> List[Lesson]:
        """
        Get all lessons that have this lesson as a prerequisite.
        
        Args:
            db: Database session
            lesson_id: Lesson ID
            
        Returns:
            List of dependent lessons
        """
        lessons = db.query(Lesson).all()
        dependent_lessons = []
        
        for lesson in lessons:
            if lesson.prerequisites and lesson_id in lesson.prerequisites:
                dependent_lessons.append(lesson)
                
        return dependent_lessons
        
    def update_lesson_metadata(self, db: Session, 
                             lesson_id: uuid.UUID, 
                             metadata: Dict[str, Any]) -> Optional[Lesson]:
        """
        Update the metadata of a lesson.
        
        Args:
            db: Database session
            lesson_id: Lesson ID
            metadata: New metadata to merge with existing
            
        Returns:
            Updated lesson or None if not found
        """
        return self.update_lesson(db, lesson_id, metadata=metadata)
