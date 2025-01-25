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
