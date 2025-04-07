"""
Test suite for the CourseService class tag management features.

This module contains unit tests for the tag management methods in the CourseService class.
"""

import unittest
import uuid
from unittest.mock import MagicMock, patch

from src.db.models.enums import Category
from src.models.tag import Tag, TagCategory
from src.services.course_service import CourseService
from src.services.tag_service import TagService
from src.tests.base_test_classes import BaseServiceTest


class TestCourseServiceTags(BaseServiceTest):
    """Test class for CourseService tag management methods."""

    def setUp(self):
        """Set up test environment before each test."""
        super().setUp()
        
        # Create mocks
        self.tag_service = MagicMock(spec=TagService)
        self.service = CourseService(tag_service=self.tag_service)
        
        # Test data
        self.test_course_id = str(uuid.uuid4())
        self.test_tag_id = str(uuid.uuid4())
        self.test_tag_name = "python"
        
        # Create mock tag
        self.mock_tag = Tag(
            id=self.test_tag_id,
            name=self.test_tag_name,
            category=TagCategory.TOPIC
        )

    def test_add_tag_to_course_success(self):
        """Test adding a tag to a course successfully."""
        # Setup mock
        self.tag_service.add_tag_to_course.return_value = True
        
        # Call the method
        result = self.service.add_tag_to_course(self.test_course_id, self.test_tag_id)
        
        # Verify results
        self.assertTrue(result)
        
        # Verify tag service called correctly
        self.tag_service.add_tag_to_course.assert_called_with(self.test_tag_id, self.test_course_id)

    def test_add_tag_to_course_failure(self):
        """Test adding a tag to a course with failure."""
        # Setup mock
        self.tag_service.add_tag_to_course.return_value = False
        
        # Call the method
        result = self.service.add_tag_to_course(self.test_course_id, self.test_tag_id)
        
        # Verify results
        self.assertFalse(result)
        
        # Verify tag service called correctly
        self.tag_service.add_tag_to_course.assert_called_with(self.test_tag_id, self.test_course_id)

    def test_remove_tag_from_course_success(self):
        """Test removing a tag from a course successfully."""
        # Setup mock
        self.tag_service.remove_tag_from_course.return_value = True
        
        # Call the method
        result = self.service.remove_tag_from_course(self.test_course_id, self.test_tag_id)
        
        # Verify results
        self.assertTrue(result)
        
        # Verify tag service called correctly
        self.tag_service.remove_tag_from_course.assert_called_with(self.test_tag_id, self.test_course_id)

    def test_remove_tag_from_course_failure(self):
        """Test removing a tag from a course with failure."""
        # Setup mock
        self.tag_service.remove_tag_from_course.return_value = False
        
        # Call the method
        result = self.service.remove_tag_from_course(self.test_course_id, self.test_tag_id)
        
        # Verify results
        self.assertFalse(result)
        
        # Verify tag service called correctly
        self.tag_service.remove_tag_from_course.assert_called_with(self.test_tag_id, self.test_course_id)

    def test_get_course_tags_success(self):
        """Test getting all tags for a course successfully."""
        # Setup mock
        self.tag_service.get_course_tags.return_value = [self.mock_tag]
        
        # Call the method
        result = self.service.get_course_tags(self.test_course_id)
        
        # Verify results
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, self.test_tag_id)
        self.assertEqual(result[0].name, self.test_tag_name)
        
        # Verify tag service called correctly
        self.tag_service.get_course_tags.assert_called_with(self.test_course_id)

    def test_add_tag_by_name_to_course_existing_tag(self):
        """Test adding a tag by name to a course when the tag already exists."""
        # Setup mock
        self.tag_service.get_tag_by_name.return_value = self.mock_tag
        self.tag_service.add_tag_to_course.return_value = True
        
        # Call the method
        result = self.service.add_tag_by_name_to_course(self.test_course_id, self.test_tag_name, TagCategory.TOPIC)
        
        # Verify results
        self.assertTrue(result)
        
        # Verify tag service called correctly
        self.tag_service.get_tag_by_name.assert_called_with(self.test_tag_name)
        self.tag_service.add_tag_to_course.assert_called_with(self.test_tag_id, self.test_course_id)

    def test_add_tag_by_name_to_course_new_tag(self):
        """Test adding a tag by name to a course when the tag does not exist."""
        # Setup mock
        self.tag_service.get_tag_by_name.return_value = None
        self.tag_service.create_tag.return_value = self.mock_tag
        self.tag_service.add_tag_to_course.return_value = True
        
        # Call the method
        result = self.service.add_tag_by_name_to_course(self.test_course_id, self.test_tag_name, TagCategory.TOPIC)
        
        # Verify results
        self.assertTrue(result)
        
        # Verify tag service called correctly
        self.tag_service.get_tag_by_name.assert_called_with(self.test_tag_name)
        self.tag_service.create_tag.assert_called_with(self.test_tag_name, TagCategory.TOPIC)
        self.tag_service.add_tag_to_course.assert_called_with(self.test_tag_id, self.test_course_id)

    def test_add_tag_by_name_to_course_failure(self):
        """Test adding a tag by name to a course with failure."""
        # Setup mock
        self.tag_service.get_tag_by_name.return_value = self.mock_tag
        self.tag_service.add_tag_to_course.return_value = False
        
        # Call the method
        result = self.service.add_tag_by_name_to_course(self.test_course_id, self.test_tag_name, TagCategory.TOPIC)
        
        # Verify results
        self.assertFalse(result)
        
        # Verify tag service called correctly
        self.tag_service.get_tag_by_name.assert_called_with(self.test_tag_name)
        self.tag_service.add_tag_to_course.assert_called_with(self.test_tag_id, self.test_course_id)

    def test_add_tags_to_course_success(self):
        """Test adding multiple tags to a course successfully."""
        # Setup tags
        tag1 = Tag(id=str(uuid.uuid4()), name="python", category=TagCategory.TOPIC)
        tag2 = Tag(id=str(uuid.uuid4()), name="beginner", category=TagCategory.SKILL)
        tags = [tag1, tag2]
        
        # Setup mock
        self.tag_service.get_tag_by_name.side_effect = [tag1, tag2]
        self.tag_service.add_tag_to_course.return_value = True
        
        # Call the method
        result = self.service.add_tags_to_course(self.test_course_id, [tag1.name, tag2.name])
        
        # Verify results
        self.assertTrue(result)
        
        # Verify tag service called correctly
        self.assertEqual(self.tag_service.get_tag_by_name.call_count, 2)
        self.assertEqual(self.tag_service.add_tag_to_course.call_count, 2)

    def test_add_tags_to_course_partial_failure(self):
        """Test adding multiple tags to a course with some failures."""
        # Setup tags
        tag1 = Tag(id=str(uuid.uuid4()), name="python", category=TagCategory.TOPIC)
        tag2 = Tag(id=str(uuid.uuid4()), name="beginner", category=TagCategory.SKILL)
        
        # Setup mock - first add succeeds, second fails
        self.tag_service.get_tag_by_name.side_effect = [tag1, tag2]
        self.tag_service.add_tag_to_course.side_effect = [True, False]
        
        # Call the method
        result = self.service.add_tags_to_course(self.test_course_id, [tag1.name, tag2.name])
        
        # Verify results - should return False if any tag fails
        self.assertFalse(result)
        
        # Verify tag service called correctly
        self.assertEqual(self.tag_service.get_tag_by_name.call_count, 2)
        self.assertEqual(self.tag_service.add_tag_to_course.call_count, 2)

    def test_add_tags_to_course_with_categories_success(self):
        """Test adding multiple tags with categories to a course successfully."""
        # Setup tags
        tag1 = Tag(id=str(uuid.uuid4()), name="python", category=TagCategory.TOPIC)
        tag2 = Tag(id=str(uuid.uuid4()), name="beginner", category=TagCategory.SKILL)
        
        # Setup mock
        self.tag_service.get_or_create_tag.side_effect = [tag1, tag2]
        self.tag_service.add_tag_to_course.return_value = True
        
        # Call the method
        result = self.service.add_tags_to_course_with_categories(
            self.test_course_id, 
            [
                {"name": tag1.name, "category": TagCategory.TOPIC},
                {"name": tag2.name, "category": TagCategory.SKILL}
            ]
        )
        
        # Verify results
        self.assertTrue(result)
        
        # Verify tag service called correctly
        self.assertEqual(self.tag_service.get_or_create_tag.call_count, 2)
        self.assertEqual(self.tag_service.add_tag_to_course.call_count, 2)

    def test_update_course_tags_success(self):
        """Test updating a course's tags successfully."""
        # Setup tags
        current_tag1 = Tag(id=str(uuid.uuid4()), name="python", category=TagCategory.TOPIC)
        current_tag2 = Tag(id=str(uuid.uuid4()), name="intermediate", category=TagCategory.SKILL)
        new_tag1 = Tag(id=str(uuid.uuid4()), name="python", category=TagCategory.TOPIC)
        new_tag2 = Tag(id=str(uuid.uuid4()), name="beginner", category=TagCategory.SKILL)
        
        # Setup mock
        self.tag_service.get_course_tags.return_value = [current_tag1, current_tag2]
        self.tag_service.get_or_create_tag.side_effect = [new_tag1, new_tag2]
        self.tag_service.add_tag_to_course.return_value = True
        self.tag_service.remove_tag_from_course.return_value = True
        
        # Call the method
        result = self.service.update_course_tags(
            self.test_course_id, 
            [
                {"name": new_tag1.name, "category": TagCategory.TOPIC},
                {"name": new_tag2.name, "category": TagCategory.SKILL}
            ]
        )
        
        # Verify results
        self.assertTrue(result)
        
        # Verify tag service called correctly
        self.tag_service.get_course_tags.assert_called_with(self.test_course_id)
        self.assertEqual(self.tag_service.get_or_create_tag.call_count, 2)
        # Should remove current_tag2
        self.tag_service.remove_tag_from_course.assert_called_with(current_tag2.id, self.test_course_id)
        # Should add new_tag2
        self.tag_service.add_tag_to_course.assert_called_with(new_tag2.id, self.test_course_id)


if __name__ == "__main__":
    unittest.main() 