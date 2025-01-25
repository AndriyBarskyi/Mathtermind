from sqlalchemy.orm import Session
from src.db.models import UserAnswer
import uuid


def create_user_answer(
    db: Session, user_id: uuid.UUID, question_id: uuid.UUID, answer: str
):
    user_answer = UserAnswer(
        id=uuid.uuid4(), user_id=user_id, question_id=question_id, answer=answer
    )
    db.add(user_answer)
    db.commit()
    db.refresh(user_answer)
    return user_answer


def delete_user_answer(db: Session, user_answer_id: uuid.UUID):
    user_answer = db.query(UserAnswer).filter(
        UserAnswer.id == user_answer_id).first()
    db.delete(user_answer)
    db.commit()
    return user_answer


def get_user_answer(db: Session, user_answer_id: uuid.UUID):
    return db.query(UserAnswer).filter(UserAnswer.id == user_answer_id).first()


def update_user_answer(db: Session, user_answer_id: uuid.UUID, answer: str):
    user_answer = db.query(UserAnswer).filter(
        UserAnswer.id == user_answer_id).first()
    if user_answer is None:
        return None  # or raise an exception
    setattr(user_answer, "answer", answer)
    db.commit()
    db.refresh(user_answer)
    return user_answer
