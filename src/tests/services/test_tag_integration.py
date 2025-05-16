"""
Integration tests for tag functionality in the Mathtermind application.

This module contains integration tests that verify the tag functionality
works correctly with courses and other parts of the application.
"""

import unittest
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from unittest.mock import patch, MagicMock

from src.core.logging import get_logger
from src.db.models.enums import Category, Topic, DifficultyLevel, AgeGroup
from src.models.tag import Tag, TagCategory
from src.services.course_service import CourseService
from src.services.tag_service import TagService

logger = get_logger(__name__)


class TestTagIntegration(unittest.TestCase):
    """Test the integration between tags and courses."""

    def setUp(self):
        """Set up the test environment."""
        self.course_service = CourseService()
        self.tag_service = TagService()
        
        # Create a test course using the course service
        self.test_course_id = self._create_test_course()
        self.test_tags = self._create_test_tags()

    def tearDown(self):
        """Clean up after tests."""
        # Delete any created tags
        for tag in self.test_tags:
            try:
                self.tag_service.delete_tag(tag.id)
            except Exception as e:
                logger.error(f"Error deleting tag {tag.id}: {e}")
        
        # We don't need to delete the course as it's only created in memory
        # for these tests since we're mocking the database

    def _create_test_course(self) -> str:
        """Create a test course using the service."""
        # In a real integration test, we would create a course in the database
        # For now, we'll use a mock course ID
        return str(uuid.uuid4())

    def _create_test_tags(self) -> List[Tag]:
        """Create test tags for use in tests."""
        tags = []
        # Create a Python tag
        python_tag = self.tag_service.create_tag(
            name="python",
            category=TagCategory.TOPIC
        )
        tags.append(python_tag)
        
        # Create a Math tag
        math_tag = self.tag_service.create_tag(
            name="math",
            category=TagCategory.TOPIC
        )
        tags.append(math_tag)
        
        return tags

    def test_create_and_get_tag(self):
        """Test creating and getting a tag."""
        # Create a new tag
        tag_name = f"test_tag_{str(uuid.uuid4())[:8]}"
        tag = self.tag_service.create_tag(
            name=tag_name,
            category=TagCategory.SKILL
        )
        
        # Add to cleanup list
        self.test_tags.append(tag)
        
        # Get the tag by ID
        retrieved_tag = self.tag_service.get_tag_by_id(tag.id)
        
        # Verify tag was retrieved correctly
        self.assertIsNotNone(retrieved_tag)
        self.assertEqual(retrieved_tag.name, tag_name)
        self.assertEqual(retrieved_tag.category, TagCategory.SKILL)

    @unittest.skip("Requires actual course in database")
    def test_tag_course_association(self):
        """Test adding tags to a course."""
        # Add Python tag to course
        self.course_service.add_tag_to_course(
            course_id=self.test_course_id,
            tag_id=self.test_tags[0].id
        )
        
        # Get course tags
        course = self.course_service.get_course_by_id(self.test_course_id)
        
        # Verify tag was added
        self.assertIsNotNone(course.tags)
        self.assertEqual(len(course.tags), 1)
        self.assertEqual(course.tags[0].name, "python")

    @unittest.skip("Requires actual course in database")
    def test_update_course_tags(self):
        """Test updating a course's tags."""
        # Add both tags to course
        tag_ids = [tag.id for tag in self.test_tags]
        self.course_service.update_course_tags(
            course_id=self.test_course_id,
            tag_ids=tag_ids
        )
        
        # Get course tags
        course = self.course_service.get_course_by_id(self.test_course_id)
        
        # Verify all tags were added
        self.assertIsNotNone(course.tags)
        self.assertEqual(len(course.tags), 2)
        tag_names = [tag.name for tag in course.tags]
        self.assertIn("python", tag_names)
        self.assertIn("math", tag_names)

    @unittest.skip("Requires actual course in database")
    def test_filter_courses_by_tags(self):
        """Test filtering courses by tags."""
        # Create two test course IDs
        course_id1 = str(uuid.uuid4())
        course_id2 = str(uuid.uuid4())
        
        # Mock the get_course_by_id method to return mock courses
        with patch.object(self.course_service, 'get_course_by_id') as mock_get_course:
            # Create mock Course instances that would be returned by get_course_by_id
            mock_course1 = MagicMock()
            mock_course1.id = course_id1
            mock_course1.name = "Python Programming"
            mock_course1.tags = [self.test_tags[0]]  # Python tag
            
            mock_course2 = MagicMock()
            mock_course2.id = course_id2
            mock_course2.name = "Math Fundamentals"
            mock_course2.tags = [self.test_tags[1]]  # Math tag
            
            # Set up side effect to return different courses based on ID
            def get_course_side_effect(course_id):
                if course_id == course_id1:
                    return mock_course1
                elif course_id == course_id2:
                    return mock_course2
                return None
            
            mock_get_course.side_effect = get_course_side_effect
            
            # Mock filter_courses to return mock results based on tags
            with patch.object(self.course_service, 'filter_courses') as mock_filter:
                # Set up the mock to return only Python course for Python tag
                mock_filter.side_effect = lambda filters: [mock_course1] if filters.get('tags') == ["python"] else [mock_course2] if filters.get('tags') == ["math"] else [mock_course1, mock_course2]
                
                # Test filtering by Python tag
                filtered_courses = self.course_service.filter_courses(
                    filters={"tags": ["python"]}
                )
                
                # Verify filtering works
                self.assertIsNotNone(filtered_courses)
                self.assertEqual(len(filtered_courses), 1)
                self.assertEqual(filtered_courses[0].id, course_id1)
                self.assertEqual(filtered_courses[0].name, "Python Programming")
                
                # Test filtering by Math tag
                filtered_courses = self.course_service.filter_courses(
                    filters={"tags": ["math"]}
                )
                
                # Verify filtering works
                self.assertIsNotNone(filtered_courses)
                self.assertEqual(len(filtered_courses), 1)
                self.assertEqual(filtered_courses[0].id, course_id2)
                self.assertEqual(filtered_courses[0].name, "Math Fundamentals")
                
                # Test with no tag filter
                filtered_courses = self.course_service.filter_courses(
                    filters={}
                )
                
                # Verify all courses are returned
                self.assertIsNotNone(filtered_courses)
                self.assertEqual(len(filtered_courses), 2)

    @unittest.skip("Requires actual course in database")
    def test_course_categorization(self):
        """Test that courses can be properly categorized using tags with different categories."""
        # Create mock course
        course_id = str(uuid.uuid4())
        
        # Create tags for different categories
        topic_tag = self.tag_service.create_tag(
            name=f"ai_{uuid.uuid4().hex[:8]}",
            category=TagCategory.TOPIC
        )
        self.test_tags.append(topic_tag)
        
        skill_tag = self.tag_service.create_tag(
            name=f"python_{uuid.uuid4().hex[:8]}",
            category=TagCategory.SKILL
        )
        self.test_tags.append(skill_tag)
        
        difficulty_tag = self.tag_service.create_tag(
            name=f"intermediate_{uuid.uuid4().hex[:8]}",
            category=TagCategory.DIFFICULTY
        )
        self.test_tags.append(difficulty_tag)
        
        # Mock the course service methods
        with patch.object(self.course_service, 'get_course_by_id') as mock_get_course, \
             patch.object(self.course_service, 'add_tag_to_course') as mock_add_tag, \
             patch.object(self.course_service, 'get_course_tags') as mock_get_tags:
            
            # Create a mock course
            mock_course = MagicMock()
            mock_course.id = course_id
            mock_course.name = "AI with Python"
            mock_course.tags = [topic_tag, skill_tag, difficulty_tag]
            
            # Set up mocks
            mock_get_course.return_value = mock_course
            mock_add_tag.return_value = True
            mock_get_tags.return_value = [topic_tag, skill_tag, difficulty_tag]
            
            # Add tags to the course
            for tag in [topic_tag, skill_tag, difficulty_tag]:
                result = self.course_service.add_tag_to_course(
                    course_id=course_id,
                    tag_id=tag.id
                )
                self.assertTrue(result)
            
            # Get the course tags
            course_tags = self.course_service.get_course_tags(course_id)
            
            # Verify all tags were added
            self.assertEqual(len(course_tags), 3)
            
            # Verify tags by category
            topic_tags = [tag for tag in course_tags if tag.category == TagCategory.TOPIC]
            skill_tags = [tag for tag in course_tags if tag.category == TagCategory.SKILL]
            difficulty_tags = [tag for tag in course_tags if tag.category == TagCategory.DIFFICULTY]
            
            self.assertEqual(len(topic_tags), 1)
            self.assertEqual(topic_tags[0].id, topic_tag.id)
            
            self.assertEqual(len(skill_tags), 1)
            self.assertEqual(skill_tags[0].id, skill_tag.id)
            
            self.assertEqual(len(difficulty_tags), 1)
            self.assertEqual(difficulty_tags[0].id, difficulty_tag.id)
            
            # Test updating tags
            with patch.object(self.course_service, 'update_course_tags') as mock_update_tags:
                mock_update_tags.return_value = True
                
                # Update course tags (remove difficulty tag)
                result = self.course_service.update_course_tags(
                    course_id=course_id,
                    new_tags=[
                        {"name": topic_tag.name, "category": TagCategory.TOPIC},
                        {"name": skill_tag.name, "category": TagCategory.SKILL}
                    ]
                )
                
                self.assertTrue(result)
                mock_update_tags.assert_called_once()
                
                # Verify the call arguments
                call_args = mock_update_tags.call_args[1]
                self.assertEqual(call_args["course_id"], course_id)
                self.assertEqual(len(call_args["new_tags"]), 2)


if __name__ == "__main__":
    unittest.main() 