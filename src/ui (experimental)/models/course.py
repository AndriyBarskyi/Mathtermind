from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class Course:
    """Data model representing a course"""
    id: str
    title: str
    description: str
    tags: List[str]
    updated_date: datetime
    duration_hours: float
    level: str
    subject: str
    is_active: bool = False
    is_completed: bool = False
    
    @property
    def formatted_updated_date(self) -> str:
        """Return formatted date string"""
        return self.updated_date.strftime("%d %B %Y")
    
    @property
    def formatted_duration(self) -> str:
        """Return formatted duration string"""
        return f"Тривалість: {self.duration_hours} годин" 