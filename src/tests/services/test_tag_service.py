"""
Test suite for the TagService class.

This module contains unit tests for the TagService class, which handles
tag-related business logic in the Mathtermind application.
"""

import unittest
import uuid
from unittest.mock import MagicMock, patch

from sqlalchemy.exc import SQLAlchemyError

from src.db.models.enums import Category
from src.db.repositories.tag_repo import TagRepository
from src.models.tag import Tag, TagCategory
from src.services.tag_service import TagService
from src.tests.base_test_classes import BaseServiceTest


class TestTagService(BaseServiceTest):
    """Test class for TagService."""

    def setUp(self):
        """Set up test environment before each test."""
        super().setUp()
        self.tag_repo = MagicMock(spec=TagRepository)
        self.service = TagService(self.tag_repo, test_session=self.mock_session)
        
        # Create test data
        self.test_tag_id = str(uuid.uuid4())
        self.test_tag_name = "python"
        self.test_tag_category = Category.TOPIC
        
        # Create a mock tag for DB results
        self.mock_db_tag = MagicMock()
        self.mock_db_tag.id = uuid.UUID(self.test_tag_id)
        self.mock_db_tag.name = self.test_tag_name
        self.mock_db_tag.category = self.test_tag_category
        
        # Create expected UI model
        self.expected_ui_tag = Tag(
            id=self.test_tag_id,
            name=self.test_tag_name,
            category=TagCategory.TOPIC
        )

    def test_create_tag_success(self):
        """Test creating a tag successfully."""
        # Setup mock
        self.tag_repo.create_tag.return_value = self.mock_db_tag
        
        # Call the method
        result = self.service.create_tag(self.test_tag_name, TagCategory.TOPIC)
        
        # Verify results
        self.assertIsNotNone(result)
        self.assertEqual(result.id, self.test_tag_id)
        self.assertEqual(result.name, self.test_tag_name)
        self.assertEqual(result.category, TagCategory.TOPIC)
        
        # Verify repository called correctly
        self.tag_repo.create_tag.assert_called_with(
            self.mock_session, self.test_tag_name, Category.TOPIC
        )

    def test_create_tag_failure(self):
        """Test creating a tag with repository failure."""
        # Setup mock
        self.tag_repo.create_tag.return_value = None
        
        # Call the method
        result = self.service.create_tag(self.test_tag_name, TagCategory.TOPIC)
        
        # Verify results
        self.assertIsNone(result)
        
        # Verify repository called correctly
        self.tag_repo.create_tag.assert_called_with(
            self.mock_session, self.test_tag_name, Category.TOPIC
        )

    def test_get_tag_by_id_success(self):
        """Test getting a tag by ID successfully."""
        # Setup mock
        self.tag_repo.get_tag_by_id.return_value = self.mock_db_tag
        
        # Call the method
        result = self.service.get_tag_by_id(self.test_tag_id)
        
        # Verify results
        self.assertIsNotNone(result)
        self.assertEqual(result.id, self.test_tag_id)
        self.assertEqual(result.name, self.test_tag_name)
        self.assertEqual(result.category, TagCategory.TOPIC)
        
        # Verify repository called correctly
        self.tag_repo.get_tag_by_id.assert_called_with(
            self.mock_session, uuid.UUID(self.test_tag_id)
        )

    def test_get_tag_by_id_not_found(self):
        """Test getting a tag by ID when not found."""
        # Setup mock
        self.tag_repo.get_tag_by_id.return_value = None
        
        # Call the method
        result = self.service.get_tag_by_id(self.test_tag_id)
        
        # Verify results
        self.assertIsNone(result)
        
        # Verify repository called correctly
        self.tag_repo.get_tag_by_id.assert_called_with(
            self.mock_session, uuid.UUID(self.test_tag_id)
        )

    def test_get_tag_by_name_success(self):
        """Test getting a tag by name successfully."""
        # Setup mock
        self.tag_repo.get_tag_by_name.return_value = self.mock_db_tag
        
        # Call the method
        result = self.service.get_tag_by_name(self.test_tag_name)
        
        # Verify results
        self.assertIsNotNone(result)
        self.assertEqual(result.id, self.test_tag_id)
        self.assertEqual(result.name, self.test_tag_name)
        self.assertEqual(result.category, TagCategory.TOPIC)
        
        # Verify repository called correctly
        self.tag_repo.get_tag_by_name.assert_called_with(
            self.mock_session, self.test_tag_name
        )

    def test_get_tag_by_name_not_found(self):
        """Test getting a tag by name when not found."""
        # Setup mock
        self.tag_repo.get_tag_by_name.return_value = None
        
        # Call the method
        result = self.service.get_tag_by_name(self.test_tag_name)
        
        # Verify results
        self.assertIsNone(result)
        
        # Verify repository called correctly
        self.tag_repo.get_tag_by_name.assert_called_with(
            self.mock_session, self.test_tag_name
        )

    def test_get_all_tags_success(self):
        """Test getting all tags successfully."""
        # Setup mock
        self.tag_repo.get_all_tags.return_value = [self.mock_db_tag]
        
        # Call the method
        result = self.service.get_all_tags()
        
        # Verify results
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, self.test_tag_id)
        self.assertEqual(result[0].name, self.test_tag_name)
        self.assertEqual(result[0].category, TagCategory.TOPIC)
        
        # Verify repository called correctly
        self.tag_repo.get_all_tags.assert_called_with(self.mock_session)

    def test_get_tags_by_category_success(self):
        """Test getting tags by category successfully."""
        # Setup mock
        self.tag_repo.get_tags_by_category.return_value = [self.mock_db_tag]
        
        # Call the method
        result = self.service.get_tags_by_category(TagCategory.TOPIC)
        
        # Verify results
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, self.test_tag_id)
        self.assertEqual(result[0].name, self.test_tag_name)
        self.assertEqual(result[0].category, TagCategory.TOPIC)
        
        # Verify repository called correctly
        self.tag_repo.get_tags_by_category.assert_called_with(
            self.mock_session, Category.TOPIC
        )

    def test_update_tag_success(self):
        """Test updating a tag successfully."""
        # Setup
        new_name = "new_tag_name"
        new_category = TagCategory.SKILL
        updated_mock_db_tag = MagicMock()
        updated_mock_db_tag.id = uuid.UUID(self.test_tag_id)
        updated_mock_db_tag.name = new_name
        updated_mock_db_tag.category = Category.SKILL
        
        # Setup mock
        self.tag_repo.update_tag.return_value = updated_mock_db_tag
        
        # Call the method
        result = self.service.update_tag(
            self.test_tag_id,
            name=new_name,
            category=new_category
        )
        
        # Verify results
        self.assertIsNotNone(result)
        self.assertEqual(result.id, self.test_tag_id)
        self.assertEqual(result.name, new_name)
        self.assertEqual(result.category, new_category)
        
        # Verify repository called correctly
        self.tag_repo.update_tag.assert_called_with(
            self.mock_session,
            uuid.UUID(self.test_tag_id),
            name=new_name,
            category=Category.SKILL
        )

    def test_update_tag_not_found(self):
        """Test updating a tag when not found."""
        # Setup mock
        self.tag_repo.update_tag.return_value = None
        
        # Call the method
        result = self.service.update_tag(
            self.test_tag_id,
            name="new_name"
        )
        
        # Verify results
        self.assertIsNone(result)
        
        # Verify repository called correctly
        self.tag_repo.update_tag.assert_called_with(
            self.mock_session,
            uuid.UUID(self.test_tag_id),
            name="new_name",
            category=None
        )

    def test_delete_tag_success(self):
        """Test deleting a tag successfully."""
        # Setup mock
        self.tag_repo.delete_tag.return_value = True
        
        # Call the method
        result = self.service.delete_tag(self.test_tag_id)
        
        # Verify results
        self.assertTrue(result)
        
        # Verify repository called correctly
        self.tag_repo.delete_tag.assert_called_with(
            self.mock_session,
            uuid.UUID(self.test_tag_id)
        )

    def test_delete_tag_failure(self):
        """Test deleting a tag with failure."""
        # Setup mock
        self.tag_repo.delete_tag.return_value = False
        
        # Call the method
        result = self.service.delete_tag(self.test_tag_id)
        
        # Verify results
        self.assertFalse(result)
        
        # Verify repository called correctly
        self.tag_repo.delete_tag.assert_called_with(
            self.mock_session,
            uuid.UUID(self.test_tag_id)
        )

    def test_add_tag_to_course_success(self):
        """Test adding a tag to a course successfully."""
        # Setup
        test_course_id = str(uuid.uuid4())
        
        # Setup mock
        self.tag_repo.add_tag_to_course.return_value = True
        
        # Call the method
        result = self.service.add_tag_to_course(self.test_tag_id, test_course_id)
        
        # Verify results
        self.assertTrue(result)
        
        # Verify repository called correctly
        self.tag_repo.add_tag_to_course.assert_called_with(
            self.mock_session,
            uuid.UUID(self.test_tag_id),
            uuid.UUID(test_course_id)
        )

    def test_add_tag_to_course_failure(self):
        """Test adding a tag to a course with failure."""
        # Setup
        test_course_id = str(uuid.uuid4())
        
        # Setup mock
        self.tag_repo.add_tag_to_course.return_value = False
        
        # Call the method
        result = self.service.add_tag_to_course(self.test_tag_id, test_course_id)
        
        # Verify results
        self.assertFalse(result)
        
        # Verify repository called correctly
        self.tag_repo.add_tag_to_course.assert_called_with(
            self.mock_session,
            uuid.UUID(self.test_tag_id),
            uuid.UUID(test_course_id)
        )

    def test_remove_tag_from_course_success(self):
        """Test removing a tag from a course successfully."""
        # Setup
        test_course_id = str(uuid.uuid4())
        
        # Setup mock
        self.tag_repo.remove_tag_from_course.return_value = True
        
        # Call the method
        result = self.service.remove_tag_from_course(self.test_tag_id, test_course_id)
        
        # Verify results
        self.assertTrue(result)
        
        # Verify repository called correctly
        self.tag_repo.remove_tag_from_course.assert_called_with(
            self.mock_session,
            uuid.UUID(self.test_tag_id),
            uuid.UUID(test_course_id)
        )

    def test_remove_tag_from_course_failure(self):
        """Test removing a tag from a course with failure."""
        # Setup
        test_course_id = str(uuid.uuid4())
        
        # Setup mock
        self.tag_repo.remove_tag_from_course.return_value = False
        
        # Call the method
        result = self.service.remove_tag_from_course(self.test_tag_id, test_course_id)
        
        # Verify results
        self.assertFalse(result)
        
        # Verify repository called correctly
        self.tag_repo.remove_tag_from_course.assert_called_with(
            self.mock_session,
            uuid.UUID(self.test_tag_id),
            uuid.UUID(test_course_id)
        )

    def test_get_course_tags_success(self):
        """Test getting all tags for a course successfully."""
        # Setup
        test_course_id = str(uuid.uuid4())
        
        # Setup mock
        self.tag_repo.get_course_tags.return_value = [self.mock_db_tag]
        
        # Call the method
        result = self.service.get_course_tags(test_course_id)
        
        # Verify results
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, self.test_tag_id)
        self.assertEqual(result[0].name, self.test_tag_name)
        self.assertEqual(result[0].category, TagCategory.TOPIC)
        
        # Verify repository called correctly
        self.tag_repo.get_course_tags.assert_called_with(
            self.mock_session,
            uuid.UUID(test_course_id)
        )

    def test_get_courses_by_tag_success(self):
        """Test getting all courses with a specific tag successfully."""
        # Setup
        mock_course = MagicMock()
        mock_course.id = uuid.uuid4()
        mock_course.name = "Test Course"
        
        # Setup mock
        self.tag_repo.get_courses_by_tag.return_value = [mock_course]
        
        # Call the method
        result = self.service.get_courses_by_tag(self.test_tag_id)
        
        # Verify results - we should verify the course objects are 
        # properly converted, but we'll skip that for brevity as it's
        # tested in the CourseService tests
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        
        # Verify repository called correctly
        self.tag_repo.get_courses_by_tag.assert_called_with(
            self.mock_session,
            uuid.UUID(self.test_tag_id)
        )

    def test_get_or_create_tag_existing(self):
        """Test getting an existing tag."""
        # Setup mock
        self.tag_repo.get_tag_by_name.return_value = self.mock_db_tag
        
        # Call the method
        result = self.service.get_or_create_tag(self.test_tag_name, TagCategory.TOPIC)
        
        # Verify results
        self.assertIsNotNone(result)
        self.assertEqual(result.id, self.test_tag_id)
        self.assertEqual(result.name, self.test_tag_name)
        self.assertEqual(result.category, TagCategory.TOPIC)
        
        # Verify repository called correctly
        self.tag_repo.get_tag_by_name.assert_called_with(
            self.mock_session, self.test_tag_name
        )
        self.tag_repo.create_tag.assert_not_called()

    def test_get_or_create_tag_new(self):
        """Test creating a new tag when it does not exist."""
        # Setup mock
        self.tag_repo.get_tag_by_name.return_value = None
        self.tag_repo.create_tag.return_value = self.mock_db_tag
        
        # Call the method
        result = self.service.get_or_create_tag(self.test_tag_name, TagCategory.TOPIC)
        
        # Verify results
        self.assertIsNotNone(result)
        self.assertEqual(result.id, self.test_tag_id)
        self.assertEqual(result.name, self.test_tag_name)
        self.assertEqual(result.category, TagCategory.TOPIC)
        
        # Verify repository called correctly
        self.tag_repo.get_tag_by_name.assert_called_with(
            self.mock_session, self.test_tag_name
        )
        self.tag_repo.create_tag.assert_called_with(
            self.mock_session, self.test_tag_name, Category.TOPIC
        )

    def test_convert_db_tag_to_ui_tag(self):
        """Test converting a database tag to a UI tag."""
        # Call the method
        result = self.service._convert_db_tag_to_ui_tag(self.mock_db_tag)
        
        # Verify results
        self.assertEqual(result.id, self.test_tag_id)
        self.assertEqual(result.name, self.test_tag_name)
        self.assertEqual(result.category, TagCategory.TOPIC)


if __name__ == "__main__":
    unittest.main() 