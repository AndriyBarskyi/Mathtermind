from dataclasses import dataclass
from typing import Dict, List, Any, Optional


@dataclass
class Lesson:
    """Data model representing a lesson"""

    id: str
    title: str
    content: Dict[str, Any]
    lesson_type: str
    difficulty_level: str
    lesson_order: int
    estimated_time: int
    points_reward: int
    prerequisites: Dict[str, Any] = None
    learning_objectives: List[str] = None

    def __post_init__(self):
        if self.prerequisites is None:
            self.prerequisites = {}
        if self.learning_objectives is None:
            self.learning_objectives = []

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

