"""
Application State Management for Mathtermind

This module provides a central store for application state,
including user session, current user data, and other global state.
"""

import threading

# Global state dictionary with thread safety
_state = {}
_state_lock = threading.RLock()

def get(key, default=None):
    """
    Get a value from the application state.
    
    Args:
        key: The key to get
        default: The default value if key not found
        
    Returns:
        The value or default if not found
    """
    with _state_lock:
        return _state.get(key, default)

def set(key, value):
    """
    Set a value in the application state.
    
    Args:
        key: The key to set
        value: The value to set
        
    Returns:
        The value that was set
    """
    with _state_lock:
        _state[key] = value
        return value

def delete(key):
    """
    Delete a value from the application state.
    
    Args:
        key: The key to delete
        
    Returns:
        The value that was deleted, or None if the key was not found
    """
    with _state_lock:
        return _state.pop(key, None)

def clear():
    """
    Clear all values from the application state.
    """
    with _state_lock:
        _state.clear()

# User session management
def set_current_user(user_data):
    """
    Set the current user in the application state.
    
    Args:
        user_data: Dictionary containing user data
    """
    set('current_user', user_data)
    
def get_current_user():
    """
    Get the current user from the application state.
    
    Returns:
        Dictionary containing user data, or None if no user is logged in
    """
    return get('current_user')
    
def clear_current_user():
    """
    Clear the current user from the application state.
    """
    delete('current_user')
    
def is_authenticated():
    """
    Check if a user is currently authenticated.
    
    Returns:
        True if a user is logged in, False otherwise
    """
    return get_current_user() is not None 