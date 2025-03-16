"""
Test data factories for Mathtermind.

This module re-exports all factory classes from the test_factories package
for backward compatibility.
"""

from src.tests.utils.test_factories import (
    BaseFactory,
    UserFactory,
    CourseFactory,
    LessonFactory,
    ContentFactory,
    TagFactory,
    AchievementFactory,
    UserAchievementFactory,
    LearningToolFactory,
    ProgressFactory,
    UserContentProgressFactory,
    LearningGoalFactory,
    PersonalBestFactory,
    LearningSessionFactory,
    StudyStreakFactory,
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