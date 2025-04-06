"""
Session management service for Mathtermind.

This module provides utilities for managing user sessions,
including creating, validating, and destroying sessions.
"""

import uuid
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Union
import secrets
from contextlib import contextmanager

# Try to import Redis, fall back to in-memory storage if not available
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

# Session configuration
SESSION_EXPIRY = 3600  # 1 hour in seconds
SESSION_COOKIE_NAME = "mathtermind_session"
TOKEN_LENGTH = 32

# Set up logging
logger = logging.getLogger(__name__)

class SessionManager:
    """
    Manages user sessions for the application.
    
    This service handles creating, validating, and destroying user sessions.
    It can use Redis for persistent storage if available, or fallback to
    in-memory storage.
    """
    
    def __init__(self, use_redis: bool = True, redis_url: str = "redis://localhost:6379/0"):
        """
        Initialize the session manager.
        
        Args:
            use_redis: Whether to use Redis for session storage
            redis_url: The Redis connection URL
        """
        self.use_redis = use_redis and REDIS_AVAILABLE
        self._in_memory_sessions = {}  # Fallback storage
        
        if self.use_redis:
            try:
                self.redis = redis.from_url(redis_url)
                # Test connection
                self.redis.ping()
                logger.info("Using Redis for session storage")
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                self.use_redis = False
                logger.info("Falling back to in-memory session storage")
        else:
            logger.info("Using in-memory session storage")
    
    def create_session(self, user_id: str, user_data: Dict[str, Any] = None, 
                      expiry: int = SESSION_EXPIRY) -> str:
        """
        Create a new session for a user.
        
        Args:
            user_id: The user ID
            user_data: Additional user data to store in the session
            expiry: Session expiry time in seconds
            
        Returns:
            A session token
        """
        # Generate a secure random token
        token = secrets.token_hex(TOKEN_LENGTH)
        
        # Create session data
        session_data = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(seconds=expiry)).isoformat(),
            "data": user_data or {}
        }
        
        # Store the session
        if self.use_redis:
            self.redis.setex(
                f"session:{token}", 
                expiry,
                json.dumps(session_data)
            )
        else:
            self._in_memory_sessions[token] = session_data
            # Set expiry for in-memory sessions by scheduling cleanup
            # (In a real app, you'd use a dedicated cleanup thread)
        
        return token
    
    def get_session(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Get a session by token.
        
        Args:
            token: The session token
            
        Returns:
            The session data or None if not found or expired
        """
        if not token:
            return None
            
        # Get the session
        if self.use_redis:
            session_json = self.redis.get(f"session:{token}")
            if not session_json:
                return None
            session_data = json.loads(session_json)
        else:
            session_data = self._in_memory_sessions.get(token)
            if not session_data:
                return None
                
            # Check if expired for in-memory sessions
            expiry_time = datetime.fromisoformat(session_data["expires_at"])
            if expiry_time < datetime.now():
                self._in_memory_sessions.pop(token, None)
                return None
        
        return session_data
    
    def validate_session(self, token: str) -> Optional[str]:
        """
        Validate a session token and return the user ID.
        
        Args:
            token: The session token
            
        Returns:
            The user ID if the session is valid, None otherwise
        """
        session = self.get_session(token)
        if not session:
            return None
        
        return session["user_id"]
    
    def extend_session(self, token: str, expiry: int = SESSION_EXPIRY) -> bool:
        """
        Extend a session's expiry time.
        
        Args:
            token: The session token
            expiry: New expiry time in seconds
            
        Returns:
            True if the session was extended, False otherwise
        """
        session_data = self.get_session(token)
        if not session_data:
            return False
            
        # Update expiry
        session_data["expires_at"] = (datetime.now() + timedelta(seconds=expiry)).isoformat()
        
        # Store updated session
        if self.use_redis:
            self.redis.setex(
                f"session:{token}", 
                expiry,
                json.dumps(session_data)
            )
        else:
            self._in_memory_sessions[token] = session_data
            
        return True
    
    def destroy_session(self, token: str) -> bool:
        """
        Destroy a session.
        
        Args:
            token: The session token
            
        Returns:
            True if the session was destroyed, False if it didn't exist
        """
        if not token:
            return False
            
        if self.use_redis:
            result = self.redis.delete(f"session:{token}")
            return result > 0
        else:
            if token in self._in_memory_sessions:
                del self._in_memory_sessions[token]
                return True
            return False
    
    def destroy_all_user_sessions(self, user_id: str) -> int:
        """
        Destroy all sessions for a user.
        
        Args:
            user_id: The user ID
            
        Returns:
            The number of sessions destroyed
        """
        if self.use_redis:
            # This is inefficient for Redis but works
            # Ideally, you'd use a secondary index
            keys = self.redis.keys("session:*")
            count = 0
            
            for key in keys:
                session_json = self.redis.get(key)
                if session_json:
                    try:
                        session_data = json.loads(session_json)
                        if session_data.get("user_id") == user_id:
                            self.redis.delete(key)
                            count += 1
                    except json.JSONDecodeError:
                        continue
            
            return count
        else:
            # For in-memory, we can do this more efficiently
            count = 0
            tokens_to_remove = []
            
            for token, session_data in self._in_memory_sessions.items():
                if session_data.get("user_id") == user_id:
                    tokens_to_remove.append(token)
                    count += 1
            
            for token in tokens_to_remove:
                del self._in_memory_sessions[token]
                
            return count
    
    def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired sessions (mainly for in-memory storage).
        
        Returns:
            The number of sessions cleaned up
        """
        if self.use_redis:
            # Redis handles expiry automatically
            return 0
        else:
            count = 0
            now = datetime.now()
            tokens_to_remove = []
            
            for token, session_data in self._in_memory_sessions.items():
                expiry_time = datetime.fromisoformat(session_data["expires_at"])
                if expiry_time < now:
                    tokens_to_remove.append(token)
                    count += 1
            
            for token in tokens_to_remove:
                del self._in_memory_sessions[token]
                
            return count
            
    @contextmanager
    def session_context(self, token: str):
        """
        Context manager for session operations.
        
        This automatically extends the session lifetime on entry and
        provides the session data.
        
        Args:
            token: The session token
            
        Yields:
            The session data or None if not valid
        """
        session_data = self.get_session(token)
        if session_data:
            self.extend_session(token)
            
        try:
            yield session_data
        finally:
            pass  # No cleanup needed 