from src.db.models import User
import uuid
from src.tests.utils.test_factories import UserFactory


def test_user_creation(test_db):
    # Create a user using the factory
    user = UserFactory.create()
    test_db.add(user)
    test_db.commit()

    # Check if the user is added
    fetched_user = test_db.query(User).filter_by(
        email=user.email).first()
    assert fetched_user is not None
    assert fetched_user.username == user.username


def test_user_deletion(test_db):
    # Create a user using the factory
    user = UserFactory.create()
    test_db.add(user)
    test_db.commit()

    # Fetch the user to ensure it was added
    fetched_user = test_db.query(User).filter_by(
        email=user.email).first()
    assert fetched_user is not None

    # Delete the user
    test_db.delete(fetched_user)
    test_db.commit()

    # Verify the user has been deleted
    deleted_user = test_db.query(User).filter_by(
        email=user.email).first()
    assert deleted_user is None


def test_user_update(test_db):
    # Create a user using the factory
    user = UserFactory.create()
    test_db.add(user)
    test_db.commit()

    # Fetch the user to ensure it was added
    fetched_user = test_db.query(User).filter_by(
        email=user.email).first()
    assert fetched_user is not None

    # Update the user's username
    new_username = "updateduser"
    fetched_user.username = new_username
    test_db.commit()

    # Verify the user's username has been updated
    updated_user = test_db.query(User).filter_by(
        email=user.email).first()
    assert updated_user is not None
    assert updated_user.username == new_username


def test_user_read(test_db):
    # Create a user using the factory with specific attributes
    user = UserFactory.create(
        username="specificuser",
        email="specific@example.com"
    )
    test_db.add(user)
    test_db.commit()

    # Fetch the user to ensure it was added
    fetched_user = test_db.query(User).filter_by(
        email="specific@example.com").first()
    assert fetched_user is not None
    assert fetched_user.username == "specificuser"
    assert fetched_user.email == "specific@example.com"
