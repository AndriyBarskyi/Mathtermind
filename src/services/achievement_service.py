from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid
import logging

from src.db import get_db
from src.db.repositories import achievement_repo, user_achievement_repo
from src.db.models import Achievement as DBAchievement, UserAchievement as DBUserAchievement

# Set up logging
logger = logging.getLogger(__name__)

class Achievement:
    """Model for an achievement"""
    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        icon: str,
        criteria: Dict[str, Any],
        points: int,
        created_at: datetime,
        is_active: bool
    ):
        self.id = id
        self.title = title
        self.description = description
        self.icon = icon
        self.criteria = criteria
        self.points = points
        self.created_at = created_at
        self.is_active = is_active


class UserAchievement:
    """Model for a user's earned achievement"""
    def __init__(
        self,
        id: str,
        user_id: str,
        achievement_id: str,
        achieved_at: datetime,
        achievement: Optional[Achievement] = None
    ):
        self.id = id
        self.user_id = user_id
        self.achievement_id = achievement_id
        self.achieved_at = achieved_at
        self.achievement = achievement


class AchievementService:
    """
    Service class for handling achievement operations.
    This class provides methods for fetching, awarding, and tracking achievements.
    """
    
    def get_all_achievements(self) -> List[Achievement]:
        """
        Get all available achievements
        
        Returns:
            List of all achievements
        """
        try:
            db = next(get_db())
            db_achievements = achievement_repo.get_all_achievements(db)
            achievements = [self._convert_db_achievement_to_achievement(achievement) for achievement in db_achievements]
            db.close()
            return achievements
        except Exception as e:
            logger.error(f"Error fetching all achievements: {str(e)}")
            return []
    
    def get_achievement(self, achievement_id: str) -> Optional[Achievement]:
        """
        Get an achievement by its ID
        
        Args:
            achievement_id: The ID of the achievement to retrieve
            
        Returns:
            The achievement if found, None otherwise
        """
        try:
            db = next(get_db())
            db_achievement = achievement_repo.get_achievement(db, achievement_id)
            if db_achievement:
                achievement = self._convert_db_achievement_to_achievement(db_achievement)
                db.close()
                return achievement
            db.close()
            return None
        except Exception as e:
            logger.error(f"Error getting achievement: {str(e)}")
            return None
    
    def get_user_achievements(self, user_id: str) -> List[UserAchievement]:
        """
        Get all achievements earned by a user
        
        Args:
            user_id: The ID of the user
            
        Returns:
            List of user achievement records
        """
        try:
            db = next(get_db())
            db_user_achievements = user_achievement_repo.get_user_achievements(db, user_id)
            
            # Get achievement details for each user achievement
            user_achievements = []
            for db_user_achievement in db_user_achievements:
                db_achievement = achievement_repo.get_achievement(db, db_user_achievement.achievement_id)
                achievement = self._convert_db_achievement_to_achievement(db_achievement) if db_achievement else None
                
                user_achievement = self._convert_db_user_achievement_to_user_achievement(
                    db_user_achievement, 
                    achievement
                )
                user_achievements.append(user_achievement)
            
            db.close()
            return user_achievements
        except Exception as e:
            logger.error(f"Error getting user achievements: {str(e)}")
            return []
    
    def award_achievement(self, user_id: str, achievement_id: str) -> Optional[UserAchievement]:
        """
        Award an achievement to a user
        
        Args:
            user_id: The ID of the user
            achievement_id: The ID of the achievement to award
            
        Returns:
            The created user achievement record if successful, None otherwise
        """
        try:
            db = next(get_db())
            
            # Check if achievement exists and is active
            db_achievement = achievement_repo.get_achievement(db, achievement_id)
            if not db_achievement or not db_achievement.is_active:
                db.close()
                return None
            
            # Check if user already has this achievement
            existing_achievement = user_achievement_repo.get_user_achievement(db, user_id, achievement_id)
            if existing_achievement:
                db.close()
                return self._convert_db_user_achievement_to_user_achievement(
                    existing_achievement,
                    self._convert_db_achievement_to_achievement(db_achievement)
                )
            
            # Create new user achievement record
            user_achievement = DBUserAchievement(
                id=uuid.uuid4(),
                user_id=user_id,
                achievement_id=achievement_id,
                achieved_at=datetime.now(timezone.utc)
            )
            
            # Save to database
            created_achievement = user_achievement_repo.create_user_achievement(db, user_achievement)
            
            # Convert to model
            result = self._convert_db_user_achievement_to_user_achievement(
                created_achievement,
                self._convert_db_achievement_to_achievement(db_achievement)
            )
            
            db.close()
            return result
        except Exception as e:
            logger.error(f"Error awarding achievement: {str(e)}")
            return None
    
    def check_achievement_criteria(self, user_id: str, event_type: str, event_data: Dict[str, Any]) -> List[Achievement]:
        """
        Check if a user has met the criteria for any achievements based on an event
        
        Args:
            user_id: The ID of the user
            event_type: The type of event (e.g., "course_completion", "points", "streak")
            event_data: Data related to the event
            
        Returns:
            List of achievements that the user has newly qualified for
        """
        try:
            db = next(get_db())
            
            # Get all active achievements
            db_achievements = achievement_repo.get_active_achievements(db)
            
            # Get user's existing achievements
            existing_achievements = user_achievement_repo.get_user_achievements(db, user_id)
            existing_achievement_ids = [str(a.achievement_id) for a in existing_achievements]
            
            # Filter achievements by event type and check criteria
            qualified_achievements = []
            
            for db_achievement in db_achievements:
                # Skip if user already has this achievement
                if str(db_achievement.id) in existing_achievement_ids:
                    continue
                
                # Check if achievement criteria matches event type
                criteria = db_achievement.criteria
                if criteria.get("type") != event_type:
                    continue
                
                # Check specific criteria based on event type
                if self._meets_criteria(criteria, event_data):
                    qualified_achievements.append(self._convert_db_achievement_to_achievement(db_achievement))
            
            db.close()
            return qualified_achievements
        except Exception as e:
            logger.error(f"Error checking achievement criteria: {str(e)}")
            return []
    
    def _meets_criteria(self, criteria: Dict[str, Any], event_data: Dict[str, Any]) -> bool:
        """
        Check if an event meets the criteria for an achievement
        
        Args:
            criteria: The achievement criteria
            event_data: Data related to the event
            
        Returns:
            True if the criteria is met, False otherwise
        """
        try:
            criteria_type = criteria.get("type")
            requirements = criteria.get("requirements", {})
            
            if criteria_type == "course_completion":
                # Check if completed course is in required courses
                course_id = event_data.get("course_id")
                required_courses = requirements.get("course_ids", [])
                return course_id in required_courses
                
            elif criteria_type == "points":
                # Check if points earned meets or exceeds required points
                points = event_data.get("points", 0)
                required_points = requirements.get("points_required", 0)
                return points >= required_points
                
            elif criteria_type == "streak":
                # Check if streak days meets or exceeds required days
                streak_days = event_data.get("streak_days", 0)
                required_days = requirements.get("days_required", 0)
                return streak_days >= required_days
                
            elif criteria_type == "time":
                # Check if study time meets or exceeds required time
                study_time = event_data.get("study_time", 0)
                required_time = requirements.get("time_required", 0)
                return study_time >= required_time
                
            elif criteria_type == "perfect_score":
                # Check if quiz is in required quizzes and score is 100%
                quiz_id = event_data.get("quiz_id")
                score = event_data.get("score", 0)
                required_quizzes = requirements.get("quiz_ids", [])
                return quiz_id in required_quizzes and score == 100
                
            return False
        except Exception as e:
            logger.error(f"Error checking achievement criteria: {str(e)}")
            return False
    
    def _convert_db_achievement_to_achievement(self, db_achievement: DBAchievement) -> Achievement:
        """Convert a database achievement model to an Achievement model"""
        try:
            return Achievement(
                id=str(db_achievement.id),
                title=db_achievement.title,
                description=db_achievement.description,
                icon=db_achievement.icon,
                criteria=db_achievement.criteria,
                points=db_achievement.points,
                created_at=db_achievement.created_at,
                is_active=db_achievement.is_active
            )
        except Exception as e:
            logger.error(f"Error converting achievement: {str(e)}")
            # Return a default achievement as fallback
            return Achievement(
                id=str(db_achievement.id) if hasattr(db_achievement, 'id') else "unknown",
                title=db_achievement.title if hasattr(db_achievement, 'title') else "Unknown Achievement",
                description="No description available",
                icon="default_icon.png",
                criteria={},
                points=0,
                created_at=datetime.now(timezone.utc),
                is_active=True
            )
    
    def _convert_db_user_achievement_to_user_achievement(
        self, 
        db_user_achievement: DBUserAchievement, 
        achievement: Optional[Achievement] = None
    ) -> UserAchievement:
        """Convert a database user achievement model to a UserAchievement model"""
        try:
            return UserAchievement(
                id=str(db_user_achievement.id),
                user_id=str(db_user_achievement.user_id),
                achievement_id=str(db_user_achievement.achievement_id),
                achieved_at=db_user_achievement.achieved_at,
                achievement=achievement
            )
        except Exception as e:
            logger.error(f"Error converting user achievement: {str(e)}")
            # Return a default user achievement as fallback
            return UserAchievement(
                id=str(db_user_achievement.id) if hasattr(db_user_achievement, 'id') else "unknown",
                user_id=str(db_user_achievement.user_id) if hasattr(db_user_achievement, 'user_id') else "unknown",
                achievement_id=str(db_user_achievement.achievement_id) if hasattr(db_user_achievement, 'achievement_id') else "unknown",
                achieved_at=datetime.now(timezone.utc),
                achievement=None
            ) 