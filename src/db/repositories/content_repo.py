"""
Repository module for Content models in the Mathtermind application.
"""

from typing import List, Optional, Dict, Any, Union, Type
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from src.db.models import (
    Content, 
    TheoryContent, 
    ExerciseContent, 
    QuizContent,
    AssessmentContent,
    InteractiveContent,
    ResourceContent
)
from .base_repository import BaseRepository


class ContentRepository(BaseRepository[Content]):
    """Repository for Content models with polymorphic capabilities."""
    
    def __init__(self):
        """Initialize the repository with the Content model."""
        super().__init__(Content)
    
    def create_theory_content(self, db: Session, 
                            lesson_id: uuid.UUID,
                            title: str,
                            text_content: str,
                            order: int,
                            estimated_time: int = 0,
                            images: Optional[List[str]] = None,
                            metadata: Optional[Dict[str, Any]] = None) -> TheoryContent:
        """
        Create a new theory content item.
        
        Args:
            db: Database session
            lesson_id: Lesson ID
            title: Content title
            text_content: Theory text
            order: Display order in the lesson
            estimated_time: Estimated time to complete in minutes
            images: List of image URLs
            metadata: Additional metadata
            
        Returns:
            Created theory content
        """
        theory_content = TheoryContent(
            lesson_id=lesson_id,
            title=title,
            content_type="theory",
            text_content=text_content,
            order=order,
            estimated_time=estimated_time,
            images=images or [],
            metadata=metadata or {}
        )
        
        db.add(theory_content)
        db.commit()
        db.refresh(theory_content)
        return theory_content
    
    def create_exercise_content(self, db: Session, 
                              lesson_id: uuid.UUID,
                              title: str,
                              problem_statement: str,
                              solution: str,
                              difficulty: str,
                              order: int,
                              hints: Optional[List[str]] = None,
                              answer_type: str = "text",
                              estimated_time: int = 0,
                              metadata: Optional[Dict[str, Any]] = None) -> ExerciseContent:
        """
        Create a new exercise content item.
        
        Args:
            db: Database session
            lesson_id: Lesson ID
            title: Content title
            problem_statement: Exercise problem to solve
            solution: Correct solution
            difficulty: Difficulty level
            order: Display order in the lesson
            hints: List of hints
            answer_type: Type of answer (text, multiple_choice, etc.)
            estimated_time: Estimated time to complete in minutes
            metadata: Additional metadata
            
        Returns:
            Created exercise content
        """
        exercise_content = ExerciseContent(
            lesson_id=lesson_id,
            title=title,
            content_type="exercise",
            problem_statement=problem_statement,
            solution=solution,
            difficulty=difficulty,
            order=order,
            hints=hints or [],
            answer_type=answer_type,
            estimated_time=estimated_time,
            metadata=metadata or {}
        )
        
        db.add(exercise_content)
        db.commit()
        db.refresh(exercise_content)
        return exercise_content
    
    def create_quiz_content(self, db: Session, 
                          lesson_id: uuid.UUID,
                          title: str,
                          questions: List[Dict[str, Any]],
                          order: int,
                          passing_score: float = 70.0,
                          estimated_time: int = 0,
                          metadata: Optional[Dict[str, Any]] = None) -> QuizContent:
        """
        Create a new quiz content item.
        
        Args:
            db: Database session
            lesson_id: Lesson ID
            title: Content title
            questions: List of question objects
            order: Display order in the lesson
            passing_score: Score required to pass the quiz
            estimated_time: Estimated time to complete in minutes
            metadata: Additional metadata
            
        Returns:
            Created quiz content
        """
        quiz_content = QuizContent(
            lesson_id=lesson_id,
            title=title,
            content_type="quiz",
            questions=questions,
            order=order,
            passing_score=passing_score,
            estimated_time=estimated_time,
            metadata=metadata or {}
        )
        
        db.add(quiz_content)
        db.commit()
        db.refresh(quiz_content)
        return quiz_content
    
    def create_assessment_content(self, db: Session, 
                                lesson_id: uuid.UUID,
                                title: str,
                                questions: List[Dict[str, Any]],
                                order: int,
                                passing_score: float = 70.0,
                                time_limit: Optional[int] = None,
                                is_final: bool = False,
                                estimated_time: int = 0,
                                metadata: Optional[Dict[str, Any]] = None) -> AssessmentContent:
        """
        Create a new assessment content item.
        
        Args:
            db: Database session
            lesson_id: Lesson ID
            title: Content title
            questions: List of question objects
            order: Display order in the lesson
            passing_score: Score required to pass the assessment
            time_limit: Time limit in minutes (if any)
            is_final: Whether this is a final assessment
            estimated_time: Estimated time to complete in minutes
            metadata: Additional metadata
            
        Returns:
            Created assessment content
        """
        assessment_content = AssessmentContent(
            lesson_id=lesson_id,
            title=title,
            content_type="assessment",
            questions=questions,
            order=order,
            passing_score=passing_score,
            time_limit=time_limit,
            is_final=is_final,
            estimated_time=estimated_time,
            metadata=metadata or {}
        )
        
        db.add(assessment_content)
        db.commit()
        db.refresh(assessment_content)
        return assessment_content
    
    def create_interactive_content(self, db: Session, 
                                 lesson_id: uuid.UUID,
                                 title: str,
                                 interaction_type: str,
                                 interaction_data: Dict[str, Any],
                                 order: int,
                                 estimated_time: int = 0,
                                 metadata: Optional[Dict[str, Any]] = None) -> InteractiveContent:
        """
        Create a new interactive content item.
        
        Args:
            db: Database session
            lesson_id: Lesson ID
            title: Content title
            interaction_type: Type of interaction (simulation, visualization, etc.)
            interaction_data: Data needed for the interaction
            order: Display order in the lesson
            estimated_time: Estimated time to complete in minutes
            metadata: Additional metadata
            
        Returns:
            Created interactive content
        """
        interactive_content = InteractiveContent(
            lesson_id=lesson_id,
            title=title,
            content_type="interactive",
            interaction_type=interaction_type,
            interaction_data=interaction_data,
            order=order,
            estimated_time=estimated_time,
            metadata=metadata or {}
        )
        
        db.add(interactive_content)
        db.commit()
        db.refresh(interactive_content)
        return interactive_content
    
    def create_resource_content(self, db: Session, 
                              lesson_id: uuid.UUID,
                              title: str,
                              resource_type: str,
                              resource_url: str,
                              description: str,
                              order: int,
                              is_required: bool = False,
                              estimated_time: int = 0,
                              metadata: Optional[Dict[str, Any]] = None) -> ResourceContent:
        """
        Create a new resource content item.
        
        Args:
            db: Database session
            lesson_id: Lesson ID
            title: Content title
            resource_type: Type of resource (pdf, video, article, etc.)
            resource_url: URL to the resource
            description: Description of the resource
            order: Display order in the lesson
            is_required: Whether this resource is required
            estimated_time: Estimated time to complete in minutes
            metadata: Additional metadata
            
        Returns:
            Created resource content
        """
        resource_content = ResourceContent(
            lesson_id=lesson_id,
            title=title,
            content_type="resource",
            resource_type=resource_type,
            resource_url=resource_url,
            description=description,
            order=order,
            is_required=is_required,
            estimated_time=estimated_time,
            metadata=metadata or {}
        )
        
        db.add(resource_content)
        db.commit()
        db.refresh(resource_content)
        return resource_content
    
    def get_lesson_content(self, db: Session, 
                         lesson_id: uuid.UUID,
                         content_type: Optional[str] = None) -> List[Content]:
        """
        Get all content for a lesson, optionally filtered by type.
        
        Args:
            db: Database session
            lesson_id: Lesson ID
            content_type: Optional content type filter
            
        Returns:
            List of content items
        """
        query = db.query(Content).filter(Content.lesson_id == lesson_id)
        
        if content_type:
            query = query.filter(Content.content_type == content_type)
            
        return query.order_by(Content.order).all()
    
    def get_content_by_type(self, db: Session, 
                          content_id: uuid.UUID) -> Optional[Union[
                              TheoryContent,
                              ExerciseContent,
                              QuizContent,
                              AssessmentContent,
                              InteractiveContent,
                              ResourceContent
                          ]]:
        """
        Get a content item by ID and return the appropriate specialized type.
        
        Args:
            db: Database session
            content_id: Content ID
            
        Returns:
            Content item with its specialized type or None if not found
        """
        base_content = db.query(Content).filter(Content.id == content_id).first()
        
        if not base_content:
            return None
            
        content_type_map = {
            "theory": TheoryContent,
            "exercise": ExerciseContent,
            "quiz": QuizContent,
            "assessment": AssessmentContent,
            "interactive": InteractiveContent,
            "resource": ResourceContent
        }
        
        if base_content.content_type in content_type_map:
            model_class = content_type_map[base_content.content_type]
            return db.query(model_class).filter(model_class.id == content_id).first()
            
        return base_content
    
    def update_content_order(self, db: Session, 
                           content_id: uuid.UUID, 
                           new_order: int) -> Optional[Content]:
        """
        Update the order of a content item.
        
        Args:
            db: Database session
            content_id: Content ID
            new_order: New display order
            
        Returns:
            Updated content item or None if not found
        """
        content = self.get_by_id(db, content_id)
        if content:
            content.order = new_order
            db.commit()
            db.refresh(content)
        return content
    
    def update_content_metadata(self, db: Session, 
                              content_id: uuid.UUID, 
                              metadata: Dict[str, Any]) -> Optional[Content]:
        """
        Update the metadata of a content item.
        
        Args:
            db: Database session
            content_id: Content ID
            metadata: New metadata to merge with existing
            
        Returns:
            Updated content item or None if not found
        """
        content = self.get_by_id(db, content_id)
        if content:
            if not content.metadata:
                content.metadata = {}
                
            content.metadata.update(metadata)
            db.commit()
            db.refresh(content)
        return content
    
    def get_estimated_lesson_time(self, db: Session, lesson_id: uuid.UUID) -> int:
        """
        Calculate the total estimated time for a lesson based on its content.
        
        Args:
            db: Database session
            lesson_id: Lesson ID
            
        Returns:
            Total estimated time in minutes
        """
        contents = self.get_lesson_content(db, lesson_id)
        return sum(content.estimated_time for content in contents if content.estimated_time)
    
    def get_required_content(self, db: Session, lesson_id: uuid.UUID) -> List[Content]:
        """
        Get required content for a lesson.
        
        Args:
            db: Database session
            lesson_id: Lesson ID
            
        Returns:
            List of required content items
        """
        # All content except optional resources
        query = db.query(Content).filter(
            Content.lesson_id == lesson_id
        ).filter(
            (Content.content_type != "resource") | 
            (Content.content_type == "resource" and Content.is_required == True)
        )
        
        return query.order_by(Content.order).all()