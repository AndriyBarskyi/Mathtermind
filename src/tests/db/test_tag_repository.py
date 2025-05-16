"""
Test suite for the TagRepository class.

This module contains unit tests for the TagRepository class, which handles
tag-related database operations in the Mathtermind application.
"""

import unittest
import uuid
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from src.db.models.content import Tag, Course, CourseTag
from src.db.models.enums import Category
from src.db.repositories.tag_repo import TagRepository


class TestTagRepository(unittest.TestCase):
    """Test class for TagRepository."""

    def setUp(self):
        """Set up test environment before each test."""
        self.mock_session = MagicMock()
        self.repo = TagRepository()
        
        # Create test data
        self.test_tag_id = str(uuid.uuid4())
        self.test_tag_name = "python"
        self.test_tag_category = Category.TOPIC
        
        # Create a mock tag
        self.mock_tag = MagicMock(spec=Tag)
        self.mock_tag.id = uuid.UUID(self.test_tag_id)
        self.mock_tag.name = self.test_tag_name
        self.mock_tag.category = self.test_tag_category
        
        # Set up session mock behavior
        self.mock_session.query.return_value.filter.return_value.first.return_value = self.mock_tag
        self.mock_session.query.return_value.all.return_value = [self.mock_tag]
        self.mock_session.query.return_value.filter.return_value.all.return_value = [self.mock_tag]

    def test_create_tag_success(self):
        """Test creating a tag successfully."""
        # Mock session add and commit
        self.mock_session.add = MagicMock()
        self.mock_session.commit = MagicMock()
        
        # Call the method
        result = self.repo.create_tag(self.mock_session, self.test_tag_name, self.test_tag_category)
        
        # Verify results
        self.assertIsNotNone(result)
        self.assertEqual(result.name, self.test_tag_name)
        self.assertEqual(result.category, self.test_tag_category)
        
        # Verify session methods called
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()

    def test_create_tag_exception(self):
        """Test handling exceptions when creating a tag."""
        # Mock session to raise exception
        self.mock_session.add = MagicMock()
        self.mock_session.commit = MagicMock(side_effect=SQLAlchemyError())
        self.mock_session.rollback = MagicMock()
        
        # Call the method and expect none as result
        result = self.repo.create_tag(self.mock_session, self.test_tag_name, self.test_tag_category)
        
        # Verify results
        self.assertIsNone(result)
        
        # Verify session methods called
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()
        self.mock_session.rollback.assert_called_once()

    def test_get_tag_by_id_success(self):
        """Test getting a tag by ID successfully."""
        # Call the method
        result = self.repo.get_tag_by_id(self.mock_session, uuid.UUID(self.test_tag_id))
        
        # Verify results
        self.assertEqual(result, self.mock_tag)
        
        # Verify query constructed correctly
        self.mock_session.query.assert_called_with(Tag)
        self.mock_session.query.return_value.filter.assert_called_once()

    def test_get_tag_by_id_not_found(self):
        """Test getting a tag by ID when not found."""
        # Mock session to return None
        self.mock_session.query.return_value.filter.return_value.first.return_value = None
        
        # Call the method
        result = self.repo.get_tag_by_id(self.mock_session, uuid.UUID(self.test_tag_id))
        
        # Verify results
        self.assertIsNone(result)

    def test_get_tag_by_name_success(self):
        """Test getting a tag by name successfully."""
        # Call the method
        result = self.repo.get_tag_by_name(self.mock_session, self.test_tag_name)
        
        # Verify results
        self.assertEqual(result, self.mock_tag)
        
        # Verify query constructed correctly
        self.mock_session.query.assert_called_with(Tag)
        self.mock_session.query.return_value.filter.assert_called_once()

    def test_get_tag_by_name_not_found(self):
        """Test getting a tag by name when not found."""
        # Mock session to return None
        self.mock_session.query.return_value.filter.return_value.first.return_value = None
        
        # Call the method
        result = self.repo.get_tag_by_name(self.mock_session, self.test_tag_name)
        
        # Verify results
        self.assertIsNone(result)

    def test_get_all_tags_success(self):
        """Test getting all tags successfully."""
        # Call the method
        result = self.repo.get_all_tags(self.mock_session)
        
        # Verify results
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.mock_tag)
        
        # Verify query constructed correctly
        self.mock_session.query.assert_called_with(Tag)
        self.mock_session.query.return_value.all.assert_called_once()

    def test_get_tags_by_category_success(self):
        """Test getting tags by category successfully."""
        # Call the method
        result = self.repo.get_tags_by_category(self.mock_session, self.test_tag_category)
        
        # Verify results
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.mock_tag)
        
        # Verify query constructed correctly
        self.mock_session.query.assert_called_with(Tag)
        self.mock_session.query.return_value.filter.assert_called_once()
        self.mock_session.query.return_value.filter.return_value.all.assert_called_once()

    def test_update_tag_success(self):
        """Test updating a tag successfully."""
        # Setup
        new_name = "new_tag_name"
        new_category = Category.SKILL
        
        # Mock session
        self.mock_session.commit = MagicMock()
        
        # Call the method
        result = self.repo.update_tag(
            self.mock_session, 
            uuid.UUID(self.test_tag_id), 
            name=new_name, 
            category=new_category
        )
        
        # Verify results
        self.assertEqual(result, self.mock_tag)
        self.assertEqual(self.mock_tag.name, new_name)
        self.assertEqual(self.mock_tag.category, new_category)
        
        # Verify session methods called
        self.mock_session.commit.assert_called_once()

    def test_update_tag_not_found(self):
        """Test updating a tag when not found."""
        # Mock session to return None for the tag
        self.mock_session.query.return_value.filter.return_value.first.return_value = None
        self.mock_session.commit = MagicMock()
        
        # Call the method
        result = self.repo.update_tag(
            self.mock_session, 
            uuid.UUID(self.test_tag_id), 
            name="new_name"
        )
        
        # Verify results
        self.assertIsNone(result)
        
        # Verify session methods not called
        self.mock_session.commit.assert_not_called()

    def test_update_tag_exception(self):
        """Test handling exceptions when updating a tag."""
        # Mock session to raise exception
        self.mock_session.commit = MagicMock(side_effect=SQLAlchemyError())
        self.mock_session.rollback = MagicMock()
        
        # Call the method
        result = self.repo.update_tag(
            self.mock_session, 
            uuid.UUID(self.test_tag_id), 
            name="new_name"
        )
        
        # Verify results
        self.assertIsNone(result)
        
        # Verify session methods called
        self.mock_session.commit.assert_called_once()
        self.mock_session.rollback.assert_called_once()

    def test_delete_tag_success(self):
        """Test deleting a tag successfully."""
        # Mock session
        self.mock_session.delete = MagicMock()
        self.mock_session.commit = MagicMock()
        
        # Call the method
        result = self.repo.delete_tag(self.mock_session, uuid.UUID(self.test_tag_id))
        
        # Verify results
        self.assertTrue(result)
        
        # Verify session methods called
        self.mock_session.delete.assert_called_once_with(self.mock_tag)
        self.mock_session.commit.assert_called_once()

    def test_delete_tag_not_found(self):
        """Test deleting a tag when not found."""
        # Mock session to return None for the tag
        self.mock_session.query.return_value.filter.return_value.first.return_value = None
        self.mock_session.delete = MagicMock()
        self.mock_session.commit = MagicMock()
        
        # Call the method
        result = self.repo.delete_tag(self.mock_session, uuid.UUID(self.test_tag_id))
        
        # Verify results
        self.assertFalse(result)
        
        # Verify session methods not called
        self.mock_session.delete.assert_not_called()
        self.mock_session.commit.assert_not_called()

    def test_delete_tag_exception(self):
        """Test handling exceptions when deleting a tag."""
        # Mock session to raise exception
        self.mock_session.delete = MagicMock()
        self.mock_session.commit = MagicMock(side_effect=SQLAlchemyError())
        self.mock_session.rollback = MagicMock()
        
        # Call the method
        result = self.repo.delete_tag(self.mock_session, uuid.UUID(self.test_tag_id))
        
        # Verify results
        self.assertFalse(result)
        
        # Verify session methods called
        self.mock_session.delete.assert_called_once_with(self.mock_tag)
        self.mock_session.commit.assert_called_once()
        self.mock_session.rollback.assert_called_once()

    def test_add_tag_to_course_success(self):
        """Test adding a tag to a course successfully."""
        # Setup
        test_course_id = str(uuid.uuid4())
        mock_course = MagicMock(spec=Course)
        mock_course.id = uuid.UUID(test_course_id)
        
        # Mock session behavior
        self.mock_session.query.return_value.filter.return_value.first.side_effect = [
            self.mock_tag,  # First call returns the tag
            mock_course,    # Second call returns the course
            None            # Third call to check if association exists returns None
        ]
        self.mock_session.add = MagicMock()
        self.mock_session.commit = MagicMock()
        
        # Call the method
        result = self.repo.add_tag_to_course(
            self.mock_session, 
            uuid.UUID(self.test_tag_id), 
            uuid.UUID(test_course_id)
        )
        
        # Verify results
        self.assertTrue(result)
        
        # Verify session methods called
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()

    def test_add_tag_to_course_already_exists(self):
        """Test adding a tag to a course when the association already exists."""
        # Setup
        test_course_id = str(uuid.uuid4())
        mock_course = MagicMock(spec=Course)
        mock_course.id = uuid.UUID(test_course_id)
        mock_association = MagicMock(spec=CourseTag)
        
        # Mock session behavior
        self.mock_session.query.return_value.filter.return_value.first.side_effect = [
            self.mock_tag,       # First call returns the tag
            mock_course,         # Second call returns the course
            mock_association     # Third call returns existing association
        ]
        self.mock_session.add = MagicMock()
        self.mock_session.commit = MagicMock()
        
        # Call the method
        result = self.repo.add_tag_to_course(
            self.mock_session, 
            uuid.UUID(self.test_tag_id), 
            uuid.UUID(test_course_id)
        )
        
        # Verify results
        self.assertTrue(result)
        
        # Verify session methods not called (no need to add again)
        self.mock_session.add.assert_not_called()
        self.mock_session.commit.assert_not_called()

    def test_add_tag_to_course_tag_not_found(self):
        """Test adding a tag to a course when tag not found."""
        # Setup
        test_course_id = str(uuid.uuid4())
        
        # Mock session behavior
        self.mock_session.query.return_value.filter.return_value.first.return_value = None
        self.mock_session.add = MagicMock()
        self.mock_session.commit = MagicMock()
        
        # Call the method
        result = self.repo.add_tag_to_course(
            self.mock_session, 
            uuid.UUID(self.test_tag_id), 
            uuid.UUID(test_course_id)
        )
        
        # Verify results
        self.assertFalse(result)
        
        # Verify session methods not called
        self.mock_session.add.assert_not_called()
        self.mock_session.commit.assert_not_called()

    def test_add_tag_to_course_course_not_found(self):
        """Test adding a tag to a course when course not found."""
        # Setup
        test_course_id = str(uuid.uuid4())
        
        # Mock session behavior
        self.mock_session.query.return_value.filter.return_value.first.side_effect = [
            self.mock_tag,  # First call returns the tag
            None            # Second call returns None for course
        ]
        self.mock_session.add = MagicMock()
        self.mock_session.commit = MagicMock()
        
        # Call the method
        result = self.repo.add_tag_to_course(
            self.mock_session, 
            uuid.UUID(self.test_tag_id), 
            uuid.UUID(test_course_id)
        )
        
        # Verify results
        self.assertFalse(result)
        
        # Verify session methods not called
        self.mock_session.add.assert_not_called()
        self.mock_session.commit.assert_not_called()

    def test_add_tag_to_course_exception(self):
        """Test handling exceptions when adding a tag to a course."""
        # Setup
        test_course_id = str(uuid.uuid4())
        mock_course = MagicMock(spec=Course)
        mock_course.id = uuid.UUID(test_course_id)
        
        # Mock session behavior
        self.mock_session.query.return_value.filter.return_value.first.side_effect = [
            self.mock_tag,  # First call returns the tag
            mock_course,    # Second call returns the course
            None            # Third call to check if association exists returns None
        ]
        self.mock_session.add = MagicMock()
        self.mock_session.commit = MagicMock(side_effect=SQLAlchemyError())
        self.mock_session.rollback = MagicMock()
        
        # Call the method
        result = self.repo.add_tag_to_course(
            self.mock_session, 
            uuid.UUID(self.test_tag_id), 
            uuid.UUID(test_course_id)
        )
        
        # Verify results
        self.assertFalse(result)
        
        # Verify session methods called
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()
        self.mock_session.rollback.assert_called_once()

    def test_remove_tag_from_course_success(self):
        """Test removing a tag from a course successfully."""
        # Setup
        test_course_id = str(uuid.uuid4())
        mock_association = MagicMock(spec=CourseTag)
        
        # Mock session behavior
        self.mock_session.query.return_value.filter.return_value.first.return_value = mock_association
        self.mock_session.delete = MagicMock()
        self.mock_session.commit = MagicMock()
        
        # Call the method
        result = self.repo.remove_tag_from_course(
            self.mock_session, 
            uuid.UUID(self.test_tag_id), 
            uuid.UUID(test_course_id)
        )
        
        # Verify results
        self.assertTrue(result)
        
        # Verify session methods called
        self.mock_session.delete.assert_called_once_with(mock_association)
        self.mock_session.commit.assert_called_once()

    def test_remove_tag_from_course_not_found(self):
        """Test removing a tag from a course when association not found."""
        # Setup
        test_course_id = str(uuid.uuid4())
        
        # Mock session behavior
        self.mock_session.query.return_value.filter.return_value.first.return_value = None
        self.mock_session.delete = MagicMock()
        self.mock_session.commit = MagicMock()
        
        # Call the method
        result = self.repo.remove_tag_from_course(
            self.mock_session, 
            uuid.UUID(self.test_tag_id), 
            uuid.UUID(test_course_id)
        )
        
        # Verify results
        self.assertFalse(result)
        
        # Verify session methods not called
        self.mock_session.delete.assert_not_called()
        self.mock_session.commit.assert_not_called()

    def test_remove_tag_from_course_exception(self):
        """Test handling exceptions when removing a tag from a course."""
        # Setup
        test_course_id = str(uuid.uuid4())
        mock_association = MagicMock(spec=CourseTag)
        
        # Mock session behavior
        self.mock_session.query.return_value.filter.return_value.first.return_value = mock_association
        self.mock_session.delete = MagicMock()
        self.mock_session.commit = MagicMock(side_effect=SQLAlchemyError())
        self.mock_session.rollback = MagicMock()
        
        # Call the method
        result = self.repo.remove_tag_from_course(
            self.mock_session, 
            uuid.UUID(self.test_tag_id), 
            uuid.UUID(test_course_id)
        )
        
        # Verify results
        self.assertFalse(result)
        
        # Verify session methods called
        self.mock_session.delete.assert_called_once_with(mock_association)
        self.mock_session.commit.assert_called_once()
        self.mock_session.rollback.assert_called_once()

    def test_get_course_tags_success(self):
        """Test getting all tags for a course successfully."""
        # Setup
        test_course_id = str(uuid.uuid4())
        
        # Mock session behavior
        self.mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = [self.mock_tag]
        
        # Call the method
        result = self.repo.get_course_tags(
            self.mock_session, 
            uuid.UUID(test_course_id)
        )
        
        # Verify results
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.mock_tag)
        
        # Verify query constructed correctly
        self.mock_session.query.assert_called_with(Tag)
        self.mock_session.query.return_value.join.assert_called_once()
        self.mock_session.query.return_value.join.return_value.filter.assert_called_once()
        self.mock_session.query.return_value.join.return_value.filter.return_value.all.assert_called_once()

    def test_get_courses_by_tag_success(self):
        """Test getting all courses with a specific tag successfully."""
        # Setup
        mock_course = MagicMock(spec=Course)
        
        # Mock session behavior
        self.mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = [mock_course]
        
        # Call the method
        result = self.repo.get_courses_by_tag(
            self.mock_session, 
            uuid.UUID(self.test_tag_id)
        )
        
        # Verify results
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], mock_course)
        
        # Verify query constructed correctly
        self.mock_session.query.assert_called_with(Course)
        self.mock_session.query.return_value.join.assert_called_once()
        self.mock_session.query.return_value.join.return_value.filter.assert_called_once()
        self.mock_session.query.return_value.join.return_value.filter.return_value.all.assert_called_once()

if __name__ == "__main__":
    unittest.main() 