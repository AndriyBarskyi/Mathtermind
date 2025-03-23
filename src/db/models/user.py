import uuid
from typing import Optional, List

from sqlalchemy import Index, String, Text, Integer, Enum, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.achievement import UserAchievement
from src.db.models.goals import LearningGoal, PersonalBest
from src.db.models.progress import Progress, UserContentProgress, ContentState, CompletedCourse
from src.db.models.tools import UserToolUsage
from src.db.models.base import Base
from src.db.models.enums import (
    AgeGroup,
    ThemeType,
    FontSize,
    PreferredSubject,
    NotificationType,
)
from src.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """User model representing a student in the learning platform."""

    __tablename__ = "users"

    # Basic information
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    age_group: Mapped[AgeGroup] = mapped_column(Enum(AgeGroup), nullable=False)

    # Progress tracking
    points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    experience_level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    total_study_time: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )  # in minutes

    # Relationships
    settings: Mapped[List["UserSetting"]] = relationship(
        "UserSetting", back_populates="user", cascade="all, delete-orphan"
    )
    progress: Mapped[List["Progress"]] = relationship(
        "Progress", back_populates="user", cascade="all, delete-orphan"
    )
    achievements: Mapped[List["UserAchievement"]] = relationship(
        "UserAchievement", back_populates="user", cascade="all, delete-orphan"
    )
    notifications: Mapped[List["UserNotification"]] = relationship(
        "UserNotification", back_populates="user", cascade="all, delete-orphan"
    )
    content_progress: Mapped[List["UserContentProgress"]] = relationship(
        "UserContentProgress",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    tool_usages: Mapped[List["UserToolUsage"]] = relationship(
        "UserToolUsage", back_populates="user", cascade="all, delete-orphan"
    )
    personal_bests: Mapped[List["PersonalBest"]] = relationship(
        "PersonalBest", back_populates="user", cascade="all, delete-orphan"
    )
    learning_goals: Mapped[List["LearningGoal"]] = relationship(
        "LearningGoal", back_populates="user", cascade="all, delete-orphan"
    )
    content_states: Mapped[List["ContentState"]] = relationship(
        "ContentState", back_populates="user", cascade="all, delete-orphan"
    )
    completed_courses: Mapped[List["CompletedCourse"]] = relationship(
        "CompletedCourse", back_populates="user", cascade="all, delete-orphan"
    )

    # Indexes
    __table_args__ = (
        Index("idx_user_username", "username"),
        Index("idx_user_email", "email"),
    )


class UserSetting(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """User preferences and settings."""

    __tablename__ = "user_settings"

    # Foreign key
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Theme settings
    theme: Mapped[ThemeType] = mapped_column(
        Enum(ThemeType), default=ThemeType.LIGHT, nullable=False
    )

    # Notification settings
    notification_daily_reminder: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    notification_achievement_alerts: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    notification_study_time: Mapped[str] = mapped_column(
        String(5), default="09:00", nullable=False
    )

    # Accessibility settings
    accessibility_font_size: Mapped[FontSize] = mapped_column(
        Enum(FontSize), default=FontSize.MEDIUM, nullable=False
    )
    accessibility_high_contrast: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    # Study preferences
    study_daily_goal_minutes: Mapped[int] = mapped_column(
        Integer, default=30, nullable=False
    )
    study_preferred_subject: Mapped[PreferredSubject] = mapped_column(
        Enum(PreferredSubject), default=PreferredSubject.MATH, nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="settings")

    # Indexes
    __table_args__ = (Index("idx_user_setting_user_id", "user_id"),)


class UserNotification(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """User notifications for various events."""

    __tablename__ = "user_notifications"

    # Foreign key
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Notification details
    type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    related_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )  # Generic reference to related entity

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="notifications")

    # Indexes
    __table_args__ = (
        Index("idx_user_notification_user_id", "user_id"),
        Index("idx_user_notification_type", "type"),
        Index("idx_user_notification_is_read", "is_read"),
        Index("idx_user_notification_created_at", "created_at"),
    )

