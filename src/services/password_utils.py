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


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: The plain text password to hash
        
    Returns:
        The hashed password
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    
    Args:
        plain_password: The plain text password to check
        hashed_password: The hashed password to check against
        
    Returns:
        True if the password matches, False otherwise
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def validate_password_strength(password: str) -> Tuple[bool, List[str]]:
    """
    Validate the strength of a password.
    
    Args:
        password: The password to validate
        
    Returns:
        A tuple with (is_valid, [list of validation errors])
    """
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
    
    return (len(errors) == 0, errors)


def generate_reset_token() -> str:
    """
    Generate a secure random token for password reset.
    
    Returns:
        A random string token
    """
    # Generate a 32-byte random token and convert to hex
    return secrets.token_hex(32)


def generate_temporary_password() -> str:
    """
    Generate a secure temporary password.
    
    Returns:
        A random string that passes the password strength validation
    """
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
    
    return ''.join(temp_password) 