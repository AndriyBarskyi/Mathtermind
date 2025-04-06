"""
Password utilities for the Mathtermind application.

This module provides utilities for password hashing and verification,
as well as password strength validation.
"""

import bcrypt
import re
import secrets
import string
from typing import Tuple, List, Dict, Any

# Import our new logging and error handling framework
from src.core import get_logger
from src.core.error_handling import (
    handle_security_errors,
    SecurityError,
    report_error
)

# Set up logging
logger = get_logger(__name__)


@handle_security_errors(operation="hash_password")
def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: The plain text password to hash
        
    Returns:
        The hashed password
        
    Raises:
        SecurityError: If there is an error during password hashing
    """
    logger.debug("Hashing password")
    
    if not password:
        logger.error("Attempted to hash empty password")
        raise SecurityError(
            message="Cannot hash empty password",
            operation="hash_password"
        )
    
    try:
        # Generate a salt and hash the password
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode(), salt)
        logger.debug("Password hashed successfully")
        return hashed.decode()
    except Exception as e:
        logger.error(f"Error hashing password: {str(e)}")
        report_error(e, operation="hash_password")
        raise SecurityError(
            message="Failed to hash password",
            operation="hash_password",
            details={"error": str(e)}
        ) from e


@handle_security_errors(operation="verify_password")
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    
    Args:
        plain_password: The plain text password to check
        hashed_password: The hashed password to check against
        
    Returns:
        True if the password matches, False otherwise
        
    Raises:
        SecurityError: If there is an error during password verification
    """
    logger.debug("Verifying password")
    
    if not plain_password or not hashed_password:
        logger.error("Attempted to verify with empty password or hash")
        raise SecurityError(
            message="Cannot verify with empty password or hash",
            operation="verify_password"
        )
    
    try:
        result = bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
        if result:
            logger.debug("Password verification successful")
        else:
            logger.debug("Password verification failed")
        return result
    except Exception as e:
        logger.error(f"Error verifying password: {str(e)}")
        report_error(e, operation="verify_password")
        raise SecurityError(
            message="Failed to verify password",
            operation="verify_password",
            details={"error": str(e)}
        ) from e


@handle_security_errors(operation="validate_password_strength")
def validate_password_strength(password: str) -> Tuple[bool, List[str]]:
    """
    Validate the strength of a password.
    
    Args:
        password: The password to validate
        
    Returns:
        A tuple with (is_valid, [list of validation errors])
    """
    logger.debug("Validating password strength")
    
    if not password:
        logger.warning("Attempted to validate empty password")
        return (False, ["Password cannot be empty"])
    
    errors = []
    
    # Check length
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    # Check for uppercase
    if not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")
    
    # Check for lowercase
    if not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter")
    
    # Check for digits
    if not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one number")
    
    # Check for special characters
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character")
    
    is_valid = len(errors) == 0
    if is_valid:
        logger.debug("Password meets strength requirements")
    else:
        logger.info(f"Password failed strength validation with {len(errors)} issues")
    
    return (is_valid, errors)


@handle_security_errors(operation="generate_reset_token")
def generate_reset_token() -> str:
    """
    Generate a secure random token for password reset.
    
    Returns:
        A random string token
        
    Raises:
        SecurityError: If there is an error generating the reset token
    """
    logger.info("Generating password reset token")
    
    try:
        # Generate a 32-byte random token and convert to hex
        token = secrets.token_hex(32)
        logger.debug("Reset token generated successfully")
        return token
    except Exception as e:
        logger.error(f"Error generating reset token: {str(e)}")
        report_error(e, operation="generate_reset_token")
        raise SecurityError(
            message="Failed to generate reset token",
            operation="generate_reset_token",
            details={"error": str(e)}
        ) from e


@handle_security_errors(operation="generate_temporary_password")
def generate_temporary_password() -> str:
    """
    Generate a secure temporary password.
    
    Returns:
        A random string that passes the password strength validation
        
    Raises:
        SecurityError: If there is an error generating the temporary password
    """
    logger.info("Generating temporary password")
    
    try:
        # Define character sets
        uppercase_letters = string.ascii_uppercase
        lowercase_letters = string.ascii_lowercase
        digits = string.digits
        special_chars = "!@#$%^&*(),.?\":{}|<>"
        
        # Ensure at least one of each type
        temp_password = [
            secrets.choice(uppercase_letters),
            secrets.choice(lowercase_letters),
            secrets.choice(digits),
            secrets.choice(special_chars)
        ]
        
        # Add more random characters (total length 12)
        all_chars = uppercase_letters + lowercase_letters + digits + special_chars
        temp_password.extend(secrets.choice(all_chars) for _ in range(8))
        
        # Shuffle the characters to avoid predictable patterns
        secrets.SystemRandom().shuffle(temp_password)
        
        password = ''.join(temp_password)
        logger.debug("Temporary password generated successfully")
        
        # Validate the generated password
        valid, errors = validate_password_strength(password)
        if not valid:
            logger.error(f"Generated temporary password failed validation: {errors}")
            raise SecurityError(
                message="Generated password does not meet strength requirements",
                operation="generate_temporary_password"
            )
        
        return password
    except Exception as e:
        logger.error(f"Error generating temporary password: {str(e)}")
        report_error(e, operation="generate_temporary_password")
        raise SecurityError(
            message="Failed to generate temporary password",
            operation="generate_temporary_password",
            details={"error": str(e)}
        ) from e 