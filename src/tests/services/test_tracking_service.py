"""
Tests for the tracking service.
"""

import pytest
import uuid
from datetime import datetime
from unittest.mock import MagicMock, patch

from src.db.models import (
    LearningSession as DBLearningSession,
    ErrorLog as DBErrorLog,
    StudyStreak as DBStudyStreak
)
from src.services.tracking_service import TrackingService
from src.core.error_handling import ValidationError, ResourceNotFoundError, DatabaseError
from src.tests.base_test_classes import BaseServiceTest


class TestTrackingService(BaseServiceTest):
    """Tests for TrackingService"""
    
    def setUp(self):
        """Set up test case."""
        super().setUp()
        self.tracking_service = TrackingService()
        self.user_id = str(uuid.uuid4())
        self.session_id = str(uuid.uuid4())
        self.activity_id = str(uuid.uuid4())
        
    def test_start_learning_session_success(self):
        """Test starting a learning session successfully."""
        # Mock the transaction context manager
        session_mock = MagicMock()
        self.tracking_service.transaction = MagicMock(return_value=self._get_transaction_cm(session_mock))
        
        # Mock _update_study_streak
        self.tracking_service._update_study_streak = MagicMock()
        
        # Call the method
        result = self.tracking_service.start_learning_session(self.user_id)
        
        # Verify result
        assert result is not None
        assert result.user_id == self.user_id
        assert session_mock.add.called
        assert session_mock.flush.called
        assert session_mock.refresh.called
        assert self.tracking_service._update_study_streak.called
        
    def test_start_learning_session_invalid_user_id(self):
        """Test starting a learning session with invalid user ID."""
        with pytest.raises(ValidationError):
            self.tracking_service.start_learning_session("invalid-uuid")
            
    def test_end_learning_session_success(self):
        """Test ending a learning session successfully."""
        # Mock db_session
        db_session = MagicMock()
        db_session.id = uuid.UUID(self.session_id)
        db_session.start_time = datetime.now()
        
        # Mock the transaction context manager
        session_mock = MagicMock()
        session_mock.query.return_value.filter.return_value.first.return_value = db_session
        self.tracking_service.transaction = MagicMock(return_value=self._get_transaction_cm(session_mock))
        
        # Mock _convert_db_session_to_ui_session
        self.tracking_service._convert_db_session_to_ui_session = MagicMock()
        
        # Call the method
        self.tracking_service.end_learning_session(self.session_id)
        
        # Verify result
        assert db_session.end_time is not None
        assert db_session.duration is not None
        assert session_mock.flush.called
        assert session_mock.refresh.called
        
    def test_end_learning_session_not_found(self):
        """Test ending a non-existent learning session."""
        # Mock the transaction context manager
        session_mock = MagicMock()
        session_mock.query.return_value.filter.return_value.first.return_value = None
        self.tracking_service.transaction = MagicMock(return_value=self._get_transaction_cm(session_mock))
        
        # Call the method and expect exception
        with pytest.raises(ResourceNotFoundError):
            self.tracking_service.end_learning_session(self.session_id)
            
    def test_log_error_success(self):
        """Test logging an error successfully."""
        # Mock the transaction context manager
        session_mock = MagicMock()
        self.tracking_service.transaction = MagicMock(return_value=self._get_transaction_cm(session_mock))
        
        # Mock _convert_db_error_to_ui_error
        self.tracking_service._convert_db_error_to_ui_error = MagicMock()
        
        # Call the method
        error_type = "calculation_error"
        error_data = {"problem": "2+2", "user_answer": "5", "correct_answer": "4"}
        self.tracking_service.log_error(self.user_id, error_type, error_data)
        
        # Verify result
        assert session_mock.add.called
        assert session_mock.flush.called
        assert session_mock.refresh.called
        
    def test_log_error_empty_data(self):
        """Test logging an error with empty data."""
        with pytest.raises(ValidationError):
            self.tracking_service.log_error(self.user_id, "calculation_error", {})
            
    def _get_transaction_cm(self, session_mock):
        """Get a mock context manager for transaction."""
        mock_cm = MagicMock()
        mock_cm.__enter__ = MagicMock(return_value=session_mock)
        mock_cm.__exit__ = MagicMock(return_value=False)
        return mock_cm 