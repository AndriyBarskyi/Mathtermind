"""
Mathtermind Exceptions

This module defines direct exception classes for Mathtermind.
For most exception handling, prefer using the classes in src.core.error_handling.
"""

from typing import Dict, List, Optional, Any
from src.core.error_handling.exceptions import ContentError, ValidationError, MathtermindError


class ContentValidationError(MathtermindError):
    """Exception raised when content validation fails."""
    
    def __init__(self, message: str = "Content validation failed", 
                 field_errors: Optional[Dict[str, List[str]]] = None,
                 content_id: Optional[str] = None, 
                 content_type: Optional[str] = None, 
                 validation_errors: Optional[List[str]] = None,
                 **kwargs):
        details = kwargs.get('details', {})
        if field_errors:
            details['field_errors'] = field_errors
        if validation_errors:
            details['validation_errors'] = validation_errors
        if content_type:
            details['content_type'] = content_type
        if content_id:
            details['content_id'] = content_id
            
        self.validation_errors = validation_errors or []
        self.content_type = content_type
        self.content_id = content_id
            
        # Initialize the base MathtermindError class directly
        super().__init__(
            message=message,

            error_code="CONTENT_VALIDATION_ERROR",
            details=details
        ) 