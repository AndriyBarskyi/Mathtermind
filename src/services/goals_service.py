"""
Goals service for Mathtermind.

This module provides service methods for managing learning goals and personal bests.
"""

from typing import List, Optional, Dict, Any
import uuid
import logging
from datetime import datetime, timedelta

from src.db import get_db
from src.db.models import LearningGoal as DBLearningGoal, PersonalBest as DBPersonalBest
from src.models.goals import LearningGoal, PersonalBest

# Set up logging
logger = logging.getLogger(__name__)


class GoalsService:
    """Service for managing learning goals and personal bests."""
    
    def __init__(self):
        """Initialize the goals service."""
        self.db = next(get_db())
    
    def get_user_goals(self, user_id: str) -> List[LearningGoal]:
        """
        Get all learning goals for a user.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            A list of learning goals
        """
        try:
            user_uuid = uuid.UUID(user_id)
            
            # Query goals from the database
            db_goals = self.db.query(DBLearningGoal).filter(
                DBLearningGoal.user_id == user_uuid
            ).order_by(DBLearningGoal.end_date).all()
            
            # Convert to UI models
            return [self._convert_db_goal_to_ui_goal(goal) for goal in db_goals]
        except Exception as e:
            logger.error(f"Error getting user goals: {str(e)}")
            return []
    
    def get_active_goals(self, user_id: str) -> List[LearningGoal]:
        """
        Get active (not completed and not overdue) goals for a user.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            A list of active learning goals
        """
        try:
            user_uuid = uuid.UUID(user_id)
            
            # Get current date
            now = datetime.now()
            
            # Query active goals from the database
            db_goals = self.db.query(DBLearningGoal).filter(
                DBLearningGoal.user_id == user_uuid,
                DBLearningGoal.is_completed == False,
                (DBLearningGoal.end_date.is_(None) | (DBLearningGoal.end_date >= now))
            ).order_by(DBLearningGoal.end_date).all()
            
            # Convert to UI models
            return [self._convert_db_goal_to_ui_goal(goal) for goal in db_goals]
        except Exception as e:
            logger.error(f"Error getting active goals: {str(e)}")
            return []
    
    def create_goal(self, 
                  user_id: str, 
                  goal_type: str, 
                  title: str, 
                  target: int, 
                  target_unit: str,
                  description: Optional[str] = None,
                  end_date: Optional[datetime] = None,
                  is_recurring: bool = False) -> Optional[LearningGoal]:
        """
        Create a new learning goal.
        
        Args:
            user_id: The ID of the user
            goal_type: The type of goal (Daily, Weekly, Course, Topic)
            title: The title of the goal
            target: The target value to achieve
            target_unit: The unit of the target (Minutes, Points, Lessons, Exercises)
            description: Optional description
            end_date: Optional deadline for the goal
            is_recurring: Whether the goal recurs
            
        Returns:
            The created learning goal if successful, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            
            # Create the goal in the database
            db_goal = DBLearningGoal(
                id=uuid.uuid4(),
                user_id=user_uuid,
                goal_type=goal_type,
                title=title,
                description=description,
                target=target,
                target_unit=target_unit,
                current_progress=0,
                start_date=datetime.now(),
                end_date=end_date,
                is_completed=False,
                is_recurring=is_recurring
            )
            
            self.db.add(db_goal)
            self.db.commit()
            self.db.refresh(db_goal)
            
            return self._convert_db_goal_to_ui_goal(db_goal)
        except Exception as e:
            logger.error(f"Error creating goal: {str(e)}")
            self.db.rollback()
            return None
    
    def update_goal_progress(self, goal_id: str, progress: int) -> Optional[LearningGoal]:
        """
        Update the progress of a goal.
        
        Args:
            goal_id: The ID of the goal
            progress: The new progress value (will be added to current progress)
            
        Returns:
            The updated learning goal if successful, None otherwise
        """
        try:
            goal_uuid = uuid.UUID(goal_id)
            
            # Get the goal from the database
            db_goal = self.db.query(DBLearningGoal).filter(DBLearningGoal.id == goal_uuid).first()
            
            if not db_goal:
                logger.warning(f"Goal not found: {goal_id}")
                return None
            
            # Update the progress
            db_goal.current_progress += progress
            
            # Check if goal is completed
            if db_goal.current_progress >= db_goal.target:
                db_goal.is_completed = True
            
            self.db.commit()
            self.db.refresh(db_goal)
            
            return self._convert_db_goal_to_ui_goal(db_goal)
        except Exception as e:
            logger.error(f"Error updating goal progress: {str(e)}")
            self.db.rollback()
            return None
    
    def complete_goal(self, goal_id: str) -> Optional[LearningGoal]:
        """
        Mark a goal as completed.
        
        Args:
            goal_id: The ID of the goal
            
        Returns:
            The updated learning goal if successful, None otherwise
        """
        try:
            goal_uuid = uuid.UUID(goal_id)
            
            # Get the goal from the database
            db_goal = self.db.query(DBLearningGoal).filter(DBLearningGoal.id == goal_uuid).first()
            
            if not db_goal:
                logger.warning(f"Goal not found: {goal_id}")
                return None
            
            # Mark as completed
            db_goal.is_completed = True
            db_goal.current_progress = db_goal.target  # Set progress to target
            
            self.db.commit()
            self.db.refresh(db_goal)
            
            return self._convert_db_goal_to_ui_goal(db_goal)
        except Exception as e:
            logger.error(f"Error completing goal: {str(e)}")
            self.db.rollback()
            return None
    
    def get_personal_bests(self, user_id: str) -> List[PersonalBest]:
        """
        Get all personal bests for a user.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            A list of personal bests
        """
        try:
            user_uuid = uuid.UUID(user_id)
            
            # Query personal bests from the database
            db_bests = self.db.query(DBPersonalBest).filter(
                DBPersonalBest.user_id == user_uuid
            ).order_by(DBPersonalBest.achieved_at.desc()).all()
            
            # Convert to UI models
            return [self._convert_db_best_to_ui_best(best) for best in db_bests]
        except Exception as e:
            logger.error(f"Error getting personal bests: {str(e)}")
            return []
    
    def record_personal_best(self, 
                          user_id: str, 
                          metric_type: str, 
                          value: float,
                          context_id: Optional[str] = None,
                          context_type: Optional[str] = None,
                          previous_best: Optional[float] = None) -> Optional[PersonalBest]:
        """
        Record a new personal best.
        
        Args:
            user_id: The ID of the user
            metric_type: The type of metric (Score, Time, Streak, Accuracy, etc.)
            value: The value achieved
            context_id: Optional ID of the related content, lesson, etc.
            context_type: Optional type of the context
            previous_best: Optional previous best value for comparison
            
        Returns:
            The recorded personal best if successful, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            context_uuid = uuid.UUID(context_id) if context_id else None
            
            # Calculate improvement if previous best is provided
            improvement = None
            if previous_best is not None:
                # For time metrics, lower is better
                if metric_type.lower() == "time":
                    improvement = previous_best - value
                else:
                    improvement = value - previous_best
            
            # Create the personal best in the database
            db_best = DBPersonalBest(
                id=uuid.uuid4(),
                user_id=user_uuid,
                metric_type=metric_type,
                value=value,
                context_id=context_uuid,
                context_type=context_type,
                achieved_at=datetime.now(),
                previous_best=previous_best,
                improvement=improvement
            )
            
            self.db.add(db_best)
            self.db.commit()
            self.db.refresh(db_best)
            
            return self._convert_db_best_to_ui_best(db_best)
        except Exception as e:
            logger.error(f"Error recording personal best: {str(e)}")
            self.db.rollback()
            return None
    
    def _convert_db_goal_to_ui_goal(self, db_goal: DBLearningGoal) -> LearningGoal:
        """
        Convert a database learning goal to a UI learning goal.
        
        Args:
            db_goal: The database learning goal
            
        Returns:
            The corresponding UI learning goal
        """
        return LearningGoal(
            id=str(db_goal.id),
            user_id=str(db_goal.user_id),
            goal_type=db_goal.goal_type,
            title=db_goal.title,
            description=db_goal.description,
            target=db_goal.target,
            target_unit=db_goal.target_unit,
            current_progress=db_goal.current_progress,
            start_date=db_goal.start_date,
            end_date=db_goal.end_date,
            is_completed=db_goal.is_completed,
            is_recurring=db_goal.is_recurring,
            created_at=db_goal.created_at,
            updated_at=db_goal.updated_at
        )
    
    def _convert_db_best_to_ui_best(self, db_best: DBPersonalBest) -> PersonalBest:
        """
        Convert a database personal best to a UI personal best.
        
        Args:
            db_best: The database personal best
            
        Returns:
            The corresponding UI personal best
        """
        return PersonalBest(
            id=str(db_best.id),
            user_id=str(db_best.user_id),
            metric_type=db_best.metric_type,
            value=db_best.value,
            context_id=str(db_best.context_id) if db_best.context_id else None,
            context_type=db_best.context_type,
            achieved_at=db_best.achieved_at,
            previous_best=db_best.previous_best,
            improvement=db_best.improvement,
            created_at=db_best.created_at,
            updated_at=db_best.updated_at
        ) 