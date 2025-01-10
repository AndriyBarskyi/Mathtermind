# database/repositories.py
from sqlalchemy.orm import Session
from .models import User, Course

class UserRepository:
    @staticmethod
    def create_user(db: Session, name: str, email: str):
        user = User(name=name, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

class CourseRepository:
    @staticmethod
    def create_course(db: Session, title: str, owner_id: int):
        course = Course(title=title, owner_id=owner_id)
        db.add(course)
        db.commit()
        db.refresh(course)
        return course
