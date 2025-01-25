from sqlalchemy.orm import Session
from src.db.models import Progress
import uuid


def create_progress(db: Session, user_id: uuid.UUID, quiz_id: uuid.UUID, score: int):
    progress = Progress(id=uuid.uuid4(), user_id=user_id,
                        quiz_id=quiz_id, score=score)
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
