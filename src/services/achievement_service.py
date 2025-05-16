"""
Achievement service for Mathtermind.

This module provides service methods for managing achievements and rewards.
"""

from typing import List, Optional, Dict, Any
import uuid
import logging
from datetime import datetime

from src.db import get_db
from src.db.models import (
    Achievement as DBAchievement,
    UserAchievement as DBUserAchievement
)
from src.db.repositories import (
    AchievementRepository,
    UserRepository,
    ProgressRepository
)
from src.models.achievement import Achievement, UserAchievement

# Set up logging
logger = logging.getLogger(__name__)


class AchievementService:
    """Service for managing user achievements and rewards."""
    
    def __init__(self):
        """Initialize the achievement service."""
        self.db = next(get_db())
        self.achievement_repo = AchievementRepository(self.db)
        self.user_repo = UserRepository(self.db)
        self.progress_repo = ProgressRepository(self.db)
    
    def get_all_achievements(self) -> List[Achievement]:
        """
        Get all available achievements.
        
        Returns:
            A list of achievements
        """
        try:
            # Get all achievements from the repository
            db_achievements = self.achievement_repo.get_all()
            
            # Convert to UI models
            return [self._convert_db_achievement_to_ui_achievement(ach) for ach in db_achievements]
        except Exception as e:
            logger.error(f"Error getting all achievements: {str(e)}")
            return []
    
    def get_achievement_by_id(self, achievement_id: str) -> Optional[Achievement]:
        """
        Get an achievement by ID.
        
        Args:
            achievement_id: The ID of the achievement
            
        Returns:
            The achievement if found, None otherwise
        """
        try:
            achievement_uuid = uuid.UUID(achievement_id)
            
            # Get the achievement from the repository
            db_achievement = self.achievement_repo.get_by_id(achievement_uuid)
            
            if not db_achievement:
                return None
                
            return self._convert_db_achievement_to_ui_achievement(db_achievement)
        except Exception as e:
            logger.error(f"Error getting achievement by ID: {str(e)}")
            return None
    
    def get_achievements_by_category(self, category: str) -> List[Achievement]:
        """
        Get achievements by category.
        
        Args:
            category: The category of achievements
            
        Returns:
            A list of achievements in the category
        """
        try:
            # Get achievements by category
            db_achievements = self.achievement_repo.get_by_category(category)
            
            # Convert to UI models
            return [self._convert_db_achievement_to_ui_achievement(ach) for ach in db_achievements]
        except Exception as e:
            logger.error(f"Error getting achievements by category: {str(e)}")
            return []
    
    def get_user_achievements(self, user_id: str) -> List[UserAchievement]:
        """
        Get all achievements earned by a user.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            A list of user achievements
        """
        try:
            user_uuid = uuid.UUID(user_id)
            
            # Get the user's achievements
            db_user_achievements = self.achievement_repo.get_user_achievements(user_uuid)
            
            # Convert to UI models
            return [self._convert_db_user_achievement_to_ui_user_achievement(ua) for ua in db_user_achievements]
        except Exception as e:
            logger.error(f"Error getting user achievements: {str(e)}")
            return []
    
    def award_achievement(self, 
                        user_id: str, 
                        achievement_id: str, 
                        progress_data: Optional[Dict[str, Any]] = None) -> Optional[UserAchievement]:
        """
        Award an achievement to a user.
        
        Args:
            user_id: The ID of the user
            achievement_id: The ID of the achievement
            progress_data: Optional progress data related to the achievement
            
        Returns:
            The awarded user achievement if successful, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            achievement_uuid = uuid.UUID(achievement_id)
            
            # Check if user already has the achievement
            existing = self.achievement_repo.get_user_achievement(user_uuid, achievement_uuid)
            if existing:
                logger.info(f"User {user_id} already has achievement {achievement_id}")
                return self._convert_db_user_achievement_to_ui_user_achievement(existing)
            
            # Get the achievement
            achievement = self.achievement_repo.get_by_id(achievement_uuid)
            if not achievement:
                logger.warning(f"Achievement not found: {achievement_id}")
                return None
            
            # Award the achievement
            db_user_achievement = self.achievement_repo.award_achievement(
                user_uuid, 
                achievement_uuid, 
                progress_data or {}
            )
           
            if not db_user_achievement:
                return None
            
            # Award points to the user
            if achievement.points_value > 0:
                user = self.user_repo.get_by_id(user_uuid)
                if user:
                    user.points = (user.points or 0) + achievement.points_value
                    self.user_repo.update(user)
            
            return self._convert_db_user_achievement_to_ui_user_achievement(db_user_achievement)
        except Exception as e:
            logger.error(f"Error awarding achievement: {str(e)}")
            self.db.rollback()
            return None
    
    def check_progress_achievements(self, user_id: str, progress_id: str) -> List[UserAchievement]:
        """
        Check and award progress-related achievements for a user.
        
        Args:
            user_id: The ID of the user
            progress_id: The ID of the progress record
            
        Returns:
            A list of newly awarded achievements
        """
        try:
            user_uuid = uuid.UUID(user_id)
            progress_uuid = uuid.UUID(progress_id)
            
            # Get the progress record
            progress = self.progress_repo.get_by_id(progress_uuid)
            if not progress:
                logger.warning(f"Progress not found: {progress_id}")
                return []
            
            # Get all progress-related achievements
            achievements = self.achievement_repo.get_by_category("progress")
            
            # Check each achievement
            awarded = []
            for achievement in achievements:
                # Skip if user already has the achievement
                if self.achievement_repo.get_user_achievement(user_uuid, achievement.id):
                    continue
                
                # Check achievement criteria
                criteria = achievement.criteria
                criteria_type = criteria.get("type", "")
                
                if criteria_type == "course_completion":
                    # Award for completing a course
                    if progress.is_completed:
                        user_achievement = self.award_achievement(
                            user_id,
                            str(achievement.id),
                            {"progress_id": str(progress_uuid), "course_id": str(progress.course_id)}
                        )
                        if user_achievement:
                            awarded.append(user_achievement)
                
                elif criteria_type == "progress_percentage":
                    # Award for reaching a progress percentage
                    min_percentage = criteria.get("min_percentage", 0)
                    if progress.progress_percentage >= min_percentage:
                        user_achievement = self.award_achievement(
                            user_id,
                            str(achievement.id),
                            {"progress_id": str(progress_uuid), "percentage": progress.progress_percentage}
                        )
                        if user_achievement:
                            awarded.append(user_achievement)
                
                elif criteria_type == "points_earned":
                    # Award for earning points
                    min_points = criteria.get("min_points", 0)
                    if progress.total_points_earned >= min_points:
                        user_achievement = self.award_achievement(
                            user_id,
                            str(achievement.id),
                            {"progress_id": str(progress_uuid), "points": progress.total_points_earned}
                        )
                        if user_achievement:
                            awarded.append(user_achievement)
            
            return awarded
        except Exception as e:
            logger.error(f"Error checking progress achievements: {str(e)}")
            return []
    
    def check_user_achievements(self, user_id: str) -> List[UserAchievement]:
        """
        Check and award user-related achievements.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            A list of newly awarded achievements
        """
        try:
            user_uuid = uuid.UUID(user_id)
            
            # Get the user
            user = self.user_repo.get_by_id(user_uuid)
            if not user:
                logger.warning(f"User not found: {user_id}")
                return []
            
            # Get all user-related achievements
            achievements = self.achievement_repo.get_by_category("user")
            
            # Check each achievement
            awarded = []
            for achievement in achievements:
                # Skip if user already has the achievement
                if self.achievement_repo.get_user_achievement(user_uuid, achievement.id):
                    continue
                
                # Check achievement criteria
                criteria = achievement.criteria
                criteria_type = criteria.get("type", "")
                
                if criteria_type == "total_points":
                    # Award for total points
                    min_points = criteria.get("min_points", 0)
                    if user.points >= min_points:
                        user_achievement = self.award_achievement(
                            user_id,
                            str(achievement.id),
                            {"total_points": user.points}
                        )
                        if user_achievement:
                            awarded.append(user_achievement)
                
                elif criteria_type == "account_age":
                    # Award for account age in days
                    min_days = criteria.get("min_days", 0)
                    account_age = (datetime.now() - user.created_at).days
                    if account_age >= min_days:
                        user_achievement = self.award_achievement(
                            user_id,
                            str(achievement.id),
                            {"account_age_days": account_age}
                        )
                        if user_achievement:
                            awarded.append(user_achievement)
                
                elif criteria_type == "study_time":
                    # Award for total study time in minutes
                    min_minutes = criteria.get("min_minutes", 0)
                    if user.total_study_time and user.total_study_time >= min_minutes:
                        user_achievement = self.award_achievement(
                            user_id,
                            str(achievement.id),
                            {"total_study_time": user.total_study_time}
                        )
                        if user_achievement:
                            awarded.append(user_achievement)
            
            return awarded
        except Exception as e:
            logger.error(f"Error checking user achievements: {str(e)}")
            return []
    
    def create_achievement(self, 
                         name: str,
                         description: str,
                         category: str,
                         criteria: Dict[str, Any],
                         icon_url: str,
                         points_value: int = 0,
                         display_order: int = 0,
                         is_hidden: bool = False,
                         metadata: Optional[Dict[str, Any]] = None) -> Optional[Achievement]:
        """
        Create a new achievement.
        
        Args:
            name: The name of the achievement
            description: The description of the achievement
            category: The category of the achievement
            criteria: The criteria for earning the achievement
            icon_url: The URL to the achievement icon
            points_value: The points value of the achievement
            display_order: The display order of the achievement
            is_hidden: Whether the achievement is hidden until earned
            metadata: Additional metadata for the achievement
            
        Returns:
            The created achievement if successful, None otherwise
        """
        try:
            # Create a new achievement
            db_achievement = self.achievement_repo.create(
                name=name,
                description=description,
                category=category,
                criteria=criteria,
                icon_url=icon_url,
                points_value=points_value,
                display_order=display_order,
                is_hidden=is_hidden,
                metadata=metadata or {}
            )
            
            if not db_achievement:
                return None
                
            return self._convert_db_achievement_to_ui_achievement(db_achievement)
        except Exception as e:
            logger.error(f"Error creating achievement: {str(e)}")
            self.db.rollback()
            return None
    
    # Conversion Methods
    
    def _convert_db_achievement_to_ui_achievement(self, db_achievement: DBAchievement) -> Achievement:
        """
        Convert a database achievement to a UI achievement.
        
        Args:
            db_achievement: The database achievement
            
        Returns:
            The corresponding UI achievement
        """
        return Achievement(
            id=str(db_achievement.id),
            name=db_achievement.name,
            description=db_achievement.description,
            category=db_achievement.category,
            criteria=db_achievement.criteria,
            icon_url=db_achievement.icon_url,
            points_value=db_achievement.points_value,
            display_order=db_achievement.display_order,
            is_hidden=db_achievement.is_hidden,
            metadata=db_achievement.metadata,
            created_at=db_achievement.created_at,
            updated_at=db_achievement.updated_at
        )
    
    def _convert_db_user_achievement_to_ui_user_achievement(self, db_user_achievement: DBUserAchievement) -> UserAchievement:
        """
        Convert a database user achievement to a UI user achievement.
        
        Args:
            db_user_achievement: The database user achievement
            
        Returns:
            The corresponding UI user achievement
        """
        return UserAchievement(
            id=str(db_user_achievement.id),
            user_id=str(db_user_achievement.user_id),
            achievement_id=str(db_user_achievement.achievement_id),
            achievement=self._convert_db_achievement_to_ui_achievement(db_user_achievement.achievement) if db_user_achievement.achievement else None,
            awarded_at=db_user_achievement.awarded_at,
            progress_data=db_user_achievement.progress_data,
            created_at=db_user_achievement.created_at,
            updated_at=db_user_achievement.updated_at
        ) 