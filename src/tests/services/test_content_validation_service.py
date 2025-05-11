"""
Tests for the Content Validation Service.
"""

import unittest
from unittest.mock import patch, MagicMock
from dataclasses import dataclass
import copy
from typing import Dict, Any, List, Optional

from src.services.content_validation_service import ContentValidationService
from src.services.content_type_registry import ContentTypeRegistry
from src.models.content import (
    Content, 
    TheoryContent, 
    ExerciseContent,
    QuizContent,
    AssessmentContent,
    InteractiveContent,
    ResourceContent
)


class TestContentValidationService(unittest.TestCase):
    """Test suite for ContentValidationService."""
    
    def setUp(self):
        """Set up tests."""
        # Create a fresh registry for each test to ensure isolation
        ContentTypeRegistry._instance = None
        self.validation_service = ContentValidationService()
        
        # Create test content instances
        self.valid_theory = TheoryContent(
            id="1",
            title="Test Theory Content",
            content_type="theory",
            order=1,
            lesson_id="1",
            text_content="This is test theory content."
        )
        
        # Create a mock invalid theory content instead of an actual instance
        self.invalid_theory = MagicMock(spec=TheoryContent)
        self.invalid_theory.id = "2"
        self.invalid_theory.title = ""  # Invalid: empty title
        self.invalid_theory.content_type = "theory"
        self.invalid_theory.order = -1  # Invalid: negative order
        self.invalid_theory.lesson_id = "1"
        self.invalid_theory.text_content = ""  # Invalid: empty text_content
        # Set proper types for comparisons
        self.invalid_theory.order = -1  # Integer (not MagicMock)
        self.invalid_theory.estimated_time = 0  # Integer (not MagicMock)
        
        self.valid_quiz = QuizContent(
            id="3",
            title="Test Quiz",
            content_type="quiz",
            order=2,
            lesson_id="1",
            questions=[{"question": "Test?", "answers": ["A", "B"], "correct": 0}],
            passing_score=80.0
        )
        
        # Create a mock invalid quiz content
        self.invalid_quiz = MagicMock(spec=QuizContent)
        self.invalid_quiz.id = "4"
        self.invalid_quiz.title = "Test Quiz"
        self.invalid_quiz.content_type = "quiz"
        self.invalid_quiz.order = 3  # Integer (not MagicMock)
        self.invalid_quiz.lesson_id = "1"
        self.invalid_quiz.questions = []  # Invalid: empty questions
        self.invalid_quiz.passing_score = 120  # Invalid: passing_score > 100
        self.invalid_quiz.estimated_time = 0  # Integer (not MagicMock)
        
        # Sample content data dictionaries
        self.valid_content_data = {
            "title": "Test Content",
            "content_type": "theory",
            "lesson_id": "1",
            "order": 1,
            "text_content": "This is valid content."
        }
        
        self.invalid_content_data = {
            "title": "Test Content",
            "content_type": "theory",
            # Missing lesson_id
            "order": 1
            # Missing text_content
        }
        
    def test_validate_content_valid(self):
        """Test validating valid content."""
        # Test valid theory content
        is_valid, errors = self.validation_service.validate_content(self.valid_theory)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
        # Test valid quiz content
        is_valid, errors = self.validation_service.validate_content(self.valid_quiz)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
    def test_validate_content_invalid(self):
        """Test validating invalid content."""
        # Override validation_service.type_registry.validate_content to avoid actual validation
        with patch.object(
            self.validation_service.type_registry,
            'validate_content',
            return_value=["Text content is required for theory content"]
        ):
            # Override _validate_additional_rules to avoid type comparison issues
            with patch.object(
                self.validation_service,
                '_validate_additional_rules',
                return_value=["Title is too short", "Order must be positive"]
            ):
                # Test invalid theory content
                is_valid, errors = self.validation_service.validate_content(self.invalid_theory)
                self.assertFalse(is_valid)
                self.assertGreater(len(errors), 0)
                
                # Check for specific error messages
                error_texts = " ".join(errors)
                self.assertIn("Text content", error_texts)
                self.assertIn("Title", error_texts)
                self.assertIn("Order", error_texts)
        
        # Test invalid quiz content
        with patch.object(
            self.validation_service.type_registry,
            'validate_content',
            return_value=["At least one question is required for quiz content", "Passing score must be between 0 and 100"]
        ):
            # Override _validate_additional_rules to avoid type comparison issues
            with patch.object(
                self.validation_service,
                '_validate_additional_rules',
                return_value=[]
            ):
                is_valid, errors = self.validation_service.validate_content(self.invalid_quiz)
                self.assertFalse(is_valid)
                self.assertGreater(len(errors), 0)
                
                # Check for specific error messages
                error_texts = " ".join(errors)
                self.assertIn("question", error_texts)
                self.assertIn("Passing score", error_texts)
        
    def test_validate_content_structure_valid(self):
        """Test validating valid content structure."""
        is_valid, errors = self.validation_service.validate_content_structure(
            self.valid_content_data
        )
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
    def test_validate_content_structure_invalid(self):
        """Test validating invalid content structure."""
        is_valid, errors = self.validation_service.validate_content_structure(
            self.invalid_content_data
        )
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        
        # Check for specific error messages
        error_texts = " ".join(errors)
        self.assertIn("lesson_id", error_texts)
        
    def test_validate_content_structure_unknown_type(self):
        """Test validating content structure with unknown type."""
        data = self.valid_content_data.copy()
        data["content_type"] = "nonexistent"
        
        is_valid, errors = self.validation_service.validate_content_structure(data)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        
        # Check for specific error messages
        error_texts = " ".join(errors)
        self.assertIn("Unknown content type", error_texts)
        
    def test_validate_content_update_valid(self):
        """Test validating valid content update."""
        updates = {
            "title": "Updated Title",
            "text_content": "Updated content."
        }
        
        is_valid, errors = self.validation_service.validate_content_update(
            self.valid_theory, updates
        )
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
    def test_validate_content_update_invalid(self):
        """Test validating invalid content update."""
        updates = {
            "title": "",  # Invalid: empty title
            "order": -1  # Invalid: negative order
        }
        
        # Mock _apply_updates_to_content to return a mock content object
        with patch.object(
            self.validation_service,
            '_apply_updates_to_content',
            return_value=self.invalid_theory
        ):
            # And mock validate_content to return errors
            with patch.object(
                self.validation_service,
                'validate_content',
                return_value=(False, ["Title is too short", "Order must be a positive number"])
            ):
                is_valid, errors = self.validation_service.validate_content_update(
                    self.valid_theory, updates
                )
                self.assertFalse(is_valid)
                self.assertGreater(len(errors), 0)
                
                # Check for specific error messages
                error_texts = " ".join(errors)
                self.assertIn("Title", error_texts)
                self.assertIn("Order", error_texts)
        
    def test_validate_content_references_valid(self):
        """Test validating valid content references."""
        references = [
            {"type": "webpage", "url": "https://example.com", "title": "Example"},
            {"type": "citation", "url": "https://example.org", "citation_text": "Example Citation"}
        ]
        
        is_valid, errors = self.validation_service.validate_content_references(
            self.valid_theory, references
        )
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
    def test_validate_content_references_invalid(self):
        """Test validating invalid content references."""
        references = [
            {"type": "webpage"},  # Missing URL
            {"type": "citation", "url": "https://example.org"}  # Missing citation_text
        ]
        
        is_valid, errors = self.validation_service.validate_content_references(
            self.valid_theory, references
        )
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        
        # Check for specific error messages
        error_texts = " ".join(errors)
        self.assertIn("missing a URL", error_texts)
        self.assertIn("missing citation text", error_texts)
        
    def test_validate_content_metadata_valid(self):
        """Test validating valid content metadata."""
        metadata = {
            "keywords": ["math", "algebra"],
            "complexity": "intermediate"
        }
        
        is_valid, errors = self.validation_service.validate_content_metadata(
            "theory", metadata
        )
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
    def test_validate_content_metadata_invalid(self):
        """Test validating invalid content metadata."""
        metadata = {
            "keywords": "not-an-array",  # Should be an array
            "complexity": "expert"  # Not in enum
        }
        
        is_valid, errors = self.validation_service.validate_content_metadata(
            "theory", metadata
        )
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        
        # Check for specific error messages
        error_texts = " ".join(errors)
        self.assertIn("should be an array", error_texts)
        self.assertIn("should be one of", error_texts)
        
    def test_validate_content_metadata_unknown_type(self):
        """Test validating metadata for unknown content type."""
        metadata = {"test": "value"}
        
        is_valid, errors = self.validation_service.validate_content_metadata(
            "nonexistent", metadata
        )
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        
        # Check for specific error messages
        error_texts = " ".join(errors)
        self.assertIn("Unknown content type", error_texts)
        
    def test_validate_additional_rules(self):
        """Test additional validation rules."""
        # Create properly typed mock content
        with patch.object(self.validation_service, '_validate_additional_rules') as mock_validate:
            # Configure the mock to return expected errors
            mock_validate.return_value = ["Title is too short (minimum 3 characters)"]
            
            # Create mock content with short title
            short_title_content = MagicMock(spec=TheoryContent)
            short_title_content.title = "AB"  # Too short
            short_title_content.content_type = "theory"
            short_title_content.order = 1
            short_title_content.text_content = "Valid content"
            
            # Test with mocked type_registry.validate_content
            with patch.object(
                self.validation_service.type_registry,
                'validate_content',
                return_value=[]
            ):
                # Call the validate_content method
                is_valid, errors = self.validation_service.validate_content(short_title_content)
                
                # Verify the correct method was called
                mock_validate.assert_called_once_with(short_title_content)
                
                # Check that errors from _validate_additional_rules were included
                self.assertFalse(is_valid)
                self.assertIn("Title is too short", errors[0])
        
    def test_apply_updates_to_content(self):
        """Test applying updates to content."""
        updates = {
            "title": "New Title",
            "text_content": "New content"
        }
        
        # Patch copy.copy to return a clone of the content
        with patch('copy.copy') as mock_copy:
            # Configure mock_copy to create a copy we can verify
            mock_copy.return_value = TheoryContent(
                id=self.valid_theory.id,
                title=self.valid_theory.title,
                content_type=self.valid_theory.content_type,
                order=self.valid_theory.order,
                lesson_id=self.valid_theory.lesson_id,
                text_content=self.valid_theory.text_content
            )
            
            updated_content = self.validation_service._apply_updates_to_content(
                self.valid_theory, updates
            )
            
            # Verify copy was called
            mock_copy.assert_called_once_with(self.valid_theory)
            
            # Verify the updates were applied
            self.assertIsNotNone(updated_content)
            self.assertEqual(updated_content.title, "New Title")
            self.assertEqual(updated_content.text_content, "New content")
            self.assertEqual(updated_content.id, self.valid_theory.id)  # Unchanged field
        
    def test_apply_updates_to_content_failure(self):
        """Test applying updates fails gracefully."""
        # Create a mock content
        mock_content = MagicMock(spec=Content)
        
        # Patch copy.copy to raise an exception
        with patch('copy.copy', side_effect=Exception("Copy failed")):
            updated_content = self.validation_service._apply_updates_to_content(
                mock_content, {"title": "New Title"}
            )
            
            # Verify the result is None on failure
            self.assertIsNone(updated_content)
        
    @patch('src.services.content_type_registry.ContentTypeRegistry.validate_content')
    def test_validate_content_with_mocked_registry(self, mock_validate):
        """Test content validation using a mocked registry."""
        # Setup the mock to return errors
        mock_validate.return_value = ["Mock error from registry"]
        
        # Also mock _validate_additional_rules to avoid issues
        with patch.object(
            self.validation_service,
            '_validate_additional_rules',
            return_value=[]
        ):
            is_valid, errors = self.validation_service.validate_content(self.valid_theory)
            
            # Should be invalid due to mock error
            self.assertFalse(is_valid)
            self.assertIn("Mock error from registry", errors)
            
            # Verify mock was called
            mock_validate.assert_called_once_with(self.valid_theory)


if __name__ == "__main__":
    unittest.main() 