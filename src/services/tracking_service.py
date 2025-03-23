"""
Tracking service for Mathtermind.

This module provides service methods for tracking learning sessions, error logs, and study streaks.
"""

from typing import List, Optional, Dict, Any
import uuid
import logging
from datetime import datetime, timedelta, date

from src.db import get_db
from src.db.models import (
    LearningSession as DBLearningSession,
    ErrorLog as DBErrorLog,
    StudyStreak as DBStudyStreak
)
from src.models.tracking import LearningSession, ErrorLog, StudyStreak

# Set up logging
logger = logging.getLogger(__name__)


class TrackingService:
    """Service for tracking learning activities."""
    
    def __init__(self):
        """Initialize the tracking service."""
        self.db = next(get_db())
    
    # Learning Session Methods
    
    def start_learning_session(self, user_id: str) -> Optional[LearningSession]:
        """
        Start a new learning session for a user.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            The created learning session if successful, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            
            # Create a new session in the database
            db_session = DBLearningSession(
                id=uuid.uuid4(),
                user_id=user_uuid,
                start_time=datetime.now(),
                session_data={
                    "activities": [],
                    "focus_metrics": {
                        "breaks_taken": 0,
                        "average_response_time": 0,
                        "completion_rate": 0
                    }
                }
            )
            
            self.db.add(db_session)
            self.db.commit()
            self.db.refresh(db_session)
            
            # Update the user's study streak
            self._update_study_streak(user_uuid)
            
            return self._convert_db_session_to_ui_session(db_session)
        except Exception as e:
            logger.error(f"Error starting learning session: {str(e)}")
            self.db.rollback()
            return None
    
    def end_learning_session(self, session_id: str) -> Optional[LearningSession]:
        """
        End a learning session and calculate the duration.
        
        Args:
            session_id: The ID of the session to end
            
        Returns:
            The updated learning session if successful, None otherwise
        """
        try:
            session_uuid = uuid.UUID(session_id)
            
            # Get the session from the database
            db_session = self.db.query(DBLearningSession).filter(DBLearningSession.id == session_uuid).first()
            
            if not db_session:
                logger.warning(f"Session not found: {session_id}")
                return None
            
            # Update the session
            db_session.end_time = datetime.now()
            
            # Calculate duration in minutes
            duration = int((db_session.end_time - db_session.start_time).total_seconds() / 60)
            db_session.duration = duration
            
            self.db.commit()
            self.db.refresh(db_session)
            
            return self._convert_db_session_to_ui_session(db_session)
        except Exception as e:
            logger.error(f"Error ending learning session: {str(e)}")
            self.db.rollback()
            return None
    
    def get_user_sessions(self, user_id: str, limit: int = 10) -> List[LearningSession]:
        """
        Get recent learning sessions for a user.
        
        Args:
            user_id: The ID of the user
            limit: Maximum number of sessions to return
            
        Returns:
            A list of learning sessions
        """
        try:
            user_uuid = uuid.UUID(user_id)
            
            # Query sessions from the database
            db_sessions = self.db.query(DBLearningSession).filter(
                DBLearningSession.user_id == user_uuid
            ).order_by(DBLearningSession.start_time.desc()).limit(limit).all()
            
            # Convert to UI models
            return [self._convert_db_session_to_ui_session(session) for session in db_sessions]
        except Exception as e:
            logger.error(f"Error getting user sessions: {str(e)}")
            return []
    
    def add_activity_to_session(self, 
                              session_id: str, 
                              activity_type: str, 
                              activity_id: str,
                              performance: Optional[Dict[str, Any]] = None) -> Optional[LearningSession]:
        """
        Add an activity to a learning session.
        
        Args:
            session_id: The ID of the session
            activity_type: The type of activity (lesson, quiz, practice)
            activity_id: The ID of the activity
            performance: Optional performance data for the activity
            
        Returns:
            The updated learning session if successful, None otherwise
        """
        try:
            session_uuid = uuid.UUID(session_id)
            activity_uuid = uuid.UUID(activity_id)
            
            # Get the session from the database
            db_session = self.db.query(DBLearningSession).filter(DBLearningSession.id == session_uuid).first()
            
            if not db_session:
                logger.warning(f"Session not found: {session_id}")
                return None
            
            # Create a new activity
            activity = {
                "type": activity_type,
                "id": str(activity_uuid),
                "start_time": datetime.now().isoformat(),
                "end_time": None,
                "completed": False,
                "performance": performance or {}
            }
            
            # Add the activity to the session data
            session_data = db_session.session_data
            session_data["activities"].append(activity)
            db_session.session_data = session_data
            
            self.db.commit()
            self.db.refresh(db_session)
            
            return self._convert_db_session_to_ui_session(db_session)
        except Exception as e:
            logger.error(f"Error adding activity to session: {str(e)}")
            self.db.rollback()
            return None
    
    # Error Log Methods
    
    def log_error(self, 
                user_id: str, 
                error_type: str, 
                error_data: Dict[str, Any],
                lesson_id: Optional[str] = None) -> Optional[ErrorLog]:
        """
        Log an error or mistake made by a user.
        
        Args:
            user_id: The ID of the user
            error_type: The type of error
            error_data: The error data including context, answer, etc.
            lesson_id: Optional ID of the related lesson
            
        Returns:
            The created error log if successful, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            lesson_uuid = uuid.UUID(lesson_id) if lesson_id else None
            
            # Ensure error_data has the error_type
            error_data["error_type"] = error_type
            
            # Create a new error log in the database
            db_error = DBErrorLog(
                id=uuid.uuid4(),
                user_id=user_uuid,
                lesson_id=lesson_uuid,
                error_data=error_data
            )
            
            self.db.add(db_error)
            self.db.commit()
            self.db.refresh(db_error)
            
            return self._convert_db_error_to_ui_error(db_error)
        except Exception as e:
            logger.error(f"Error logging error: {str(e)}")
            self.db.rollback()
            return None
    
    def get_user_errors(self, user_id: str, limit: int = 20) -> List[ErrorLog]:
        """
        Get recent errors for a user.
        
        Args:
            user_id: The ID of the user
            limit: Maximum number of errors to return
            
        Returns:
            A list of error logs
        """
        try:
            user_uuid = uuid.UUID(user_id)
            
            # Query errors from the database
            db_errors = self.db.query(DBErrorLog).filter(
                DBErrorLog.user_id == user_uuid
            ).order_by(DBErrorLog.created_at.desc()).limit(limit).all()
            
            # Convert to UI models
            return [self._convert_db_error_to_ui_error(error) for error in db_errors]
        except Exception as e:
            logger.error(f"Error getting user errors: {str(e)}")
            return []
    
    # Study Streak Methods
    
    def get_user_streak(self, user_id: str) -> Optional[StudyStreak]:
        """
        Get the study streak for a user.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            The user's study streak if exists, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            
            # Get the streak from the database
            db_streak = self.db.query(DBStudyStreak).filter(DBStudyStreak.user_id == user_uuid).first()
            
            if not db_streak:
                return None
                
            return self._convert_db_streak_to_ui_streak(db_streak)
        except Exception as e:
            logger.error(f"Error getting user streak: {str(e)}")
            return None
    
    def _update_study_streak(self, user_uuid: uuid.UUID) -> Optional[DBStudyStreak]:
        """
        Update the study streak for a user when they study.
        
        Args:
            user_uuid: The UUID of the user
            
        Returns:
            The updated study streak
        """
        try:
            # Get the current date
            today = datetime.now().date()
            
            # Get the streak from the database
            db_streak = self.db.query(DBStudyStreak).filter(DBStudyStreak.user_id == user_uuid).first()
            
            if not db_streak:
                # Create a new streak
                db_streak = DBStudyStreak(
                    id=uuid.uuid4(),
                    user_id=user_uuid,
                    current_streak=1,
                    longest_streak=1,
                    last_study_date=datetime.now(),
                    streak_data={
                        "daily_records": [{
                            "date": datetime.now().isoformat(),
                            "minutes_studied": 0,
                            "topics_covered": [],
                            "achievements_earned": []
                        }],
                        "weekly_summary": {
                            "total_time": 0,
                            "topics_mastered": [],
                            "average_daily_time": 0
                        }
                    }
                )
                self.db.add(db_streak)
            else:
                # Update existing streak
                last_study = db_streak.last_study_date.date()
                
                # If last study was yesterday, increment streak
                if last_study == today - timedelta(days=1):
                    db_streak.current_streak += 1
                    if db_streak.current_streak > db_streak.longest_streak:
                        db_streak.longest_streak = db_streak.current_streak
                # If last study was not today but earlier, reset streak
                elif last_study != today:
                    db_streak.current_streak = 1
                
                # Update last study date
                db_streak.last_study_date = datetime.now()
                
                # Add new daily record
                streak_data = db_streak.streak_data
                daily_records = streak_data.get("daily_records", [])
                
                # Check if there's already a record for today
                today_record = None
                for record in daily_records:
                    record_date = date.fromisoformat(record["date"].split("T")[0])
                    if record_date == today:
                        today_record = record
                        break
                
                if not today_record:
                    # Add new record for today
                    daily_records.append({
                        "date": datetime.now().isoformat(),
                        "minutes_studied": 0,
                        "topics_covered": [],
                        "achievements_earned": []
                    })
                    streak_data["daily_records"] = daily_records
                    db_streak.streak_data = streak_data
            
            self.db.commit()
            self.db.refresh(db_streak)
            
            return db_streak
        except Exception as e:
            logger.error(f"Error updating study streak: {str(e)}")
            self.db.rollback()
            return None
    
    def update_streak_time(self, user_id: str, minutes: int) -> Optional[StudyStreak]:
        """
        Update the study time for a user's streak.
        
        Args:
            user_id: The ID of the user
            minutes: The minutes to add to the study time
            
        Returns:
            The updated study streak if successful, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            
            # Get the streak from the database
            db_streak = self.db.query(DBStudyStreak).filter(DBStudyStreak.user_id == user_uuid).first()
            
            if not db_streak:
                logger.warning(f"Streak not found for user: {user_id}")
                return None
            
            # Update the streak data
            today = datetime.now().date()
            streak_data = db_streak.streak_data
            daily_records = streak_data.get("daily_records", [])
            
            # Find today's record
            today_record = None
            for record in daily_records:
                record_date = date.fromisoformat(record["date"].split("T")[0])
                if record_date == today:
                    today_record = record
                    break
            
            if today_record:
                # Update minutes studied
                today_record["minutes_studied"] += minutes
                
                # Update weekly summary
                weekly_summary = streak_data.get("weekly_summary", {})
                weekly_summary["total_time"] = weekly_summary.get("total_time", 0) + minutes
                
                # Calculate average daily time
                week_start = today - timedelta(days=today.weekday())
                week_records = [r for r in daily_records if date.fromisoformat(r["date"].split("T")[0]) >= week_start]
                total_week_time = sum(r.get("minutes_studied", 0) for r in week_records)
                days_with_study = len(week_records)
                
                if days_with_study > 0:
                    weekly_summary["average_daily_time"] = total_week_time / days_with_study
                
                streak_data["weekly_summary"] = weekly_summary
                db_streak.streak_data = streak_data
                
                self.db.commit()
                self.db.refresh(db_streak)
            
            return self._convert_db_streak_to_ui_streak(db_streak)
        except Exception as e:
            logger.error(f"Error updating streak time: {str(e)}")
            self.db.rollback()
            return None
    
    # Conversion Methods
    
    def _convert_db_session_to_ui_session(self, db_session: DBLearningSession) -> LearningSession:
        """
        Convert a database learning session to a UI learning session.
        
        Args:
            db_session: The database learning session
            
        Returns:
            The corresponding UI learning session
        """
        return LearningSession(
            id=str(db_session.id),
            user_id=str(db_session.user_id),
            start_time=db_session.start_time,
            end_time=db_session.end_time,
            duration=db_session.duration,
            session_data=db_session.session_data,
            created_at=db_session.created_at,
            updated_at=db_session.updated_at
        )
    
    def _convert_db_error_to_ui_error(self, db_error: DBErrorLog) -> ErrorLog:
        """
        Convert a database error log to a UI error log.
        
        Args:
            db_error: The database error log
            
        Returns:
            The corresponding UI error log
        """
        return ErrorLog(
            id=str(db_error.id),
            user_id=str(db_error.user_id),
            lesson_id=str(db_error.lesson_id) if db_error.lesson_id else None,
            error_data=db_error.error_data,
            created_at=db_error.created_at,
            updated_at=db_error.updated_at
        )
    
    def _convert_db_streak_to_ui_streak(self, db_streak: DBStudyStreak) -> StudyStreak:
        """
        Convert a database study streak to a UI study streak.
        
        Args:
            db_streak: The database study streak
            
        Returns:
            The corresponding UI study streak
        """
        return StudyStreak(
            id=str(db_streak.id),
            user_id=str(db_streak.user_id),
            current_streak=db_streak.current_streak,
            longest_streak=db_streak.longest_streak,
            last_study_date=db_streak.last_study_date,
            streak_data=db_streak.streak_data,
            created_at=db_streak.created_at,
            updated_at=db_streak.updated_at
        ) 