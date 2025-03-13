# Mathtermind Tests

This directory contains unit tests for the Mathtermind application.

## Test Structure

The tests are organized by component type:

- `services/`: Tests for service classes that handle business logic
- `widgets/`: Tests for UI widgets
- `pages/`: Tests for page components

## Running Tests

### Running All Tests

To run all tests, use the test runner script:

```bash
python tests/run_tests.py
```

Or make it executable and run it directly:

```bash
chmod +x tests/run_tests.py
./tests/run_tests.py
```

### Running Specific Test Modules

To run a specific test module:

```bash
python -m unittest tests.ui.services.test_course_service
```

### Running Specific Test Cases

To run a specific test case:

```bash
python -m unittest tests.ui.services.test_course_service.TestCourseService
```

### Running Specific Test Methods

To run a specific test method:

```bash
python -m unittest tests.ui.services.test_course_service.TestCourseService.test_filter_courses_by_search_text_in_name
```

## Writing Tests

When writing tests, follow these guidelines:

1. Create a new test file for each component you want to test
2. Use descriptive test method names that explain what is being tested
3. Use the `setUp` method to prepare test fixtures
4. Use the `tearDown` method to clean up after tests
5. Use mocks to isolate the component being tested
6. Test both normal and edge cases

## Test Coverage

To generate a test coverage report, install the `coverage` package:

```bash
pip install coverage
```

Then run the tests with coverage:

```bash
coverage run tests/run_tests.py
```

And generate a report:

```bash
coverage report
```

Or an HTML report:

```bash
coverage html
``` 