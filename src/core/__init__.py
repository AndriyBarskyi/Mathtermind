"""
Core Framework for Mathtermind

This package provides core functionality used throughout the Mathtermind application,
including logging and error handling.
"""

# Import from logging package
from .logging import (
    setup as setup_logging,
    get_logger,
    set_level,
    debug_mode,
    
    # Log levels
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL
)

# Import from error_handling package
from .error_handling import (
    # Base exception
    MathtermindError,
    
    # Error reporting
    report_error,
    safe_execute,
    create_error_boundary,
    
    # Decorators
    handle_service_errors,
    handle_ui_errors,
    handle_db_errors,
    with_error_boundary
)


def initialize(environment=None):
    """
    Initialize the core framework.
    
    This function initializes both the logging and error handling systems.
    
    Args:
        environment: The application environment (development, testing, production)
    """
    # Set up logging
    setup_logging(environment)
    
    # Log initialization
    logger = get_logger("mathtermind.core")
    logger.info(f"Core framework initialized in {environment or 'development'} environment")
    
    return True
