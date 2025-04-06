"""
User statistics service for Mathtermind.

This module provides a service for tracking and managing user statistics,
demonstrating the use of enhanced BaseService features.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import functools
import time
import uuid
from contextlib import contextmanager

from src.services.base_service import (
    BaseService, 
    EntityNotFoundError, 
    ValidationError, 
    DatabaseError
)
from src.db.repositories.user_repo import UserRepository
from src.db.repositories.progress_repo import ProgressRepository
from src.db.repositories.completed_course_repo import CompletedCourseRepository
from src.db.repositories.completed_lesson_repo import CompletedLessonRepository
from src.db.repositories.achievement_repo import AchievementRepository


class UserStatsService(BaseService):
    """Service for managing user statistics.
    
    This service demonstrates the use of enhanced BaseService features:
    - Transaction management
    - Caching
    - Validation
    - Custom error handling
    """
    
    def __init__(self):
        """Initialize the service with repositories."""
        # Note: We're not passing a specific repository to super().__init__()
        # since this service works with multiple repositories
        super().__init__()
        
        self.user_repository = UserRepository()
        self.progress_repository = ProgressRepository()
        self.completed_course_repository = CompletedCourseRepository()
        self.completed_lesson_repository = CompletedLessonRepository()
        self.achievement_repository = AchievementRepository()
        
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Validators for various operations
        self.stat_validators = {
            "user_id": lambda x: isinstance(x, str) and len(x) > 0,
            "points": lambda x: isinstance(x, int) and x >= 0,
            "time_spent": lambda x: isinstance(x, int) and x >= 0,
            "date": lambda x: isinstance(x, datetime)
        }
    
    # Use a decorator directly defined in this service as a workaround
    def cache_user_stats(func):
        """Cache decorator for user statistics methods."""
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Generate a unique key based on args and kwargs
            cache_key = f"user_stats:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Check if result is cached and not expired
            if cache_key in self._cache:
                expiry_time = self._cache_ttl.get(cache_key)
                if expiry_time is None or expiry_time > time.time():
                    self.logger.debug(f"Cache hit for key: {cache_key}")
                    return self._cache[cache_key]
            
            # Execute the function
            result = func(self, *args, **kwargs)
            
            # Cache the result with a 15-minute TTL
            self._cache[cache_key] = result
            ttl_seconds = timedelta(minutes=15).total_seconds()
            self._cache_ttl[cache_key] = time.time() + ttl_seconds
            
            # Manage cache size
            self._manage_cache_size()
            
            return result
        return wrapper
    
    # Use a decorator directly defined in this service as a workaround
    def cache_top_users(func):
        """Cache decorator for top users methods."""
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Generate a unique key based on args and kwargs
            cache_key = f"top_users:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Check if result is cached and not expired
            if cache_key in self._cache:
                expiry_time = self._cache_ttl.get(cache_key)
                if expiry_time is None or expiry_time > time.time():
                    self.logger.debug(f"Cache hit for key: {cache_key}")
                    return self._cache[cache_key]
            
            # Execute the function
            result = func(self, *args, **kwargs)
            
            # Cache the result with a 1-hour TTL
            self._cache[cache_key] = result
            ttl_seconds = timedelta(hours=1).total_seconds()
            self._cache_ttl[cache_key] = time.time() + ttl_seconds
            
            # Manage cache size
            self._manage_cache_size()
            
            return result
        return wrapper
    
    @cache_user_stats
    def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive statistics for a user.
        
        This method demonstrates caching for a computationally expensive operation.
        
        Args:
            user_id: The ID of the user.
            
        Returns:
            Dictionary containing user statistics.
            
        Raises:
            EntityNotFoundError: If the user is not found.
        """
        try:
            # Validate the user_id
            self.validate({"user_id": user_id}, {"user_id": self.stat_validators["user_id"]})
            
            # Check if user exists
            user = self.user_repository.get_by_id(self.db, user_id)
            if user is None:
                raise EntityNotFoundError(f"User with ID {user_id} not found")
            
            # Get various statistics
            total_points = user.points
            study_time = user.study_time
            
            # Get completed courses count
            completed_courses = self.completed_course_repository.get_by_user_id(
                self.db, user_id
            )
            completed_courses_count = len(completed_courses)
            
            # Get completed lessons count
            completed_lessons = self.completed_lesson_repository.get_by_user_id(
                self.db, user_id
            )
            completed_lessons_count = len(completed_lessons)
            
            # Get progress data
            progress_entries = self.progress_repository.get_by_user_id(
                self.db, user_id
            )
            
            # Calculate average progress percentage
            if progress_entries:
                avg_progress = sum(entry.progress_percentage for entry in progress_entries) / len(progress_entries)
            else:
                avg_progress = 0
            
            # Assemble the statistics
            return {
                "user_id": user_id,
                "username": user.username,
                "total_points": total_points,
                "study_time_minutes": study_time,
                "completed_courses": completed_courses_count,
                "completed_lessons": completed_lessons_count,
                "average_progress": avg_progress,
                "last_updated": datetime.now()
            }
        
        except EntityNotFoundError:
            self.logger.warning(f"User with ID {user_id} not found")
            raise
        except ValidationError as e:
            self.logger.warning(f"Validation error: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error getting user statistics: {str(e)}")
            raise DatabaseError(f"Error retrieving user statistics: {str(e)}")
    
    def update_user_points(self, user_id: str, points_to_add: int) -> Dict[str, Any]:
        """Update a user's points.
        
        This method demonstrates transaction management and cache invalidation.
        
        Args:
            user_id: The ID of the user.
            points_to_add: Points to add to the user's total.
            
        Returns:
            Updated user statistics.
            
        Raises:
            EntityNotFoundError: If the user is not found.
            ValidationError: If the input data is invalid.
        """
        try:
            # Validate inputs
            self.validate(
                {"user_id": user_id, "points": points_to_add},
                {"user_id": self.stat_validators["user_id"], "points": self.stat_validators["points"]}
            )
            
            # Update points in a transaction
            with self.transaction():
                # Get current user
                user = self.user_repository.get_by_id(self.db, user_id)
                if user is None:
                    raise EntityNotFoundError(f"User with ID {user_id} not found")
                
                # Update points
                new_points = user.points + points_to_add
                self.user_repository.update(self.db, user_id, points=new_points)
            
            # Invalidate cache
            self.invalidate_cache(f"user_stats")
            
            # Return updated statistics
            return self.get_user_statistics(user_id)
        
        except (EntityNotFoundError, ValidationError):
            # Re-raise these exceptions for higher-level handling
            raise
        except Exception as e:
            self.logger.error(f"Error updating user points: {str(e)}")
            raise DatabaseError(f"Error updating user points: {str(e)}")
    
    def update_user_study_time(self, user_id: str, minutes_to_add: int) -> Dict[str, Any]:
        """Update a user's study time.
        
        This method demonstrates transaction management and cache invalidation.
        
        Args:
            user_id: The ID of the user.
            minutes_to_add: Minutes to add to the user's study time.
            
        Returns:
            Updated user statistics.
            
        Raises:
            EntityNotFoundError: If the user is not found.
            ValidationError: If the input data is invalid.
        """
        try:
            # Validate inputs
            self.validate(
                {"user_id": user_id, "time_spent": minutes_to_add},
                {"user_id": self.stat_validators["user_id"], "time_spent": self.stat_validators["time_spent"]}
            )
            
            # Define the update operation
            def update_time():
                # Get current user
                user = self.user_repository.get_by_id(self.db, user_id)
                if user is None:
                    raise EntityNotFoundError(f"User with ID {user_id} not found")
                
                # Update study time
                new_time = user.study_time + minutes_to_add
                self.user_repository.update(self.db, user_id, study_time=new_time)
            
            # Execute the update in a transaction
            self.execute_in_transaction(update_time)
            
            # Invalidate cache
            self.invalidate_cache(f"user_stats")
            
            # Return updated statistics
            return self.get_user_statistics(user_id)
        
        except (EntityNotFoundError, ValidationError):
            # Re-raise these exceptions for higher-level handling
            raise
        except Exception as e:
            self.logger.error(f"Error updating user study time: {str(e)}")
            raise DatabaseError(f"Error updating user study time: {str(e)}")
    
    def batch_update_user_stats(self, stats_updates: List[Dict[str, Any]]) -> int:
        """Update statistics for multiple users in batches.
        
        This method demonstrates batch operations.
        
        Args:
            stats_updates: List of dictionaries with user_id, points, and time_spent.
            
        Returns:
            Number of users successfully updated.
            
        Raises:
            ValidationError: If any of the input data is invalid.
        """
        # Validate all updates first
        for update in stats_updates:
            self.validate(
                {
                    "user_id": update.get("user_id", ""),
                    "points": update.get("points", 0),
                    "time_spent": update.get("time_spent", 0)
                },
                {
                    "user_id": self.stat_validators["user_id"],
                    "points": self.stat_validators["points"],
                    "time_spent": self.stat_validators["time_spent"]
                }
            )
        
        updated_count = 0
        
        def update_user_stats(update_data):
            nonlocal updated_count
            user_id = update_data.get("user_id")
            points = update_data.get("points", 0)
            time_spent = update_data.get("time_spent", 0)
            
            try:
                # Get current user
                user = self.user_repository.get_by_id(self.db, user_id)
                if user is None:
                    self.logger.warning(f"User with ID {user_id} not found during batch update")
                    return
                
                # Update stats
                new_points = user.points + points
                new_time = user.study_time + time_spent
                self.user_repository.update(
                    self.db, user_id, 
                    points=new_points, 
                    study_time=new_time
                )
                updated_count += 1
                
                # We would invalidate cache here, but we'll do it once after the batch
            except Exception as e:
                self.logger.error(f"Error updating stats for user {user_id}: {str(e)}")
        
        # Perform batch operation
        self.batch_operation(stats_updates, update_user_stats, batch_size=50)
        
        # Invalidate all user stats caches
        self.invalidate_cache("user_stats")
        
        return updated_count
    
    @cache_top_users
    def get_top_users_by_points(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top users by points.
        
        This method demonstrates caching for a leaderboard.
        
        Args:
            limit: Maximum number of users to return.
            
        Returns:
            List of top users with their statistics.
        """
        try:
            # Validate limit
            if not isinstance(limit, int) or limit <= 0:
                limit = 10
            
            # Get top users
            top_users = self.user_repository.get_top_by_points(self.db, limit)
            
            # Format result
            result = []
            for user in top_users:
                result.append({
                    "user_id": user.id,
                    "username": user.username,
                    "points": user.points,
                    "completed_courses": len(self.completed_course_repository.get_by_user_id(
                        self.db, user.id
                    ))
                })
            
            return result
        
        except Exception as e:
            self.logger.error(f"Error getting top users: {str(e)}")
            return []
    
    def get_user_achievements_stats(self, user_id: str) -> Dict[str, Any]:
        """Get statistics about a user's achievements.
        
        This method demonstrates structured error handling.
        
        Args:
            user_id: The ID of the user.
            
        Returns:
            Dictionary containing achievement statistics or error information.
        """
        try:
            # Validate user_id
            self.validate({"user_id": user_id}, {"user_id": self.stat_validators["user_id"]})
            
            # Check if user exists
            user = self.user_repository.get_by_id(self.db, user_id)
            if user is None:
                raise EntityNotFoundError(f"User with ID {user_id} not found")
            
            # This would normally get data from an achievement repository
            # For demonstration, we'll return mock data
            return {
                "status": "success",
                "total_achievements": 10,
                "completed_achievements": 5,
                "latest_achievement": "Completed first course",
                "achievement_points": 500
            }
            
        except ValidationError as e:
            self.logger.warning(f"Validation error for user {user_id}: {str(e)}")
            return {
                "status": "error",
                "error_type": "validation",
                "message": str(e)
            }
        except EntityNotFoundError as e:
            self.logger.warning(str(e))
            return {
                "status": "error",
                "error_type": "not_found",
                "message": str(e)
            }
        except DatabaseError as e:
            self.logger.error(f"Database error: {str(e)}")
            return {
                "status": "error",
                "error_type": "database",
                "message": "A database error occurred"
            }
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return {
                "status": "error",
                "error_type": "unknown",
                "message": "An unexpected error occurred"
            } 