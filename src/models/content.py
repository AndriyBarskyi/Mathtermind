from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime
from abc import ABC


@dataclass
class Content(ABC):
    """Base data model representing content"""
    id: str
    title: str
    content_type: str
    order: int
    lesson_id: str
    description: Optional[str] = None
    estimated_time: int = 0  # in minutes
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
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


@dataclass
class TheoryContent(Content):
    """Data model representing theory content"""
    text_content: str
    images: List[str] = None
    examples: Dict[str, Any] = None
    references: Dict[str, Any] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.images is None:
            self.images = []
        if self.examples is None:
            self.examples = {}
        if self.references is None:
            self.references = {}


@dataclass
class ExerciseContent(Content):
    """Data model representing exercise content"""
    problem_statement: str
    solution: str
    difficulty: str
    hints: List[str] = None
    answer_type: str = "text"
    
    def __post_init__(self):
        super().__post_init__()
        if self.hints is None:
            self.hints = []


@dataclass
class QuizContent(Content):
    """Data model representing quiz content"""
    questions: List[Dict[str, Any]]
    passing_score: float = 70.0
    
    def __post_init__(self):
        super().__post_init__()
        content_type = "quiz"


@dataclass
class AssessmentContent(Content):
    """Data model representing assessment content"""
    questions: List[Dict[str, Any]]
    passing_score: float = 70.0
    time_limit: Optional[int] = None  # in minutes
    attempts_allowed: int = 3
    is_final: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        content_type = "assessment"


@dataclass
class InteractiveContent(Content):
    """Data model representing interactive content"""
    interaction_type: str
    interaction_data: Dict[str, Any]
    instructions: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        content_type = "interactive"


@dataclass
class ResourceContent(Content):
    """Data model representing resource content"""
    resource_type: str
    resource_url: str
    description: str
    is_required: bool = False
    created_by: Optional[str] = None
    resource_metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        super().__post_init__()
        content_type = "resource"
        if self.resource_metadata is None:
            self.resource_metadata = {} 