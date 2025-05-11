"""
Content Validation Service for Mathtermind.

This service handles validation of content items across different content types.
"""

from typing import List, Dict, Any, Optional, Set, Tuple
import logging
import json
import uuid

from src.services.content_type_registry import ContentTypeRegistry
from src.models.content import Content
from src.core.error_handling.exceptions import ContentError

# Set up logging
logger = logging.getLogger(__name__)


class ContentValidationService:
    """Service for validating content against schema and business rules."""
    
    def __init__(self):
        """Initialize the validation service."""
        self.type_registry = ContentTypeRegistry()
        
    def validate_content(self, content: Content) -> Tuple[bool, List[str]]:
        """
        Validate content against its type's schema and business rules.
        
        Args:
            content: The content to validate
            
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        # Get type-specific errors from the registry
        type_errors = self.type_registry.validate_content(content)
        if type_errors:
            errors.extend(type_errors)
            
        # Add additional validations beyond the basic type validation
        errors.extend(self._validate_additional_rules(content))
            
        return (len(errors) == 0, errors)
    
    def validate_content_structure(self, content_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate the structure of content data (before creating a Content object).
        
        Args:
            content_data: Dictionary of content data
            
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        # Validate required fields
        required_fields = ["title", "content_type", "lesson_id", "order"]
        for field in required_fields:
            if field not in content_data:
                errors.append(f"Missing required field: {field}")
                
        if not errors:
            # If content_type is present, check additional requirements
            content_type = content_data.get("content_type")
            if content_type:
                # Get the type info
                type_info = self.type_registry.get_content_type(content_type)
                if not type_info:
                    errors.append(f"Unknown content type: {content_type}")
                else:
                    # Check type-specific required fields
                    if content_type == "theory" and "text_content" not in content_data:
                        errors.append("Missing required field for theory content: text_content")
                    elif content_type == "exercise" and "problem_statement" not in content_data:
                        errors.append("Missing required field for exercise content: problem_statement")
                    elif content_type in ["quiz", "assessment"] and "questions" not in content_data:
                        errors.append(f"Missing required field for {content_type} content: questions")
                    elif content_type == "interactive":
                        if "interaction_type" not in content_data:
                            errors.append("Missing required field for interactive content: interaction_type")
                        if "interaction_data" not in content_data:
                            errors.append("Missing required field for interactive content: interaction_data")
                    elif content_type == "resource":
                        if "resource_type" not in content_data:
                            errors.append("Missing required field for resource content: resource_type")
                        if "resource_url" not in content_data:
                            errors.append("Missing required field for resource content: resource_url")
            
        return (len(errors) == 0, errors)
    
    def validate_content_update(self, current_content: Content, updates: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate updates to an existing content item.
        
        Args:
            current_content: The current content
            updates: The updates to apply
            
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        # Create a copy of the content with updates applied to validate the result
        updated_content = self._apply_updates_to_content(current_content, updates)
        
        if updated_content:
            # Validate the updated content
            _, validation_errors = self.validate_content(updated_content)
            errors.extend(validation_errors)
        else:
            errors.append("Failed to apply updates to content for validation")
            
        return (len(errors) == 0, errors)
    
    def validate_content_references(self, content: Content, references: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        """
        Validate external references in content (links, resources, etc.)
        
        Args:
            content: The content to validate
            references: List of reference dictionaries
            
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        # Each reference should have a type and a url at minimum
        for i, ref in enumerate(references):
            if "type" not in ref:
                errors.append(f"Reference #{i+1} is missing a type")
            if "url" not in ref:
                errors.append(f"Reference #{i+1} is missing a URL")
            
            # If it's a citation, ensure it has the required fields
            if ref.get("type") == "citation" and "citation_text" not in ref:
                errors.append(f"Citation reference #{i+1} is missing citation text")
                
        return (len(errors) == 0, errors)
    
    def validate_content_metadata(self, content_type: str, metadata: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate metadata for a specific content type against its schema.
        
        Args:
            content_type: The type of content
            metadata: The metadata to validate
            
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        # Get the type info and schema
        type_info = self.type_registry.get_content_type(content_type)
        if not type_info:
            errors.append(f"Unknown content type: {content_type}")
            return (False, errors)
            
        # If there's no schema, all metadata is valid
        if not type_info.metadata_schema:
            return (True, [])
            
        # Simple schema validation using JSON Schema structure
        schema = type_info.metadata_schema
        
        # Validate required properties
        if "required" in schema:
            for field in schema["required"]:
                if field not in metadata:
                    errors.append(f"Missing required metadata field: {field}")
        
        # Validate property types and enums
        if "properties" in schema:
            for prop_name, prop_schema in schema["properties"].items():
                if prop_name in metadata:
                    value = metadata[prop_name]
                    
                    # Type checking
                    if "type" in prop_schema:
                        expected_type = prop_schema["type"]
                        if expected_type == "string" and not isinstance(value, str):
                            errors.append(f"Metadata field '{prop_name}' should be a string")
                        elif expected_type == "number" and not isinstance(value, (int, float)):
                            errors.append(f"Metadata field '{prop_name}' should be a number")
                        elif expected_type == "integer" and not isinstance(value, int):
                            errors.append(f"Metadata field '{prop_name}' should be an integer")
                        elif expected_type == "boolean" and not isinstance(value, bool):
                            errors.append(f"Metadata field '{prop_name}' should be a boolean")
                        elif expected_type == "array" and not isinstance(value, list):
                            errors.append(f"Metadata field '{prop_name}' should be an array")
                        elif expected_type == "object" and not isinstance(value, dict):
                            errors.append(f"Metadata field '{prop_name}' should be an object")
                    
                    # Enum validation
                    if "enum" in prop_schema and value not in prop_schema["enum"]:
                        allowed_values = ", ".join(str(v) for v in prop_schema["enum"])
                        errors.append(f"Metadata field '{prop_name}' should be one of: {allowed_values}")
                        
                    # Pattern validation
                    if "pattern" in prop_schema and isinstance(value, str):
                        import re
                        pattern = re.compile(prop_schema["pattern"])
                        if not pattern.match(value):
                            errors.append(f"Metadata field '{prop_name}' does not match required pattern")
                            
        return (len(errors) == 0, errors)
    
    def _validate_additional_rules(self, content: Content) -> List[str]:
        """
        Apply additional validation rules beyond the basic type validation.
        
        Args:
            content: The content to validate
            
        Returns:
            List of error messages
        """
        errors = []
        
        # Add cross-field validations here
        
        # Title length constraints
        if len(content.title) < 3:
            errors.append("Title is too short (minimum 3 characters)")
        elif len(content.title) > 255:
            errors.append("Title is too long (maximum 255 characters)")
        
        # Check that order is a positive number
        if content.order < 0:
            errors.append("Order must be a positive number")
            
        # If there's an estimated time, ensure it's positive
        if hasattr(content, 'estimated_time') and content.estimated_time < 0:
            errors.append("Estimated time must be a positive number")
            
        # Content type specific validations
        if content.content_type == "quiz" or content.content_type == "assessment":
            if hasattr(content, 'passing_score'):
                if content.passing_score < 0 or content.passing_score > 100:
                    errors.append("Passing score must be between 0 and 100")
                    
        # For assessment content, time limit should be positive if present
        if content.content_type == "assessment" and hasattr(content, 'time_limit'):
            if content.time_limit is not None and content.time_limit <= 0:
                errors.append("Time limit must be a positive number")
                
        return errors
    
    def _apply_updates_to_content(self, content: Content, updates: Dict[str, Any]) -> Optional[Content]:
        """
        Create a copy of content with updates applied for validation purposes.
        
        Args:
            content: The current content
            updates: The updates to apply
            
        Returns:
            Updated content object or None if update fails
        """
        try:
            # Create a shallow copy of the content
            import copy
            content_copy = copy.copy(content)
            
            # Apply the updates
            for key, value in updates.items():
                if hasattr(content_copy, key):
                    setattr(content_copy, key, value)
                    
            return content_copy
        except Exception as e:
            logger.error(f"Error applying updates to content: {str(e)}")
            return None 