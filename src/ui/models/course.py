from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime

@dataclass
class Course:
    """Data model representing a course"""
    id: str
    topic: str  # "Informatics" or "Math"
    name: str
    description: str
    metadata: Dict[str, Any]
    created_at: datetime
    
    @property
    def formatted_created_date(self) -> str:
        """Return formatted date string"""
        return self.created_at.strftime("%d %B %Y")
    
    @property
    def formatted_duration(self) -> str:
        """Return formatted duration string"""
        estimated_time = self.metadata.get("estimated_time", 0)
        hours = estimated_time // 60
        minutes = estimated_time % 60
        
        if hours > 0 and minutes > 0:
            return f"Тривалість: {hours} год {minutes} хв"
        elif hours > 0:
            return f"Тривалість: {hours} год"
        else:
            return f"Тривалість: {minutes} хв"
    
    @property
    def difficulty_level(self) -> str:
        """Get the difficulty level from metadata"""
        return self.metadata.get("difficulty_level", "Beginner")
    
    @property
    def tags(self) -> List[str]:
        """Get tags from metadata"""
        return self.metadata.get("tags", [])
    
    @property
    def points_reward(self) -> int:
        """Get points reward from metadata"""
        return self.metadata.get("points_reward", 0)
    
    @property
    def target_age_group(self) -> str:
        """Get target age group from metadata"""
        return self.metadata.get("target_age_group", "13-14") 