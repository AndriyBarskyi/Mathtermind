from datetime import datetime, timezone
import uuid
from typing import Optional, List

from sqlalchemy import Index, String, Text, Integer, Enum, TIMESTAMP, ForeignKey, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.progress import Progress, UserContentProgress
from src.db.models.base import Base
from src.db.models.enums import Category, DifficultyLevel, LessonType, ResourceType, Topic
from src.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

class Course(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Course model representing a complete learning module."""
    __tablename__ = "courses"

    topic: Mapped[Topic] = mapped_column(
        Enum(Topic), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Relationships
    lessons: Mapped[List["Lesson"]] = relationship(
        "Lesson", back_populates="course", cascade="all, delete-orphan"
    )
    progress: Mapped[List["Progress"]] = relationship(
        "Progress", back_populates="course"
    )
    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary="course_tags", back_populates="courses"
    )
    
    # Indexes
    __table_args__ = (
        Index('idx_course_topic', 'topic'),
        Index('idx_course_name', 'name'),
    )


class CourseTag(Base):
    """Association table for courses and tags."""
    __tablename__ = "course_tags"

    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        primary_key=True,
    )
    tag_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    )
    
    # Indexes
    __table_args__ = (
        Index('idx_course_tag_course_id', 'course_id'),
        Index('idx_course_tag_tag_id', 'tag_id'),
    )


class Lesson(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Individual lesson within a course."""
    __tablename__ = "lessons"

    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    lesson_type: Mapped[LessonType] = mapped_column(
        Enum(LessonType),
        nullable=False
    )
    difficulty_level: Mapped[DifficultyLevel] = mapped_column(
        Enum(DifficultyLevel),
        nullable=False
    )
    lesson_order: Mapped[int] = mapped_column(Integer, nullable=False)
    estimated_time: Mapped[int] = mapped_column(Integer, nullable=False)  # in minutes
    points_reward: Mapped[int] = mapped_column(Integer, default=10, nullable=False)

    # Relationships
    course: Mapped["Course"] = relationship("Course", back_populates="lessons")
    resources: Mapped[List["Resource"]] = relationship(
        "Resource", back_populates="lesson", cascade="all, delete-orphan"
    )
    contents: Mapped[List["Content"]] = relationship(
        "Content", back_populates="lesson", cascade="all, delete-orphan"
    )
    
    # Indexes
    __table_args__ = (
        Index('idx_lesson_course_id', 'course_id'),
        Index('idx_lesson_lesson_type', 'lesson_type'),
        Index('idx_lesson_difficulty_level', 'difficulty_level'),
        Index('idx_lesson_lesson_order', 'lesson_order'),
    )


class Content(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Base model for all learning content with polymorphic mapping."""
    __tablename__ = "content"

    lesson_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[str] = mapped_column(
        Enum("theory", "exercise", "assessment", "interactive", name="content_type_enum"),
        nullable=False
    )
    status: Mapped[str] = mapped_column(
        Enum("Draft", "Published", "Archived", name="content_status_enum"),
        nullable=False,
        default="Draft"
    )
    content_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Polymorphic mapping
    __mapper_args__ = {
        "polymorphic_on": content_type,
        "polymorphic_identity": "content"
    }

    # Relationships
    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="contents")
    user_progress: Mapped[List["UserContentProgress"]] = relationship(
        "UserContentProgress", back_populates="content", cascade="all, delete-orphan"
    )
    
    # Indexes
    __table_args__ = (
        Index('idx_content_lesson_id', 'lesson_id'),
        Index('idx_content_content_type', 'content_type'),
        Index('idx_content_status', 'status'),
        Index('idx_content_order', 'order'),
    )


class TheoryContent(Content):
    """Theoretical content with explanations."""
    __tablename__ = "theory_content"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("content.id", ondelete="CASCADE"), 
        primary_key=True
    )
    text_content: Mapped[str] = mapped_column(Text, nullable=False)
    examples: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    references: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "theory"
    }


class ExerciseContent(Content):
    """Practice exercises for reinforcement."""
    __tablename__ = "exercise_content"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("content.id", ondelete="CASCADE"), 
        primary_key=True
    )
    problems: Mapped[dict] = mapped_column(JSON, nullable=False)
    difficulty_level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    estimated_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # in minutes
    
    __mapper_args__ = {
        "polymorphic_identity": "exercise"
    }


class AssessmentContent(Content):
    """Formal assessments (quizzes)."""
    __tablename__ = "assessment_content"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("content.id", ondelete="CASCADE"), 
        primary_key=True
    )
    questions: Mapped[dict] = mapped_column(JSON, nullable=False)
    time_limit: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # in minutes
    passing_score: Mapped[float] = mapped_column(Float, default=70.0, nullable=False)
    attempts_allowed: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    
    __mapper_args__ = {
        "polymorphic_identity": "assessment"
    }


class InteractiveContent(Content):
    """Interactive elements like simulations."""
    __tablename__ = "interactive_content"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("content.id", ondelete="CASCADE"), 
        primary_key=True
    )
    interactive_type: Mapped[str] = mapped_column(
        Enum("simulation", "tool", "game", "visualization", name="interactive_type_enum"),
        nullable=False
    )
    configuration: Mapped[dict] = mapped_column(JSON, nullable=False)
    instructions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "interactive"
    }


class Tag(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Tags for categorizing content."""
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    category: Mapped[Category] = mapped_column(
        Enum(Category),
        nullable=False,
        default=Category.TOPIC
    )

    # Relationships
    courses: Mapped[List["Course"]] = relationship(
        "Course", secondary="course_tags", back_populates="tags"
    )
    
    # Indexes
    __table_args__ = (
        Index('idx_tag_name', 'name'),
        Index('idx_tag_category', 'category'),
    )


class Resource(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Educational resources and media files."""
    __tablename__ = "resources"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    type: Mapped[ResourceType] = mapped_column(
        Enum(ResourceType),
        nullable=False
    )
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    lesson_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=True,
    )
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    lesson: Mapped[Optional["Lesson"]] = relationship("Lesson", back_populates="resources")
    creator: Mapped[Optional["User"]] = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_resource_type', 'type'),
        Index('idx_resource_lesson_id', 'lesson_id'),
        Index('idx_resource_created_by', 'created_by'),
    )
