"""
Error Handling Framework for Mathtermind

This package provides a comprehensive error handling and reporting framework
for the Mathtermind application.
"""

# Import from exceptions module
from .exceptions import (
    # Base exception
    MathtermindError,
    
    # Database exceptions
    DatabaseError,
    DatabaseConnectionError,
    QueryError,
    MigrationError,
    
    # Authentication exceptions
    AuthenticationError,
    LoginError,
    PermissionError,
    AuthorizationError,
    TokenError,
    
    # Service exceptions
    ServiceError,
    ValidationError,
    ResourceNotFoundError,
    DependencyError,
    
    # UI exceptions
    UIError,
    RenderError,
    InputError,
    
    # File system exceptions
    FileSystemError,
    FileNotFoundError,
    AccessDeniedError,
    
    # Configuration exceptions
    ConfigurationError,
    
    # Content exceptions
    ContentError,
    ContentNotFoundError,
    ContentFormatError,
    
    # Security exceptions
    SecurityError,
    StorageError,
    SessionError
)

# Import from handlers module
from .handlers import (
    # Handler classes
    ErrorHandler,
    ServiceErrorHandler,
    UIErrorHandler,
    DatabaseErrorHandler,
    SecurityErrorHandler,
    
    # Decorators
    handle_service_errors,
    handle_ui_errors,
    handle_db_errors,
    handle_security_errors,
    with_error_boundary
)

# Import from reporting module
from .reporting import (
    ErrorContext,
    ErrorReporter,
    error_reporter,
    report_error,
    ErrorReportingContext
)

# Define a simplified API for common operations

def safe_execute(func, *args, context_name=None, **kwargs):
    """
    Execute a function safely, catching and reporting any exceptions.
    
    Args:
        func: The function to execute
        *args: Arguments to pass to the function
        context_name: Name of the context (for error reporting)
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        The return value of the function, or None if an exception occurred
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        context = context_name or func.__name__
        report_error(e, function=func.__name__, args=args, kwargs=kwargs, context=context)
        return None


def create_error_boundary(name):
    """
    Create an error boundary that can be used as a context manager.
    
    Args:
        name: Name of the error boundary
        
    Returns:
        An ErrorReportingContext instance
    """
    return ErrorReportingContext(name)
