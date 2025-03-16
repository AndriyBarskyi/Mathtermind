# Import all models to make them available when importing from models
from .base import Base
from .mixins import TimestampMixin, UUIDPrimaryKeyMixin
from .enums import (
    AgeGroup, 
    AnswerType, 
    Category, 
    ContentType, 
    DifficultyLevel, 
    FontSize,
    InformaticsToolType, 
    InteractiveType, 
    LessonType, 
    MathToolType, 
    MetricType, 
    NotificationType,
    PreferredSubject,
    ResourceType, 
    ThemeType,
    Topic
)
from .user import User, UserSetting, UserNotification
from .content import (
    Course, 
    CourseTag, 
    Lesson, 
    Content, 
    TheoryContent, 
    ExerciseContent, 
    AssessmentContent, 
    InteractiveContent,
    Tag,
    Resource
)
from .progress import Progress, UserContentProgress, CompletedLesson
from .achievement import Achievement, UserAchievement
from .tools import LearningTool, MathTool, InformaticsTool, UserToolUsage
from .goals import LearningGoal, PersonalBest
from .tracking import LearningSession, ErrorLog, StudyStreak

# For convenience, export all models
__all__ = [
    'Base',
    'TimestampMixin',
    'UUIDPrimaryKeyMixin',
    # Models
    'User', 'UserSetting', 'UserNotification',
    'Achievement', 'UserAchievement',
    'Course', 'CourseTag', 'Lesson', 'Content', 'TheoryContent', 'ExerciseContent', 
    'AssessmentContent', 'InteractiveContent', 'Tag', 'Resource',
    'LearningGoal', 'PersonalBest',
    'Progress', 'UserContentProgress', 'CompletedLesson',
    'LearningTool', 'MathTool', 'InformaticsTool', 'UserToolUsage',
    'LearningSession', 'ErrorLog', 'StudyStreak',
    # Enums
    'AgeGroup', 'AnswerType', 'Category', 'ContentType', 'DifficultyLevel',
    'FontSize', 'InformaticsToolType', 'InteractiveType', 'LessonType',
    'MathToolType', 'MetricType', 'NotificationType', 'PreferredSubject',
    'ResourceType', 'ThemeType', 'Topic'
] 