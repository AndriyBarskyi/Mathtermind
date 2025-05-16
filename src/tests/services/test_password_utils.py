import unittest
from unittest.mock import patch, MagicMock
import re
from src.services.password_utils import (
    hash_password,
    verify_password,
    validate_password_strength,
    generate_reset_token,
    generate_temporary_password
)
from src.core.error_handling.exceptions import SecurityError


class TestPasswordUtils(unittest.TestCase):
    """Unit tests for the password utilities module."""

    def setUp(self):
        """Set up test environment before each test."""
        self.test_password = "TestPassword123!"
        self.weak_passwords = [
            "short",  # Too short
            "lowercase",  # No uppercase, digits, or special chars
            "UPPERCASE",  # No lowercase, digits, or special chars
            "12345678",  # No letters or special chars
            "Password",  # No digits or special chars
            "password123",  # No uppercase or special chars
            "Password123",  # No special chars
            "Password!",  # No digits
        ]
        self.strong_passwords = [
            "StrongP@ssw0rd",
            "C0mplex!Password",
            "Sup3r$3cur3P@ss",
            "MyP@ssw0rd123",
            "P@$$w0rd"
        ]

    def test_hash_password(self):
        """Test that hashing a password produces a non-empty string."""
        hashed = hash_password(self.test_password)
        
        # Check that the hash is not empty
        self.assertTrue(hashed)
        self.assertIsInstance(hashed, str)
        
        # Check that the hash is not the original password
        self.assertNotEqual(hashed, self.test_password)
        
        # Check that the hash contains the bcrypt identifier
        self.assertTrue(hashed.startswith('$2'))

    def test_verify_password(self):
        """Test that password verification works correctly."""
        # Hash the test password
        hashed = hash_password(self.test_password)
        
        # Verify the correct password
        self.assertTrue(verify_password(self.test_password, hashed))
        
        # Verify an incorrect password
        self.assertFalse(verify_password("WrongPassword123!", hashed))
        
        # Verify with an empty password should raise SecurityError
        with self.assertRaises(SecurityError):
            verify_password("", hashed)

    def test_validate_password_strength_weak_passwords(self):
        """Test that weak passwords fail validation."""
        for password in self.weak_passwords:
            is_valid, errors = validate_password_strength(password)
            self.assertFalse(is_valid, f"Password '{password}' should be considered weak")
            self.assertTrue(len(errors) > 0, f"Password '{password}' should have validation errors")

    def test_validate_password_strength_strong_passwords(self):
        """Test that strong passwords pass validation."""
        for password in self.strong_passwords:
            is_valid, errors = validate_password_strength(password)
            self.assertTrue(is_valid, f"Password '{password}' should be considered strong")
            self.assertEqual(len(errors), 0, f"Password '{password}' should not have validation errors")

    def test_validate_password_strength_specific_requirements(self):
        """Test that validation checks for specific requirements."""
        # Test password length requirement
        is_valid, errors = validate_password_strength("Short1!")
        self.assertFalse(is_valid)
        self.assertTrue(any("8 characters" in error for error in errors))
        
        # Test uppercase requirement
        is_valid, errors = validate_password_strength("lowercase123!")
        self.assertFalse(is_valid)
        self.assertTrue(any("uppercase" in error for error in errors))
        
        # Test lowercase requirement
        is_valid, errors = validate_password_strength("UPPERCASE123!")
        self.assertFalse(is_valid)
        self.assertTrue(any("lowercase" in error for error in errors))
        
        # Test digit requirement
        is_valid, errors = validate_password_strength("NoDigitsHere!")
        self.assertFalse(is_valid)
        self.assertTrue(any("number" in error for error in errors))
        
        # Test special character requirement
        is_valid, errors = validate_password_strength("NoSpecialChars123")
        self.assertFalse(is_valid)
        self.assertTrue(any("special character" in error for error in errors))

    def test_generate_reset_token(self):
        """Test that reset token generation produces valid tokens."""
        token = generate_reset_token()
        
        # Check that the token is not empty
        self.assertTrue(token)
        self.assertIsInstance(token, str)
        
        # Check token length (64 characters for a 32-byte token in hex)
        self.assertEqual(len(token), 64)
        
        # Check that the token consists of hexadecimal characters
        self.assertTrue(all(c in "0123456789abcdef" for c in token))
        
        # Check that multiple calls generate different tokens
        another_token = generate_reset_token()
        self.assertNotEqual(token, another_token)

    def test_generate_temporary_password(self):
        """Test that temporary password generation produces strong passwords."""
        temp_password = generate_temporary_password()
        
        # Check that the password is not empty
        self.assertTrue(temp_password)
        self.assertIsInstance(temp_password, str)
        
        # Check password length (should be 12 characters)
        self.assertEqual(len(temp_password), 12)
        
        # Check that the password meets all the strength requirements
        is_valid, errors = validate_password_strength(temp_password)
        self.assertTrue(is_valid, f"Generated password '{temp_password}' is not strong enough")
        self.assertEqual(len(errors), 0)
        
        # Check that multiple calls generate different passwords
        another_temp_password = generate_temporary_password()
        self.assertNotEqual(temp_password, another_temp_password)
        
        # Verify it contains at least one of each required character type
        self.assertTrue(any(c.isupper() for c in temp_password), 
                      f"Password '{temp_password}' should contain uppercase letters")
        self.assertTrue(any(c.islower() for c in temp_password), 
                      f"Password '{temp_password}' should contain lowercase letters")
        self.assertTrue(any(c.isdigit() for c in temp_password), 
                      f"Password '{temp_password}' should contain digits")
        self.assertTrue(any(c in "!@#$%^&*(),.?\":{}|<>" for c in temp_password), 
                      f"Password '{temp_password}' should contain special characters")


if __name__ == '__main__':
    unittest.main() 