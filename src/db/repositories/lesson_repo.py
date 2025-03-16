from sqlalchemy.orm import Session
from src.db.models import Lesson
import uuid


def create_lesson(db: Session, name: str, description: str, course_id: uuid.UUID):
    lesson = Lesson(
        id=uuid.uuid4(), name=name, description=description, course_id=course_id
    )
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


def delete_lesson(db: Session, lesson_id: uuid.UUID):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    db.delete(lesson)
    db.commit()
    return lesson


def get_lesson(db: Session, lesson_id: uuid.UUID):
    return db.query(Lesson).filter(Lesson.id == lesson_id).first()


def update_lesson(db: Session, lesson_id: uuid.UUID, name: str, description: str):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson is None:
        return None  # or raise an exception
    setattr(lesson, "name", name)
    setattr(lesson, "description", description)
    db.commit()
    db.refresh(lesson)
    return lesson


def get_all_lessons(db: Session):
    return db.query(Lesson).all()


def get_lessons_by_course_id(db: Session, course_id: uuid.UUID):
    return db.query(Lesson).filter(Lesson.course_id == course_id).all()
