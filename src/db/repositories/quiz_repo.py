from sqlalchemy.orm import Session
from src.db.models import Quiz
import uuid


def create_quiz(db: Session, name: str, description: str, course_id: uuid.UUID):
    quiz = Quiz(
        id=uuid.uuid4(), name=name, description=description, course_id=course_id
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return quiz


def delete_quiz(db: Session, quiz_id: uuid.UUID):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    db.delete(quiz)
    db.commit()
    return quiz


def get_quiz(db: Session, quiz_id: uuid.UUID):
    return db.query(Quiz).filter(Quiz.id == quiz_id).first()


def update_quiz(db: Session, quiz_id: uuid.UUID, name: str, description: str):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if quiz is None:
        return None  # or raise an exception
    setattr(quiz, "name", name)
    setattr(quiz, "description", description)
    db.commit()
    db.refresh(quiz)
    return quiz
