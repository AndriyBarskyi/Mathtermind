from sqlalchemy.orm import Session
from src.db.models import Progress
import uuid


def create_progress(db: Session, user_id: uuid.UUID, quiz_id: uuid.UUID, score: int):
    progress = Progress(id=uuid.uuid4(), user_id=user_id, quiz_id=quiz_id, score=score)
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress


def delete_progress(db: Session, progress_id: uuid.UUID):
    progress = db.query(Progress).filter(Progress.id == progress_id).first()
    db.delete(progress)
    db.commit()
    return progress


def update_progress(db: Session, progress_id: uuid.UUID, score: int):
    progress = db.query(Progress).filter(Progress.id == progress_id).first()
    if progress is None:
        return None  # or raise an exception
    setattr(progress, "score", score)
    db.commit()
    db.refresh(progress)
    return progress


def get_progress_by_user_and_course(
    db: Session, user_id: uuid.UUID, quiz_id: uuid.UUID
):
    return (
        db.query(Progress)
        .filter(Progress.user_id == user_id, Progress.quiz_id == quiz_id)
        .first()
    )


def get_progress_by_user(db: Session, user_id: uuid.UUID):
    return db.query(Progress).filter(Progress.user_id == user_id).all()


def get_user_progress(db: Session, user_id: uuid.UUID):
    """
    Get all progress records for a user, grouped by course.
    This is used to determine which courses are active for a user.
    """
    return db.query(Progress).filter(Progress.user_id == user_id).all()


def get_completed_progress(db: Session, user_id: uuid.UUID):
    """
    Get all completed progress records for a user.
    A course is considered completed if the user has a progress record with a progress_percentage of 100.
    """
    return db.query(Progress).filter(Progress.user_id == user_id, Progress.progress_percentage == 100).all()
