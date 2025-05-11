"""
Interactive Content Handler Service for Mathtermind.

This module provides specialized handling for interactive content types, enabling
state persistence, event tracking, and validation of interactive elements.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
import uuid
import logging
from datetime import datetime, timezone

from src.db import get_db
from src.db.repositories import (
    ContentStateRepository,
    ContentRepository,
    ProgressRepository,
    UserContentProgressRepository
)
from src.models.content import InteractiveContent
from src.core.error_handling.exceptions import ValidationError, ResourceNotFoundError

# Set up logging
logger = logging.getLogger(__name__)

# Constants for state types
STATE_INTERACTION_DATA = "interaction_data"
STATE_INTERACTION_HISTORY = "interaction_history"
STATE_INTERACTION_POSITION = "interaction_position"
STATE_CURRENT_STEP = "current_step"
STATE_COMPLETION_STATUS = "completion_status"
STATE_USER_INPUT = "user_input"


class InteractiveContentHandlerService:
    """
    Service for handling interactive content elements in Mathtermind.
    
    This service manages:
    - State persistence for interactive content
    - Event tracking for user interactions
    - Validation of interactive content elements
    - Resumption of interrupted interactive activities
    """
    
    def __init__(self):
        """Initialize the interactive content handler service."""
        self.db = next(get_db())
        self.content_state_repo = ContentStateRepository()
        self.content_repo = ContentRepository()
        self.progress_repo = ProgressRepository()
        self.user_content_progress_repo = UserContentProgressRepository()
    
    def get_content_state(self, 
                         user_id: str, 
                         content_id: str, 
                         state_type: str) -> Optional[Dict[str, Any]]:
        """
        Get the state of an interactive content item.
        
        Args:
            user_id: User ID
            content_id: Content ID
            state_type: Type of state to retrieve
            
        Returns:
            State data if found, None otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            content_uuid = uuid.UUID(content_id)
            
            # Get the content state
            content_state = self.content_state_repo.get_content_state(
                self.db, user_uuid, content_uuid, state_type
            )
            
            if not content_state:
                return None
                
            # Return the appropriate value based on state type
            if content_state.json_value is not None:
                return content_state.json_value
            elif content_state.numeric_value is not None:
                return {"value": content_state.numeric_value}
            elif content_state.text_value is not None:
                return {"value": content_state.text_value}
                
            return None
        except Exception as e:
            logger.error(f"Error getting content state: {str(e)}")
            return None
    
    def save_content_state(self, 
                          user_id: str, 
                          content_id: str, 
                          state_type: str,
                          state_value: Union[Dict[str, Any], float, str]) -> bool:
        """
        Save the state of an interactive content item.
        
        Args:
            user_id: User ID
            content_id: Content ID
            state_type: Type of state to save
            state_value: The state data to save
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            content_uuid = uuid.UUID(content_id)
            
            # Get the progress record for the user and course containing this content
            content = self.content_repo.get_by_id(self.db, content_uuid)
            if not content:
                logger.warning(f"Content not found with ID: {content_id}")
                return False
                
            lesson_id = content.lesson_id
            
            # Get course ID from lesson
            lesson = self.content_repo.get_lesson_by_id(self.db, uuid.UUID(lesson_id))
            if not lesson:
                logger.warning(f"Lesson not found with ID: {lesson_id}")
                return False
                
            course_id = lesson.course_id
            
            # Get progress record
            progress = self.progress_repo.get_course_progress(
                self.db, user_uuid, course_id
            )
            if not progress:
                logger.warning(f"Progress record not found for user {user_id} in course {course_id}")
                return False
            
            # Update or create the content state
            try:
                self.content_state_repo.update_or_create_state(
                    self.db, user_uuid, progress.id, content_uuid, state_type, state_value
                )
                return True
            except Exception as e:
                logger.error(f"Error saving content state: {str(e)}")
                self.db.rollback()
                return False
                
        except Exception as e:
            logger.error(f"Error in save_content_state: {str(e)}")
            return False
    
    def get_all_states(self, 
                      user_id: str, 
                      content_id: str) -> Dict[str, Any]:
        """
        Get all state data for an interactive content item.
        
        Args:
            user_id: User ID
            content_id: Content ID
            
        Returns:
            Dictionary mapping state types to their values
        """
        try:
            user_uuid = uuid.UUID(user_id)
            content_uuid = uuid.UUID(content_id)
            
            # Get all states for this content
            content_states = self.content_state_repo.get_all_content_states(
                self.db, user_uuid, content_uuid
            )
            
            # Build result dictionary
            result = {}
            for state in content_states:
                if state.json_value is not None:
                    result[state.state_type] = state.json_value
                elif state.numeric_value is not None:
                    result[state.state_type] = state.numeric_value
                elif state.text_value is not None:
                    result[state.state_type] = state.text_value
            
            return result
        except Exception as e:
            logger.error(f"Error getting all content states: {str(e)}")
            return {}
    
    def clear_content_state(self, 
                           user_id: str, 
                           content_id: str, 
                           state_type: Optional[str] = None) -> bool:
        """
        Clear the state of an interactive content item.
        
        Args:
            user_id: User ID
            content_id: Content ID
            state_type: Type of state to clear, or None to clear all states
            
        Returns:
            True if cleared successfully, False otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            content_uuid = uuid.UUID(content_id)
            
            if state_type:
                # Clear specific state type
                state = self.content_state_repo.get_content_state(
                    self.db, user_uuid, content_uuid, state_type
                )
                if state:
                    self.db.delete(state)
                    self.db.commit()
            else:
                # Clear all states
                states = self.content_state_repo.get_all_content_states(
                    self.db, user_uuid, content_uuid
                )
                for state in states:
                    self.db.delete(state)
                self.db.commit()
            
            return True
        except Exception as e:
            logger.error(f"Error clearing content state: {str(e)}")
            self.db.rollback()
            return False
    
    def record_interaction_event(self, 
                                user_id: str, 
                                content_id: str, 
                                event_type: str,
                                event_data: Dict[str, Any]) -> bool:
        """
        Record an interaction event for an interactive content item.
        
        This adds to the interaction history for the content.
        
        Args:
            user_id: User ID
            content_id: Content ID
            event_type: Type of interaction event
            event_data: Data associated with the event
            
        Returns:
            True if recorded successfully, False otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            content_uuid = uuid.UUID(content_id)
            
            # Get current interaction history
            history_state = self.get_content_state(
                user_id, content_id, STATE_INTERACTION_HISTORY
            )
            
            history = history_state if history_state else {"events": []}
            
            # Add new event
            event = {
                "type": event_type,
                "data": event_data,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            history["events"].append(event)
            
            # Save updated history
            return self.save_content_state(
                user_id, content_id, STATE_INTERACTION_HISTORY, history
            )
        except Exception as e:
            logger.error(f"Error recording interaction event: {str(e)}")
            return False
    
    def update_completion_progress(self, 
                                  user_id: str, 
                                  content_id: str,
                                  progress_percentage: float,
                                  is_completed: bool = False) -> bool:
        """
        Update the completion progress for an interactive content item.
        
        Args:
            user_id: User ID
            content_id: Content ID
            progress_percentage: Percentage of completion (0-100)
            is_completed: Whether the content is fully completed
            
        Returns:
            True if updated successfully, False otherwise
        """
        try:
            user_uuid = uuid.UUID(user_id)
            content_uuid = uuid.UUID(content_id)
            
            # Update user content progress
            progress = self.user_content_progress_repo.get_progress(
                self.db, user_uuid, content_uuid
            )
            
            if progress:
                updates = {
                    "status": "completed" if is_completed else "in_progress",
                    "percentage": progress_percentage
                }
                
                # Update the last interaction time
                updates["last_interaction"] = datetime.now(timezone.utc)
                
                # Update content progress
                self.user_content_progress_repo.update_progress(
                    self.db, progress.id, updates
                )
            else:
                # Create new progress record
                self.user_content_progress_repo.create_progress(
                    self.db,
                    user_id=user_uuid,
                    content_id=content_uuid,
                    status="completed" if is_completed else "in_progress",
                    percentage=progress_percentage,
                    last_interaction=datetime.now(timezone.utc)
                )
            
            # Also save the state
            completion_state = {
                "percentage": progress_percentage,
                "is_completed": is_completed,
                "last_updated": datetime.now(timezone.utc).isoformat()
            }
            
            return self.save_content_state(
                user_id, content_id, STATE_COMPLETION_STATUS, completion_state
            )
        except Exception as e:
            logger.error(f"Error updating completion progress: {str(e)}")
            self.db.rollback()
            return False
    
    def get_interactive_content(self, content_id: str) -> Optional[InteractiveContent]:
        """
        Get interactive content by ID.
        
        Args:
            content_id: Content ID
            
        Returns:
            Interactive content if found, None otherwise
        """
        try:
            content_uuid = uuid.UUID(content_id)
            
            # Get the content
            db_content = self.content_repo.get_by_id(self.db, content_uuid)
            
            if not db_content or db_content.content_type != "interactive":
                return None
                
            # Convert to UI model
            content = InteractiveContent(
                id=str(db_content.id),
                title=db_content.title,
                content_type=db_content.content_type,
                order=db_content.order,
                lesson_id=str(db_content.lesson_id),
                description=db_content.description,
                estimated_time=db_content.estimated_time,
                created_at=db_content.created_at,
                updated_at=db_content.updated_at,
                metadata=db_content.metadata or {},
                interaction_type=db_content.interactive_type,
                interaction_data=db_content.data.get("interaction_data", {}),
                instructions=db_content.data.get("instructions")
            )
            
            return content
        except Exception as e:
            logger.error(f"Error getting interactive content: {str(e)}")
            return None
    
    def validate_interactive_content(self, content: InteractiveContent) -> List[str]:
        """
        Validate interactive content for correctness.
        
        Args:
            content: Interactive content to validate
            
        Returns:
            List of validation errors, empty if no errors
        """
        errors = []
        
        # Check required fields
        if not content.interaction_type:
            errors.append("Interaction type is required")
        
        if not content.interaction_data:
            errors.append("Interaction data is required")
        
        # Validate based on interaction type
        if content.interaction_type == "simulation":
            if "simulation_config" not in content.interaction_data:
                errors.append("Simulation configuration is required for simulation type")
        
        elif content.interaction_type == "interactive_exercise":
            if "exercise_data" not in content.interaction_data:
                errors.append("Exercise data is required for interactive exercise type")
            if "verification_criteria" not in content.interaction_data:
                errors.append("Verification criteria is required for interactive exercise type")
        
        elif content.interaction_type == "visualization":
            if "visualization_data" not in content.interaction_data:
                errors.append("Visualization data is required for visualization type")
        
        return errors
    
    def verify_interaction_completion(self, 
                                    user_id: str, 
                                    content_id: str) -> Tuple[bool, str]:
        """
        Verify whether an interactive content interaction is completed correctly.
        
        This evaluates the current state against completion criteria.
        
        Args:
            user_id: User ID
            content_id: Content ID
            
        Returns:
            Tuple of (is_completed, feedback_message)
        """
        try:
            # Get the content
            content = self.get_interactive_content(content_id)
            if not content:
                return False, "Content not found"
            
            # Get current state
            current_state = self.get_all_states(user_id, content_id)
            
            # Get interaction data
            interaction_data = content.interaction_data
            
            # Check if verification criteria exists
            if "verification_criteria" not in interaction_data:
                # If no verification criteria, check for completion status
                completion_status = current_state.get(STATE_COMPLETION_STATUS, {})
                if isinstance(completion_status, dict) and completion_status.get("is_completed", False):
                    return True, "Activity marked as completed"
                return False, "No verification criteria available"
            
            # Extract verification criteria
            criteria = interaction_data["verification_criteria"]
            
            # Evaluate each criterion
            all_criteria_met = True
            feedback = []
            
            if "required_states" in criteria:
                for state_key, expected_value in criteria["required_states"].items():
                    if state_key not in current_state:
                        all_criteria_met = False
                        feedback.append(f"Missing required state: {state_key}")
                    elif current_state[state_key] != expected_value:
                        all_criteria_met = False
                        feedback.append(f"State '{state_key}' does not match expected value")
            
            if "required_events" in criteria:
                event_history = current_state.get(STATE_INTERACTION_HISTORY, {}).get("events", [])
                event_types = [event["type"] for event in event_history]
                
                for required_event in criteria["required_events"]:
                    if required_event not in event_types:
                        all_criteria_met = False
                        feedback.append(f"Missing required interaction: {required_event}")
            
            if "custom_criteria" in criteria and criteria["custom_criteria"] == "steps_completed":
                total_steps = criteria.get("total_steps", 1)
                current_step = current_state.get(STATE_CURRENT_STEP, {}).get("value", 0)
                
                if current_step < total_steps:
                    all_criteria_met = False
                    feedback.append(f"Not all steps completed: {current_step}/{total_steps}")
            
            # Update completion status
            if all_criteria_met:
                self.update_completion_progress(user_id, content_id, 100.0, True)
                return True, "All completion criteria met"
            else:
                # Calculate approximate percentage based on feedback
                if feedback:
                    percentage = (1 - (len(feedback) / len(criteria))) * 100
                    percentage = max(0, min(99, percentage))  # Cap at 99% until all criteria met
                    self.update_completion_progress(user_id, content_id, percentage, False)
                
                return False, "; ".join(feedback)
        except Exception as e:
            logger.error(f"Error verifying interaction completion: {str(e)}")
            return False, f"Error during verification: {str(e)}"
    
    def resume_interactive_content(self, 
                                 user_id: str, 
                                 content_id: str) -> Dict[str, Any]:
        """
        Get all data needed to resume an interactive content session.
        
        Args:
            user_id: User ID
            content_id: Content ID
            
        Returns:
            Dictionary with content and state information
        """
        try:
            # Get the content
            content = self.get_interactive_content(content_id)
            if not content:
                return {"error": "Content not found", "success": False}
            
            # Get all states
            states = self.get_all_states(user_id, content_id)
            
            # Get content progress
            user_uuid = uuid.UUID(user_id)
            content_uuid = uuid.UUID(content_id)
            progress = self.user_content_progress_repo.get_progress(
                self.db, user_uuid, content_uuid
            )
            
            progress_data = None
            if progress:
                progress_data = {
                    "status": progress.status,
                    "percentage": progress.percentage if hasattr(progress, "percentage") else None,
                    "score": progress.score,
                    "time_spent": progress.time_spent,
                    "last_interaction": progress.last_interaction.isoformat() if progress.last_interaction else None
                }
            
            # Record resume event
            self.record_interaction_event(
                user_id, 
                content_id, 
                "resume", 
                {"timestamp": datetime.now(timezone.utc).isoformat()}
            )
            
            # Return combined data
            return {
                "success": True,
                "content": {
                    "id": content.id,
                    "title": content.title,
                    "interaction_type": content.interaction_type,
                    "interaction_data": content.interaction_data,
                    "instructions": content.instructions,
                    "metadata": content.metadata
                },
                "saved_state": states,
                "progress": progress_data
            }
        except Exception as e:
            logger.error(f"Error resuming interactive content: {str(e)}")
            return {"error": str(e), "success": False} 