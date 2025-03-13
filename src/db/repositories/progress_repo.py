from sqlalchemy.orm import Session
from src.db.models import Progress
import uuid


def create_progress(db: Session, user_id: uuid.UUID, course_id: uuid.UUID, current_lesson_id: uuid.UUID = None):
    """Create a new progress record for a user and course"""
    progress = Progress(
        id=uuid.uuid4(),
        user_id=user_id,
        course_id=course_id,
        current_lesson_id=current_lesson_id,
        completed_lessons=[],
        progress_percentage=0.0,
        total_points_earned=0,
        time_spent=0,
        strengths=[],
        weaknesses=[],
        learning_path={},
        progress_data={"quiz_attempts": [], "practice_sessions": []}
    )
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress


def delete_progress(db: Session, progress_id: uuid.UUID):
    """Delete a progress record"""
    progress = db.query(Progress).filter(Progress.id == progress_id).first()
    if not progress:
        return None
    db.delete(progress)
    db.commit()
    return progress


def update_progress(db: Session, progress_id: uuid.UUID, update_data: dict):
    """Update a progress record with new data"""
    progress = db.query(Progress).filter(Progress.id == progress_id).first()
    if progress is None:
        return None
    
    # Update fields from update_data
    for key, value in update_data.items():
        if hasattr(progress, key):
            setattr(progress, key, value)
    
    db.commit()
    db.refresh(progress)
    return progress


def get_progress_by_user_and_course(db: Session, user_id: uuid.UUID, course_id: uuid.UUID):
    """Get progress for a specific user and course"""
    return (
        db.query(Progress)
        .filter(Progress.user_id == user_id, Progress.course_id == course_id)
        .first()
    )


def get_user_progress(db: Session, user_id: str):
    """Get all progress records for a user"""
    try:
        user_uuid = uuid.UUID(user_id)
        return db.query(Progress).filter(Progress.user_id == user_uuid).all()
    except ValueError:
        # Handle invalid UUID
        return []


def get_completed_progress(db: Session, user_id: str):
    """Get completed courses progress for a user (progress_percentage = 100)"""
    try:
        user_uuid = uuid.UUID(user_id)
        return (
            db.query(Progress)
            .filter(Progress.user_id == user_uuid, Progress.progress_percentage >= 100.0)
            .all()
        )
    except ValueError:
        # Handle invalid UUID
        return []


def update_lesson_completion(db: Session, user_id: uuid.UUID, course_id: uuid.UUID, 
                            lesson_id: uuid.UUID, score: float, time_spent: int):
    """Update a user's progress when they complete a lesson"""
    progress = get_progress_by_user_and_course(db, user_id, course_id)
    
    if not progress:
        # Create new progress if it doesn't exist
        progress = create_progress(db, user_id, course_id)
    
    # Add completed lesson to the list
    completed_lesson = {
        "lesson_id": str(lesson_id),
        "completed_at": str(uuid.uuid1().time),  # Use current time
        "score": score,
        "time_spent": time_spent
    }
    
    # Check if lesson is already completed
    lesson_already_completed = False
    for lesson in progress.completed_lessons:
        if lesson.get("lesson_id") == str(lesson_id):
            lesson_already_completed = True
            # Update existing completion data
            lesson.update(completed_lesson)
            break
    
    if not lesson_already_completed:
        progress.completed_lessons.append(completed_lesson)
    
    # Update total time spent
    progress.time_spent += time_spent
    
    # Update total points earned (assuming each lesson has points)
    # This would need to be calculated based on the lesson's points and score
    
    # Update progress percentage
    # This would need to calculate based on total lessons in the course
    
    db.commit()
    db.refresh(progress)
    return progress
