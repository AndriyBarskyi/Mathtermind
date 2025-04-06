"""
Tests for the progress service.
"""

import pytest
import uuid
from datetime import datetime
from unittest.mock import MagicMock, patch

from src.core.error_handling.exceptions import ValidationError, ResourceNotFoundError, DatabaseError
from src.models.progress import (
    Progress, 
    ContentState, 
    CompletedLesson, 
    CompletedCourse, 
    UserContentProgress
)
from src.db.models import (
    Progress as DBProgress,
    ContentState as DBContentState,
    CompletedLesson as DBCompletedLesson,
    CompletedCourse as DBCompletedCourse,
    UserContentProgress as DBUserContentProgress
)
from src.db.repositories import (
    ProgressRepository,
    ContentStateRepository,
    CompletedLessonRepository,
    CompletedCourseRepository,
    UserContentProgressRepository,
    LessonRepository,
    CourseRepository
)
from src.services.progress_service import ProgressService
from src.tests.base_test_classes import BaseServiceTest


class TestProgressService(BaseServiceTest):
    """Tests for ProgressService"""
    
    def setUp(self):
        """Set up test case."""
        super().setUp()
        
        # Mock all repositories used by ProgressService
        self.progress_repo_mock = MagicMock(spec=ProgressRepository)
        self.content_state_repo_mock = MagicMock(spec=ContentStateRepository)
        self.completed_lesson_repo_mock = MagicMock(spec=CompletedLessonRepository)
        self.completed_course_repo_mock = MagicMock(spec=CompletedCourseRepository)
        self.user_content_progress_repo_mock = MagicMock(spec=UserContentProgressRepository)
        self.lesson_repo_mock = MagicMock(spec=LessonRepository)
        self.course_repo_mock = MagicMock(spec=CourseRepository)
        
        # Patch all repository classes to return our mocks on instantiation
        self.progress_repo_patcher = patch('src.services.progress_service.ProgressRepository')
        self.content_state_repo_patcher = patch('src.services.progress_service.ContentStateRepository')
        self.completed_lesson_repo_patcher = patch('src.services.progress_service.CompletedLessonRepository')
        self.completed_course_repo_patcher = patch('src.services.progress_service.CompletedCourseRepository')
        self.user_content_progress_repo_patcher = patch('src.services.progress_service.UserContentProgressRepository')
        self.lesson_repo_patcher = patch('src.services.progress_service.LessonRepository')
        self.course_repo_patcher = patch('src.services.progress_service.CourseRepository')
        
        # Start all patches
        self.progress_repo_class_mock = self.progress_repo_patcher.start()
        self.content_state_repo_class_mock = self.content_state_repo_patcher.start()
        self.completed_lesson_repo_class_mock = self.completed_lesson_repo_patcher.start()
        self.completed_course_repo_class_mock = self.completed_course_repo_patcher.start()
        self.user_content_progress_repo_class_mock = self.user_content_progress_repo_patcher.start()
        self.lesson_repo_class_mock = self.lesson_repo_patcher.start()
        self.course_repo_class_mock = self.course_repo_patcher.start()
        
        # Set the mock returns
        self.progress_repo_class_mock.return_value = self.progress_repo_mock
        self.content_state_repo_class_mock.return_value = self.content_state_repo_mock
        self.completed_lesson_repo_class_mock.return_value = self.completed_lesson_repo_mock
        self.completed_course_repo_class_mock.return_value = self.completed_course_repo_mock
        self.user_content_progress_repo_class_mock.return_value = self.user_content_progress_repo_mock
        self.lesson_repo_class_mock.return_value = self.lesson_repo_mock
        self.course_repo_class_mock.return_value = self.course_repo_mock
        
        # Now create the service which will use our mocked repos
        self.progress_service = ProgressService()
        
        # Assign mock repositories to the service
        self.progress_service.progress_repo = self.progress_repo_mock
        self.progress_service.content_state_repo = self.content_state_repo_mock
        self.progress_service.completed_lesson_repo = self.completed_lesson_repo_mock
        self.progress_service.completed_course_repo = self.completed_course_repo_mock
        self.progress_service.user_content_progress_repo = self.user_content_progress_repo_mock
        self.progress_service.lesson_repo = self.lesson_repo_mock
        self.progress_service.course_repo = self.course_repo_mock
        
        # Set up common test data
        self.user_id = str(uuid.uuid4())
        self.course_id = str(uuid.uuid4())
        self.lesson_id = str(uuid.uuid4())
        self.progress_id = str(uuid.uuid4())
        self.content_id = str(uuid.uuid4())
        
        # Helper method for getting a transaction context manager
        self._get_transaction_cm = lambda: MagicMock(
            __enter__=MagicMock(return_value=self.mock_db),
            __exit__=MagicMock(return_value=None)
        )
        
    def tearDown(self):
        """Clean up test case."""
        super().tearDown()
        self.progress_repo_patcher.stop()
        self.content_state_repo_patcher.stop()
        self.completed_lesson_repo_patcher.stop()
        self.completed_course_repo_patcher.stop()
        self.user_content_progress_repo_patcher.stop()
        self.lesson_repo_patcher.stop()
        self.course_repo_patcher.stop()
        
    def test_get_user_progress_success(self):
        """Test getting user progress successfully."""
        # Create mock progress records
        mock_progress1 = MagicMock(spec=DBProgress)
        mock_progress1.id = uuid.UUID(self.progress_id)
        mock_progress1.user_id = uuid.UUID(self.user_id)
        mock_progress1.course_id = uuid.UUID(self.course_id)
        
        mock_progress2 = MagicMock(spec=DBProgress)
        mock_progress2.id = uuid.uuid4()
        mock_progress2.user_id = uuid.UUID(self.user_id)
        mock_progress2.course_id = uuid.uuid4()
        
        # Mock the progress_repo.get_user_progress method
        self.progress_repo_mock.get_user_progress.return_value = [mock_progress1, mock_progress2]
        
        # Create mock UI progress instances
        mock_ui_progress1 = MagicMock(spec=Progress)
        mock_ui_progress2 = MagicMock(spec=Progress)
        
        # Mock the _convert_db_progress_to_ui_progress method
        self.progress_service._convert_db_progress_to_ui_progress = MagicMock(
            side_effect=[mock_ui_progress1, mock_ui_progress2]
        )
        
        # Call the method
        result = self.progress_service.get_user_progress(self.user_id)
        
        # Verify method calls
        self.progress_repo_mock.get_user_progress.assert_called_once_with(uuid.UUID(self.user_id))
        assert self.progress_service._convert_db_progress_to_ui_progress.call_count == 2
        assert len(result) == 2
        assert result[0] == mock_ui_progress1
        assert result[1] == mock_ui_progress2
        
    def test_get_user_progress_empty(self):
        """Test getting user progress when there are no records."""
        # Mock the progress_repo.get_user_progress method to return an empty list
        self.progress_repo_mock.get_user_progress.return_value = []
        
        # Call the method
        result = self.progress_service.get_user_progress(self.user_id)
        
        # Verify method calls
        self.progress_repo_mock.get_user_progress.assert_called_once_with(uuid.UUID(self.user_id))
        assert len(result) == 0
        
    def test_get_user_progress_exception(self):
        """Test getting user progress when an exception occurs."""
        # Mock the progress_repo.get_user_progress method to raise an exception
        self.progress_repo_mock.get_user_progress.side_effect = Exception("Database error")
        
        # Call the method
        result = self.progress_service.get_user_progress(self.user_id)
        
        # Verify method calls
        self.progress_repo_mock.get_user_progress.assert_called_once_with(uuid.UUID(self.user_id))
        assert len(result) == 0
        
    def test_get_course_progress_success(self):
        """Test getting course progress successfully."""
        # Create mock progress
        mock_progress = MagicMock(spec=DBProgress)
        mock_progress.id = uuid.UUID(self.progress_id)
        mock_progress.user_id = uuid.UUID(self.user_id)
        mock_progress.course_id = uuid.UUID(self.course_id)
        
        # Mock the progress_repo.get_course_progress method
        self.progress_repo_mock.get_course_progress.return_value = mock_progress
        
        # Create mock UI progress
        mock_ui_progress = MagicMock(spec=Progress)
        
        # Mock the _convert_db_progress_to_ui_progress method
        self.progress_service._convert_db_progress_to_ui_progress = MagicMock(return_value=mock_ui_progress)
        
        # Call the method
        result = self.progress_service.get_course_progress(self.user_id, self.course_id)
        
        # Verify method calls
        self.progress_repo_mock.get_course_progress.assert_called_once_with(
            uuid.UUID(self.user_id), uuid.UUID(self.course_id)
        )
        self.progress_service._convert_db_progress_to_ui_progress.assert_called_once_with(mock_progress)
        assert result == mock_ui_progress
        
    def test_get_course_progress_not_found(self):
        """Test getting course progress when it doesn't exist."""
        # Mock the progress_repo.get_course_progress method to return None
        self.progress_repo_mock.get_course_progress.return_value = None
        
        # Call the method
        result = self.progress_service.get_course_progress(self.user_id, self.course_id)
        
        # Verify method calls
        self.progress_repo_mock.get_course_progress.assert_called_once_with(
            uuid.UUID(self.user_id), uuid.UUID(self.course_id)
        )
        assert result is None
        
    def test_get_course_progress_exception(self):
        """Test getting course progress when an exception occurs."""
        # Mock the progress_repo.get_course_progress method to raise an exception
        self.progress_repo_mock.get_course_progress.side_effect = Exception("Database error")
        
        # Call the method
        result = self.progress_service.get_course_progress(self.user_id, self.course_id)
        
        # Verify method calls
        self.progress_repo_mock.get_course_progress.assert_called_once_with(
            uuid.UUID(self.user_id), uuid.UUID(self.course_id)
        )
        assert result is None
        
    def test_create_course_progress_success(self):
        """Test creating course progress successfully."""
        # Create mock course and lesson
        mock_course = MagicMock()
        mock_lesson = MagicMock()
        mock_lesson.id = uuid.UUID(self.lesson_id)
        
        # Create mock progress
        mock_progress = MagicMock(spec=DBProgress)
        mock_progress.id = uuid.UUID(self.progress_id)
        mock_progress.user_id = uuid.UUID(self.user_id)
        mock_progress.course_id = uuid.UUID(self.course_id)
        
        # Mock repository methods
        self.progress_repo_mock.get_course_progress.return_value = None
        self.course_repo_mock.get_by_id.return_value = mock_course
        self.lesson_repo_mock.get_lessons_by_course_id.return_value = [mock_lesson]
        self.progress_repo_mock.create_progress.return_value = mock_progress
        
        # Create mock UI progress
        mock_ui_progress = MagicMock(spec=Progress)
        
        # Mock the _convert_db_progress_to_ui_progress method
        self.progress_service._convert_db_progress_to_ui_progress = MagicMock(return_value=mock_ui_progress)
        
        # Call the method
        result = self.progress_service.create_course_progress(self.user_id, self.course_id)
        
        # Verify method calls
        self.progress_repo_mock.get_course_progress.assert_called_once_with(
            uuid.UUID(self.user_id), uuid.UUID(self.course_id)
        )
        self.course_repo_mock.get_by_id.assert_called_once_with(uuid.UUID(self.course_id))
        self.lesson_repo_mock.get_lessons_by_course_id.assert_called_once_with(uuid.UUID(self.course_id))
        self.progress_repo_mock.create_progress.assert_called_once_with(
            user_id=uuid.UUID(self.user_id),
            course_id=uuid.UUID(self.course_id),
            current_lesson_id=uuid.UUID(self.lesson_id)
        )
        self.progress_service._convert_db_progress_to_ui_progress.assert_called_once_with(mock_progress)
        assert result == mock_ui_progress
        
    def test_create_course_progress_already_exists(self):
        """Test creating course progress when it already exists."""
        # Create mock progress
        mock_progress = MagicMock(spec=DBProgress)
        mock_progress.id = uuid.UUID(self.progress_id)
        mock_progress.user_id = uuid.UUID(self.user_id)
        mock_progress.course_id = uuid.UUID(self.course_id)
        
        # Mock repository methods
        self.progress_repo_mock.get_course_progress.return_value = mock_progress
        
        # Create mock UI progress
        mock_ui_progress = MagicMock(spec=Progress)
        
        # Mock the _convert_db_progress_to_ui_progress method
        self.progress_service._convert_db_progress_to_ui_progress = MagicMock(return_value=mock_ui_progress)
        
        # Call the method
        result = self.progress_service.create_course_progress(self.user_id, self.course_id)
        
        # Verify method calls
        self.progress_repo_mock.get_course_progress.assert_called_once_with(
            uuid.UUID(self.user_id), uuid.UUID(self.course_id)
        )
        self.course_repo_mock.get_by_id.assert_not_called()
        self.progress_repo_mock.create_progress.assert_not_called()
        self.progress_service._convert_db_progress_to_ui_progress.assert_called_once_with(mock_progress)
        assert result == mock_ui_progress
        
    def test_create_course_progress_course_not_found(self):
        """Test creating course progress when the course doesn't exist."""
        # Mock repository methods
        self.progress_repo_mock.get_course_progress.return_value = None
        self.course_repo_mock.get_by_id.return_value = None
        
        # Call the method
        result = self.progress_service.create_course_progress(self.user_id, self.course_id)
        
        # Verify method calls
        self.progress_repo_mock.get_course_progress.assert_called_once_with(
            uuid.UUID(self.user_id), uuid.UUID(self.course_id)
        )
        self.course_repo_mock.get_by_id.assert_called_once_with(uuid.UUID(self.course_id))
        self.lesson_repo_mock.get_lessons_by_course_id.assert_not_called()
        self.progress_repo_mock.create_progress.assert_not_called()
        assert result is None
        
    def test_create_course_progress_exception(self):
        """Test creating course progress when an exception occurs."""
        # Mock repository methods
        self.progress_repo_mock.get_course_progress.side_effect = Exception("Database error")
        
        # Call the method
        result = self.progress_service.create_course_progress(self.user_id, self.course_id)
        
        # Verify method calls
        self.progress_repo_mock.get_course_progress.assert_called_once_with(
            uuid.UUID(self.user_id), uuid.UUID(self.course_id)
        )
        assert result is None
        
    def test_update_progress_percentage_success(self):
        """Test updating progress percentage successfully."""
        # Create mock progress
        mock_progress = MagicMock(spec=DBProgress)
        mock_progress.id = uuid.UUID(self.progress_id)
        
        # Mock repository methods
        self.progress_repo_mock.update_progress_percentage.return_value = mock_progress
        
        # Create mock UI progress
        mock_ui_progress = MagicMock(spec=Progress)
        
        # Mock the _convert_db_progress_to_ui_progress method
        self.progress_service._convert_db_progress_to_ui_progress = MagicMock(return_value=mock_ui_progress)
        
        # Call the method
        percentage = 75.5
        result = self.progress_service.update_progress_percentage(self.progress_id, percentage)
        
        # Verify method calls
        self.progress_repo_mock.update_progress_percentage.assert_called_once_with(
            progress_id=uuid.UUID(self.progress_id),
            percentage=percentage
        )
        self.progress_service._convert_db_progress_to_ui_progress.assert_called_once_with(mock_progress)
        assert result == mock_ui_progress
        
    def test_update_progress_percentage_not_found(self):
        """Test updating progress percentage when the progress is not found."""
        # Mock repository methods
        self.progress_repo_mock.update_progress_percentage.return_value = None
        
        # Call the method
        percentage = 75.5
        result = self.progress_service.update_progress_percentage(self.progress_id, percentage)
        
        # Verify method calls
        self.progress_repo_mock.update_progress_percentage.assert_called_once_with(
            progress_id=uuid.UUID(self.progress_id),
            percentage=percentage
        )
        assert result is None
        
    def test_update_progress_percentage_exception(self):
        """Test updating progress percentage when an exception occurs."""
        # Mock repository methods
        self.progress_repo_mock.update_progress_percentage.side_effect = Exception("Database error")
        
        # Call the method
        percentage = 75.5
        result = self.progress_service.update_progress_percentage(self.progress_id, percentage)
        
        # Verify method calls
        self.progress_repo_mock.update_progress_percentage.assert_called_once_with(
            progress_id=uuid.UUID(self.progress_id),
            percentage=percentage
        )
        assert result is None
        
    def test_update_current_lesson_success(self):
        """Test updating current lesson successfully."""
        # Create mock progress
        mock_progress = MagicMock(spec=DBProgress)
        mock_progress.id = uuid.UUID(self.progress_id)
        
        # Mock repository methods
        self.progress_repo_mock.update_current_lesson.return_value = mock_progress
        
        # Create mock UI progress
        mock_ui_progress = MagicMock(spec=Progress)
        
        # Mock the _convert_db_progress_to_ui_progress method
        self.progress_service._convert_db_progress_to_ui_progress = MagicMock(return_value=mock_ui_progress)
        
        # Call the method
        result = self.progress_service.update_current_lesson(self.progress_id, self.lesson_id)
        
        # Verify method calls
        self.progress_repo_mock.update_current_lesson.assert_called_once_with(
            progress_id=uuid.UUID(self.progress_id),
            lesson_id=uuid.UUID(self.lesson_id)
        )
        self.progress_service._convert_db_progress_to_ui_progress.assert_called_once_with(mock_progress)
        assert result == mock_ui_progress
        
    def test_update_current_lesson_not_found(self):
        """Test updating current lesson when the progress is not found."""
        # Mock repository methods
        self.progress_repo_mock.update_current_lesson.return_value = None
        
        # Call the method
        result = self.progress_service.update_current_lesson(self.progress_id, self.lesson_id)
        
        # Verify method calls
        self.progress_repo_mock.update_current_lesson.assert_called_once_with(
            progress_id=uuid.UUID(self.progress_id),
            lesson_id=uuid.UUID(self.lesson_id)
        )
        assert result is None
        
    def test_update_current_lesson_exception(self):
        """Test updating current lesson when an exception occurs."""
        # Mock repository methods
        self.progress_repo_mock.update_current_lesson.side_effect = Exception("Database error")
        
        # Call the method
        result = self.progress_service.update_current_lesson(self.progress_id, self.lesson_id)
        
        # Verify method calls
        self.progress_repo_mock.update_current_lesson.assert_called_once_with(
            progress_id=uuid.UUID(self.progress_id),
            lesson_id=uuid.UUID(self.lesson_id)
        )
        assert result is None
        
    def test_add_points_success(self):
        """Test adding points successfully."""
        # Create mock progress
        mock_progress = MagicMock(spec=DBProgress)
        mock_progress.id = uuid.UUID(self.progress_id)
        
        # Mock repository methods
        self.progress_repo_mock.add_points.return_value = mock_progress
        
        # Create mock UI progress
        mock_ui_progress = MagicMock(spec=Progress)
        
        # Mock the _convert_db_progress_to_ui_progress method
        self.progress_service._convert_db_progress_to_ui_progress = MagicMock(return_value=mock_ui_progress)
        
        # Call the method
        points = 50
        result = self.progress_service.add_points(self.progress_id, points)
        
        # Verify method calls
        self.progress_repo_mock.add_points.assert_called_once_with(
            progress_id=uuid.UUID(self.progress_id),
            points=points
        )
        self.progress_service._convert_db_progress_to_ui_progress.assert_called_once_with(mock_progress)
        assert result == mock_ui_progress
        
    def test_add_points_not_found(self):
        """Test adding points when the progress is not found."""
        # Mock repository methods
        self.progress_repo_mock.add_points.return_value = None
        
        # Call the method
        points = 50
        result = self.progress_service.add_points(self.progress_id, points)
        
        # Verify method calls
        self.progress_repo_mock.add_points.assert_called_once_with(
            progress_id=uuid.UUID(self.progress_id),
            points=points
        )
        assert result is None
        
    def test_add_points_exception(self):
        """Test adding points when an exception occurs."""
        # Mock repository methods
        self.progress_repo_mock.add_points.side_effect = Exception("Database error")
        
        # Call the method
        points = 50
        result = self.progress_service.add_points(self.progress_id, points)
        
        # Verify method calls
        self.progress_repo_mock.add_points.assert_called_once_with(
            progress_id=uuid.UUID(self.progress_id),
            points=points
        )
        assert result is None
        
    def test_add_time_spent_success(self):
        """Test adding time spent successfully."""
        # Create mock progress
        mock_progress = MagicMock(spec=DBProgress)
        mock_progress.id = uuid.UUID(self.progress_id)
        
        # Mock repository methods
        self.progress_repo_mock.add_time_spent.return_value = mock_progress
        
        # Create mock UI progress
        mock_ui_progress = MagicMock(spec=Progress)
        
        # Mock the _convert_db_progress_to_ui_progress method
        self.progress_service._convert_db_progress_to_ui_progress = MagicMock(return_value=mock_ui_progress)
        
        # Call the method
        minutes = 30
        result = self.progress_service.add_time_spent(self.progress_id, minutes)
        
        # Verify method calls
        self.progress_repo_mock.add_time_spent.assert_called_once_with(
            progress_id=uuid.UUID(self.progress_id),
            minutes=minutes
        )
        self.progress_service._convert_db_progress_to_ui_progress.assert_called_once_with(mock_progress)
        assert result == mock_ui_progress
        
    def test_add_time_spent_not_found(self):
        """Test adding time spent when the progress is not found."""
        # Mock repository methods
        self.progress_repo_mock.add_time_spent.return_value = None
        
        # Call the method
        minutes = 30
        result = self.progress_service.add_time_spent(self.progress_id, minutes)
        
        # Verify method calls
        self.progress_repo_mock.add_time_spent.assert_called_once_with(
            progress_id=uuid.UUID(self.progress_id),
            minutes=minutes
        )
        assert result is None
        
    def test_add_time_spent_exception(self):
        """Test adding time spent when an exception occurs."""
        # Mock repository methods
        self.progress_repo_mock.add_time_spent.side_effect = Exception("Database error")
        
        # Call the method
        minutes = 30
        result = self.progress_service.add_time_spent(self.progress_id, minutes)
        
        # Verify method calls
        self.progress_repo_mock.add_time_spent.assert_called_once_with(
            progress_id=uuid.UUID(self.progress_id),
            minutes=minutes
        )
        assert result is None
        
    def test_complete_progress_success(self):
        """Test completing progress successfully."""
        # Create mock progress
        mock_progress = MagicMock(spec=DBProgress)
        mock_progress.id = uuid.UUID(self.progress_id)
        
        # Mock repository methods
        self.progress_repo_mock.mark_as_completed.return_value = mock_progress
        
        # Call the service method
        self.progress_service.complete_progress(
            user_id=self.user_id,
            progress_id=self.progress_id
        )
        
        # Verify the repository method was called
        self.progress_repo_mock.mark_as_completed.assert_called_once_with(uuid.UUID(self.progress_id))
        
    def test_complete_progress_not_found(self):
        """Test completing progress when the progress is not found."""
        # Mock repository methods
        self.progress_repo_mock.mark_as_completed.return_value = None
        
        # Call the service method
        self.progress_service.complete_progress(
            user_id=self.user_id,
            progress_id=self.progress_id
        )
        
        # Verify the repository method was called
        self.progress_repo_mock.mark_as_completed.assert_called_once_with(uuid.UUID(self.progress_id))
        
    def test_complete_progress_exception(self):
        """Test completing progress when an exception occurs."""
        # Mock repository methods
        self.progress_repo_mock.mark_as_completed.side_effect = Exception("Database error")
        
        # Call the service method
        with self.assertRaises(Exception):
            self.progress_service.complete_progress(
                user_id=self.user_id,
                progress_id=self.progress_id
            )
        
        # Verify the repository method was called
        self.progress_repo_mock.mark_as_completed.assert_called_once_with(uuid.UUID(self.progress_id))
        
    def test_complete_lesson_success(self):
        """Test completing a lesson successfully."""
        # Create mock completed lesson
        mock_completed_lesson = MagicMock(spec=DBCompletedLesson)
        mock_completed_lesson.id = uuid.uuid4()
        mock_completed_lesson.user_id = uuid.UUID(self.user_id)
        mock_completed_lesson.lesson_id = uuid.UUID(self.lesson_id)
        mock_completed_lesson.course_id = uuid.UUID(self.course_id)
        
        # Create mock progress
        mock_progress = MagicMock(spec=DBProgress)
        mock_progress.id = uuid.UUID(self.progress_id)
        
        # Mock repository methods
        self.completed_lesson_repo_mock.is_lesson_completed.return_value = False
        self.completed_lesson_repo_mock.create_completed_lesson.return_value = mock_completed_lesson
        self.progress_repo_mock.get_course_progress.return_value = mock_progress
        self.lesson_repo_mock.get_lessons_by_course_id.return_value = [MagicMock() for _ in range(10)]
        self.completed_lesson_repo_mock.count_completed_lessons.return_value = 5
        
        # Create mock UI completed lesson
        mock_ui_completed_lesson = MagicMock(spec=CompletedLesson)
        
        # Mock the _convert_db_completed_lesson_to_ui_completed_lesson method
        self.progress_service._convert_db_completed_lesson_to_ui_completed_lesson = MagicMock(
            return_value=mock_ui_completed_lesson
        )
        
        # Call the method
        score = 95
        time_spent = 45
        result = self.progress_service.complete_lesson(
            self.user_id, self.lesson_id, self.course_id, score, time_spent
        )
        
        # Verify method calls
        self.completed_lesson_repo_mock.is_lesson_completed.assert_called_once_with(
            uuid.UUID(self.user_id), uuid.UUID(self.lesson_id)
        )
        self.completed_lesson_repo_mock.create_completed_lesson.assert_called_once_with(
            user_id=uuid.UUID(self.user_id),
            lesson_id=uuid.UUID(self.lesson_id),
            course_id=uuid.UUID(self.course_id),
            score=score,
            time_spent=time_spent
        )
        self.progress_repo_mock.get_course_progress.assert_called_once_with(
            uuid.UUID(self.user_id), uuid.UUID(self.course_id)
        )
        self.lesson_repo_mock.get_lessons_by_course_id.assert_called_once_with(uuid.UUID(self.course_id))
        self.completed_lesson_repo_mock.count_completed_lessons.assert_called_once_with(
            uuid.UUID(self.user_id), uuid.UUID(self.course_id)
        )
        # Progress percentage should be updated to 50%
        self.progress_repo_mock.update_progress_percentage.assert_called_once_with(
            mock_progress.id, 50.0
        )
        # Progress should not be marked as completed
        self.progress_repo_mock.mark_as_completed.assert_not_called()
        self.completed_course_repo_mock.create_completed_course.assert_not_called()
        
        self.progress_service._convert_db_completed_lesson_to_ui_completed_lesson.assert_called_once_with(
            mock_completed_lesson
        )
        assert result == mock_ui_completed_lesson
        
    def test_complete_lesson_already_completed(self):
        """Test completing a lesson that's already completed."""
        # Create mock completed lesson
        mock_completed_lesson = MagicMock(spec=DBCompletedLesson)
        mock_completed_lesson.id = uuid.uuid4()
        mock_completed_lesson.user_id = uuid.UUID(self.user_id)
        mock_completed_lesson.lesson_id = uuid.UUID(self.lesson_id)
        mock_completed_lesson.course_id = uuid.UUID(self.course_id)
        
        # Mock repository methods
        self.completed_lesson_repo_mock.is_lesson_completed.return_value = True
        self.completed_lesson_repo_mock.get_lesson_completion.return_value = mock_completed_lesson
        
        # Create mock UI completed lesson
        mock_ui_completed_lesson = MagicMock(spec=CompletedLesson)
        
        # Mock the _convert_db_completed_lesson_to_ui_completed_lesson method
        self.progress_service._convert_db_completed_lesson_to_ui_completed_lesson = MagicMock(
            return_value=mock_ui_completed_lesson
        )
        
        # Call the method
        result = self.progress_service.complete_lesson(
            self.user_id, self.lesson_id, self.course_id
        )
        
        # Verify method calls
        self.completed_lesson_repo_mock.is_lesson_completed.assert_called_once_with(
            uuid.UUID(self.user_id), uuid.UUID(self.lesson_id)
        )
        self.completed_lesson_repo_mock.get_lesson_completion.assert_called_once_with(
            uuid.UUID(self.user_id), uuid.UUID(self.lesson_id)
        )
        self.completed_lesson_repo_mock.create_completed_lesson.assert_not_called()
        self.progress_repo_mock.get_course_progress.assert_not_called()
        
        self.progress_service._convert_db_completed_lesson_to_ui_completed_lesson.assert_called_once_with(
            mock_completed_lesson
        )
        assert result == mock_ui_completed_lesson
        
    def test_complete_lesson_all_lessons_completed(self):
        """Test completing the last lesson in a course."""
        # Create mock completed lesson
        mock_completed_lesson = MagicMock(spec=DBCompletedLesson)
        mock_completed_lesson.id = uuid.uuid4()
        mock_completed_lesson.user_id = uuid.UUID(self.user_id)
        mock_completed_lesson.lesson_id = uuid.UUID(self.lesson_id)
        mock_completed_lesson.course_id = uuid.UUID(self.course_id)
        
        # Create mock progress
        mock_progress = MagicMock(spec=DBProgress)
        mock_progress.id = uuid.UUID(self.progress_id)
        
        # Mock repository methods
        self.completed_lesson_repo_mock.is_lesson_completed.return_value = False
        self.completed_lesson_repo_mock.create_completed_lesson.return_value = mock_completed_lesson
        self.progress_repo_mock.get_course_progress.return_value = mock_progress
        self.lesson_repo_mock.get_lessons_by_course_id.return_value = [MagicMock() for _ in range(10)]
        self.completed_lesson_repo_mock.count_completed_lessons.return_value = 10  # All lessons completed
        
        # Create mock UI completed lesson
        mock_ui_completed_lesson = MagicMock(spec=CompletedLesson)
        
        # Mock the _convert_db_completed_lesson_to_ui_completed_lesson method
        self.progress_service._convert_db_completed_lesson_to_ui_completed_lesson = MagicMock(
            return_value=mock_ui_completed_lesson
        )
        
        # Call the method
        result = self.progress_service.complete_lesson(
            self.user_id, self.lesson_id, self.course_id
        )
        
        # Verify method calls
        self.completed_lesson_repo_mock.is_lesson_completed.assert_called_once_with(
            uuid.UUID(self.user_id), uuid.UUID(self.lesson_id)
        )
        self.completed_lesson_repo_mock.create_completed_lesson.assert_called_once_with(
            user_id=uuid.UUID(self.user_id),
            lesson_id=uuid.UUID(self.lesson_id),
            course_id=uuid.UUID(self.course_id),
            score=None,
            time_spent=None
        )
        self.progress_repo_mock.get_course_progress.assert_called_once_with(
            uuid.UUID(self.user_id), uuid.UUID(self.course_id)
        )
        self.lesson_repo_mock.get_lessons_by_course_id.assert_called_once_with(uuid.UUID(self.course_id))
        self.completed_lesson_repo_mock.count_completed_lessons.assert_called_once_with(
            uuid.UUID(self.user_id), uuid.UUID(self.course_id)
        )
        # Progress percentage should be updated to 100%
        self.progress_repo_mock.update_progress_percentage.assert_called_once_with(
            mock_progress.id, 100.0
        )
        # Progress should be marked as completed
        self.progress_repo_mock.mark_as_completed.assert_called_once_with(mock_progress.id)
        # A completed course record should be created
        self.completed_course_repo_mock.create_completed_course.assert_called_once_with(
            user_id=uuid.UUID(self.user_id),
            course_id=uuid.UUID(self.course_id)
        )
        
        self.progress_service._convert_db_completed_lesson_to_ui_completed_lesson.assert_called_once_with(
            mock_completed_lesson
        )
        assert result == mock_ui_completed_lesson
        
    def test_complete_lesson_exception(self):
        """Test completing a lesson when an exception occurs."""
        # Mock repository methods
        self.completed_lesson_repo_mock.is_lesson_completed.side_effect = Exception("Database error")
        
        # Call the method
        result = self.progress_service.complete_lesson(
            self.user_id, self.lesson_id, self.course_id
        )
        
        # Verify method calls
        self.completed_lesson_repo_mock.is_lesson_completed.assert_called_once_with(
            uuid.UUID(self.user_id), uuid.UUID(self.lesson_id)
        )
        assert result is None
        
    def test_get_user_completed_lessons_success(self):
        """Test getting all completed lessons for a user successfully."""
        # Create mock completed lessons
        mock_completed_lesson1 = MagicMock(spec=DBCompletedLesson)
        mock_completed_lesson1.id = uuid.uuid4()
        mock_completed_lesson1.user_id = uuid.UUID(self.user_id)
        
        mock_completed_lesson2 = MagicMock(spec=DBCompletedLesson)
        mock_completed_lesson2.id = uuid.uuid4()
        mock_completed_lesson2.user_id = uuid.UUID(self.user_id)
        
        # Mock repository methods
        self.completed_lesson_repo_mock.get_user_completed_lessons.return_value = [
            mock_completed_lesson1, mock_completed_lesson2
        ]
        
        # Create mock UI completed lessons
        mock_ui_completed_lesson1 = MagicMock(spec=CompletedLesson)
        mock_ui_completed_lesson2 = MagicMock(spec=CompletedLesson)
        
        # Mock the _convert_db_completed_lesson_to_ui_completed_lesson method
        self.progress_service._convert_db_completed_lesson_to_ui_completed_lesson = MagicMock(
            side_effect=[mock_ui_completed_lesson1, mock_ui_completed_lesson2]
        )
        
        # Call the method
        result = self.progress_service.get_user_completed_lessons(self.user_id)
        
        # Verify method calls
        self.completed_lesson_repo_mock.get_user_completed_lessons.assert_called_once_with(
            uuid.UUID(self.user_id)
        )
        assert self.progress_service._convert_db_completed_lesson_to_ui_completed_lesson.call_count == 2
        assert len(result) == 2
        assert result[0] == mock_ui_completed_lesson1
        assert result[1] == mock_ui_completed_lesson2
        
    def test_get_user_completed_lessons_empty(self):
        """Test getting completed lessons when there are none."""
        # Mock repository methods
        self.completed_lesson_repo_mock.get_user_completed_lessons.return_value = []
        
        # Call the method
        result = self.progress_service.get_user_completed_lessons(self.user_id)
        
        # Verify method calls
        self.completed_lesson_repo_mock.get_user_completed_lessons.assert_called_once_with(
            uuid.UUID(self.user_id)
        )
        assert len(result) == 0
        
    def test_get_user_completed_lessons_exception(self):
        """Test getting completed lessons when an exception occurs."""
        # Mock repository methods
        self.completed_lesson_repo_mock.get_user_completed_lessons.side_effect = Exception("Database error")
        
        # Call the method
        result = self.progress_service.get_user_completed_lessons(self.user_id)
        
        # Verify method calls
        self.completed_lesson_repo_mock.get_user_completed_lessons.assert_called_once_with(
            uuid.UUID(self.user_id)
        )
        assert len(result) == 0 