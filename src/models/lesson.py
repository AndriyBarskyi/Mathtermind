from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime


@dataclass
class Lesson:
    """
    Data model representing a lesson.
    
    Note: Lessons don't have types - they are containers for various content items.
    Content items within lessons have types, not the lessons themselves.
    """

    id: str
    title: str
    course_id: str
    lesson_order: int
    estimated_time: int  # in minutes
    points_reward: int
    difficulty_level: Optional[str] = None
    content: Dict[str, Any] = None
    prerequisites: Dict[str, Any] = None
    learning_objectives: List[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.prerequisites is None:
            self.prerequisites = {}
        if self.learning_objectives is None:
            self.learning_objectives = []
        if self.content is None:
            self.content = {}

    @property
    def formatted_duration(self) -> str:
        """Return formatted duration string"""
        hours = self.estimated_time // 60
        minutes = self.estimated_time % 60

        if hours > 0 and minutes > 0:
            return f"Тривалість: {hours} год {minutes} хв"
        elif hours > 0:
            return f"Тривалість: {hours} год"
        else:
            return f"Тривалість: {minutes} хв"

    @property
    def formatted_points(self) -> str:
        """Return formatted points string"""
        return f"Бали: {self.points_reward}"

    @property
    def formatted_created_date(self) -> str:
        """Return formatted creation date"""
        if not self.created_at:
            return "N/A"
        return self.created_at.strftime("%d %B %Y")

    @property
    def formatted_updated_date(self) -> str:
        """Return formatted update date"""
        if not self.updated_at:
            return "N/A"
        return self.updated_at.strftime("%d %B %Y")

    @property
    def lesson_number(self) -> str:
        """Return formatted lesson number"""
        return f"Урок {self.lesson_order}"

    @property
    def is_advanced(self) -> bool:
        """Check if lesson is advanced difficulty"""
        return self.difficulty_level and self.difficulty_level.lower() in ["advanced", "досвідчений"]

    @property
    def has_prerequisites(self) -> bool:
        """Check if lesson has prerequisites"""
        return bool(self.prerequisites and len(self.prerequisites) > 0)

