# Import all models to make them available when importing from models
from src.db.models.base import Base
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
    ContentType, 
    MathToolType, 
    MetricType, 
    NotificationType,
    PreferredSubject,
    ResourceType, 
    ThemeType,
    Topic
)
from src.db.models.user import User, UserSetting, UserNotification, UserAnswer, Setting
from src.db.models.content import (
    Course, Lesson, Content, TheoryContent, ExerciseContent, 
    AssessmentContent, InteractiveContent, ResourceContent, Tag, CourseTag
)
from src.db.models.progress import (
    Progress, UserContentProgress, CompletedLesson, 
    ContentState, CompletedCourse
)
from src.db.models.achievement import Achievement, UserAchievement
from src.db.models.tools import LearningTool, MathTool, InformaticsTool, UserToolUsage
from src.db.models.goals import LearningGoal, PersonalBest
from src.db.models.tracking import LearningSession, ErrorLog, StudyStreak

# For convenience, export all models
__all__ = [
    'Base',
    'TimestampMixin',
    'UUIDPrimaryKeyMixin',
    # Models
    'User', 'UserSetting', 'UserNotification', 'UserAnswer', 'Setting',
    'Achievement', 'UserAchievement',
    'Course', 'CourseTag', 'Lesson', 'Content', 'TheoryContent', 'ExerciseContent', 
    'AssessmentContent', 'InteractiveContent', 'ResourceContent', 'Tag',
    'LearningGoal', 'PersonalBest',
    'Progress', 'UserContentProgress', 'CompletedLesson',
    'LearningTool', 'MathTool', 'InformaticsTool', 'UserToolUsage',
    'LearningSession', 'ErrorLog', 'StudyStreak',
    # Enums
    'AgeGroup', 'AnswerType', 'Category', 'ContentType', 'DifficultyLevel',
    'FontSize', 'InformaticsToolType', 'InteractiveType', 'ContentType',
    'MathToolType', 'MetricType', 'NotificationType', 'PreferredSubject',
    'ResourceType', 'ThemeType', 'Topic'
] 