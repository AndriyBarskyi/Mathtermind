# Test-Driven Development in Mathtermind

This directory contains tests for the Mathtermind project, following a Test-Driven Development (TDD) approach.

## TDD Approach

The Mathtermind project follows a Test-Driven Development approach, which means:

1. **Write a failing test** for a new feature or functionality
2. **Implement the minimum code** needed to make the test pass
3. **Refactor** the code while ensuring the tests still pass

This approach ensures that all code is tested, and that the tests drive the design of the code.

## Test Structure

The tests are organized into the following directories:

- `db/`: Tests for database models and repositories
- `services/`: Tests for service layer components
- `ui/`: Tests for UI components

## Base Test Classes

The `base_test_classes.py` file contains base classes for testing repositories, services, and models. These classes provide common functionality and fixtures for tests.

- `BaseRepositoryTest`: Base class for repository tests
- `BaseServiceTest`: Base class for service tests
- `BaseModelTest`: Base class for model tests

## Fixtures

The `conftest.py` file contains fixtures for creating test data and database sessions. These fixtures are used by the tests to set up the test environment.

## Running Tests

You can run the tests using the `run_tests.py` script in the root directory:

```bash
# Run all tests
./run_tests.py

# Run unit tests only
./run_tests.py -u

# Run repository tests only
./run_tests.py -r

# Run service tests only
./run_tests.py -s

# Run tests with coverage report
./run_tests.py -c

# Run tests for a specific module
./run_tests.py --module db

# Run tests for a specific file
./run_tests.py --file db/test_user_repo.py
```

## Writing New Tests

When writing new tests, follow these guidelines:

1. **Use the base test classes** to ensure consistent testing patterns
2. **Follow the Arrange-Act-Assert pattern** to structure your tests
3. **Use descriptive test names** that explain what the test is checking
4. **Keep tests focused** on a single aspect of functionality
5. **Use fixtures** to set up test data and environments

## Example Test

Here's an example of a test for a repository:

```python
@pytest.mark.repository
@pytest.mark.unit
class TestUserRepository(BaseRepositoryTest):
    """Tests for the UserRepository class."""
    
    def setup_method(self):
        """Set up the test environment before each test."""
        self.user_repo = UserRepository()
    
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

## Test Coverage

The tests aim to achieve high code coverage, ensuring that all code paths are tested. You can generate a coverage report using:

```bash
./run_tests.py -c --html
```

This will generate an HTML coverage report in the `htmlcov` directory. 