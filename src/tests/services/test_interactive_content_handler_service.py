"""
Tests for the interactive content handler service.
"""

import pytest
import uuid
import logging
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from src.models.content import InteractiveContent
from src.db.models import (
    ContentState as DBContentState,
    UserContentProgress as DBUserContentProgress,
    Content as DBContent
)
from src.db.repositories import (
    ContentStateRepository,
    ContentRepository,
    ProgressRepository,
    UserContentProgressRepository
)
from src.services.interactive_content_handler_service import (
    InteractiveContentHandlerService,
    STATE_INTERACTION_DATA,
    STATE_INTERACTION_HISTORY,
    STATE_CURRENT_STEP,
    STATE_COMPLETION_STATUS
)
from src.tests.base_test_classes import BaseServiceTest

logger = logging.getLogger(__name__)


class TestInteractiveContentHandlerService(BaseServiceTest):
    """Tests for InteractiveContentHandlerService"""
    
    def setUp(self):
        """Set up the test environment before each test."""
        # Call the parent class's setUp method first
        super().setUp()
        
        self.user_id = str(uuid.uuid4())
        self.content_id = str(uuid.uuid4())
        self.lesson_id = str(uuid.uuid4())
        self.course_id = str(uuid.uuid4())
        self.progress_id = str(uuid.uuid4())
        
        # Create mocks for repositories
        self.content_state_repo_mock = MagicMock(spec=ContentStateRepository)
        self.content_repo_mock = MagicMock(spec=ContentRepository)
        self.progress_repo_mock = MagicMock(spec=ProgressRepository)
        self.user_content_progress_repo_mock = MagicMock(spec=UserContentProgressRepository)
        
        # Create a real service with mocked repositories
        self.interactive_handler_service = InteractiveContentHandlerService()
        self.interactive_handler_service.content_state_repo = self.content_state_repo_mock
        self.interactive_handler_service.content_repo = self.content_repo_mock
        self.interactive_handler_service.progress_repo = self.progress_repo_mock
        self.interactive_handler_service.user_content_progress_repo = self.user_content_progress_repo_mock
        
        # Configure the service to use the mock DB session
        self.interactive_handler_service.db = self.mock_db
    
    def test_get_content_state_json_value(self):
        """Test getting content state with JSON value."""
        # Create mock content state
        mock_state = MagicMock(spec=DBContentState)
        mock_state.json_value = {"position": {"x": 10, "y": 20}}
        mock_state.numeric_value = None
        mock_state.text_value = None
        
        # Mock the repository call
        self.content_state_repo_mock.get_content_state.return_value = mock_state
        
        # Call the method
        result = self.interactive_handler_service.get_content_state(
            self.user_id, self.content_id, STATE_INTERACTION_DATA
        )
        
        # Verify method calls
        self.content_state_repo_mock.get_content_state.assert_called_once_with(
            self.mock_db, uuid.UUID(self.user_id), uuid.UUID(self.content_id), STATE_INTERACTION_DATA
        )
        
        # Verify result
        assert result == {"position": {"x": 10, "y": 20}}
    
    def test_get_content_state_numeric_value(self):
        """Test getting content state with numeric value."""
        # Create mock content state
        mock_state = MagicMock(spec=DBContentState)
        mock_state.json_value = None
        mock_state.numeric_value = 42.5
        mock_state.text_value = None
        
        # Mock the repository call
        self.content_state_repo_mock.get_content_state.return_value = mock_state
        
        # Call the method
        result = self.interactive_handler_service.get_content_state(
            self.user_id, self.content_id, STATE_CURRENT_STEP
        )
        
        # Verify method calls
        self.content_state_repo_mock.get_content_state.assert_called_once_with(
            self.mock_db, uuid.UUID(self.user_id), uuid.UUID(self.content_id), STATE_CURRENT_STEP
        )
        
        # Verify result
        assert result == {"value": 42.5}
    
    def test_get_content_state_not_found(self):
        """Test getting content state when it doesn't exist."""
        # Mock the repository call
        self.content_state_repo_mock.get_content_state.return_value = None
        
        # Call the method
        result = self.interactive_handler_service.get_content_state(
            self.user_id, self.content_id, STATE_INTERACTION_DATA
        )
        
        # Verify method calls
        self.content_state_repo_mock.get_content_state.assert_called_once_with(
            self.mock_db, uuid.UUID(self.user_id), uuid.UUID(self.content_id), STATE_INTERACTION_DATA
        )
        
        # Verify result
        assert result is None
    
    def test_get_content_state_exception(self):
        """Test getting content state when an exception occurs."""
        # Mock the repository call to raise an exception
        self.content_state_repo_mock.get_content_state.side_effect = Exception("Database error")
        
        # Call the method
        result = self.interactive_handler_service.get_content_state(
            self.user_id, self.content_id, STATE_INTERACTION_DATA
        )
        
        # Verify method calls
        self.content_state_repo_mock.get_content_state.assert_called_once_with(
            self.mock_db, uuid.UUID(self.user_id), uuid.UUID(self.content_id), STATE_INTERACTION_DATA
        )
        
        # Verify result
        assert result is None
    
    def test_save_content_state_success(self):
        """Test saving content state successfully."""
        # Create mock content, lesson, and progress
        mock_content = MagicMock(spec=DBContent)
        mock_content.lesson_id = self.lesson_id  # String UUID that can be converted
        
        mock_lesson = MagicMock()
        mock_lesson.course_id = uuid.UUID(self.course_id)
        
        mock_progress = MagicMock()
        mock_progress.id = uuid.UUID(self.progress_id)
        
        # Mock repository calls
        self.content_repo_mock.get_by_id.return_value = mock_content
        self.content_repo_mock.get_lesson_by_id = MagicMock(return_value=mock_lesson)
        self.progress_repo_mock.get_course_progress.return_value = mock_progress
        self.content_state_repo_mock.update_or_create_state.return_value = MagicMock()
        
        # Call the method
        state_value = {"position": {"x": 100, "y": 200}}
        result = self.interactive_handler_service.save_content_state(
            self.user_id, self.content_id, STATE_INTERACTION_DATA, state_value
        )
        
        # Verify method calls
        self.content_repo_mock.get_by_id.assert_called_once_with(
            self.mock_db, uuid.UUID(self.content_id)
        )
        self.content_repo_mock.get_lesson_by_id.assert_called_once_with(
            self.mock_db, uuid.UUID(self.lesson_id)
        )
        self.progress_repo_mock.get_course_progress.assert_called_once_with(
            self.mock_db, uuid.UUID(self.user_id), uuid.UUID(self.course_id)
        )
        self.content_state_repo_mock.update_or_create_state.assert_called_once_with(
            self.mock_db, 
            uuid.UUID(self.user_id), 
            uuid.UUID(self.progress_id), 
            uuid.UUID(self.content_id), 
            STATE_INTERACTION_DATA, 
            state_value
        )
        
        # Verify result
        assert result is True
    
    def test_save_content_state_content_not_found(self):
        """Test saving content state when content is not found."""
        # Mock repository call
        self.content_repo_mock.get_by_id.return_value = None
        
        # Call the method
        state_value = {"position": {"x": 100, "y": 200}}
        result = self.interactive_handler_service.save_content_state(
            self.user_id, self.content_id, STATE_INTERACTION_DATA, state_value
        )
        
        # Verify method calls
        self.content_repo_mock.get_by_id.assert_called_once_with(
            self.mock_db, uuid.UUID(self.content_id)
        )
        
        # Verify result
        assert result is False
    
    def test_save_content_state_lesson_not_found(self):
        """Test saving content state when lesson is not found."""
        # Create mock content
        mock_content = MagicMock(spec=DBContent)
        mock_content.lesson_id = self.lesson_id
        
        # Mock repository calls
        self.content_repo_mock.get_by_id.return_value = mock_content
        self.content_repo_mock.get_lesson_by_id = MagicMock(return_value=None)
        
        # Call the method
        state_value = {"position": {"x": 100, "y": 200}}
        result = self.interactive_handler_service.save_content_state(
            self.user_id, self.content_id, STATE_INTERACTION_DATA, state_value
        )
        
        # Verify method calls
        self.content_repo_mock.get_by_id.assert_called_once_with(
            self.mock_db, uuid.UUID(self.content_id)
        )
        self.content_repo_mock.get_lesson_by_id.assert_called_once_with(
            self.mock_db, uuid.UUID(self.lesson_id)
        )
        
        # Verify result
        assert result is False
    
    def test_save_content_state_progress_not_found(self):
        """Test saving content state when progress record is not found."""
        # Create mock content and lesson
        mock_content = MagicMock(spec=DBContent)
        mock_content.lesson_id = self.lesson_id
        
        mock_lesson = MagicMock()
        mock_lesson.course_id = uuid.UUID(self.course_id)
        
        # Mock repository calls
        self.content_repo_mock.get_by_id.return_value = mock_content
        self.content_repo_mock.get_lesson_by_id = MagicMock(return_value=mock_lesson)
        self.progress_repo_mock.get_course_progress.return_value = None
        
        # Call the method
        state_value = {"position": {"x": 100, "y": 200}}
        result = self.interactive_handler_service.save_content_state(
            self.user_id, self.content_id, STATE_INTERACTION_DATA, state_value
        )
        
        # Verify method calls
        self.content_repo_mock.get_by_id.assert_called_once_with(
            self.mock_db, uuid.UUID(self.content_id)
        )
        self.content_repo_mock.get_lesson_by_id.assert_called_once_with(
            self.mock_db, uuid.UUID(self.lesson_id)
        )
        self.progress_repo_mock.get_course_progress.assert_called_once_with(
            self.mock_db, uuid.UUID(self.user_id), uuid.UUID(self.course_id)
        )
        
        # Verify result
        assert result is False
    
    def test_save_content_state_repository_exception(self):
        """Test saving content state when repository throws exception."""
        # Create mock content, lesson, and progress
        mock_content = MagicMock(spec=DBContent)
        mock_content.lesson_id = self.lesson_id
        
        mock_lesson = MagicMock()
        mock_lesson.course_id = uuid.UUID(self.course_id)
        
        mock_progress = MagicMock()
        mock_progress.id = uuid.UUID(self.progress_id)
        
        # Mock repository calls
        self.content_repo_mock.get_by_id.return_value = mock_content
        self.content_repo_mock.get_lesson_by_id = MagicMock(return_value=mock_lesson)
        self.progress_repo_mock.get_course_progress.return_value = mock_progress
        self.content_state_repo_mock.update_or_create_state.side_effect = Exception("Database error")
        
        # Call the method
        state_value = {"position": {"x": 100, "y": 200}}
        result = self.interactive_handler_service.save_content_state(
            self.user_id, self.content_id, STATE_INTERACTION_DATA, state_value
        )
        
        # Verify method calls
        self.content_repo_mock.get_by_id.assert_called_once_with(
            self.mock_db, uuid.UUID(self.content_id)
        )
        self.content_repo_mock.get_lesson_by_id.assert_called_once_with(
            self.mock_db, uuid.UUID(self.lesson_id)
        )
        self.progress_repo_mock.get_course_progress.assert_called_once_with(
            self.mock_db, uuid.UUID(self.user_id), uuid.UUID(self.course_id)
        )
        self.content_state_repo_mock.update_or_create_state.assert_called_once()
        self.mock_db.rollback.assert_called_once()
        
        # Verify result
        assert result is False
    
    def test_save_content_state_invalid_uuid(self):
        """Test saving content state with invalid UUIDs."""
        # Call the method with invalid UUID
        state_value = {"position": {"x": 100, "y": 200}}
        result = self.interactive_handler_service.save_content_state(
            "invalid-uuid", self.content_id, STATE_INTERACTION_DATA, state_value
        )
        
        # Verify no repository methods were called
        self.content_repo_mock.get_by_id.assert_not_called()
        
        # Verify result
        assert result is False
    
    def test_get_all_states(self):
        """Test getting all content states."""
        # Create mock content states
        mock_state1 = MagicMock(spec=DBContentState)
        mock_state1.state_type = STATE_INTERACTION_DATA
        mock_state1.json_value = {"position": {"x": 10, "y": 20}}
        mock_state1.numeric_value = None
        mock_state1.text_value = None
        
        mock_state2 = MagicMock(spec=DBContentState)
        mock_state2.state_type = STATE_CURRENT_STEP
        mock_state2.json_value = None
        mock_state2.numeric_value = 3.0
        mock_state2.text_value = None
        
        # Mock repository call
        self.content_state_repo_mock.get_all_content_states.return_value = [mock_state1, mock_state2]
        
        # Call the method
        result = self.interactive_handler_service.get_all_states(
            self.user_id, self.content_id
        )
        
        # Verify method calls
        self.content_state_repo_mock.get_all_content_states.assert_called_once_with(
            self.mock_db, uuid.UUID(self.user_id), uuid.UUID(self.content_id)
        )
        
        # Verify result
        assert result == {
            STATE_INTERACTION_DATA: {"position": {"x": 10, "y": 20}},
            STATE_CURRENT_STEP: 3.0
        }
    
    def test_clear_content_state_specific(self):
        """Test clearing a specific content state."""
        # Create mock content state
        mock_state = MagicMock(spec=DBContentState)
        
        # Mock repository call
        self.content_state_repo_mock.get_content_state.return_value = mock_state
        
        # Call the method
        result = self.interactive_handler_service.clear_content_state(
            self.user_id, self.content_id, STATE_INTERACTION_DATA
        )
        
        # Verify method calls
        self.content_state_repo_mock.get_content_state.assert_called_once_with(
            self.mock_db, uuid.UUID(self.user_id), uuid.UUID(self.content_id), STATE_INTERACTION_DATA
        )
        self.mock_db.delete.assert_called_once_with(mock_state)
        self.mock_db.commit.assert_called_once()
        
        # Verify result
        assert result is True
    
    def test_clear_content_state_all(self):
        """Test clearing all content states."""
        # Create mock content states
        mock_state1 = MagicMock(spec=DBContentState)
        mock_state2 = MagicMock(spec=DBContentState)
        mock_states = [mock_state1, mock_state2]
        
        # Mock repository call
        self.content_state_repo_mock.get_all_content_states.return_value = mock_states
        
        # Call the method
        result = self.interactive_handler_service.clear_content_state(
            self.user_id, self.content_id
        )
        
        # Verify method calls
        self.content_state_repo_mock.get_all_content_states.assert_called_once_with(
            self.mock_db, uuid.UUID(self.user_id), uuid.UUID(self.content_id)
        )
        # Verify that delete was called for each state
        assert self.mock_db.delete.call_count == 2
        self.mock_db.delete.assert_any_call(mock_state1)
        self.mock_db.delete.assert_any_call(mock_state2)
        self.mock_db.commit.assert_called_once()
        
        # Verify result
        assert result is True
    
    def test_clear_content_state_exception(self):
        """Test clearing content state when an exception occurs."""
        # Mock repository call to raise an exception
        self.content_state_repo_mock.get_content_state.side_effect = Exception("Database error")
        
        # Call the method
        result = self.interactive_handler_service.clear_content_state(
            self.user_id, self.content_id, STATE_INTERACTION_DATA
        )
        
        # Verify method calls
        self.content_state_repo_mock.get_content_state.assert_called_once_with(
            self.mock_db, uuid.UUID(self.user_id), uuid.UUID(self.content_id), STATE_INTERACTION_DATA
        )
        self.mock_db.rollback.assert_called_once()
        
        # Verify result
        assert result is False
    
    def test_record_interaction_event(self):
        """Test recording an interaction event."""
        # Mock get_content_state to return existing history
        history = {"events": [{"type": "click", "data": {"x": 10, "y": 20}, "timestamp": "2023-01-01T12:00:00Z"}]}
        self.interactive_handler_service.get_content_state = MagicMock(return_value=history)
        self.interactive_handler_service.save_content_state = MagicMock(return_value=True)
        
        # Call the method
        event_data = {"x": 30, "y": 40}
        result = self.interactive_handler_service.record_interaction_event(
            self.user_id, self.content_id, "drag", event_data
        )
        
        # Verify method calls
        self.interactive_handler_service.get_content_state.assert_called_once_with(
            self.user_id, self.content_id, STATE_INTERACTION_HISTORY
        )
        
        # Verify save_content_state was called with updated history
        save_call_args = self.interactive_handler_service.save_content_state.call_args[0]
        assert save_call_args[0] == self.user_id
        assert save_call_args[1] == self.content_id
        assert save_call_args[2] == STATE_INTERACTION_HISTORY
        
        # Check that events were appended correctly
        updated_history = save_call_args[3]
        assert len(updated_history["events"]) == 2
        assert updated_history["events"][0] == {"type": "click", "data": {"x": 10, "y": 20}, "timestamp": "2023-01-01T12:00:00Z"}
        assert updated_history["events"][1]["type"] == "drag"
        assert updated_history["events"][1]["data"] == {"x": 30, "y": 40}
        
        # Verify result
        assert result is True
    
    def test_update_completion_progress_existing(self):
        """Test updating completion progress with existing state."""
        # Create mock user content progress
        mock_progress = MagicMock()
        mock_progress.id = uuid.uuid4()
        
        # Mock repository calls
        self.user_content_progress_repo_mock.get_progress.return_value = mock_progress
        self.interactive_handler_service.save_content_state = MagicMock(return_value=True)
        
        # Call the method
        result = self.interactive_handler_service.update_completion_progress(
            self.user_id, self.content_id, 75, True
        )
        
        # Verify method calls
        self.user_content_progress_repo_mock.get_progress.assert_called_once_with(
            self.mock_db, uuid.UUID(self.user_id), uuid.UUID(self.content_id)
        )
        self.user_content_progress_repo_mock.update_progress.assert_called_once()
        
        # Verify save_content_state was called with correct parameters
        self.interactive_handler_service.save_content_state.assert_called_once()
        call_args = self.interactive_handler_service.save_content_state.call_args[0]
        assert call_args[0] == self.user_id
        assert call_args[1] == self.content_id
        assert call_args[2] == STATE_COMPLETION_STATUS
        assert call_args[3]["percentage"] == 75
        assert call_args[3]["is_completed"] is True
        
        # Verify result
        assert result is True
    
    def test_update_completion_progress_no_existing(self):
        """Test updating completion progress with no existing state."""
        # Mock repository calls
        self.user_content_progress_repo_mock.get_progress.return_value = None
        self.interactive_handler_service.save_content_state = MagicMock(return_value=True)
        
        # Call the method
        result = self.interactive_handler_service.update_completion_progress(
            self.user_id, self.content_id, 30, False
        )
        
        # Verify method calls
        self.user_content_progress_repo_mock.get_progress.assert_called_once_with(
            self.mock_db, uuid.UUID(self.user_id), uuid.UUID(self.content_id)
        )
        self.user_content_progress_repo_mock.create_progress.assert_called_once()
        
        # Verify create_progress arguments
        create_args = self.user_content_progress_repo_mock.create_progress.call_args[1]
        assert create_args["user_id"] == uuid.UUID(self.user_id)
        assert create_args["content_id"] == uuid.UUID(self.content_id)
        assert create_args["status"] == "in_progress"
        assert create_args["percentage"] == 30
        
        # Verify save_content_state was called with correct parameters
        self.interactive_handler_service.save_content_state.assert_called_once()
        call_args = self.interactive_handler_service.save_content_state.call_args[0]
        assert call_args[0] == self.user_id
        assert call_args[1] == self.content_id
        assert call_args[2] == STATE_COMPLETION_STATUS
        assert call_args[3]["percentage"] == 30
        assert call_args[3]["is_completed"] is False
        
        # Verify result
        assert result is True
    
    def test_update_completion_progress_save_fails(self):
        """Test updating completion progress when save fails."""
        # Mock repository calls
        self.user_content_progress_repo_mock.get_progress.return_value = None
        self.interactive_handler_service.save_content_state = MagicMock(return_value=False)
        
        # Call the method
        result = self.interactive_handler_service.update_completion_progress(
            self.user_id, self.content_id, 30, False
        )
        
        # Verify method calls
        self.user_content_progress_repo_mock.get_progress.assert_called_once_with(
            self.mock_db, uuid.UUID(self.user_id), uuid.UUID(self.content_id)
        )
        self.user_content_progress_repo_mock.create_progress.assert_called_once()
        
        # Verify save_content_state was called with correct parameters
        self.interactive_handler_service.save_content_state.assert_called_once()
        call_args = self.interactive_handler_service.save_content_state.call_args[0]
        assert call_args[0] == self.user_id
        assert call_args[1] == self.content_id
        assert call_args[2] == STATE_COMPLETION_STATUS
        
        # Verify result
        assert result is False
    
    def test_update_completion_progress_exception(self):
        """Test updating completion progress when an exception occurs."""
        # Mock repository calls to raise an exception
        self.user_content_progress_repo_mock.get_progress.side_effect = Exception("Database error")
        
        # Call the method
        result = self.interactive_handler_service.update_completion_progress(
            self.user_id, self.content_id, 30, False
        )
        
        # Verify method calls
        self.user_content_progress_repo_mock.get_progress.assert_called_once_with(
            self.mock_db, uuid.UUID(self.user_id), uuid.UUID(self.content_id)
        )
        self.mock_db.rollback.assert_called_once()
        
        # Verify result
        assert result is False
    
    def test_get_interactive_content_success(self):
        """Test getting interactive content successfully."""
        # Create mock DB content
        mock_db_content = MagicMock(spec=DBContent)
        mock_db_content.id = uuid.UUID(self.content_id)
        mock_db_content.title = "Interactive Simulation"
        mock_db_content.content_type = "interactive"
        mock_db_content.order = 1
        mock_db_content.lesson_id = uuid.UUID(self.lesson_id)
        mock_db_content.description = "A test simulation"
        mock_db_content.estimated_time = 30
        mock_db_content.created_at = datetime.now(timezone.utc)
        mock_db_content.updated_at = datetime.now(timezone.utc)
        mock_db_content.metadata = {"difficulty": "medium"}
        mock_db_content.interactive_type = "simulation"
        mock_db_content.data = {
            "interaction_data": {"simulation_config": {"speed": 1.0}},
            "instructions": "Follow the steps"
        }
        
        # Mock repository call
        self.content_repo_mock.get_by_id.return_value = mock_db_content
        
        # Call the method
        result = self.interactive_handler_service.get_interactive_content(self.content_id)
        
        # Verify method calls
        self.content_repo_mock.get_by_id.assert_called_once_with(
            self.mock_db, uuid.UUID(self.content_id)
        )
        
        # Verify result
        assert isinstance(result, InteractiveContent)
        assert result.id == self.content_id
        assert result.title == "Interactive Simulation"
        assert result.content_type == "interactive"
        assert result.interaction_type == "simulation"
        assert result.interaction_data == {"simulation_config": {"speed": 1.0}}
        assert result.instructions == "Follow the steps"
    
    def test_validate_interactive_content_valid(self):
        """Test validating a valid interactive content."""
        # Create interactive content
        content = InteractiveContent(
            id=self.content_id,
            title="Test Simulation",
            content_type="interactive",
            order=1,
            lesson_id=self.lesson_id,
            interaction_type="simulation",
            interaction_data={"simulation_config": {"speed": 1.0}}
        )
        
        # Call the method
        errors = self.interactive_handler_service.validate_interactive_content(content)
        
        # Verify result
        assert len(errors) == 0
    
    def test_validate_interactive_content_invalid(self):
        """Test validating an invalid interactive content."""
        # Create interactive content with missing required fields for simulation_config
        content = InteractiveContent(
            id=self.content_id,
            title="Test Simulation",
            content_type="interactive",
            order=1,
            lesson_id=self.lesson_id,
            interaction_type="simulation",
            interaction_data={"other_field": "value"}  # Has data but missing simulation_config
        )
        
        # Call the method
        errors = self.interactive_handler_service.validate_interactive_content(content)
        
        # Verify result
        assert len(errors) == 1
        assert "Simulation configuration is required for simulation type" in errors
    
    def test_verify_interaction_completion_success(self):
        """Test verifying interaction completion when all criteria are met."""
        # Mock get_interactive_content
        mock_content = MagicMock(spec=InteractiveContent)
        mock_content.interaction_data = {
            "verification_criteria": {
                "required_states": {
                    "current_step": {"value": 5}
                },
                "total_steps": 5
            }
        }
        self.interactive_handler_service.get_interactive_content = MagicMock(return_value=mock_content)
        
        # Mock get_all_states
        mock_states = {
            "current_step": {"value": 5}
        }
        self.interactive_handler_service.get_all_states = MagicMock(return_value=mock_states)
        
        # Mock update_completion_progress
        self.interactive_handler_service.update_completion_progress = MagicMock(return_value=True)
        
        # Call the method
        is_completed, message = self.interactive_handler_service.verify_interaction_completion(
            self.user_id, self.content_id
        )
        
        # Verify method calls
        self.interactive_handler_service.get_interactive_content.assert_called_once_with(self.content_id)
        self.interactive_handler_service.get_all_states.assert_called_once_with(self.user_id, self.content_id)
        self.interactive_handler_service.update_completion_progress.assert_called_once_with(
            self.user_id, self.content_id, 100.0, True
        )
        
        # Verify result
        assert is_completed is True
        assert message == "All completion criteria met"
    
    def test_resume_interactive_content(self):
        """Test resuming interactive content."""
        # Mock get_interactive_content
        mock_content = MagicMock(spec=InteractiveContent)
        mock_content.id = self.content_id
        mock_content.title = "Test Simulation"
        mock_content.interaction_type = "simulation"
        mock_content.interaction_data = {"simulation_config": {"speed": 1.0}}
        mock_content.instructions = "Follow the steps"
        mock_content.metadata = {"difficulty": "medium"}
        self.interactive_handler_service.get_interactive_content = MagicMock(return_value=mock_content)
        
        # Mock get_all_states
        mock_states = {
            "current_step": {"value": 3},
            "interaction_data": {"position": {"x": 10, "y": 20}}
        }
        self.interactive_handler_service.get_all_states = MagicMock(return_value=mock_states)
        
        # Mock get_progress
        mock_progress = MagicMock(spec=DBUserContentProgress)
        mock_progress.status = "in_progress"
        mock_progress.percentage = 60.0
        mock_progress.score = None
        mock_progress.time_spent = 300
        mock_progress.last_interaction = datetime.now(timezone.utc)
        self.user_content_progress_repo_mock.get_progress.return_value = mock_progress
        
        # Mock record_interaction_event
        self.interactive_handler_service.record_interaction_event = MagicMock(return_value=True)
        
        # Call the method
        result = self.interactive_handler_service.resume_interactive_content(
            self.user_id, self.content_id
        )
        
        # Verify method calls
        self.interactive_handler_service.get_interactive_content.assert_called_once_with(self.content_id)
        self.interactive_handler_service.get_all_states.assert_called_once_with(self.user_id, self.content_id)
        self.user_content_progress_repo_mock.get_progress.assert_called_once_with(
            self.mock_db, uuid.UUID(self.user_id), uuid.UUID(self.content_id)
        )
        self.interactive_handler_service.record_interaction_event.assert_called_once()
        
        # Verify result
        assert result["success"] is True
        assert "content" in result
        assert result["content"]["id"] == self.content_id
        assert result["content"]["title"] == "Test Simulation"
        assert result["content"]["interaction_type"] == "simulation"
        
        assert "saved_state" in result
        assert result["saved_state"] == mock_states
        
        assert "progress" in result
        assert result["progress"]["status"] == "in_progress"
        assert result["progress"]["percentage"] == 60.0
    
    def test_get_all_states_exception(self):
        """Test getting all content states when an exception occurs."""
        # Mock the repository call to raise an exception
        self.content_state_repo_mock.get_all_content_states.side_effect = Exception("Database error")
        
        # Call the method
        result = self.interactive_handler_service.get_all_states(
            self.user_id, self.content_id
        )
        
        # Verify method calls
        self.content_state_repo_mock.get_all_content_states.assert_called_once_with(
            self.mock_db, uuid.UUID(self.user_id), uuid.UUID(self.content_id)
        )
        
        # Verify result is an empty dictionary
        assert result == {}
    
    def test_record_interaction_event_exception(self):
        """Test recording an interaction event when an exception occurs."""
        # Mock the get_content_state method to raise an exception
        with patch.object(
            self.interactive_handler_service, 'get_content_state', side_effect=Exception("Database error")
        ):
            # Call the method
            result = self.interactive_handler_service.record_interaction_event(
                self.user_id, self.content_id, "click", {"button": "submit"}
            )
            
            # Verify result
            assert result is False
    
    def test_get_interactive_content_invalid_type(self):
        """Test getting interactive content when content type is not 'interactive'."""
        # Create mock content with non-interactive type
        mock_content = MagicMock()
        mock_content.content_type = "text"  # Not interactive
        
        # Mock repository call
        self.content_repo_mock.get_by_id.return_value = mock_content
        
        # Call the method
        result = self.interactive_handler_service.get_interactive_content(self.content_id)
        
        # Verify method calls
        self.content_repo_mock.get_by_id.assert_called_once_with(
            self.mock_db, uuid.UUID(self.content_id)
        )
        
        # Verify result
        assert result is None
    
    def test_verify_interaction_completion_no_criteria(self):
        """Test verifying interaction completion when no verification criteria exist but completion status is set."""
        # Mock content and interaction data without verification criteria
        mock_content = MagicMock(spec=InteractiveContent)
        mock_content.interaction_data = {}  # No verification criteria
        
        # Mock the get_interactive_content method
        with patch.object(
            self.interactive_handler_service, 'get_interactive_content', return_value=mock_content
        ):
            # Mock get_all_states to return completion status
            with patch.object(
                self.interactive_handler_service, 'get_all_states', 
                return_value={STATE_COMPLETION_STATUS: {"is_completed": True}}
            ):
                # Call the method
                result, message = self.interactive_handler_service.verify_interaction_completion(
                    self.user_id, self.content_id
                )
                
                # Verify result
                assert result is True
                assert message == "Activity marked as completed"
    
    def test_resume_interactive_content_exception(self):
        """Test resuming interactive content when an exception occurs."""
        # Mock the get_interactive_content method to raise an exception
        with patch.object(
            self.interactive_handler_service, 'get_interactive_content', side_effect=Exception("Content error")
        ):
            # Call the method
            result = self.interactive_handler_service.resume_interactive_content(
                self.user_id, self.content_id
            )
            
            # Verify result
            assert result["success"] is False
            assert "error" in result
            assert "Content error" in result["error"]
    
    def test_get_content_state_text_value(self):
        """Test getting content state with text value."""
        # Create mock content state
        mock_state = MagicMock(spec=DBContentState)
        mock_state.json_value = None
        mock_state.numeric_value = None
        mock_state.text_value = "some text value"
        
        # Mock the repository call
        self.content_state_repo_mock.get_content_state.return_value = mock_state
        
        # Call the method
        result = self.interactive_handler_service.get_content_state(
            self.user_id, self.content_id, "text_state"
        )
        
        # Verify method calls
        self.content_state_repo_mock.get_content_state.assert_called_once_with(
            self.mock_db, uuid.UUID(self.user_id), uuid.UUID(self.content_id), "text_state"
        )
        
        # Verify result
        assert result == {"value": "some text value"}
    
    def test_verify_interaction_completion_required_events(self):
        """Test verifying interaction completion with required events criteria."""
        # Mock content and interaction data with required events criteria
        mock_content = MagicMock(spec=InteractiveContent)
        mock_content.interaction_data = {
            "verification_criteria": {
                "required_events": ["click", "submit"]
            }
        }
        
        # Mock the get_interactive_content method
        with patch.object(
            self.interactive_handler_service, 'get_interactive_content', return_value=mock_content
        ):
            # Mock get_all_states to return interaction history with one missing event
            with patch.object(
                self.interactive_handler_service, 'get_all_states', 
                return_value={
                    STATE_INTERACTION_HISTORY: {
                        "events": [
                            {"type": "click", "data": {}, "timestamp": "2023-01-01T00:00:00Z"}
                            # "submit" event is missing
                        ]
                    }
                }
            ):
                # Mock update_completion_progress to do nothing
                with patch.object(self.interactive_handler_service, 'update_completion_progress'):
                    # Call the method
                    result, message = self.interactive_handler_service.verify_interaction_completion(
                        self.user_id, self.content_id
                    )
                    
                    # Verify result
                    assert result is False
                    assert "Missing required interaction: submit" in message
    
    def test_verify_interaction_completion_custom_criteria(self):
        """Test verifying interaction completion with custom steps_completed criteria."""
        # Mock content and interaction data with custom criteria
        mock_content = MagicMock(spec=InteractiveContent)
        mock_content.interaction_data = {
            "verification_criteria": {
                "custom_criteria": "steps_completed",
                "total_steps": 3
            }
        }
        
        # Mock the get_interactive_content method
        with patch.object(
            self.interactive_handler_service, 'get_interactive_content', return_value=mock_content
        ):
            # Mock get_all_states to return current step that's less than total
            with patch.object(
                self.interactive_handler_service, 'get_all_states', 
                return_value={
                    STATE_CURRENT_STEP: {"value": 2}  # Only at step 2 of 3
                }
            ):
                # Mock update_completion_progress to do nothing
                with patch.object(self.interactive_handler_service, 'update_completion_progress'):
                    # Call the method
                    result, message = self.interactive_handler_service.verify_interaction_completion(
                        self.user_id, self.content_id
                    )
                    
                    # Verify result
                    assert result is False
                    assert "Not all steps completed: 2/3" in message
    
    def test_verify_interaction_completion_partial_criteria_met(self):
        """Test verifying interaction completion with some criteria met for percentage calculation."""
        # Mock content and interaction data with multiple criteria
        mock_content = MagicMock(spec=InteractiveContent)
        mock_content.interaction_data = {
            "verification_criteria": {
                "required_states": {"state1": "value1", "state2": "value2"},
                "required_events": ["event1", "event2"],
                "custom_criteria": "steps_completed",
                "total_steps": 3
            }
        }
        
        # Mock the get_interactive_content method
        with patch.object(
            self.interactive_handler_service, 'get_interactive_content', return_value=mock_content
        ):
            # Mock get_all_states to return some criteria met, some not
            with patch.object(
                self.interactive_handler_service, 'get_all_states', 
                return_value={
                    "state1": "value1",  # This state matches
                    # state2 is missing
                    STATE_INTERACTION_HISTORY: {
                        "events": [
                            {"type": "event1", "data": {}, "timestamp": "2023-01-01T00:00:00Z"}
                            # event2 is missing
                        ]
                    },
                    STATE_CURRENT_STEP: {"value": 2}  # Only at step 2 of 3
                }
            ):
                # Mock update_completion_progress to verify it's called with calculated percentage
                with patch.object(self.interactive_handler_service, 'update_completion_progress') as mock_update:
                    # Call the method
                    result, message = self.interactive_handler_service.verify_interaction_completion(
                        self.user_id, self.content_id
                    )
                    
                    # Verify result
                    assert result is False
                    # Verify update_completion_progress was called with a percentage value
                    mock_update.assert_called_once()
                    # Check that it was called with a percentage value that's non-zero but less than 100
                    percentage = mock_update.call_args[0][2]
                    assert 0 < percentage < 100 
    
    def test_verify_interaction_completion_required_states_missing(self):
        """Test verifying interaction completion with required states when the state is missing."""
        # Mock content and interaction data with required states criteria
        mock_content = MagicMock(spec=InteractiveContent)
        mock_content.interaction_data = {
            "verification_criteria": {
                "required_states": {"state1": "value1"}
            }
        }
        
        # Mock the get_interactive_content method
        with patch.object(
            self.interactive_handler_service, 'get_interactive_content', return_value=mock_content
        ):
            # Mock get_all_states to return empty states
            with patch.object(
                self.interactive_handler_service, 'get_all_states', 
                return_value={}  # No states available
            ):
                # Mock update_completion_progress to do nothing
                with patch.object(self.interactive_handler_service, 'update_completion_progress'):
                    # Call the method
                    result, message = self.interactive_handler_service.verify_interaction_completion(
                        self.user_id, self.content_id
                    )
                    
                    # Verify result
                    assert result is False
                    assert "Missing required state: state1" in message
    
    def test_verify_interaction_completion_no_required_events(self):
        """Test verifying interaction completion with required events but no event history."""
        # Mock content and interaction data with required events criteria
        mock_content = MagicMock(spec=InteractiveContent)
        mock_content.interaction_data = {
            "verification_criteria": {
                "required_events": ["click"]
            }
        }
        
        # Mock the get_interactive_content method
        with patch.object(
            self.interactive_handler_service, 'get_interactive_content', return_value=mock_content
        ):
            # Mock get_all_states to return no event history
            with patch.object(
                self.interactive_handler_service, 'get_all_states', 
                return_value={}  # No interaction history available
            ):
                # Mock update_completion_progress to do nothing
                with patch.object(self.interactive_handler_service, 'update_completion_progress'):
                    # Call the method
                    result, message = self.interactive_handler_service.verify_interaction_completion(
                        self.user_id, self.content_id
                    )
                    
                    # Verify result
                    assert result is False
                    assert "Missing required interaction: click" in message
    
    def test_verify_interaction_completion_all_criteria_met(self):
        """Test verifying interaction completion when all criteria are met."""
        # Mock content and interaction data with multiple criteria
        mock_content = MagicMock(spec=InteractiveContent)
        mock_content.interaction_data = {
            "verification_criteria": {
                "required_states": {"state1": "value1"},
                "required_events": ["event1"],
                "custom_criteria": "steps_completed",
                "total_steps": 3
            }
        }
        
        # Mock the get_interactive_content method
        with patch.object(
            self.interactive_handler_service, 'get_interactive_content', return_value=mock_content
        ):
            # Mock get_all_states to return all criteria met
            with patch.object(
                self.interactive_handler_service, 'get_all_states', 
                return_value={
                    "state1": "value1",  # State matches
                    STATE_INTERACTION_HISTORY: {
                        "events": [
                            {"type": "event1", "data": {}, "timestamp": "2023-01-01T00:00:00Z"}
                        ]
                    },
                    STATE_CURRENT_STEP: {"value": 3}  # At final step (3 of 3)
                }
            ):
                # Mock update_completion_progress to verify it's called with 100% completion
                with patch.object(self.interactive_handler_service, 'update_completion_progress') as mock_update:
                    # Call the method
                    result, message = self.interactive_handler_service.verify_interaction_completion(
                        self.user_id, self.content_id
                    )
                    
                    # Verify result
                    assert result is True
                    assert "All completion criteria met" in message
                    # Verify update_completion_progress was called with 100% and True for completion
                    mock_update.assert_called_once_with(self.user_id, self.content_id, 100.0, True) 