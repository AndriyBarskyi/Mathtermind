from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Boolean,
    String,
    Text,
    Integer,
    ForeignKey,
    TIMESTAMP,
    JSON,
    Enum,
    Float,
)
from datetime import datetime, timezone
import uuid

Base = declarative_base()


# Models
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
    age_group: Mapped[str] = mapped_column(
        Enum("10-12", "13-14", "15-17", name="age_group_enum"), nullable=False
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

    settings: Mapped[list["Setting"]] = relationship(
        "Setting", back_populates="user", cascade="all, delete-orphan"
    )
    progress: Mapped[list["Progress"]] = relationship(
        "Progress", back_populates="user", cascade="all, delete-orphan"
    )
    answers: Mapped[list["UserAnswer"]] = relationship(
        "UserAnswer", back_populates="user", cascade="all, delete-orphan"
    )
    achievements: Mapped[list["UserAchievement"]] = relationship(
        "UserAchievement", back_populates="user", cascade="all, delete-orphan"
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
    # JSON Structure for completed_lessons:
    # [
    #     {
    #         "lesson_id": uuid,
    #         "completed_at": datetime,
    #         "score": float,
    #         "time_spent": int (minutes)
    #     }
    # ]
    completed_lessons: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    current_difficulty: Mapped[str] = mapped_column(
        Enum("Beginner", "Intermediate", "Advanced", name="progress_difficulty_enum"),
        nullable=False,
        default="Beginner"
    )
    progress_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_points_earned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    time_spent: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # in minutes
    # JSON Structure for strengths/weaknesses:
    # [
    #     {
    #         "topic": str,
    #         "subtopic": str,
    #         "confidence_score": float,
    #         "last_assessed": datetime
    #     }
    # ]
    strengths: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    weaknesses: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    # JSON Structure for learning_path:
    # {
    #     "current_path": [uuid, uuid, uuid],  # lesson IDs
    #     "recommended_next": [uuid, uuid],    # lesson IDs
    #     "mastery_goals": {
    #         "topic": float (percentage)
    #     }
    # }
    learning_path: Mapped[dict] = mapped_column(JSON, nullable=True)
    # JSON Structure for progress_data:
    # {
    #     "quiz_attempts": [
    #         {
    #             "quiz_id": uuid,
    #             "score": float,
    #             "date": datetime,
    #             "mistakes": [str]
    #         }
    #     ],
    #     "practice_sessions": [
    #         {
    #             "date": datetime,
    #             "duration": int,
    #             "topics_covered": [str]
    #         }
    #     ]
    # }
    progress_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    last_accessed: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="progress")
    course: Mapped["Course"] = relationship("Course", back_populates="progress")
    current_lesson: Mapped["Lesson"] = relationship("Lesson")


# id, title, description, topic, difficulty, tags, version, author, created_at, updated_at, is_installed, published_at, version_date, estimated_time
class Course(Base):
    """Course model representing a complete learning module."""
    __tablename__ = "courses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    topic: Mapped[str] = mapped_column(
        Enum("Informatics", "Math", name="topic_enum"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty_level: Mapped[str] = mapped_column(
        Enum("BEGINNER", "INTERMEDIATE", "ADVANCED", name="difficulty_level_enum"), 
        nullable=True, 
        default="BEGINNER"
    )
    target_age_group: Mapped[str] = mapped_column(String(50), nullable=True)
    estimated_time: Mapped[int] = mapped_column(Integer, nullable=True)
    points_reward: Mapped[int] = mapped_column(Integer, nullable=True)
    prerequisites: Mapped[list] = mapped_column(JSON, nullable=True)
    tags: Mapped[list] = mapped_column(JSON, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=True, default=datetime.now(timezone.utc)
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.now(timezone.utc)
    )
    lessons: Mapped[list["Lesson"]] = relationship(
        "Lesson", back_populates="course", cascade="all, delete-orphan"
    )
    progress: Mapped[list["Progress"]] = relationship(
        "Progress", back_populates="course"
    )


# id, course_id, position, title, description, content, lesson_type, created_at, updated_at, practice, test, (later: rewards, adaptive_rules), estimated_time
class Lesson(Base):
    """Individual lesson within a course."""
    __tablename__ = "lessons"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    # JSON Structure for content:
    # {
    #     "theory": {
    #         "sections": [
    #             {
    #                 "title": str,
    #                 "content": str (markdown),
    #                 "examples": [
    #                     {
    #                         "description": str,
    #                         "code": str,
    #                         "output": str
    #                     }
    #                 ]
    #             }
    #         ],
    #         "resources": [
    #             {
    #                 "type": "video" | "document" | "link",
    #                 "url": str,
    #                 "description": str
    #             }
    #         ]
    #     },
    #     "practice": {
    #         "exercises": [
    #             {
    #                 "question": str,
    #                 "type": "code" | "multiple_choice" | "open_ended",
    #                 "options": [],  # for multiple choice
    #                 "solution": str,
    #                 "hints": [str]
    #             }
    #         ]
    #     }
    # }
    content: Mapped[dict] = mapped_column(JSON, nullable=False)
    lesson_type: Mapped[str] = mapped_column(
        Enum("Theory", "Practice", "Quiz", "Challenge", name="lesson_type_enum"),
        nullable=False
    )
    difficulty_level: Mapped[str] = mapped_column(
        Enum("Beginner", "Intermediate", "Advanced", name="lesson_difficulty_enum"),
        nullable=False
    )
    lesson_order: Mapped[int] = mapped_column(Integer, nullable=False)
    estimated_time: Mapped[int] = mapped_column(Integer, nullable=False)  # in minutes
    points_reward: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    # JSON Structure for prerequisites:
    # {
    #     "required_lessons": [uuid],
    #     "required_concepts": [str]
    # }
    prerequisites: Mapped[dict] = mapped_column(JSON, nullable=True)
    # JSON Structure for adaptive_rules:
    # {
    #     "difficulty_adjustment": {
    #         "increase_if": {
    #             "consecutive_correct": int,
    #             "time_under": int (minutes)
    #         },
    #         "decrease_if": {
    #             "consecutive_wrong": int,
    #             "time_over": int (minutes)
    #         }
    #     },
    #     "reinforcement_triggers": {
    #         "wrong_attempts": int,
    #         "time_threshold": int (minutes)
    #     }
    # }
    adaptive_rules: Mapped[dict] = mapped_column(JSON, nullable=True)
    # JSON Structure for learning_objectives:
    # [
    #     {
    #         "objective": str,
    #         "assessment_criteria": [str],
    #         "minimum_score": float
    #     }
    # ]
    learning_objectives: Mapped[list] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.now(timezone.utc)
    )

    course: Mapped["Course"] = relationship("Course", back_populates="lessons")
    quizzes: Mapped[list["Quiz"]] = relationship(
        "Quiz", back_populates="lesson", cascade="all, delete-orphan"
    )


class Quiz(Base):
    """Quiz model for assessing student knowledge."""
    __tablename__ = "quizzes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    lesson_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    # JSON Structure for questions:
    # {
    #     "questions": [
    #         {
    #             "id": str,
    #             "type": "multiple_choice" | "open_ended" | "code",
    #             "question": str,
    #             "options": [],  # for multiple choice
    #             "correct_answer": str | [str],
    #             "explanation": str,
    #             "points": int,
    #             "hints": [str],
    #             "tags": [str]  # for topic identification
    #         }
    #     ],
    #     "settings": {
    #         "time_limit": int,  # in minutes
    #         "passing_score": float,
    #         "shuffle_questions": bool,
    #         "show_answers": bool
    #     }
    # }
    questions: Mapped[dict] = mapped_column(JSON, nullable=False)
    time_limit: Mapped[int] = mapped_column(Integer, nullable=True)  # in minutes
    passing_score: Mapped[float] = mapped_column(Float, default=70.0, nullable=False)
    attempts_allowed: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.now(timezone.utc)
    )

    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="quizzes")
    answers: Mapped[list["UserAnswer"]] = relationship(
        "UserAnswer", back_populates="quiz", cascade="all, delete-orphan"
    )


class UserAnswer(Base):
    """Records of user answers to quizzes."""
    __tablename__ = "user_answers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    quiz_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("quizzes.id", ondelete="CASCADE"),
        nullable=False,
    )
    # JSON Structure for answers:
    # {
    #     "answers": [
    #         {
    #             "question_id": str,
    #             "answer": str | [str],
    #             "is_correct": bool,
    #             "time_taken": int,  # in seconds
    #             "hints_used": int,
    #             "attempts": int
    #         }
    #     ],
    #     "metadata": {
    #         "start_time": datetime,
    #         "end_time": datetime,
    #         "total_time": int,  # in seconds
    #         "score": float,
    #         "passed": bool
    #     }
    # }
    answers: Mapped[dict] = mapped_column(JSON, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    attempt_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="answers")
    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="answers")


class Achievement(Base):
    """Achievements that users can unlock."""
    __tablename__ = "achievements"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    icon: Mapped[str] = mapped_column(String(255), nullable=False)
    # JSON Structure for criteria:
    # {
    #     "type": "course_completion" | "points" | "streak" | "time" | "perfect_score",
    #     "requirements": {
    #         "course_ids": [uuid],  # for course_completion
    #         "points_required": int,  # for points
    #         "days_required": int,   # for streak
    #         "time_required": int,   # for time (minutes)
    #         "quiz_ids": [uuid]      # for perfect_score
    #     },
    #     "progress_tracking": {
    #         "count_type": "cumulative" | "consecutive",
    #         "reset_period": "never" | "daily" | "weekly" | "monthly"
    #     }
    # }
    criteria: Mapped[dict] = mapped_column(JSON, nullable=False)
    points: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.now(timezone.utc)
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class UserAchievement(Base):
    """Records of achievements earned by users."""
    __tablename__ = "user_achievements"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    achievement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("achievements.id", ondelete="CASCADE"),
        nullable=False,
    )
    achieved_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User")
    achievement: Mapped["Achievement"] = relationship("Achievement")


class LearningSession(Base):
    """Records of individual learning sessions."""
    __tablename__ = "learning_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    start_time: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.now(timezone.utc)
    )
    end_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    duration: Mapped[int] = mapped_column(Integer, nullable=True)  # in minutes
    # JSON Structure for session_data:
    # {
    #     "activities": [
    #         {
    #             "type": "lesson" | "quiz" | "practice",
    #             "id": uuid,
    #             "start_time": datetime,
    #             "end_time": datetime,
    #             "completed": bool,
    #             "performance": {
    #                 "score": float,
    #                 "time_spent": int,
    #                 "mistakes": int
    #             }
    #         }
    #     ],
    #     "focus_metrics": {
    #         "breaks_taken": int,
    #         "average_response_time": float,
    #         "completion_rate": float
    #     }
    # }
    session_data: Mapped[dict] = mapped_column(JSON, nullable=False)

    user: Mapped["User"] = relationship("User")


class ErrorLog(Base):
    """Records of student mistakes for analysis."""
    __tablename__ = "error_logs"

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
        nullable=True,
    )
    quiz_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("quizzes.id", ondelete="CASCADE"),
        nullable=True,
    )
    # JSON Structure for error_data:
    # {
    #     "error_type": "concept_misunderstanding" | "calculation" | "logic" | "syntax",
    #     "topic": str,
    #     "subtopic": str,
    #     "question_context": str,
    #     "student_answer": str,
    #     "correct_answer": str,
    #     "misconception_pattern": str,
    #     "recommended_resources": [
    #         {
    #             "type": "lesson" | "exercise" | "example",
    #             "id": uuid,
    #             "description": str
    #         }
    #     ]
    # }
    error_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User")
    lesson: Mapped["Lesson"] = relationship("Lesson")
    quiz: Mapped["Quiz"] = relationship("Quiz")


class StudyStreak(Base):
    """Tracks user's learning consistency."""
    __tablename__ = "study_streaks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    current_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    longest_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_study_date: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.now(timezone.utc)
    )
    # JSON Structure for streak_data:
    # {
    #     "daily_records": [
    #         {
    #             "date": datetime,
    #             "minutes_studied": int,
    #             "topics_covered": [str],
    #             "achievements_earned": [uuid]
    #         }
    #     ],
    #     "weekly_summary": {
    #         "total_time": int,
    #         "topics_mastered": [str],
    #         "average_daily_time": float
    #     }
    # }
    streak_data: Mapped[dict] = mapped_column(JSON, nullable=False)

    user: Mapped["User"] = relationship("User")
