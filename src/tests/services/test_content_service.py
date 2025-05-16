"""
Tests for the Content Service.

This module contains tests for content service methods.
"""

import uuid
from unittest.mock import patch, MagicMock, ANY
from datetime import datetime, timedelta

import pytest
from src.tests.base_test_classes import BaseServiceTest
from src.services.content_service import ContentService
from src.models.content import Content, TheoryContent, ExerciseContent, QuizContent, AssessmentContent, InteractiveContent, ResourceContent
from src.models.course import Course
from src.models.lesson import Lesson
from src.db.models import Content as DBContent, Lesson as DBLesson, Course as DBCourse
from src.exceptions import ContentValidationError


class TestContentService(BaseServiceTest):
    """Test class for ContentService."""
    
    def setUp(self):
        """Set up test environment before each test."""
        super().setUp()
        
        # Create mocks for repositories
        self.content_repo_mock = MagicMock()
        self.lesson_repo_mock = MagicMock()
        self.course_repo_mock = MagicMock()
        self.content_state_repo_mock = MagicMock()
        
        # Patch the repository classes
        self.repo_patches = [
            patch('src.services.content_service.ContentRepository', return_value=self.content_repo_mock),
            patch('src.services.content_service.LessonRepository', return_value=self.lesson_repo_mock),
            patch('src.services.content_service.CourseRepository', return_value=self.course_repo_mock),
            patch('src.services.content_service.ContentStateRepository', return_value=self.content_state_repo_mock)
        ]
        
        # Start all patches
        for p in self.repo_patches:
            p.start()
            self.addCleanup(p.stop)
        
        # Create the service instance
        self.content_service = ContentService()
        
        # Create test data
        self.test_content_id = str(uuid.uuid4())
        self.test_lesson_id = str(uuid.uuid4())
        self.test_course_id = str(uuid.uuid4())
        self.test_user_id = str(uuid.uuid4())
        
        # Create mock DB lesson first (before content)
        self.mock_db_lesson = MagicMock(spec=DBLesson)
        self.mock_db_lesson.id = uuid.UUID(self.test_lesson_id)
        self.mock_db_lesson.title = "Test Lesson"
        self.mock_db_lesson.description = "This is a test lesson"
        self.mock_db_lesson.course_id = uuid.UUID(self.test_course_id)
        
        # Create mock DB course
        self.mock_db_course = MagicMock(spec=DBCourse)
        self.mock_db_course.id = uuid.UUID(self.test_course_id)
        self.mock_db_course.title = "Test Course"
        self.mock_db_course.description = "This is a test course"
        
        # Create mock DB content
        self.mock_db_theory_content = self._create_mock_content("theory")
        self.mock_db_exercise_content = self._create_mock_content("exercise")
        self.mock_db_quiz_content = self._create_mock_content("quiz")
        
        # Mock UI models
        self.mock_ui_theory_content = TheoryContent(
            id=self.test_content_id,
            title="Test Theory Content",
            content_type="theory",
            lesson_id=self.test_lesson_id,
            order=1,
            text_content="Test content text",
            images=[],
            examples=[],
            references=[]
        )
        
        self.mock_ui_lesson = Lesson(
            id=self.test_lesson_id,
            title="Test Lesson",
            course_id=self.test_course_id,
            lesson_order=1,
            estimated_time=60,
            points_reward=10
        )
        
        self.mock_ui_course = Course(
            id=self.test_course_id,
            topic="Math",
            name="Test Course",
            description="This is a test course",
            created_at=datetime.now(),
            is_active=True
        )
    
    def _create_mock_content(self, content_type):
        """Helper to create a mock content object."""
        mock_content = MagicMock(spec=DBContent)
        mock_content.id = uuid.UUID(self.test_content_id)
        mock_content.title = f"Test {content_type.capitalize()} Content"
        mock_content.content_type = content_type
        mock_content.lesson_id = uuid.UUID(self.test_lesson_id)
        mock_content.order = 1
        mock_content.description = f"This is a test {content_type} content"
        mock_content.estimated_time = 30
        mock_content.created_at = datetime.now()
        mock_content.updated_at = datetime.now()
        mock_content.metadata = {}
        
        # Set content_data based on type
        if content_type == "theory":
            mock_content.content_data = {
                "text_content": "Test content text",
                "images": [],
                "examples": [],
                "references": []
            }
        elif content_type == "exercise":
            mock_content.content_data = {
                "problem_statement": "Test problem",
                "solution": "Test solution",
                "difficulty": "medium",
                "hints": ["Hint 1", "Hint 2"]
            }
        elif content_type == "quiz":
            mock_content.content_data = {
                "questions": [
                    {
                        "id": "q1",
                        "text": "Test question",
                        "answers": [
                            {"id": "a1", "text": "Answer 1", "is_correct": True},
                            {"id": "a2", "text": "Answer 2", "is_correct": False}
                        ]
                    }
                ],
                "passing_score": 70
            }
        
        # Create a mock lesson relationship
        mock_content.lesson = self.mock_db_lesson
        
        return mock_content
    
    def test_get_content_by_id(self):
        """Test getting content by ID."""
        # Set up mock
        self.content_repo_mock.get_by_id.return_value = self.mock_db_theory_content
        
        # Mock the conversion method
        with patch.object(
            self.content_service, 
            '_convert_db_content_to_ui_content', 
            return_value=self.mock_ui_theory_content
        ):
            # Call the method
            result = self.content_service.get_content_by_id(self.test_content_id)
            
            # Verify the result
            self.assertIsNotNone(result)
            self.assertIsInstance(result, Content)
            self.assertEqual(result.id, self.test_content_id)
            self.assertEqual(result.title, "Test Theory Content")
            
            # Verify mock was called
            self.content_repo_mock.get_by_id.assert_called_once_with(uuid.UUID(self.test_content_id))
    
    def test_get_content_by_id_not_found(self):
        """Test getting content by ID when not found."""
        # Set up mock
        self.content_repo_mock.get_by_id.return_value = None
        
        # Call the method
        result = self.content_service.get_content_by_id(self.test_content_id)
        
        # Verify the result
        self.assertIsNone(result)
        
        # Verify mock was called
        self.content_repo_mock.get_by_id.assert_called_once_with(uuid.UUID(self.test_content_id))
    
    def test_get_content_by_id_invalid_id(self):
        """Test getting content by ID with invalid ID."""
        # Call the method with invalid ID
        result = self.content_service.get_content_by_id("invalid-id")
        
        # Verify the result
        self.assertIsNone(result)
        
        # Verify mock was not called
        self.content_repo_mock.get_by_id.assert_not_called()
    
    def test_get_lesson_content(self):
        """Test getting all content for a lesson."""
        # Set up mock
        self.content_repo_mock.get_by_lesson_id.return_value = [
            self.mock_db_theory_content,
            self.mock_db_exercise_content,
            self.mock_db_quiz_content
        ]
        
        # Mock the conversion method
        with patch.object(
            self.content_service, 
            '_convert_db_content_to_ui_content', 
            side_effect=[
                self.mock_ui_theory_content,
                ExerciseContent(
                    id=self.test_content_id,
                    title="Test Exercise Content",
                    content_type="exercise",
                    lesson_id=self.test_lesson_id,
                    order=2,
                    problem_statement="Test problem",
                    solution="Test solution",
                    difficulty="medium",
                    hints=["Hint 1", "Hint 2"]
                ),
                QuizContent(
                    id=self.test_content_id,
                    title="Test Quiz Content",
                    content_type="quiz",
                    lesson_id=self.test_lesson_id,
                    order=3,
                    questions=[
                        {
                            "id": "q1",
                            "text": "Test question",
                            "answers": [
                                {"id": "a1", "text": "Answer 1", "is_correct": True},
                                {"id": "a2", "text": "Answer 2", "is_correct": False}
                            ]
                        }
                    ],
                    passing_score=70
                )
            ]
        ):
            # Call the method
            result = self.content_service.get_lesson_content(self.test_lesson_id)
            
            # Verify the result
            self.assertEqual(len(result), 3)
            self.assertIsInstance(result[0], TheoryContent)
            self.assertIsInstance(result[1], ExerciseContent)
            self.assertIsInstance(result[2], QuizContent)
            
            # Verify mock was called
            self.content_repo_mock.get_by_lesson_id.assert_called_once_with(uuid.UUID(self.test_lesson_id))
    
    def test_get_lesson_content_empty(self):
        """Test getting lesson content when empty."""
        # Set up mock
        self.content_repo_mock.get_by_lesson_id.return_value = []
        
        # Call the method
        result = self.content_service.get_lesson_content(self.test_lesson_id)
        
        # Verify the result
        self.assertEqual(len(result), 0)
        
        # Verify mock was called
        self.content_repo_mock.get_by_lesson_id.assert_called_once_with(uuid.UUID(self.test_lesson_id))
    
    def test_get_lesson_content_invalid_id(self):
        """Test getting lesson content with invalid ID."""
        # Call the method with invalid ID
        result = self.content_service.get_lesson_content("invalid-id")
        
        # Verify the result
        self.assertEqual(len(result), 0)
        
        # Verify mock was not called
        self.content_repo_mock.get_by_lesson_id.assert_not_called()
    
    def test_update_content(self):
        """Test updating content."""
        # Set up mocks
        self.content_repo_mock.get_by_id.return_value = self.mock_db_theory_content
        self.content_repo_mock.update.return_value = self.mock_db_theory_content
        
        # Updates to apply
        updates = {
            "title": "Updated Theory Content",
            "description": "Updated description"
        }
        
        # Mock the conversion method
        with patch.object(
            self.content_service, 
            '_convert_db_content_to_ui_content', 
            return_value=TheoryContent(
                id=self.test_content_id,
                title="Updated Theory Content",
                content_type="theory",
                lesson_id=self.test_lesson_id,
                order=1,
                text_content="Test content text",
                images=[],
                examples=[],
                references=[]
            )
        ):
            # Call the method
            result = self.content_service.update_content(self.test_content_id, updates)
            
            # Verify the result
            self.assertIsNotNone(result)
            self.assertEqual(result.title, "Updated Theory Content")
            
            # Verify mocks were called correctly
            self.content_repo_mock.get_by_id.assert_called_once_with(uuid.UUID(self.test_content_id))
            self.content_repo_mock.update.assert_called_once()
    
    def test_update_content_not_found(self):
        """Test updating content that doesn't exist."""
        # Set up mock
        self.content_repo_mock.get_by_id.return_value = None
        
        # Call the method
        result = self.content_service.update_content(self.test_content_id, {"title": "Updated Content"})
        
        # Verify the result
        self.assertIsNone(result)
        
        # Verify mocks were called correctly
        self.content_repo_mock.get_by_id.assert_called_once_with(uuid.UUID(self.test_content_id))
        self.content_repo_mock.update.assert_not_called()
    
    def test_update_content_invalid_id(self):
        """Test updating content with invalid ID."""
        # Call the method with invalid ID
        result = self.content_service.update_content("invalid-id", {"title": "Updated Content"})
        
        # Verify the result
        self.assertIsNone(result)
        
        # Verify mocks were not called
        self.content_repo_mock.get_by_id.assert_not_called()
        self.content_repo_mock.update.assert_not_called()
    
    def test_update_content_data(self):
        """Test updating content data."""
        # Set up mocks
        self.content_repo_mock.get_by_id.return_value = self.mock_db_theory_content
        self.content_repo_mock.update.return_value = self.mock_db_theory_content
        
        # Updates to apply
        content_data_updates = {
            "text_content": "Updated content text",
            "references": ["Reference 1", "Reference 2"]
        }
        
        # Mock the conversion method
        with patch.object(
            self.content_service, 
            '_convert_db_content_to_ui_content', 
            return_value=TheoryContent(
                id=self.test_content_id,
                title="Test Theory Content",
                content_type="theory",
                lesson_id=self.test_lesson_id,
                order=1,
                text_content="Updated content text",
                images=[],
                examples=[],
                references=["Reference 1", "Reference 2"]
            )
        ):
            # Call the method
            result = self.content_service.update_content_data(self.test_content_id, content_data_updates)
            
            # Verify the result
            self.assertIsNotNone(result)
            self.assertEqual(result.text_content, "Updated content text")
            self.assertEqual(result.references, ["Reference 1", "Reference 2"])
            
            # Verify mocks were called correctly
            self.content_repo_mock.get_by_id.assert_called_once_with(uuid.UUID(self.test_content_id))
            self.content_repo_mock.update.assert_called_once()
    
    def test_get_all_courses(self):
        """Test getting all courses."""
        # Set up mock
        self.course_repo_mock.get_active_courses.return_value = [self.mock_db_course]
        
        # Mock the conversion method
        with patch.object(
            self.content_service, 
            '_convert_db_course_to_ui_course', 
            return_value=self.mock_ui_course
        ):
            # Call the method
            result = self.content_service.get_all_courses()
            
            # Verify the result
            self.assertEqual(len(result), 1)
            self.assertIsInstance(result[0], Course)
            self.assertEqual(result[0].id, self.test_course_id)
            self.assertEqual(result[0].title, "Test Course")
            
            # Verify mocks were called correctly
            self.course_repo_mock.get_active_courses.assert_called_once()
            self.course_repo_mock.get_all.assert_not_called()
    
    def test_get_all_courses_include_inactive(self):
        """Test getting all courses including inactive ones."""
        # Set up mock
        self.course_repo_mock.get_all.return_value = [self.mock_db_course]
        
        # Mock the conversion method
        with patch.object(
            self.content_service, 
            '_convert_db_course_to_ui_course', 
            return_value=self.mock_ui_course
        ):
            # Call the method
            result = self.content_service.get_all_courses(include_inactive=True)
            
            # Verify the result
            self.assertEqual(len(result), 1)
            
            # Verify mocks were called correctly
            self.course_repo_mock.get_all.assert_called_once()
            self.course_repo_mock.get_active_courses.assert_not_called()
    
    def test_get_all_courses_exception(self):
        """Test getting all courses when an exception occurs."""
        # Set up mock
        self.course_repo_mock.get_active_courses.side_effect = Exception("Database error")
        
        # Call the method
        result = self.content_service.get_all_courses()
        
        # Verify the result
        self.assertEqual(len(result), 0)
        
        # Verify mock was called
        self.course_repo_mock.get_active_courses.assert_called_once()
    
    def test_delete_content(self):
        """Test deleting content."""
        # Set up mock
        self.content_repo_mock.delete.return_value = True
        
        # Call the method
        result = self.content_service.delete_content(self.test_content_id)
        
        # Verify the result
        self.assertTrue(result)
        
        # Verify mock was called
        self.content_repo_mock.delete.assert_called_once_with(uuid.UUID(self.test_content_id))
    
    def test_delete_content_failure(self):
        """Test deleting content with failure."""
        # Set up mock
        self.content_repo_mock.delete.return_value = False
        
        # Call the method
        result = self.content_service.delete_content(self.test_content_id)
        
        # Verify the result
        self.assertFalse(result)
        
        # Verify mock was called
        self.content_repo_mock.delete.assert_called_once_with(uuid.UUID(self.test_content_id))
    
    def test_delete_content_invalid_id(self):
        """Test deleting content with invalid ID."""
        # Call the method with invalid ID
        result = self.content_service.delete_content("invalid-id")
        
        # Verify the result
        self.assertFalse(result)
        
        # Verify mock was not called
        self.content_repo_mock.delete.assert_not_called()
    
    def test_create_content_success(self):
        """Test creating content successfully."""
        # Setup mocks
        self.content_repo_mock.create.return_value = self.mock_db_theory_content
        
        # Mock validation service - use validate_content for both checks
        with patch.object(
            self.content_service.validation_service, 
            'validate_content', 
            return_value=(True, [])
        ) as mock_validate:
            
            with patch.object(
                self.content_service, 
                '_convert_db_content_to_ui_content', 
                return_value=self.mock_ui_theory_content
            ) as mock_convert:
                
                # Call the method
                result = self.content_service.create_content(
                    content_type="theory",
                    lesson_id=self.test_lesson_id,
                    title="Test Theory Content",
                    description="This is a test theory content",
                    order=1,
                    estimated_time=30,
                    metadata={"key": "value"},
                    text_content="Test content text",
                    images=[],
                    examples=[],
                    references=[]
                )
                
                # Verify the result
                self.assertIsNotNone(result)
                self.assertEqual(result.id, self.test_content_id)
                self.assertEqual(result.title, "Test Theory Content")
                
                # Verify mocks were called
                self.assertEqual(mock_validate.call_count, 2)  # Called twice (initial + final validation)
                mock_convert.assert_called_once()
    
    def test_create_content_validation_fails(self):
        """Test creating content when validation fails."""
        # Mock validation service
        validation_errors = ["Field X is required", "Field Y must be a string"]
        
        with patch.object(
            self.content_service.validation_service, 
            'validate_content', 
            return_value=(False, validation_errors)
        ) as mock_validate:
            
            # Call the method and ensure it raises ContentValidationError
            with self.assertRaises(ContentValidationError) as context:
                self.content_service.create_content(
                    content_type="theory",
                    lesson_id=self.test_lesson_id,
                    title="Invalid Content",
                    description="Invalid description",
                    text_content=""  # Invalid, should be non-empty
                )
            
            # Verify the exception
            self.assertEqual(context.exception.content_type, "theory")
            self.assertEqual(context.exception.validation_errors, validation_errors)
            
            # Verify mock was called
            mock_validate.assert_called_once()
            
            # Verify repository method was not called
            self.content_repo_mock.create.assert_not_called()
    
    def test_create_content_post_validation_fails(self):
        """Test creating content when post-creation validation fails."""
        # Mock validation service for initial validation
        with patch.object(
            self.content_service.validation_service, 
            'validate_content', 
            return_value=(True, [])  # Initial validation passes
        ) as mock_validate:
            
            # Mock the repository to return a valid DB content
            mock_db_content = MagicMock(spec=DBContent)
            mock_db_content.id = uuid.uuid4()
            mock_db_content.content_type = "theory"
            
            self.content_repo_mock.create.return_value = mock_db_content
            
            # Mock UI content conversion to fail post-creation validation
            with patch.object(
                self.content_service, 
                '_convert_db_content_to_ui_content'
            ) as mock_convert:
                # Mock the conversion function to raise an exception
                mock_convert.side_effect = ContentValidationError(
                    message="Post-creation validation failed",
                    content_type="theory",
                    validation_errors=["Post-creation check failed"]
                )
                
                # Call the method and ensure it raises ContentValidationError
                with self.assertRaises(ContentValidationError) as context:
                    self.content_service.create_content(
                        content_type="theory",
                        lesson_id=self.test_lesson_id,
                        title="Invalid After Creation",
                        description="This content fails validation after creation",
                        text_content="This fails after creation"
                    )
                
                # Verify the exception
                self.assertEqual(context.exception.content_type, "theory")
                self.assertEqual(context.exception.validation_errors, ["Post-creation check failed"])
                
                # Verify mocks were called
                mock_validate.assert_called_once()
                self.content_repo_mock.create.assert_called_once()
                mock_convert.assert_called_once_with(mock_db_content)
    
    def test_create_theory_content_success(self):
        """Test creating theory content successfully."""
        # Setup mocks
        with patch.object(
            self.content_service, 
            'create_content', 
            return_value=self.mock_ui_theory_content
        ) as mock_create_content:
            
            # Call the method
            result = self.content_service.create_theory_content(
                lesson_id=self.test_lesson_id,
                title="Test Theory Content",
                description="This is a test theory content",
                text_content="Test content text",
                images=[],
                examples=[],
                references=[],
                order=1,
                estimated_time=30
            )
            
            # Verify the result
            self.assertIsNotNone(result)
            self.assertEqual(result.id, self.test_content_id)
            self.assertEqual(result.title, "Test Theory Content")
            
            # Verify create_content was called with the right arguments
            mock_create_content.assert_called_once_with(
                content_type="theory",
                lesson_id=self.test_lesson_id,
                title="Test Theory Content",
                description="This is a test theory content",
                text_content="Test content text",
                images=[],
                examples=[],
                references=[],
                order=1,
                estimated_time=30,
                metadata=None
            )
    
    def test_create_exercise_content_success(self):
        """Test creating exercise content successfully."""
        # Create mock exercise content
        mock_exercise = ExerciseContent(
            id=self.test_content_id,
            title="Test Exercise Content",
            content_type="exercise",
            lesson_id=self.test_lesson_id,
            order=1,
            description="This is a test exercise content",
            problem_statement="Test problem",
            solution="Test solution",
            difficulty="medium",
            hints=["Hint 1", "Hint 2"]
        )
        
        # Setup mocks
        # Mock the repository.create to return a DBContent that will be converted to our exercise
        mock_db_content = MagicMock(spec=DBContent)
        mock_db_content.id = uuid.UUID(self.test_content_id)
        mock_db_content.title = "Test Exercise Content"
        mock_db_content.content_type = "exercise"
        mock_db_content.lesson_id = uuid.UUID(self.test_lesson_id)
        mock_db_content.order = 1
        mock_db_content.description = "This is a test exercise content"
        mock_db_content.content_data = {
            "problem_statement": "Test problem",
            "solution": "Test solution",
            "difficulty": "medium",
            "hints": ["Hint 1", "Hint 2"]
        }
        
        self.content_repo_mock.create.return_value = mock_db_content
        
        # Mock the conversion method to return our predefined exercise content
        with patch.object(
            self.content_service,
            '_convert_db_content_to_ui_content',
            return_value=mock_exercise
        ):
            # Call the method
            result = self.content_service.create_exercise_content(
                lesson_id=self.test_lesson_id,
                title="Test Exercise Content",
                description="This is a test exercise content",
                problem_statement="Test problem",
                solution="Test solution",
                difficulty="medium",
                hints=["Hint 1", "Hint 2"],
                order=1,
                estimated_time=30
            )
            
            # Verify the result
            self.assertIsNotNone(result)
            self.assertEqual(result.id, self.test_content_id)
            self.assertEqual(result.title, "Test Exercise Content")
            self.assertEqual(result.problem_statement, "Test problem")
            self.assertEqual(result.solution, "Test solution")
            self.assertEqual(result.difficulty, "medium")
            self.assertEqual(result.hints, ["Hint 1", "Hint 2"])
            
            # Verify repository create was called
            self.content_repo_mock.create.assert_called_once()
    
    def test_create_assessment_content_success(self):
        """Test creating assessment content successfully."""
        # Create mock questions
        questions = [
            {
                "id": "q1",
                "text": "Test question 1",
                "answers": [
                    {"id": "a1", "text": "Answer 1", "is_correct": True},
                    {"id": "a2", "text": "Answer 2", "is_correct": False}
                ]
            },
            {
                "id": "q2",
                "text": "Test question 2",
                "answers": [
                    {"id": "a3", "text": "Answer 3", "is_correct": False},
                    {"id": "a4", "text": "Answer 4", "is_correct": True}
                ]
            }
        ]
    
        # Create mock assessment content
        mock_assessment = AssessmentContent(
            id=self.test_content_id,
            title="Test Assessment Content",
            content_type="assessment",
            lesson_id=self.test_lesson_id,
            order=1,
            description="This is a test assessment content",
            questions=questions,
            passing_score=70,
            time_limit=60,
            attempts_allowed=3,
            is_final=True
        )
    
        # Setup mocks
        # Mock the repository.create to return a DBContent that will be converted to our assessment
        mock_db_content = MagicMock(spec=DBContent)
        mock_db_content.id = uuid.UUID(self.test_content_id)
        mock_db_content.title = "Test Assessment Content"
        mock_db_content.content_type = "assessment"
        mock_db_content.lesson_id = uuid.UUID(self.test_lesson_id)
        mock_db_content.order = 1
        mock_db_content.description = "This is a test assessment content"
        mock_db_content.content_data = {
            "questions": questions,
            "passing_score": 70,
            "time_limit": 60,
            "attempts_allowed": 3,
            "is_final": True
        }
        
        self.content_repo_mock.create.return_value = mock_db_content
        
        # Mock the conversion method to return our predefined assessment content
        with patch.object(
            self.content_service,
            '_convert_db_content_to_ui_content',
            return_value=mock_assessment
        ):
            # Call the method
            result = self.content_service.create_assessment_content(
                lesson_id=self.test_lesson_id,
                title="Test Assessment Content",
                description="This is a test assessment content",
                questions=questions,
                passing_score=70,
                time_limit=60,
                attempts_allowed=3,
                is_final=True
            )
    
            # Verify the result
            self.assertIsNotNone(result)
            self.assertEqual(result.id, self.test_content_id)
            self.assertEqual(result.title, "Test Assessment Content")
            self.assertEqual(result.questions, questions)
            self.assertEqual(result.passing_score, 70)
            self.assertEqual(result.time_limit, 60)
            self.assertEqual(result.attempts_allowed, 3)
            self.assertEqual(result.is_final, True)
    
            # Verify repository create was called
            self.content_repo_mock.create.assert_called_once()
    
    def test_get_content_types(self):
        """Test getting available content types."""
        # Mock registry's get_all_content_types
        type_info1 = MagicMock()
        type_info1.name = "theory"
        type_info1.display_name = "Theory"
        type_info1.description = "Theory content"
        
        type_info2 = MagicMock()
        type_info2.name = "exercise"
        type_info2.display_name = "Exercise"
        type_info2.description = "Exercise content"
        
        expected_types = [type_info1, type_info2]
        
        with patch.object(
            self.content_service.type_registry, 
            'get_all_content_types', 
            return_value=expected_types
        ) as mock_get_types:
            
            # Call the method
            result = self.content_service.get_content_types()
            
            # Verify the result
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["type"], "theory")
            self.assertEqual(result[0]["name"], "Theory")
            
            # Verify mock was called
            mock_get_types.assert_called_once()