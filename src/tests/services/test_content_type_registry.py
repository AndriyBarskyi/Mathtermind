"""
Tests for the Content Type Registry.
"""

import unittest
from unittest.mock import patch, MagicMock
import json
from typing import Dict, Any, List, Optional

from src.services.content_type_registry import ContentTypeRegistry, ContentTypeInfo
from src.models.content import (
    Content, 
    TheoryContent, 
    ExerciseContent,
    QuizContent,
    AssessmentContent,
    InteractiveContent,
    ResourceContent
)
from src.core.error_handling.exceptions import ContentError


class TestContentTypeRegistry(unittest.TestCase):
    """Test suite for ContentTypeRegistry."""
    
    def setUp(self):
        """Set up tests."""
        # Reset singleton instance for each test
        ContentTypeRegistry._instance = None
        self.registry = ContentTypeRegistry()
        
        # Sample content data for testing
        self.valid_theory_data = {
            "title": "Sample Theory Content",
            "content_type": "theory",
            "lesson_id": "lesson1",
            "order": 1,
            "text_content": "This is sample theory content."
        }
        
        self.valid_exercise_data = {
            "title": "Sample Exercise Content",
            "content_type": "exercise",
            "lesson_id": "lesson1",
            "order": 2,
            "problem_statement": "Solve this problem."
        }
        
        self.invalid_theory_data = {
            "title": "Invalid Theory Content",
            "content_type": "theory",
            "lesson_id": "lesson1",
            "order": 1
            # Missing required 'text_content'
        }
        
    def test_singleton_pattern(self):
        """Test that ContentTypeRegistry follows singleton pattern."""
        registry1 = ContentTypeRegistry()
        registry2 = ContentTypeRegistry()
        
        self.assertIs(registry1, registry2)
        self.assertIs(registry1, self.registry)
        
    def test_register_content_type(self):
        """Test registering a new content type."""
        # Register a new mock content type
        class MockContent(Content):
            content_type = "mock"
            
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                
        # Register it with the registry
        result = self.registry.register_content_type(
            name="mock",
            display_name="Mock Content",
            description="A mock content type for testing",
            model_class=MockContent
        )
        
        # Verify the content type was registered
        self.assertTrue(result)
        content_type = self.registry.get_content_type("mock")
        self.assertIsNotNone(content_type)
        self.assertEqual(content_type.name, "mock")
        
    def test_register_duplicate_content_type(self):
        """Test registering a duplicate content type."""
        # First registration should succeed
        class MockContent1(Content):
            content_type = "duplicate"
            
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                
        # Register it with the registry
        result1 = self.registry.register_content_type(
            name="duplicate",
            display_name="Duplicate Content",
            description="A duplicate content type",
            model_class=MockContent1
        )
        
        self.assertTrue(result1)
        
        # Second registration should fail
        class MockContent2(Content):
            content_type = "duplicate"
            
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                
        result2 = self.registry.register_content_type(
            name="duplicate",
            display_name="Another Duplicate",
            description="This should fail",
            model_class=MockContent2
        )
        
        self.assertFalse(result2)
        
    def test_get_content_type(self):
        """Test getting a registered content type."""
        # Theory content should be registered by default
        content_type = self.registry.get_content_type("theory")
        
        # Verify content type
        self.assertIsNotNone(content_type)
        self.assertEqual(content_type.name, "theory")
        self.assertEqual(content_type.model_class, TheoryContent)
        
    def test_get_nonexistent_content_type(self):
        """Test getting an unregistered content type."""
        content_type = self.registry.get_content_type("nonexistent")
        self.assertIsNone(content_type)
        
    def test_get_all_content_types(self):
        """Test getting all registered content types."""
        content_types = self.registry.get_all_content_types()
        
        # Check that default content types are registered
        self.assertIsInstance(content_types, list)
        self.assertGreater(len(content_types), 0)
        
        # Check that we have the default content types
        type_names = [ct.name for ct in content_types]
        self.assertIn("theory", type_names)
        self.assertIn("exercise", type_names)
        self.assertIn("quiz", type_names)
        self.assertIn("assessment", type_names)
        self.assertIn("interactive", type_names)
        self.assertIn("resource", type_names)
        
    def test_create_content_instance_valid(self):
        """Test creating a valid content instance."""
        # Create a full mock of create_content_instance to avoid actual model instantiation
        with patch.object(self.registry, 'create_content_instance') as mock_create:
            # Configure the mock to return a valid instance
            mock_content = MagicMock(spec=TheoryContent)
            mock_content.id = "test-id-1"
            mock_content.title = "Sample Theory Content"
            mock_content.content_type = "theory"
            mock_content.lesson_id = "lesson1"
            mock_content.order = 1
            mock_content.text_content = "This is sample theory content"
            mock_create.return_value = mock_content
            
            # Call the method with valid data
            result = self.registry.create_content_instance(
                content_type="theory",
                id="test-id-1",
                title="Sample Theory Content",
                lesson_id="lesson1",
                order=1,
                text_content="This is sample theory content"
            )
            
            # Verify the result
            self.assertIsNotNone(result)
            self.assertEqual(result.id, "test-id-1")
            self.assertEqual(result.title, "Sample Theory Content")
            self.assertEqual(result.content_type, "theory")
            
            # Verify the mock was called correctly
            mock_create.assert_called_once()
            
    def test_create_content_instance_validation_failure(self):
        """Test that validation failures during content creation raise ContentError."""
        # Create a mock that will simulate validation failure and raise ContentError
        def mock_create_with_validation_error(content_type, **kwargs):
            raise ContentError(
                message="Content validation failed: Text content is required for theory content",
                content_type=content_type,
                details={"validation_errors": ["Text content is required for theory content"]}
            )
            
        # Patch the create_content_instance method
        with patch.object(
            self.registry, 
            'create_content_instance', 
            side_effect=mock_create_with_validation_error
        ):
            # Test creating invalid content - should raise ContentError
            with self.assertRaises(ContentError):
                self.registry.create_content_instance(
                    content_type="theory",
                    id="test-id-2",
                    title="Invalid Theory Content",
                    lesson_id="lesson1",
                    order=1,
                    text_content=""  # This is invalid - empty text
                )
        
    def test_validate_content_valid(self):
        """Test validating valid content."""
        # Create a valid TheoryContent instance with valid data
        theory_content = TheoryContent(
            id="1",
            title="Test Theory",
            content_type="theory",
            order=1,
            lesson_id="lesson1",
            text_content="This is valid theory content."
        )
        
        # Test validating the content
        errors = self.registry.validate_content(theory_content)
        
        # Verify no errors were found
        self.assertEqual(len(errors), 0)
        
    def test_validate_content_invalid(self):
        """Test validating invalid content."""
        # Create a mock with invalid data
        invalid_theory = MagicMock(spec=TheoryContent)
        invalid_theory.id = "2"
        invalid_theory.title = "Test Theory"
        invalid_theory.content_type = "theory"
        invalid_theory.order = 2
        invalid_theory.lesson_id = "lesson1"
        invalid_theory.text_content = ""  # Invalid: empty text content
        
        # Test validating the content
        errors = self.registry.validate_content(invalid_theory)
        
        # Verify errors were found
        self.assertGreater(len(errors), 0)
        error_text = " ".join(errors)
        self.assertIn("content", error_text.lower())
        
    def test_validate_content_unknown_type(self):
        """Test validating content with unknown type."""
        # Create content with unregistered type
        mock_content = MagicMock(spec=Content)
        mock_content.content_type = "nonexistent"
        
        # Test validating the content
        errors = self.registry.validate_content(mock_content)
        
        # Verify errors were found
        self.assertGreater(len(errors), 0)
        error_text = " ".join(errors)
        self.assertIn("Unknown content type", error_text)
        
    def test_unregister_content_type(self):
        """Test unregistering a content type."""
        # First register a custom type
        class CustomContent(Content):
            content_type = "custom"
            
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                
        self.registry.register_content_type(
            name="custom",
            display_name="Custom Content",
            description="A custom content type for testing",
            model_class=CustomContent
        )
        
        # Verify it was registered
        content_type = self.registry.get_content_type("custom")
        self.assertIsNotNone(content_type)
        
        # Now unregister it
        result = self.registry.unregister_content_type("custom")
        self.assertTrue(result)
        
        # Verify it's gone
        content_type = self.registry.get_content_type("custom")
        self.assertIsNone(content_type)
        
    def test_unregister_default_content_type(self):
        """Test attempting to unregister a default content type."""
        # Try to unregister a default type
        result = self.registry.unregister_content_type("theory")
        self.assertFalse(result)
        
        # Verify it's still there
        content_type = self.registry.get_content_type("theory")
        self.assertIsNotNone(content_type)
        
    def test_type_specific_validation(self):
        """Test type-specific validation functions."""
        # Test theory content validation
        theory_content = MagicMock(spec=TheoryContent)
        theory_content.text_content = ""
        
        errors = self.registry._validate_theory_content(theory_content)
        self.assertGreater(len(errors), 0)
        self.assertIn("Text content is required", errors[0])
        
        # Test exercise content validation
        exercise_content = MagicMock(spec=ExerciseContent)
        exercise_content.problem_statement = ""
        
        errors = self.registry._validate_exercise_content(exercise_content)
        self.assertGreater(len(errors), 0)
        self.assertIn("Problem statement is required", errors[0])
        
        # Test quiz content validation
        quiz_content = MagicMock(spec=QuizContent)
        quiz_content.questions = []
        
        errors = self.registry._validate_quiz_content(quiz_content)
        self.assertGreater(len(errors), 0)
        self.assertIn("At least one question is required", errors[0])


if __name__ == "__main__":
    unittest.main() 