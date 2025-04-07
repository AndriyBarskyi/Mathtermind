"""
Content service for Mathtermind.

This module provides service methods for managing different types of content.
"""

from typing import List, Optional, Dict, Any, Union, Type, TypeVar
import uuid
import logging
from datetime import datetime

from src.db import get_db
from src.db.models import (
    Content as DBContent,
    Lesson as DBLesson,
    Course as DBCourse
)
from src.db.repositories import (
    ContentRepository,
    LessonRepository,
    CourseRepository,
    ContentStateRepository
)
from src.models.content import (
    Content, 
    TheoryContent, 
    ExerciseContent, 
    QuizContent, 
    AssessmentContent, 
    InteractiveContent, 
    ResourceContent
)
from src.models.course import Course
from src.models.lesson import Lesson

# Type variable for content types
T = TypeVar('T', bound=Content)

# Set up logging
logger = logging.getLogger(__name__)


class ContentService:
    """Service for managing content."""
    
    def __init__(self):
        """Initialize the content service."""
        self.db = next(get_db())
        self.content_repo = ContentRepository(self.db)
        self.lesson_repo = LessonRepository(self.db)
        self.course_repo = CourseRepository(self.db)
        self.content_state_repo = ContentStateRepository(self.db)
    
    # Content Methods
    
    def get_content_by_id(self, content_id: str) -> Optional[Content]:
        """
        Get content by ID.
        
        Args:
            content_id: The ID of the content
            
        Returns:
            The content item if found, None otherwise
        """
        try:
            content_uuid = uuid.UUID(content_id)
            
            # Get the content from the repository
            db_content = self.content_repo.get_by_id(content_uuid)
            
            if not db_content:
                return None
                
            return self._convert_db_content_to_ui_content(db_content)
        except Exception as e:
            logger.error(f"Error getting content by ID: {str(e)}")
            return None
    
    def get_lesson_content(self, lesson_id: str) -> List[Content]:
        """
        Get all content items for a lesson.
        
        Args:
            lesson_id: The ID of the lesson
            
        Returns:
            A list of content items
        """
        try:
            lesson_uuid = uuid.UUID(lesson_id)
            
            # Get all content items for the lesson
            db_content_items = self.content_repo.get_by_lesson_id(lesson_uuid)
            
            # Convert to UI models
            return [self._convert_db_content_to_ui_content(item) for item in db_content_items]
        except Exception as e:
            logger.error(f"Error getting lesson content: {str(e)}")
            return []
    
    def create_theory_content(self, 
                           lesson_id: str,
                           title: str,
                           description: str,
                           text_content: str,
                           images: Optional[List[Dict[str, Any]]] = None,
                           examples: Optional[List[Dict[str, Any]]] = None,
                           references: Optional[List[Dict[str, Any]]] = None,
                           order: int = 0,
                           estimated_time: int = 0,
                           metadata: Optional[Dict[str, Any]] = None) -> Optional[TheoryContent]:
        """
        Create theory content.
        
        Args:
            lesson_id: The ID of the lesson
            title: The title of the content
            description: The description of the content
            text_content: The main text content
            images: Optional list of images
            examples: Optional list of examples
            references: Optional list of references
            order: The order of the content within the lesson
            estimated_time: The estimated time to complete in minutes
            metadata: Additional metadata
            
        Returns:
            The created theory content if successful, None otherwise
        """
        try:
            lesson_uuid = uuid.UUID(lesson_id)
            
            # Create content data
            content_data = {
                "text_content": text_content,
                "images": images or [],
                "examples": examples or [],
                "references": references or []
            }
            
            # Create the content
            db_content = self.content_repo.create(
                lesson_id=lesson_uuid,
                title=title,
                content_type="theory",
                order=order,
                description=description,
                content_data=content_data,
                estimated_time=estimated_time,
                metadata=metadata or {}
            )
            
            if not db_content:
                return None
                
            return self._convert_db_content_to_ui_content(db_content)
        except Exception as e:
            logger.error(f"Error creating theory content: {str(e)}")
            self.db.rollback()
            return None
    
    def create_exercise_content(self, 
                             lesson_id: str,
                             title: str,
                             description: str,
                             problem_statement: str,
                             solution: str,
                             difficulty: str,
                             hints: Optional[List[str]] = None,
                             order: int = 0,
                             estimated_time: int = 0,
                             metadata: Optional[Dict[str, Any]] = None) -> Optional[ExerciseContent]:
        """
        Create exercise content.
        
        Args:
            lesson_id: The ID of the lesson
            title: The title of the content
            description: The description of the content
            problem_statement: The problem statement
            solution: The solution to the problem
            difficulty: The difficulty level
            hints: Optional list of hints
            order: The order of the content within the lesson
            estimated_time: The estimated time to complete in minutes
            metadata: Additional metadata
            
        Returns:
            The created exercise content if successful, None otherwise
        """
        try:
            lesson_uuid = uuid.UUID(lesson_id)
            
            # Create content data
            content_data = {
                "problem_statement": problem_statement,
                "solution": solution,
                "difficulty": difficulty,
                "hints": hints or []
            }
            
            # Create the content
            db_content = self.content_repo.create(
                lesson_id=lesson_uuid,
                title=title,
                content_type="exercise",
                order=order,
                description=description,
                content_data=content_data,
                estimated_time=estimated_time,
                metadata=metadata or {}
            )
            
            if not db_content:
                return None
                
            return self._convert_db_content_to_ui_content(db_content)
        except Exception as e:
            logger.error(f"Error creating exercise content: {str(e)}")
            self.db.rollback()
            return None
    
    def create_assessment_content(self, 
                               lesson_id: str,
                               title: str,
                               description: str,
                               questions: List[Dict[str, Any]],
                               passing_score: int,
                               time_limit: int,
                               attempts_allowed: int,
                               is_final: bool = False,
                               order: int = 0,
                               estimated_time: int = 0,
                               metadata: Optional[Dict[str, Any]] = None) -> Optional[AssessmentContent]:
        """
        Create assessment content.
        
        Args:
            lesson_id: The ID of the lesson
            title: The title of the content
            description: The description of the content
            questions: List of questions
            passing_score: The passing score percentage
            time_limit: The time limit in minutes
            attempts_allowed: The number of attempts allowed
            is_final: Whether this is a final assessment
            order: The order of the content within the lesson
            estimated_time: The estimated time to complete in minutes
            metadata: Additional metadata
            
        Returns:
            The created assessment content if successful, None otherwise
        """
        try:
            lesson_uuid = uuid.UUID(lesson_id)
            
            # Create content data
            content_data = {
                "questions": questions,
                "passing_score": passing_score,
                "time_limit": time_limit,
                "attempts_allowed": attempts_allowed,
                "is_final": is_final
            }
            
            # Create the content
            db_content = self.content_repo.create(
                lesson_id=lesson_uuid,
                title=title,
                content_type="assessment",
                order=order,
                description=description,
                content_data=content_data,
                estimated_time=estimated_time,
                metadata=metadata or {}
            )
            
            if not db_content:
                return None
                
            return self._convert_db_content_to_ui_content(db_content)
        except Exception as e:
            logger.error(f"Error creating assessment content: {str(e)}")
            self.db.rollback()
            return None
    
    def create_interactive_content(self, 
                                lesson_id: str,
                                title: str,
                                description: str,
                                interaction_type: str,
                                interaction_data: Dict[str, Any],
                                instructions: Optional[str] = None,
                                order: int = 0,
                                estimated_time: int = 0,
                                metadata: Optional[Dict[str, Any]] = None) -> Optional[InteractiveContent]:
        """
        Create interactive content.
        
        Args:
            lesson_id: The ID of the lesson
            title: The title of the content
            description: The description of the content
            interaction_type: The type of interaction
            interaction_data: The interaction data
            instructions: Optional instructions for the interactive content
            order: The order of the content within the lesson
            estimated_time: The estimated time to complete in minutes
            metadata: Additional metadata
            
        Returns:
            The created interactive content if successful, None otherwise
        """
        try:
            lesson_uuid = uuid.UUID(lesson_id)
            
            # Create content data
            content_data = {
                "interaction_type": interaction_type,
                "interaction_data": interaction_data,
                "instructions": instructions
            }
            
            # Create the content
            db_content = self.content_repo.create(
                lesson_id=lesson_uuid,
                title=title,
                content_type="interactive",
                order=order,
                description=description,
                content_data=content_data,
                estimated_time=estimated_time,
                metadata=metadata or {}
            )
            
            if not db_content:
                return None
                
            return self._convert_db_content_to_ui_content(db_content)
        except Exception as e:
            logger.error(f"Error creating interactive content: {str(e)}")
            self.db.rollback()
            return None
    
    def create_resource_content(self, 
                             lesson_id: str,
                             title: str,
                             description: str,
                             resource_type: str,
                             resource_url: str,
                             is_required: bool = False,
                             created_by: Optional[str] = None,
                             resource_metadata: Optional[Dict[str, Any]] = None,
                             order: int = 0,
                             estimated_time: int = 0,
                             metadata: Optional[Dict[str, Any]] = None) -> Optional[ResourceContent]:
        """
        Create resource content.
        
        Args:
            lesson_id: The ID of the lesson
            title: The title of the content
            description: The description of the content
            resource_type: The type of resource (pdf, video, link, etc.)
            resource_url: The URL to the resource
            is_required: Whether the resource is required
            created_by: Optional creator of the resource
            resource_metadata: Optional metadata specific to the resource
            order: The order of the content within the lesson
            estimated_time: The estimated time to complete in minutes
            metadata: Additional metadata
            
        Returns:
            The created resource content if successful, None otherwise
        """
        try:
            lesson_uuid = uuid.UUID(lesson_id)
            
            # Create content data
            content_data = {
                "resource_type": resource_type,
                "resource_url": resource_url,
                "description": description,
                "is_required": is_required,
                "created_by": created_by,
                "resource_metadata": resource_metadata or {}
            }
            
            # Create the content
            db_content = self.content_repo.create(
                lesson_id=lesson_uuid,
                title=title,
                content_type="resource",
                order=order,
                description=description,
                content_data=content_data,
                estimated_time=estimated_time,
                metadata=metadata or {}
            )
            
            if not db_content:
                return None
                
            return self._convert_db_content_to_ui_content(db_content)
        except Exception as e:
            logger.error(f"Error creating resource content: {str(e)}")
            self.db.rollback()
            return None
    
    def update_content(self, 
                     content_id: str, 
                     updates: Dict[str, Any]) -> Optional[Content]:
        """
        Update content.
        
        Args:
            content_id: The ID of the content
            updates: The updates to apply
            
        Returns:
            The updated content if successful, None otherwise
        """
        try:
            content_uuid = uuid.UUID(content_id)
            
            # Get the content
            db_content = self.content_repo.get_by_id(content_uuid)
            if not db_content:
                logger.warning(f"Content not found: {content_id}")
                return None
            
            # Update the content
            for key, value in updates.items():
                if hasattr(db_content, key):
                    setattr(db_content, key, value)
            
            # Save the updates
            updated_content = self.content_repo.update(db_content)
            
            if not updated_content:
                return None
                
            return self._convert_db_content_to_ui_content(updated_content)
        except Exception as e:
            logger.error(f"Error updating content: {str(e)}")
            self.db.rollback()
            return None
    
    def update_content_data(self, 
                         content_id: str, 
                         content_data_updates: Dict[str, Any]) -> Optional[Content]:
        """
        Update content data.
        
        Args:
            content_id: The ID of the content
            content_data_updates: The updates to apply to the content data
            
        Returns:
            The updated content if successful, None otherwise
        """
        try:
            content_uuid = uuid.UUID(content_id)
            
            # Get the content
            db_content = self.content_repo.get_by_id(content_uuid)
            if not db_content:
                logger.warning(f"Content not found: {content_id}")
                return None
            
            # Update the content data
            content_data = db_content.content_data or {}
            for key, value in content_data_updates.items():
                content_data[key] = value
            
            # Save the updates
            db_content.content_data = content_data
            updated_content = self.content_repo.update(db_content)
            
            if not updated_content:
                return None
                
            return self._convert_db_content_to_ui_content(updated_content)
        except Exception as e:
            logger.error(f"Error updating content data: {str(e)}")
            self.db.rollback()
            return None
    
    def delete_content(self, content_id: str) -> bool:
        """
        Delete content.
        
        Args:
            content_id: The ID of the content
            
        Returns:
            True if successful, False otherwise
        """
        try:
            content_uuid = uuid.UUID(content_id)
            
            # Delete the content
            return self.content_repo.delete(content_uuid)
        except Exception as e:
            logger.error(f"Error deleting content: {str(e)}")
            self.db.rollback()
            return False
    
    # Lesson Methods
    
    def get_lesson_by_id(self, lesson_id: str) -> Optional[Lesson]:
        """
        Get lesson by ID.
        
        Args:
            lesson_id: The ID of the lesson
            
        Returns:
            The lesson if found, None otherwise
        """
        try:
            lesson_uuid = uuid.UUID(lesson_id)
            
            # Get the lesson from the repository
            db_lesson = self.lesson_repo.get_by_id(lesson_uuid)
            
            if not db_lesson:
                return None
                
            return self._convert_db_lesson_to_ui_lesson(db_lesson)
        except Exception as e:
            logger.error(f"Error getting lesson by ID: {str(e)}")
            return None
    
    def get_course_lessons(self, course_id: str) -> List[Lesson]:
        """
        Get all lessons for a course.
        
        Args:
            course_id: The ID of the course
            
        Returns:
            A list of lessons
        """
        try:
            course_uuid = uuid.UUID(course_id)
            
            # Get all lessons for the course
            db_lessons = self.lesson_repo.get_by_course_id(course_uuid)
            
            # Convert to UI models
            return [self._convert_db_lesson_to_ui_lesson(lesson) for lesson in db_lessons]
        except Exception as e:
            logger.error(f"Error getting course lessons: {str(e)}")
            return []
    
    # Course Methods
    
    def get_course_by_id(self, course_id: str) -> Optional[Course]:
        """
        Get course by ID.
        
        Args:
            course_id: The ID of the course
            
        Returns:
            The course if found, None otherwise
        """
        try:
            course_uuid = uuid.UUID(course_id)
            
            # Get the course from the repository
            db_course = self.course_repo.get_by_id(course_uuid)
            
            if not db_course:
                return None
                
            return self._convert_db_course_to_ui_course(db_course)
        except Exception as e:
            logger.error(f"Error getting course by ID: {str(e)}")
            return None
    
    def get_all_courses(self, include_inactive: bool = False) -> List[Course]:
        """
        Get all courses.
        
        Args:
            include_inactive: Whether to include inactive courses
            
        Returns:
            A list of courses
        """
        try:
            # Get all courses
            if include_inactive:
                db_courses = self.course_repo.get_all()
            else:
                db_courses = self.course_repo.get_active_courses()
            
            # Convert to UI models
            return [self._convert_db_course_to_ui_course(course) for course in db_courses]
        except Exception as e:
            logger.error(f"Error getting all courses: {str(e)}")
            return []
    
    # Content State Methods
    
    def get_content_state(self, 
                       user_id: str, 
                       content_id: str, 
                       state_type: str) -> Optional[Dict[str, Any]]:
        """
        Get content state.
        
        Args:
            user_id: The ID of the user
            content_id: The ID of the content
            state_type: The type of state
            
        Returns:
            The content state value if found, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            content_uuid = uuid.UUID(content_id)
            
            # Get the content state
            content_state = self.content_state_repo.get_content_state(
                user_id=user_uuid,
                content_id=content_uuid,
                state_type=state_type
            )
            
            if not content_state:
                return None
            
            # Return the appropriate value based on state type
            if content_state.json_value is not None:
                return content_state.json_value
            elif content_state.numeric_value is not None:
                return {"value": content_state.numeric_value}
            elif content_state.text_value is not None:
                return {"value": content_state.text_value}
            else:
                return {}
        except Exception as e:
            logger.error(f"Error getting content state: {str(e)}")
            return None
    
    def update_content_state(self, 
                          user_id: str, 
                          content_id: str, 
                          state_type: str, 
                          value: Union[Dict[str, Any], str, int, float]) -> bool:
        """
        Update content state.
        
        Args:
            user_id: The ID of the user
            content_id: The ID of the content
            state_type: The type of state
            value: The value to set
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            content_uuid = uuid.UUID(content_id)
            
            # Get the content
            content = self.content_repo.get_by_id(content_uuid)
            if not content:
                logger.warning(f"Content not found: {content_id}")
                return False
            
            # Get the user's progress for this content's lesson
            progress = self.progress_repo.get_user_course_progress(
                user_uuid, 
                content.lesson.course_id
            )
            if not progress:
                logger.warning(f"Progress not found for user {user_id} in course {content.lesson.course_id}")
                return False
            
            # Update or create the content state
            if isinstance(value, dict):
                result = self.content_state_repo.update_or_create_state(
                    user_id=user_uuid,
                    progress_id=progress.id,
                    content_id=content_uuid,
                    state_type=state_type,
                    json_value=value
                )
            elif isinstance(value, (int, float)):
                result = self.content_state_repo.update_or_create_state(
                    user_id=user_uuid,
                    progress_id=progress.id,
                    content_id=content_uuid,
                    state_type=state_type,
                    numeric_value=value
                )
            else:
                result = self.content_state_repo.update_or_create_state(
                    user_id=user_uuid,
                    progress_id=progress.id,
                    content_id=content_uuid,
                    state_type=state_type,
                    text_value=str(value)
                )
            
            return result is not None
        except Exception as e:
            logger.error(f"Error updating content state: {str(e)}")
            self.db.rollback()
            return False
    
    # Conversion Methods
    
    def _convert_db_content_to_ui_content(self, db_content: DBContent) -> Content:
        """
        Convert a database content to a UI content.
        
        Args:
            db_content: The database content
            
        Returns:
            The corresponding UI content
        """
        # Base content attributes
        base_attrs = {
            "id": str(db_content.id),
            "title": db_content.title,
            "content_type": db_content.content_type,
            "order": db_content.order,
            "lesson_id": str(db_content.lesson_id),
            "description": db_content.description,
            "estimated_time": db_content.estimated_time,
            "created_at": db_content.created_at,
            "updated_at": db_content.updated_at,
            "metadata": db_content.metadata or {}
        }
        
        content_data = db_content.content_data or {}
        
        # Create the appropriate content type
        if db_content.content_type == "theory":
            return TheoryContent(
                **base_attrs,
                text_content=content_data.get("text_content", ""),
                images=content_data.get("images", []),
                examples=content_data.get("examples", []),
                references=content_data.get("references", [])
            )
        elif db_content.content_type == "exercise":
            return ExerciseContent(
                **base_attrs,
                problem_statement=content_data.get("problem_statement", ""),
                solution=content_data.get("solution", ""),
                difficulty=content_data.get("difficulty", "medium"),
                hints=content_data.get("hints", [])
            )
        elif db_content.content_type == "quiz":
            return QuizContent(
                **base_attrs,
                questions=content_data.get("questions", []),
                passing_score=content_data.get("passing_score", 70)
            )
        elif db_content.content_type == "assessment":
            return AssessmentContent(
                **base_attrs,
                questions=content_data.get("questions", []),
                passing_score=content_data.get("passing_score", 70),
                time_limit=content_data.get("time_limit", 0),
                attempts_allowed=content_data.get("attempts_allowed", 1),
                is_final=content_data.get("is_final", False)
            )
        elif db_content.content_type == "interactive":
            return InteractiveContent(
                **base_attrs,
                interaction_type=content_data.get("interaction_type", ""),
                interaction_data=content_data.get("interaction_data", {}),
                instructions=content_data.get("instructions")
            )
        elif db_content.content_type == "resource":
            return ResourceContent(
                **base_attrs,
                resource_type=content_data.get("resource_type", ""),
                resource_url=content_data.get("resource_url", ""),
                is_required=content_data.get("is_required", False),
                created_by=content_data.get("created_by"),
                resource_metadata=content_data.get("resource_metadata", {})
            )
        else:
            # Generic content
            return Content(**base_attrs)
    
    def _convert_db_lesson_to_ui_lesson(self, db_lesson: DBLesson) -> Lesson:
        """
        Convert a database lesson to a UI lesson.
        
        Args:
            db_lesson: The database lesson
            
        Returns:
            The corresponding UI lesson
        """
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
            learning_objectives=db_lesson.learning_objectives,
            course_id=str(db_lesson.course_id),
            topic=db_lesson.topic,
            skills_taught=db_lesson.skills_taught,
            metadata=db_lesson.metadata,
            created_at=db_lesson.created_at,
            updated_at=db_lesson.updated_at
        )
    
    def _convert_db_course_to_ui_course(self, db_course: DBCourse) -> Course:
        """
        Convert a database course to a UI course.
        
        Args:
            db_course: The database course
            
        Returns:
            The corresponding UI course
        """
        return Course(
            id=str(db_course.id),
            topic=db_course.topic,
            name=db_course.name,
            description=db_course.description,
            created_at=db_course.created_at,
            tags=db_course.tags,
            metadata=db_course.metadata,
            is_active=db_course.is_active,
            is_completed=False
        ) 