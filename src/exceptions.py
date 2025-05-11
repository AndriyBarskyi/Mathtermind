"""
Mathtermind Exceptions

This module defines direct exception classes for Mathtermind.
For most exception handling, prefer using the classes in src.core.error_handling.
"""

from typing import Dict, List, Optional, Any
from src.core.error_handling.exceptions import ContentError, ValidationError


class ContentValidationError(ContentError, ValidationError):
    """Exception raised when content validation fails."""
    
    def __init__(self, message: str = "Content validation failed", 
                 field_errors: Optional[Dict[str, List[str]]] = None,
                 content_id: Optional[str] = None, 
                 content_type: Optional[str] = None, **kwargs):
        details = kwargs.get('details', {})
        if field_errors:
            details['field_errors'] = field_errors
        kwargs['details'] = details
        
        # Set error code
        kwargs['error_code'] = "CONTENT_VALIDATION_ERROR"
        
        # Initialize both parent classes
        ContentError.__init__(
            self, 
            message=message, 
            content_id=content_id, 
            content_type=content_type, 
            **kwargs
        ) 