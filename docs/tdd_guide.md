# Test-Driven Development Guide for Mathtermind

This guide outlines the Test-Driven Development (TDD) approach used in the Mathtermind project.

## What is TDD?

Test-Driven Development is a software development process that relies on the repetition of a very short development cycle:

1. **Red**: Write a failing test for the functionality you want to implement
2. **Green**: Write the minimum amount of code to make the test pass
3. **Refactor**: Improve the code while ensuring the tests still pass

## Benefits of TDD

- **Higher code quality**: TDD encourages simple, modular designs and prevents over-engineering
- **Better test coverage**: All code is written to satisfy a test, ensuring high test coverage
- **Documentation**: Tests serve as documentation for how the code should behave
- **Confidence in changes**: Tests provide a safety net for refactoring and adding new features
- **Faster debugging**: When a test fails, you know exactly what broke and where

## TDD Workflow in Mathtermind

### 1. Identify the Feature

Before writing any code, clearly define what feature or functionality you want to implement. Break it down into small, testable units.

### 2. Write a Failing Test

Write a test that defines the expected behavior of the feature. The test should fail because the feature doesn't exist yet.

```python
# Example: Testing a user repository's get_by_username method
def test_get_by_username(self, test_db, test_user):
    """Test getting a user by username."""
    # Arrange
    username = test_user.username
    
    # Act
    result = self.user_repo.get_by_username(test_db, username)
    
    # Assert
    assert result is not None
    assert result.id == test_user.id
    assert result.username == username
```

### 3. Run the Test

Run the test to verify that it fails. This confirms that the test is actually testing something and that the feature doesn't already exist.

```bash
./run_tests.py --file db/test_user_repo.py
```

### 4. Implement the Feature

Write the minimum amount of code needed to make the test pass.

```python
def get_by_username(self, db: Session, username: str) -> Optional[User]:
    """Get a user by username."""
    return db.query(User).filter(User.username == username).first()
```

### 5. Run the Test Again

Run the test again to verify that it passes. This confirms that your implementation satisfies the requirements defined in the test.

### 6. Refactor

Improve the code while ensuring the tests still pass. This might involve:

- Removing duplication
- Improving naming
- Enhancing performance
- Simplifying logic

### 7. Repeat

Repeat the process for the next feature or functionality.

## TDD Best Practices

### Keep Tests Focused

Each test should focus on a single aspect of functionality. This makes tests easier to understand and maintain.

### Use Descriptive Test Names

Test names should clearly describe what the test is checking. This makes it easier to understand what's being tested and what's failing.

```python
# Good
def test_get_by_username_returns_correct_user(self):
    # ...

# Bad
def test_get_user(self):
    # ...
```

### Follow the Arrange-Act-Assert Pattern

Structure your tests using the Arrange-Act-Assert pattern:

- **Arrange**: Set up the test data and environment
- **Act**: Perform the action being tested
- **Assert**: Verify the expected outcome

```python
def test_create_user(self, test_db):
    # Arrange
    user_data = {
        "id": uuid.uuid4(),
        "username": "newuser",
        "email": "newuser@example.com",
        "password_hash": "hashed_password",
        "age_group": "15-17"
    }
    
    # Act
    result = self.user_repo.create(test_db, **user_data)
    
    # Assert
    assert result is not None
    assert result.username == "newuser"
    assert result.email == "newuser@example.com"
```

### Use Fixtures

Use fixtures to set up test data and environments. This reduces duplication and makes tests more maintainable.

```python
@pytest.fixture
def test_user(test_db):
    """Fixture for creating a test user."""
    user = User(
        id=uuid.uuid4(),
        username="testuser",
        email="testuser@example.com",
        password_hash="hashed_password",
        age_group="15-17"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user
```

### Test Edge Cases

Don't just test the happy path. Test edge cases and error conditions to ensure your code handles them correctly.

```python
def test_get_by_username_nonexistent_user(self, test_db):
    """Test getting a user by a username that doesn't exist."""
    # Arrange
    username = "nonexistentuser"
    
    # Act
    result = self.user_repo.get_by_username(test_db, username)
    
    # Assert
    assert result is None
```

### Use Mocks for External Dependencies

Use mocks to isolate the code being tested from external dependencies.

```python
def test_get_user_service(self):
    """Test getting a user from the service."""
    # Arrange
    self.mock_repository.get_by_id.return_value = self.test_user
    
    # Act
    result = self.service.get_by_id(self.test_user_id)
    
    # Assert
    self.mock_repository.get_by_id.assert_called_once_with(self.mock_db, self.test_user_id)
    assert result is self.test_user
```

## TDD Resources

- [Test-Driven Development: By Example](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530) by Kent Beck
- [Clean Code: A Handbook of Agile Software Craftsmanship](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882) by Robert C. Martin
- [Python Testing with pytest](https://pragprog.com/titles/bopytest/python-testing-with-pytest/) by Brian Okken 