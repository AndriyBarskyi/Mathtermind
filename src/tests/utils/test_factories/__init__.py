"""
Factory classes for generating test data for Mathtermind tests.

This package provides a set of factory classes for creating test entities
with sensible defaults, making it easier to generate test data.
"""

# Base factory
from src.tests.utils.test_factories.base import BaseFactory

# User factories
from src.tests.utils.test_factories.user import UserFactory

# Content factories
from src.tests.utils.test_factories.content import (
    CourseFactory, LessonFactory, ContentFactory
)

# Tag factories
from src.tests.utils.test_factories.tag import TagFactory

# Achievement factories
from src.tests.utils.test_factories.achievement import (
    AchievementFactory, UserAchievementFactory
)

# Learning tool factories
from src.tests.utils.test_factories.tools import LearningToolFactory

# Progress factories
from src.tests.utils.test_factories.progress import (
    ProgressFactory, UserContentProgressFactory
)

# Goal factories
from src.tests.utils.test_factories.goals import (
    LearningGoalFactory, PersonalBestFactory
)

# Tracking factories
from src.tests.utils.test_factories.tracking import (
    LearningSessionFactory, StudyStreakFactory
)

# Export all factories
__all__ = [
    'BaseFactory',
    'UserFactory',
    'CourseFactory',
    'LessonFactory',
    'ContentFactory',
    'TagFactory',
    'AchievementFactory',
    'UserAchievementFactory',
    'LearningToolFactory',
    'ProgressFactory',
    'UserContentProgressFactory',
    'LearningGoalFactory',
    'PersonalBestFactory',
    'LearningSessionFactory',
    'StudyStreakFactory',
] 