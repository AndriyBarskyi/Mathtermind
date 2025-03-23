from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime
from abc import ABC


@dataclass
class LearningTool(ABC):
    """Base data model representing a learning tool"""
    id: str
    name: str
    description: str
    tool_category: str  # Math, Informatics, General
    tool_type: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @property
    def formatted_created_date(self) -> str:
        """Return formatted date string"""
        if not self.created_at:
            return "N/A"
        return self.created_at.strftime("%d %B %Y")
    
    @property
    def formatted_updated_date(self) -> str:
        """Return formatted date string"""
        if not self.updated_at:
            return "N/A"
        return self.updated_at.strftime("%d %B %Y")


@dataclass
class MathTool(LearningTool):
    """Data model representing a mathematical tool"""
    math_tool_type: str  # Calculator, Graphing, Geometry, etc.
    capabilities: Dict[str, Any]
    default_config: Dict[str, Any]
    
    def __post_init__(self):
        if self.tool_category != "Math":
            self.tool_category = "Math"


@dataclass
class InformaticsTool(LearningTool):
    """Data model representing an informatics tool"""
    informatics_tool_type: str  # Code Editor, Algorithm Visualizer, etc.
    capabilities: Dict[str, Any]
    default_config: Dict[str, Any]
    
    def __post_init__(self):
        if self.tool_category != "Informatics":
            self.tool_category = "Informatics"


@dataclass
class UserToolUsage:
    """Data model representing user interaction with a tool"""
    id: str
    user_id: str
    tool_id: str
    content_id: Optional[str] = None
    start_time: datetime = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None  # in seconds
    usage_data: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.usage_data is None:
            self.usage_data = {}
        if self.start_time is None:
            self.start_time = datetime.now()
    
    @property
    def formatted_start_time(self) -> str:
        """Return formatted start time"""
        return self.start_time.strftime("%d %B %Y, %H:%M")
    
    @property
    def formatted_end_time(self) -> str:
        """Return formatted end time"""
        if not self.end_time:
            return "In progress"
        return self.end_time.strftime("%d %B %Y, %H:%M")
    
    @property
    def formatted_duration(self) -> str:
        """Return formatted duration"""
        if not self.duration:
            if not self.end_time:
                return "In progress"
            # Calculate duration if we have end_time but no explicit duration
            seconds = int((self.end_time - self.start_time).total_seconds())
            self.duration = seconds
        
        minutes = self.duration // 60
        seconds = self.duration % 60
        
        if minutes > 0:
            return f"{minutes}:{seconds:02d}"
        else:
            return f"{seconds} сек"
    
    @property
    def is_complete(self) -> bool:
        """Check if the tool usage session is complete"""
        return self.end_time is not None 