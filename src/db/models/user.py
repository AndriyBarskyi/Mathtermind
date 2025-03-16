from datetime import datetime, timezone
import uuid

from sqlalchemy import Index, String, Text, Integer, Enum, TIMESTAMP, ForeignKey, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .achievement import UserAchievement
from .goals import LearningGoal, PersonalBest
from .progress import Progress, UserContentProgress
from .tools import UserToolUsage
from .base import Base
from .enums import AgeGroup

class User(Base):
    """User model representing a student in the learning platform."""
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    age_group: Mapped[AgeGroup] = mapped_column(
        Enum(AgeGroup), nullable=False
    )
    points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    experience_level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    total_study_time: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # in minutes
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships defined in their respective models
    settings: Mapped[list["Setting"]] = relationship(
        "Setting", back_populates="user", cascade="all, delete-orphan"
    )
    progress: Mapped[list["Progress"]] = relationship(
        "Progress", back_populates="user", cascade="all, delete-orphan"
    )
    achievements: Mapped[list["UserAchievement"]] = relationship(
        "UserAchievement", back_populates="user", cascade="all, delete-orphan"
    )
    notifications: Mapped[list["Notification"]] = relationship(
        "Notification", back_populates="user", cascade="all, delete-orphan"
    )
    content_progress: Mapped[list["UserContentProgress"]] = relationship(
        "UserContentProgress", back_populates="user", cascade="all, delete-orphan"
    )
    tool_usages: Mapped[list["UserToolUsage"]] = relationship(
        "UserToolUsage", back_populates="user", cascade="all, delete-orphan"
    )
    personal_bests: Mapped[list["PersonalBest"]] = relationship(
        "PersonalBest", back_populates="user", cascade="all, delete-orphan"
    )
    learning_goals: Mapped[list["LearningGoal"]] = relationship(
        "LearningGoal", back_populates="user", cascade="all, delete-orphan"
    )

    # Indexes
    __table_args__ = (
        Index('idx_user_username', 'username'),
        Index('idx_user_email', 'email'),
    )


class Setting(Base):
    """User preferences and settings."""
    __tablename__ = "settings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    # JSON Structure for preferences:
    # {
    #     "theme": "light" | "dark",
    #     "notifications": {
    #         "daily_reminder": bool,
    #         "achievement_alerts": bool,
    #         "study_time": str (HH:MM)
    #     },
    #     "accessibility": {
    #         "font_size": "small" | "medium" | "large",
    #         "high_contrast": bool
    #     },
    #     "study_preferences": {
    #         "daily_goal_minutes": int,
    #         "preferred_subject": "Math" | "Informatics"
    #     }
    # }
    preferences: Mapped[dict] = mapped_column(JSON, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="settings")
    
    # Indexes
    __table_args__ = (
        Index('idx_setting_user_id', 'user_id'),
    )


class Notification(Base):
    """User notifications for various events."""
    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    type: Mapped[str] = mapped_column(
        Enum("Achievement", "Comment", "Course", "Reminder", "System", name="notification_type_enum"),
        nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    related_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)  # Generic reference to related entity
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="notifications")
    
    # Indexes
    __table_args__ = (
        Index('idx_notification_user_id', 'user_id'),
        Index('idx_notification_type', 'type'),
        Index('idx_notification_is_read', 'is_read'),
        Index('idx_notification_created_at', 'created_at'),
    ) 