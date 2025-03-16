from datetime import datetime, timezone
import uuid
from typing import Optional

from sqlalchemy import Index, String, Text, Integer, Enum, TIMESTAMP, ForeignKey, Float, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base
from src.db.models.enums import MetricType
from src.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

class LearningGoal(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """User-defined learning goals and targets."""
    __tablename__ = "learning_goals"
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    goal_type: Mapped[str] = mapped_column(
        Enum("Daily", "Weekly", "Course", "Topic", name="goal_type_enum"),
        nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    target: Mapped[int] = mapped_column(Integer, nullable=False)  # Minutes, points, or lessons depending on type
    target_unit: Mapped[str] = mapped_column(
        Enum("Minutes", "Points", "Lessons", "Exercises", name="target_unit_enum"),
        nullable=False
    )
    current_progress: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    start_date: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    end_date: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    user: Mapped["User"] = relationship("User", back_populates="learning_goals")
    
    # Indexes
    __table_args__ = (
        Index('idx_learning_goal_user_id', 'user_id'),
        Index('idx_learning_goal_goal_type', 'goal_type'),
        Index('idx_learning_goal_is_completed', 'is_completed'),
    )


class PersonalBest(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Tracks personal best performances for self-improvement."""
    __tablename__ = "personal_bests"
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    metric_type: Mapped[MetricType] = mapped_column(
        Enum(MetricType), nullable=False
    )
    value: Mapped[float] = mapped_column(Float, nullable=False)
    context_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)  # Content ID, Lesson ID, etc.
    context_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # "lesson", "content", "course", etc.
    achieved_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    previous_best: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    improvement: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Percentage or absolute improvement
    
    user: Mapped["User"] = relationship("User", back_populates="personal_bests")
    
    # Indexes
    __table_args__ = (
        Index('idx_personal_best_user_id', 'user_id'),
        Index('idx_personal_best_metric_type', 'metric_type'),
        Index('idx_personal_best_context_id', 'context_id'),
    ) 