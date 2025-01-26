from sqlalchemy.orm import Session
from src.db.models import User
import uuid
from typing import Optional


def create_user(db: Session, user: User) -> User:
    """
    Add a new user to the database.
    """
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: uuid.UUID) -> Optional[User]:
    """
    Retrieve a user by their ID.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Retrieve a user by their email.
    """
    return db.query(User).filter(User.email == email).first()


def delete_user(db: Session, user: User) -> None:
    """
    Delete a user from the database.
    """
    db.delete(user)
    db.commit()


def update_user(db: Session, user: User) -> User:
    """
    Update a user's information.
    """
    db.commit()
    db.refresh(user)
    return user
