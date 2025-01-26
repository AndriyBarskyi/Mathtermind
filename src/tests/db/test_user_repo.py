from src.db.models import User
import uuid


def test_user_creation(test_db):
    user = User(
        id=uuid.uuid4(),
        username="testuser",
        email="testuser@example.com",
        password_hash="hashed_password",
    )
    test_db.add(user)
    test_db.commit()

    # Check if the user is added
    fetched_user = test_db.query(User).filter_by(
        email="testuser@example.com").first()
    assert fetched_user is not None
    assert fetched_user.username == "testuser"


def test_user_deletion(test_db):
    # First, create a user to delete
    user = User(
        id=uuid.uuid4(),
        username="testuser",
        email="testuser@example.com",
        password_hash="hashed_password",
    )
    test_db.add(user)
    test_db.commit()

    # Fetch the user to ensure it was added
    fetched_user = test_db.query(User).filter_by(
        email="testuser@example.com").first()
    assert fetched_user is not None

    # Delete the user
    test_db.delete(fetched_user)
    test_db.commit()

    # Verify the user has been deleted
    deleted_user = test_db.query(User).filter_by(
        email="testuser@example.com").first()
    assert deleted_user is None


def test_user_update(test_db):
    # First, create a user to update
    user = User(
        id=uuid.uuid4(),
        username="testuser",
        email="testuser@example.com",
        password_hash="hashed_password",
    )
    test_db.add(user)
    test_db.commit()

    # Fetch the user to ensure it was added
    fetched_user = test_db.query(User).filter_by(
        email="testuser@example.com").first()
    assert fetched_user is not None

    # Update the user's username
    fetched_user.username = "updateduser"
    test_db.commit()

    # Verify the user's username has been updated
    updated_user = test_db.query(User).filter_by(
        email="testuser@example.com").first()
    assert updated_user is not None
    assert updated_user.username == "updateduser"


def test_user_read(test_db):
    # First, create a user to read
    user = User(
        id=uuid.uuid4(),
        username="testuser",
        email="testuser@example.com",
        password_hash="hashed_password",
    )
    test_db.add(user)
    test_db.commit()

    # Fetch the user to ensure it was added
    fetched_user = test_db.query(User).filter_by(
        email="testuser@example.com").first()
    assert fetched_user is not None
    assert fetched_user.username == "testuser"
    assert fetched_user.email == "testuser@example.com"
