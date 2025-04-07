# Changelog

## 2024-04-07
- Added flexible course filtering capabilities to `CourseService`
  - Implemented filtering by difficulty level, age group, topic, tags, and duration range
  - Created unified `filter_courses` method that replaces specific getter methods
  - Added comprehensive test coverage for all filtering scenarios
  
- Added course sorting capabilities to `CourseService`
  - Implemented sorting by name, duration, creation date, and difficulty level
  - Added support for both ascending and descending sorting
  - Created tests to verify sorting functionality and combined filtering/sorting workflow

- Implemented course categorization and tagging system
  - Added tag management methods to `CourseService` for adding/removing tags to/from courses
  - Created integration between `CourseService` and `TagService`
  - Implemented tag-based filtering for courses
  - Added support for categorizing courses with different tag categories (TOPIC, SKILL, DIFFICULTY)
  - Created comprehensive tests for tag operations and course categorization
