"""
Goal factories for Mathtermind tests.
"""

import uuid
from datetime import datetime, timezone, timedelta
from typing import Any, Dict

from src.db.models import User
from src.db.models.goals import LearningGoal, PersonalBest
from src.db.models.enums import MetricType
from src.tests.utils.test_factories.base import BaseFactory
from src.tests.utils.test_factories.user import UserFactory


class LearningGoalFactory(BaseFactory[LearningGoal]):
    """Factory for creating LearningGoal instances."""
    model_class = LearningGoal
    
    @classmethod
    def _get_defaults(cls) -> Dict[str, Any]:
        """Get default values for LearningGoal attributes."""
        now = datetime.now(timezone.utc)
        return {
            'user_id': uuid.uuid4(),  # Should be overridden with an actual user ID
            'title': f"Test Learning Goal {uuid.uuid4().hex[:8]}",
            'description': "A test learning goal for unit testing",
            'goal_type': "daily",
            'target_value': 60,  # 60 minutes
            'current_value': 30,
            'start_date': now,
            'end_date': now + timedelta(days=7),
            'is_completed': False
        }
    
    @classmethod
    def with_user(cls, user: User = None, **kwargs) -> LearningGoal:
        """
        Create a learning goal associated with a user.
        
        Args:
            user: The user to associate with the learning goal.
            **kwargs: Additional attributes to override defaults.
            
        Returns:
            LearningGoal: A learning goal instance.
        """
        if user is None:
            user = UserFactory.create()
            
        return cls.create(user_id=user.id, **kwargs)


class PersonalBestFactory(BaseFactory[PersonalBest]):
    """Factory for creating PersonalBest instances."""
    model_class = PersonalBest
    
    @classmethod
    def _get_defaults(cls) -> Dict[str, Any]:
        """Get default values for PersonalBest attributes."""
        return {
            'user_id': uuid.uuid4(),  # Should be overridden with an actual user ID
            'metric_type': MetricType.SCORE,
            'value': 95,
            'context_type': "quiz",
            'context_id': str(uuid.uuid4()),
            'achieved_at': datetime.now(timezone.utc)
        }
    
    @classmethod
    def with_user(cls, user: User = None, **kwargs) -> PersonalBest:
        """
        Create a personal best associated with a user.
        
        Args:
            user: The user to associate with the personal best.
            **kwargs: Additional attributes to override defaults.
            
        Returns:
            PersonalBest: A personal best instance.
        """
        if user is None:
            user = UserFactory.create()
            
        return cls.create(user_id=user.id, **kwargs) 