from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid
import logging

from src.db import get_db
from src.db.repositories import quiz_repo, user_answers_repo
from src.db.models import Quiz as DBQuiz, UserAnswer as DBUserAnswer

# Set up logging
logger = logging.getLogger(__name__)

class Quiz:
    """Model for a quiz"""
    def __init__(
        self,
        id: str,
        lesson_id: str,
        title: str,
        questions: Dict[str, Any],
        time_limit: Optional[int],
        passing_score: float,
        attempts_allowed: int,
        created_at: datetime
    ):
        self.id = id
        self.lesson_id = lesson_id
        self.title = title
        self.questions = questions
        self.time_limit = time_limit
        self.passing_score = passing_score
        self.attempts_allowed = attempts_allowed
        self.created_at = created_at


class UserAnswer:
    """Model for a user's answer to a quiz"""
    def __init__(
        self,
        id: str,
        user_id: str,
        quiz_id: str,
        answers: Dict[str, Any],
        score: float,
        attempt_number: int,
        completed: bool,
        created_at: datetime
    ):
        self.id = id
        self.user_id = user_id
        self.quiz_id = quiz_id
        self.answers = answers
        self.score = score
        self.attempt_number = attempt_number
        self.completed = completed
        self.created_at = created_at


class QuizService:
    """
    Service class for handling quiz operations.
    This class provides methods for fetching, submitting, and analyzing quizzes and answers.
    """
    
    def get_quiz(self, quiz_id: str) -> Optional[Quiz]:
        """
        Get a quiz by its ID
        
        Args:
            quiz_id: The ID of the quiz to retrieve
            
        Returns:
            The quiz if found, None otherwise
        """
        try:
            db = next(get_db())
            db_quiz = quiz_repo.get_quiz(db, quiz_id)
            if db_quiz:
                quiz = self._convert_db_quiz_to_quiz(db_quiz)
                db.close()
                return quiz
            db.close()
            return None
        except Exception as e:
            logger.error(f"Error getting quiz: {str(e)}")
            return None
    
    def get_lesson_quizzes(self, lesson_id: str) -> List[Quiz]:
        """
        Get all quizzes for a lesson
        
        Args:
            lesson_id: The ID of the lesson
            
        Returns:
            List of quizzes for the lesson
        """
        try:
            db = next(get_db())
            db_quizzes = quiz_repo.get_quizzes_by_lesson(db, lesson_id)
            quizzes = [self._convert_db_quiz_to_quiz(quiz) for quiz in db_quizzes]
            db.close()
            return quizzes
        except Exception as e:
            logger.error(f"Error getting lesson quizzes: {str(e)}")
            return []
    
    def get_user_quiz_attempts(self, user_id: str, quiz_id: str) -> List[UserAnswer]:
        """
        Get all attempts by a user for a specific quiz
        
        Args:
            user_id: The ID of the user
            quiz_id: The ID of the quiz
            
        Returns:
            List of user answer records for the quiz
        """
        try:
            db = next(get_db())
            db_answers = user_answers_repo.get_user_answers_by_quiz(db, user_id, quiz_id)
            answers = [self._convert_db_user_answer_to_user_answer(answer) for answer in db_answers]
            db.close()
            return answers
        except Exception as e:
            logger.error(f"Error getting user quiz attempts: {str(e)}")
            return []
    
    def get_latest_quiz_attempt(self, user_id: str, quiz_id: str) -> Optional[UserAnswer]:
        """
        Get the latest attempt by a user for a specific quiz
        
        Args:
            user_id: The ID of the user
            quiz_id: The ID of the quiz
            
        Returns:
            The latest user answer record if found, None otherwise
        """
        try:
            db = next(get_db())
            db_answers = user_answers_repo.get_user_answers_by_quiz(db, user_id, quiz_id)
            
            if not db_answers:
                db.close()
                return None
            
            # Sort by created_at in descending order and get the first one
            latest_answer = sorted(db_answers, key=lambda a: a.created_at, reverse=True)[0]
            result = self._convert_db_user_answer_to_user_answer(latest_answer)
            
            db.close()
            return result
        except Exception as e:
            logger.error(f"Error getting latest quiz attempt: {str(e)}")
            return None
    
    def submit_quiz_answers(self, user_id: str, quiz_id: str, answers: Dict[str, Any]) -> Optional[UserAnswer]:
        """
        Submit answers for a quiz and calculate the score
        
        Args:
            user_id: The ID of the user
            quiz_id: The ID of the quiz
            answers: Dictionary containing the user's answers
            
        Returns:
            The created user answer record if successful, None otherwise
        """
        try:
            db = next(get_db())
            
            # Get the quiz
            quiz = quiz_repo.get_quiz(db, quiz_id)
            if not quiz:
                db.close()
                return None
            
            # Get previous attempts to determine attempt number
            previous_attempts = user_answers_repo.get_user_answers_by_quiz(db, user_id, quiz_id)
            attempt_number = len(previous_attempts) + 1
            
            # Check if maximum attempts reached
            if attempt_number > quiz.attempts_allowed:
                db.close()
                return None
            
            # Calculate score
            score = self._calculate_quiz_score(quiz.questions, answers)
            
            # Create user answer record
            user_answer = DBUserAnswer(
                id=uuid.uuid4(),
                user_id=user_id,
                quiz_id=quiz_id,
                answers=answers,
                score=score,
                attempt_number=attempt_number,
                completed=True,
                created_at=datetime.now(timezone.utc)
            )
            
            # Save to database
            created_answer = user_answers_repo.create_user_answer(db, user_answer)
            
            # Convert to model
            result = self._convert_db_user_answer_to_user_answer(created_answer)
            
            db.close()
            return result
        except Exception as e:
            logger.error(f"Error submitting quiz answers: {str(e)}")
            return None
    
    def has_passed_quiz(self, user_id: str, quiz_id: str) -> bool:
        """
        Check if a user has passed a quiz
        
        Args:
            user_id: The ID of the user
            quiz_id: The ID of the quiz
            
        Returns:
            True if the user has passed the quiz, False otherwise
        """
        try:
            db = next(get_db())
            
            # Get the quiz
            quiz = quiz_repo.get_quiz(db, quiz_id)
            if not quiz:
                db.close()
                return False
            
            # Get user answers for this quiz
            user_answers = user_answers_repo.get_user_answers_by_quiz(db, user_id, quiz_id)
            
            # Check if any attempt has a passing score
            for answer in user_answers:
                if answer.score >= quiz.passing_score:
                    db.close()
                    return True
            
            db.close()
            return False
        except Exception as e:
            logger.error(f"Error checking if user passed quiz: {str(e)}")
            return False
    
    def _calculate_quiz_score(self, quiz_questions: Dict[str, Any], user_answers: Dict[str, Any]) -> float:
        """
        Calculate the score for a quiz based on the user's answers
        
        Args:
            quiz_questions: The quiz questions
            user_answers: The user's answers
            
        Returns:
            The score as a percentage (0-100)
        """
        try:
            # Extract questions and user answers
            questions = quiz_questions.get("questions", [])
            answers_data = user_answers.get("answers", [])
            
            if not questions or not answers_data:
                return 0.0
            
            # Create a map of question ID to correct answer
            question_map = {q["id"]: q for q in questions}
            
            # Calculate score
            total_points = sum(q.get("points", 1) for q in questions)
            earned_points = 0
            
            for answer in answers_data:
                question_id = answer.get("question_id")
                user_answer = answer.get("answer")
                
                if question_id in question_map:
                    question = question_map[question_id]
                    correct_answer = question.get("correct_answer")
                    points = question.get("points", 1)
                    
                    # Check if answer is correct
                    is_correct = False
                    
                    # Handle different question types
                    if isinstance(correct_answer, list):
                        # Multiple correct answers
                        if isinstance(user_answer, list):
                            is_correct = set(user_answer) == set(correct_answer)
                        else:
                            is_correct = False
                    else:
                        # Single correct answer
                        is_correct = user_answer == correct_answer
                    
                    if is_correct:
                        earned_points += points
                        answer["is_correct"] = True
                    else:
                        answer["is_correct"] = False
            
            # Calculate percentage score
            if total_points > 0:
                score = (earned_points / total_points) * 100
            else:
                score = 0.0
            
            return round(score, 2)
        except Exception as e:
            logger.error(f"Error calculating quiz score: {str(e)}")
            return 0.0
    
    def _convert_db_quiz_to_quiz(self, db_quiz: DBQuiz) -> Quiz:
        """Convert a database quiz model to a Quiz model"""
        try:
            return Quiz(
                id=str(db_quiz.id),
                lesson_id=str(db_quiz.lesson_id),
                title=db_quiz.title,
                questions=db_quiz.questions,
                time_limit=db_quiz.time_limit,
                passing_score=db_quiz.passing_score,
                attempts_allowed=db_quiz.attempts_allowed,
                created_at=db_quiz.created_at
            )
        except Exception as e:
            logger.error(f"Error converting quiz: {str(e)}")
            # Return a default quiz as fallback
            return Quiz(
                id=str(db_quiz.id) if hasattr(db_quiz, 'id') else "unknown",
                lesson_id=str(db_quiz.lesson_id) if hasattr(db_quiz, 'lesson_id') else "unknown",
                title=db_quiz.title if hasattr(db_quiz, 'title') else "Unknown Quiz",
                questions={"questions": []},
                time_limit=None,
                passing_score=70.0,
                attempts_allowed=3,
                created_at=datetime.now(timezone.utc)
            )
    
    def _convert_db_user_answer_to_user_answer(self, db_user_answer: DBUserAnswer) -> UserAnswer:
        """Convert a database user answer model to a UserAnswer model"""
        try:
            return UserAnswer(
                id=str(db_user_answer.id),
                user_id=str(db_user_answer.user_id),
                quiz_id=str(db_user_answer.quiz_id),
                answers=db_user_answer.answers,
                score=db_user_answer.score,
                attempt_number=db_user_answer.attempt_number,
                completed=db_user_answer.completed,
                created_at=db_user_answer.created_at
            )
        except Exception as e:
            logger.error(f"Error converting user answer: {str(e)}")
            # Return a default user answer as fallback
            return UserAnswer(
                id=str(db_user_answer.id) if hasattr(db_user_answer, 'id') else "unknown",
                user_id=str(db_user_answer.user_id) if hasattr(db_user_answer, 'user_id') else "unknown",
                quiz_id=str(db_user_answer.quiz_id) if hasattr(db_user_answer, 'quiz_id') else "unknown",
                answers={"answers": []},
                score=0.0,
                attempt_number=1,
                completed=False,
                created_at=datetime.now(timezone.utc)
            ) 