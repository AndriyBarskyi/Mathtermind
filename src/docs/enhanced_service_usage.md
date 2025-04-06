# Enhanced BaseService Usage Guide

This document provides guidelines and examples on how to effectively use the enhanced `BaseService` functionality in your service implementations.

## Table of Contents

1. [Introduction](#introduction)
2. [Transaction Management](#transaction-management)
3. [Caching](#caching)
4. [Validation](#validation)
5. [Error Handling](#error-handling)
6. [Best Practices](#best-practices)

## Introduction

The enhanced `BaseService` class provides several utilities to make service implementations more robust:

- **Transaction Management**: Proper handling of database transactions
- **Caching**: In-memory caching for frequently accessed data
- **Validation**: Data validation utilities
- **Error Handling**: Structured exception handling

## Transaction Management

### Using the Transaction Context Manager

The transaction context manager provides a clean way to handle transactions:

```python
def create_user_with_profile(self, user_data, profile_data):
    """Create a user with a profile in a single transaction."""
    with self.transaction():
        user = self.repository.create(self.db, **user_data)
        profile_data["user_id"] = user.id
        profile = self.profile_repository.create(self.db, **profile_data)
        return {"user": user, "profile": profile}
```

### Using execute_in_transaction

For simpler operations, you can use the `execute_in_transaction` method:

```python
def update_username(self, user_id, new_username):
    """Update a user's username in a transaction."""
    def _update():
        user = self.repository.get_by_id(self.db, user_id)
        if user is None:
            raise EntityNotFoundError(f"User with ID {user_id} not found")
        return self.repository.update(self.db, user_id, username=new_username)
    
    return self.execute_in_transaction(_update)
```

### Using batch_operation

For operations that need to be performed on multiple items:

```python
def deactivate_inactive_users(self, inactive_days=30):
    """Deactivate users who haven't logged in for a specified number of days."""
    cutoff_date = datetime.now() - timedelta(days=inactive_days)
    inactive_users = self.repository.get_inactive_users(self.db, cutoff_date)
    
    def deactivate_user(user):
        self.repository.update(self.db, user.id, is_active=False)
    
    self.batch_operation(inactive_users, deactivate_user, batch_size=50)
```

## Caching

### Basic Caching

Use the `cache` decorator to cache method results:

```python
@BaseService.cache("user")
def get_user_by_username(self, username):
    """Get a user by username with caching."""
    return self.repository.get_by_username(self.db, username)
```

### Caching with TTL

Specify a time-to-live for cached data:

```python
@BaseService.cache("leaderboard", ttl=timedelta(minutes=15))
def get_leaderboard(self, limit=10):
    """Get the top users by points, cached for 15 minutes."""
    return self.repository.get_top_users_by_points(self.db, limit)
```

### Cache Invalidation

Invalidate cache when data changes:

```python
def update_user_points(self, user_id, points_to_add):
    """Update a user's points and invalidate relevant caches."""
    with self.transaction():
        user = self.get_by_id(user_id)
        new_points = user.points + points_to_add
        self.repository.update(self.db, user_id, points=new_points)
        
    # Invalidate user cache entries and leaderboard
    self.invalidate_cache(f"user:{user_id}")
    self.invalidate_cache("leaderboard")
```

## Validation

### Simple Validation

Validate data before processing:

```python
def create_user(self, **user_data):
    """Create a new user with validation."""
    validators = {
        "username": lambda x: isinstance(x, str) and 3 <= len(x) <= 50,
        "email": lambda x: isinstance(x, str) and "@" in x,
        "age": lambda x: isinstance(x, int) and x >= 18
    }
    
    try:
        self.validate(user_data, validators)
        return super().create(**user_data)
    except ValidationError as e:
        self.logger.error(f"Validation failed: {str(e)}")
        raise
```

### Custom Validators

Define reusable validators:

```python
# In a validators.py module
def is_valid_email(email):
    """Check if an email is valid."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return isinstance(email, str) and bool(re.match(pattern, email))

# In your service
from src.utils.validators import is_valid_email

def update_user_email(self, user_id, email):
    """Update a user's email with validation."""
    self.validate({"email": email}, {"email": is_valid_email})
    return self.update(user_id, email=email)
```

## Error Handling

### Using Custom Exceptions

The base service provides several custom exceptions:

```python
from src.services.base_service import EntityNotFoundError, ValidationError, DatabaseError

def get_active_user(self, user_id):
    """Get an active user by ID."""
    user = self.get_by_id(user_id)  # This may raise EntityNotFoundError
    
    if not user.is_active:
        raise ValidationError(f"User {user_id} is not active")
    
    return user
```

### Structured Error Handling

Handle exceptions in a structured way:

```python
def perform_complex_operation(self, data):
    """Perform a complex operation with structured error handling."""
    try:
        # Validation
        self.validate(data, self.validators)
        
        # Database operation
        with self.transaction():
            # ... complex operations ...
            pass
            
        return {"status": "success"}
    except ValidationError as e:
        self.logger.warning(f"Validation error: {str(e)}")
        return {"status": "error", "error_type": "validation", "message": str(e)}
    except EntityNotFoundError as e:
        self.logger.warning(f"Not found error: {str(e)}")
        return {"status": "error", "error_type": "not_found", "message": str(e)}
    except DatabaseError as e:
        self.logger.error(f"Database error: {str(e)}")
        return {"status": "error", "error_type": "database", "message": "A database error occurred"}
    except Exception as e:
        self.logger.error(f"Unexpected error: {str(e)}")
        return {"status": "error", "error_type": "unknown", "message": "An unexpected error occurred"}
```

## Best Practices

1. **Use Transactions**: Always use transactions for operations that involve multiple database updates.

2. **Cache Wisely**: Cache read-heavy data that doesn't change frequently.

3. **Invalidate Cache**: Remember to invalidate cache when data changes.

4. **Validate Early**: Validate data as early as possible to prevent invalid data from reaching the database.

5. **Structured Error Handling**: Use the custom exceptions for clear error communication.

6. **Batch Operations**: Use batch operations for large data sets to improve performance.

7. **Include TTL**: Always include a TTL for cached data to prevent stale data issues.

8. **Log Exceptions**: Log exceptions at the appropriate level (warning, error, etc.).

9. **Test Thoroughly**: Test your service methods thoroughly, including failure cases.

10. **Document Clearly**: Document your methods clearly, including parameters, return values, and exceptions.

## Example: Full Service Implementation

Here's an example of a service that uses many of the enhanced features:

```python
from datetime import timedelta
from src.services.base_service import BaseService, EntityNotFoundError, ValidationError
from src.db.repositories.user_repository import UserRepository
from src.db.repositories.profile_repository import ProfileRepository

class UserService(BaseService):
    """Service for user management."""
    
    def __init__(self):
        """Initialize the service."""
        super().__init__(repository=UserRepository())
        self.profile_repository = ProfileRepository()
        
        # Validators
        self.user_validators = {
            "username": lambda x: isinstance(x, str) and 3 <= len(x) <= 50,
            "email": lambda x: isinstance(x, str) and "@" in x,
            "password": lambda x: isinstance(x, str) and len(x) >= 8
        }
    
    @BaseService.cache("user", ttl=timedelta(minutes=30))
    def get_by_username(self, username):
        """Get a user by username."""
        user = self.repository.get_by_username(self.db, username)
        if user is None:
            raise EntityNotFoundError(f"User with username {username} not found")
        return user
    
    def create_user_with_profile(self, user_data, profile_data):
        """Create a user with a profile."""
        # Validate data
        self.validate(user_data, self.user_validators)
        
        # Create user and profile in a transaction
        with self.transaction():
            user = self.repository.create(self.db, **user_data)
            profile_data["user_id"] = user.id
            profile = self.profile_repository.create(self.db, **profile_data)
        
        return {"user": user, "profile": profile}
    
    def update_email(self, user_id, email):
        """Update a user's email."""
        self.validate({"email": email}, {"email": self.user_validators["email"]})
        
        with self.transaction():
            user = self.get_by_id(user_id)  # May raise EntityNotFoundError
            result = self.repository.update(self.db, user_id, email=email)
        
        # Invalidate cache
        self.invalidate_cache(f"user:{user_id}")
        self.invalidate_cache(f"user")  # Invalidate all user caches
        
        return result
    
    @BaseService.cache("leaderboard", ttl=timedelta(hours=1))
    def get_leaderboard(self, limit=10):
        """Get the top users by points."""
        return self.repository.get_top_users_by_points(self.db, limit)
    
    def deactivate_inactive_users(self, inactive_days=30):
        """Deactivate users who haven't logged in for a specified number of days."""
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.now() - timedelta(days=inactive_days)
        inactive_users = self.repository.get_inactive_users(self.db, cutoff_date)
        
        def deactivate_user(user):
            self.repository.update(self.db, user.id, is_active=False)
            self.invalidate_cache(f"user:{user.id}")
        
        self.batch_operation(inactive_users, deactivate_user, batch_size=50)
        return len(inactive_users)
```

This example demonstrates how to combine transactions, caching, validation, and error handling in a service implementation. 