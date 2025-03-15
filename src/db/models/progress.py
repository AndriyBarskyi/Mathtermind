from datetime import datetime, timezone
import uuid

from sqlalchemy import Index, String, Text, Integer, Enum, TIMESTAMP, ForeignKey, Float, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Progress(Base):
    """Tracks user progress in courses."""
    __tablename__ = "progress"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
    )
    current_lesson_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=True,
    )
    current_difficulty: Mapped[str] = mapped_column(
        Enum("Beginner", "Intermediate", "Advanced", name="progress_difficulty_enum"),
        nullable=False,
        default="Beginner"
    )
    progress_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_points_earned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    time_spent: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # in minutes
    progress_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    last_accessed: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="progress")
    course: Mapped["Course"] = relationship("Course", back_populates="progress")
    current_lesson: Mapped["Lesson"] = relationship("Lesson")


class UserContentProgress(Base):
    """Tracks user progress through individual content items."""
    __tablename__ = "user_content_progress"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    content_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("content.id", ondelete="CASCADE"),
        nullable=False,
    )
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=True)
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    time_spent: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # in seconds
    last_interaction: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.now(timezone.utc)
    )
    
    user: Mapped["User"] = relationship("User", back_populates="content_progress")
    content: Mapped["Content"] = relationship("Content", back_populates="user_progress")
    
    # Indexes
    __table_args__ = (
        Index('idx_user_content_progress_user_id', 'user_id'),
        Index('idx_user_content_progress_content_id', 'content_id'),
        Index('idx_user_content_progress_is_completed', 'is_completed'),
    )


class CompletedLesson(Base):
    """Normalized model for completed lessons, extracted from Progress.completed_lessons."""
    __tablename__ = "completed_lessons"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    lesson_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
    )
    completed_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.now(timezone.utc)
    )
    score: Mapped[float] = mapped_column(Float, nullable=True)
    time_spent: Mapped[int] = mapped_column(Integer, nullable=False)  # in minutes
    
    user: Mapped["User"] = relationship("User")
    lesson: Mapped["Lesson"] = relationship("Lesson")
    
    # Indexes
    __table_args__ = (
        Index('idx_completed_lesson_user_id', 'user_id'),
        Index('idx_completed_lesson_lesson_id', 'lesson_id'),
        Index('idx_completed_lesson_completed_at', 'completed_at'),
    )
