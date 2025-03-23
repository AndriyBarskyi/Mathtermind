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
    
    def create_lesson(self, db: Session, 
                    course_id: uuid.UUID,
                    name: str, 
                    description: str,
                    order: int,
                    prerequisites: Optional[List[uuid.UUID]] = None,
                    estimated_time: int = 0,
                    difficulty: str = "beginner",
                    is_required: bool = True,
                    metadata: Optional[Dict[str, Any]] = None) -> Lesson:
        """
        Create a new lesson.
        
        Args:
            db: Database session
            course_id: Course ID
            name: Lesson name
            description: Lesson description
            order: Display order in the course
            prerequisites: List of prerequisite lesson IDs
            estimated_time: Estimated time to complete in minutes
            difficulty: Lesson difficulty level
            is_required: Whether this lesson is required to complete the course
            metadata: Additional metadata
            
        Returns:
            Created lesson
        """
        lesson = Lesson(
            course_id=course_id,
            name=name,
            description=description,
            order=order,
            prerequisites=prerequisites or [],
            estimated_time=estimated_time,
            difficulty=difficulty,
            is_required=is_required,
            metadata=metadata or {}
        )
        
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        return lesson
    
    def update_lesson(self, db: Session, 
                    lesson_id: uuid.UUID,
                    name: Optional[str] = None,
                    description: Optional[str] = None,
                    order: Optional[int] = None,
                    prerequisites: Optional[List[uuid.UUID]] = None,
                    estimated_time: Optional[int] = None,
                    difficulty: Optional[str] = None,
                    is_required: Optional[bool] = None,
                    metadata: Optional[Dict[str, Any]] = None) -> Optional[Lesson]:
        """
        Update a lesson.
        
        Args:
            db: Database session
            lesson_id: Lesson ID
            name: New lesson name
            description: New lesson description
            order: New display order
            prerequisites: New list of prerequisite lesson IDs
            estimated_time: New estimated time to complete
            difficulty: New difficulty level
            is_required: New required status
            metadata: New metadata to merge with existing
            
        Returns:
            Updated lesson or None if not found
        """
        lesson = self.get_by_id(db, lesson_id)
        if lesson:
            if name is not None:
                lesson.name = name
                
            if description is not None:
                lesson.description = description
                
            if order is not None:
                lesson.order = order
                
            if prerequisites is not None:
                lesson.prerequisites = prerequisites
                
            if estimated_time is not None:
                lesson.estimated_time = estimated_time
                
            if difficulty is not None:
                lesson.difficulty = difficulty
                
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
        ).order_by(Lesson.order).all()
    
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
        ).order_by(Lesson.order).all()
    
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
        return self.update_lesson(db, lesson_id, order=new_order)
    
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
