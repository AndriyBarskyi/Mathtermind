from sqlalchemy.orm import Session
from src.db.models import Course
import uuid


def create_course(db: Session, name: str, description: str):
    course = Course(id=uuid.uuid4(), name=name, description=description)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def delete_course(db: Session, course_id: uuid.UUID):
    course = db.query(Course).filter(Course.id == course_id).first()
    db.delete(course)
    db.commit()
    return course


def get_course(db: Session, course_id: uuid.UUID):
    return db.query(Course).filter(Course.id == course_id).first()


def update_course(db: Session, course_id: uuid.UUID, name: str, description: str):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        return None  # or raise an exception
    setattr(course, "name", name)
    setattr(course, "description", description)
    db.commit()
    db.refresh(course)
    return course
