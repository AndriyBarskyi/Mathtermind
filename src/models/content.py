from dataclasses import dataclass, field
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
    metadata: Dict[str, Any] = field(default_factory=dict)
    
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
    text_content: str = ""  # Provide a default value to avoid dataclass ordering issues
    images: List[str] = field(default_factory=list)
    examples: Dict[str, Any] = field(default_factory=dict)
    references: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()
        if self.images is None:
            self.images = []
        if self.examples is None:
            self.examples = {}
        if self.references is None:
            self.references = {}
        # Ensure content type is correct
        if not self.text_content:
            raise ValueError("Text content cannot be empty for TheoryContent")


@dataclass
class ExerciseContent(Content):
    """Data model representing exercise content"""
    problem_statement: str = ""  # Provide a default value to avoid dataclass ordering issues
    solution: str = ""  # Provide a default value to avoid dataclass ordering issues
    difficulty: str = ""  # Provide a default value to avoid dataclass ordering issues
    hints: List[str] = field(default_factory=list)
    answer_type: str = "text"
    
    def __post_init__(self):
        super().__post_init__()
        if self.hints is None:
            self.hints = []
        # Ensure content type is correct
        self.content_type = "exercise"
        # Validate required fields
        if not self.problem_statement:
            raise ValueError("Problem statement cannot be empty for ExerciseContent")
        if not self.solution:
            raise ValueError("Solution cannot be empty for ExerciseContent")
        if not self.difficulty:
            raise ValueError("Difficulty cannot be empty for ExerciseContent")


@dataclass
class QuizContent(Content):
    """Data model representing quiz content"""
    questions: List[Dict[str, Any]] = field(default_factory=list)
    passing_score: float = 70.0
    
    def __post_init__(self):
        super().__post_init__()
        self.content_type = "quiz"
        # Validate required fields
        if not self.questions:
            raise ValueError("Questions cannot be empty for QuizContent")


@dataclass
class AssessmentContent(Content):
    """Data model representing assessment content"""
    questions: List[Dict[str, Any]] = field(default_factory=list)
    passing_score: float = 70.0
    time_limit: Optional[int] = None  # in minutes
    attempts_allowed: int = 3
    is_final: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.content_type = "assessment"
        # Validate required fields
        if not self.questions:
            raise ValueError("Questions cannot be empty for AssessmentContent")


@dataclass
class InteractiveContent(Content):
    """Data model representing interactive content"""
    interaction_type: str = ""  # Provide a default value to avoid dataclass ordering issues
    interaction_data: Dict[str, Any] = field(default_factory=dict)
    instructions: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.content_type = "interactive"
        # Validate required fields
        if not self.interaction_type:
            raise ValueError("Interaction type cannot be empty for InteractiveContent")
        if not self.interaction_data:
            raise ValueError("Interaction data cannot be empty for InteractiveContent")


@dataclass
class ResourceContent(Content):
    """Data model representing resource content"""
    resource_type: str = ""  # Provide a default value to avoid dataclass ordering issues
    resource_url: str = ""  # Provide a default value to avoid dataclass ordering issues
    description: str = ""  # Provide a default value to avoid dataclass ordering issues
    is_required: bool = False
    created_by: Optional[str] = None
    resource_metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()
        self.content_type = "resource"
        if self.resource_metadata is None:
            self.resource_metadata = {}
        # Validate required fields
        if not self.resource_type:
            raise ValueError("Resource type cannot be empty for ResourceContent")
        if not self.resource_url:
            raise ValueError("Resource URL cannot be empty for ResourceContent")
        if not self.description:
            raise ValueError("Description cannot be empty for ResourceContent") 