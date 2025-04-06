"""
Init module for repositories layer.

This module imports and initializes all repository classes.
"""

from src.db.repositories.user_repo import UserRepository
from src.db.repositories.course_repo import CourseRepository
from src.db.repositories.lesson_repo import LessonRepository
from src.db.repositories.achievement_repo import AchievementRepository
from src.db.repositories.progress_repo import ProgressRepository
from src.db.repositories.content_repo import ContentRepository
from src.db.repositories.content_state_repo import ContentStateRepository
from src.db.repositories.user_content_progress_repo import UserContentProgressRepository
from src.db.repositories.completed_course_repo import CompletedCourseRepository
from src.db.repositories.completed_lesson_repo import CompletedLessonRepository
from src.db.repositories.settings_repo import SettingsRepository
from src.db.repositories.user_answers_repo import UserAnswersRepository

# Initialize repositories
user_repo = UserRepository()
course_repo = CourseRepository()
lesson_repo = LessonRepository()
achievement_repo = AchievementRepository()
progress_repo = ProgressRepository()
content_repo = ContentRepository()
content_state_repo = ContentStateRepository()
user_content_progress_repo = UserContentProgressRepository()
completed_course_repo = CompletedCourseRepository()
completed_lesson_repo = CompletedLessonRepository()
settings_repo = SettingsRepository()
user_answers_repo = UserAnswersRepository()

__all__ = [
    'user_repo',
    'course_repo',
    'lesson_repo',
    'achievement_repo',
    'progress_repo',
    'content_repo',
    'content_state_repo',
    'user_content_progress_repo',
    'completed_course_repo',
    'completed_lesson_repo',
    'settings_repo',
    'user_answers_repo'
] 