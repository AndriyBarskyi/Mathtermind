import unittest
from unittest.mock import patch, MagicMock, call, ANY
import time
import re
from src.services.auth_service import AuthService
from src.services.password_utils import hash_password
from src.services.permission_service import Permission
import uuid
from datetime import datetime, timedelta


class TestAuthService(unittest.TestCase):
    """Unit tests for the AuthService class."""

    def setUp(self):
        """Set up test environment before each test."""
        # Create mock repository
        self.mock_user_repo = MagicMock()
        
        # Patch dependencies
        self.db_patcher = patch('src.services.auth_service.get_db')
        self.mock_db = self.db_patcher.start()
        
        self.repository_patcher = patch('src.services.auth_service.user_repo', self.mock_user_repo)
        self.repository_patcher.start()
        
        self.session_manager_patcher = patch('src.services.auth_service.SessionManager')
        self.mock_session_manager = self.session_manager_patcher.start().return_value
        
        self.permission_service_patcher = patch('src.services.auth_service.PermissionService')
        self.mock_permission_service = self.permission_service_patcher.start().return_value
        
        # Set up AuthService with mocks
        self.auth_service = AuthService()
        
        # Set the mocked dependencies
        self.auth_service.session_manager = self.mock_session_manager
        self.auth_service.permission_service = self.mock_permission_service
        
        # Test user data
        self.test_user_id = "user-123"
        self.test_username = "testuser"
        self.test_email = "test@example.com"
        self.test_password = "SecureP@ss123"
        self.test_hashed_password = hash_password(self.test_password)
        
        self.test_user = {
            "id": self.test_user_id,
            "username": self.test_username,
            "email": self.test_email,
            "password_hash": self.test_hashed_password,
            "is_active": True,
            "is_admin": False,
            "role": "STUDENT"
        }
        
        # Create a MagicMock for the User object
        self.mock_user = MagicMock()
        for key, value in self.test_user.items():
            setattr(self.mock_user, key, value)
        
        # Set up session token
        self.test_session_token = "test-session-token-123"
        
        # Set up reset token
        self.test_reset_token = "abcdef1234567890"

    def tearDown(self):
        """Clean up after each test."""
        self.db_patcher.stop()
        self.repository_patcher.stop()
        self.session_manager_patcher.stop()
        self.permission_service_patcher.stop()

    @patch('src.services.auth_service.verify_password')
    def test_login_with_username_success(self, mock_verify_password):
        """Test successful login with username."""
        # Set up mocks
        self.mock_user_repo.get_user_by_username.return_value = self.mock_user
        self.mock_user_repo.get_user_by_email.return_value = None
        mock_verify_password.return_value = True
        self.mock_session_manager.create_session.return_value = self.test_session_token
        
        # Call login
        success, token, user_data = self.auth_service.login(
            username_or_email=self.test_username,
            password=self.test_password
        )
        
        # Verify result
        self.assertTrue(success)
        self.assertEqual(token, self.test_session_token)
        self.assertEqual(user_data["id"], self.test_user_id)
        self.assertEqual(user_data["username"], self.test_username)
        self.assertEqual(user_data["email"], self.test_email)
        self.assertEqual(user_data["role"], "STUDENT")
        
        # Verify method calls
        self.mock_user_repo.get_user_by_username.assert_called_once_with(ANY, self.test_username)
        mock_verify_password.assert_called_once_with(self.test_password, self.test_hashed_password)
        self.mock_session_manager.create_session.assert_called_once()

    @patch('src.services.auth_service.verify_password')
    def test_login_with_email_success(self, mock_verify_password):
        """Test successful login with email."""
        # Set up mocks
        self.mock_user_repo.get_user_by_username.return_value = None
        self.mock_user_repo.get_user_by_email.return_value = self.mock_user
        mock_verify_password.return_value = True
        self.mock_session_manager.create_session.return_value = self.test_session_token
        
        # Call login
        success, token, user_data = self.auth_service.login(
            username_or_email=self.test_email,
            password=self.test_password
        )
        
        # Verify result
        self.assertTrue(success)
        self.assertEqual(token, self.test_session_token)
        self.assertEqual(user_data["id"], self.test_user_id)
        
        # Verify method calls
        self.mock_user_repo.get_user_by_email.assert_called_once_with(ANY, self.test_email)

    @patch('src.services.auth_service.verify_password')
    def test_login_user_not_found(self, mock_verify_password):
        """Test login with nonexistent user."""
        # Set up mocks
        self.mock_user_repo.get_user_by_username.return_value = None
        self.mock_user_repo.get_user_by_email.return_value = None
        
        # Call login 
        success, token, user_data = self.auth_service.login(
            username_or_email="nonexistent",
            password=self.test_password
        )
        
        # Verify result
        self.assertFalse(success)
        self.assertIsNone(token)
        self.assertIsNone(user_data)
        
        # Verify method calls
        mock_verify_password.assert_not_called()

    @patch('src.services.auth_service.verify_password')
    def test_login_invalid_password(self, mock_verify_password):
        """Test login with invalid password."""
        # Set up mocks
        self.mock_user_repo.get_user_by_username.return_value = self.mock_user
        mock_verify_password.return_value = False
        
        # Call login
        success, token, user_data = self.auth_service.login(
            username_or_email=self.test_username,
            password="WrongPassword123!"
        )
        
        # Verify result
        self.assertFalse(success)
        self.assertIsNone(token)
        self.assertIsNone(user_data)
        
        # Verify method calls
        mock_verify_password.assert_called_once_with("WrongPassword123!", self.test_hashed_password)
        self.mock_session_manager.create_session.assert_not_called()

    @patch('src.services.auth_service.validate_password_strength')
    @patch('src.services.auth_service.hash_password')
    def test_register_success(self, mock_hash_password, mock_validate_password):
        """Test successful user registration."""
        # Set up mocks
        self.mock_user_repo.get_user_by_username.return_value = None
        self.mock_user_repo.get_user_by_email.return_value = None
        mock_validate_password.return_value = (True, [])
        mock_hash_password.return_value = self.test_hashed_password
        
        # Create a mock user with ID
        new_user = MagicMock()
        new_user.id = self.test_user_id
        self.mock_user_repo.create_user.return_value = new_user
        
        # Call register
        success, user_id, error = self.auth_service.register(
            username=self.test_username,
            email=self.test_email,
            password=self.test_password
        )
        
        # Verify result
        self.assertTrue(success)
        self.assertEqual(user_id, self.test_user_id)
        self.assertIsNone(error)
        
        # Verify method calls
        self.mock_user_repo.get_user_by_username.assert_called_once_with(ANY, self.test_username)
        self.mock_user_repo.get_user_by_email.assert_called_once_with(ANY, self.test_email)
        mock_validate_password.assert_called_once_with(self.test_password)
        mock_hash_password.assert_called_once_with(self.test_password)
        self.mock_user_repo.create_user.assert_called_once()

    def test_register_username_taken(self):
        """Test registration with taken username."""
        # Set up mocks
        self.mock_user_repo.get_user_by_username.return_value = self.mock_user
        
        # Call register
        success, user_id, error = self.auth_service.register(
            username=self.test_username,
            email=self.test_email,
            password=self.test_password
        )
        
        # Verify result
        self.assertFalse(success)
        self.assertIsNone(user_id)
        self.assertIn("Username", error)

    def test_register_email_taken(self):
        """Test registration with taken email."""
        # Set up mocks
        self.mock_user_repo.get_user_by_username.return_value = None
        self.mock_user_repo.get_user_by_email.return_value = self.mock_user
        
        # Call register
        success, user_id, error = self.auth_service.register(
            username=self.test_username,
            email=self.test_email,
            password=self.test_password
        )
        
        # Verify result
        self.assertFalse(success)
        self.assertIsNone(user_id)
        self.assertIn("Email", error)

    def test_register_invalid_email(self):
        """Test registration with invalid email format."""
        # Call register
        success, user_id, error = self.auth_service.register(
            username=self.test_username,
            email="invalid-email",
            password=self.test_password
        )
        
        # Verify result
        self.assertFalse(success)
        self.assertIsNone(user_id)
        self.assertIn("Invalid email", error)

    @patch('src.services.auth_service.validate_password_strength')
    def test_register_weak_password(self, mock_validate_password):
        """Test registration with weak password."""
        # Set up mocks
        self.mock_user_repo.get_user_by_username.return_value = None
        self.mock_user_repo.get_user_by_email.return_value = None
        mock_validate_password.return_value = (False, ["Password is too weak"])
        
        # Call register
        success, user_id, error = self.auth_service.register(
            username=self.test_username,
            email=self.test_email,
            password="weak"
        )
        
        # Verify result
        self.assertFalse(success)
        self.assertIsNone(user_id)
        self.assertIn("Password is too weak", error)

    def test_logout(self):
        """Test logging out a user."""
        # Set up mocks
        self.mock_session_manager.destroy_session.return_value = True
        
        # Call logout
        result = self.auth_service.logout(self.test_session_token)
        
        # Verify result
        self.assertTrue(result)
        
        # Verify session is destroyed
        self.mock_session_manager.destroy_session.assert_called_once_with(self.test_session_token)

    def test_validate_session_valid(self):
        """Test validating a valid session."""
        # Set up mocks
        session_data = {
            "user_id": self.test_user_id,
            "data": {
                "id": self.test_user_id,
                "username": self.test_username,
                "email": self.test_email,
                "role": "STUDENT"
            }
        }
        self.mock_session_manager.get_session.return_value = session_data
        
        # Call validate_session
        result = self.auth_service.validate_session(self.test_session_token)
        
        # Verify result
        self.assertEqual(result, session_data)
        
        # Verify session is validated
        self.mock_session_manager.get_session.assert_called_once_with(self.test_session_token)

    def test_validate_session_invalid(self):
        """Test validating an invalid session."""
        # Set up mocks
        self.mock_session_manager.get_session.return_value = None
        
        # Call validate_session
        result = self.auth_service.validate_session(self.test_session_token)
        
        # Verify result
        self.assertIsNone(result)

    def test_get_current_user_valid_session(self):
        """Test getting current user with valid session."""
        # Set up mocks
        user_data = {
            "id": self.test_user_id,
            "username": self.test_username,
            "email": self.test_email,
            "role": "STUDENT"
        }
        session_data = {
            "user_id": self.test_user_id,
            "data": user_data
        }
        self.mock_session_manager.get_session.return_value = session_data
        
        # Call get_current_user
        result = self.auth_service.get_current_user(self.test_session_token)
        
        # Verify result
        self.assertEqual(result, user_data)

    def test_get_current_user_invalid_session(self):
        """Test getting current user with invalid session."""
        # Set up mocks
        self.mock_session_manager.get_session.return_value = None
        
        # Call get_current_user
        result = self.auth_service.get_current_user(self.test_session_token)
        
        # Verify result
        self.assertIsNone(result)

    @patch('src.services.auth_service.verify_password')
    @patch('src.services.auth_service.validate_password_strength')
    @patch('src.services.auth_service.hash_password')
    def test_change_password_success(self, mock_hash_password, mock_validate_password, mock_verify_password):
        """Test successful password change."""
        # Set up mocks
        self.mock_user_repo.get_by_id.return_value = self.mock_user
        mock_verify_password.return_value = True
        mock_validate_password.return_value = (True, [])
        new_hashed_password = hash_password("NewSecureP@ss456")
        mock_hash_password.return_value = new_hashed_password
        
        # Make sure UUID conversion works properly
        self.test_user_id = str(uuid.uuid4())
        
        # Call change_password
        success, error = self.auth_service.change_password(
            user_id=self.test_user_id,
            current_password=self.test_password,
            new_password="NewSecureP@ss456"
        )
        
        # Verify result
        self.assertTrue(success)
        self.assertIsNone(error)
        
        # Verify method calls
        self.mock_user_repo.get_by_id.assert_called_once()
        mock_verify_password.assert_called_once_with(self.test_password, self.test_hashed_password)
        mock_validate_password.assert_called_once_with("NewSecureP@ss456")
        mock_hash_password.assert_called_once_with("NewSecureP@ss456")
        
        # Verify user update
        self.mock_user_repo.update_user.assert_called_once()

    @patch('src.services.auth_service.verify_password')
    def test_change_password_incorrect_current_password(self, mock_verify_password):
        """Test password change with incorrect current password."""
        # Set up mocks
        self.mock_user_repo.get_by_id.return_value = self.mock_user
        mock_verify_password.return_value = False
        
        # Make sure UUID conversion works properly
        self.test_user_id = str(uuid.uuid4())
        
        # Call change_password
        success, error = self.auth_service.change_password(
            user_id=self.test_user_id,
            current_password="WrongPassword123!",
            new_password="NewSecureP@ss456"
        )
        
        # Verify result
        self.assertFalse(success)
        self.assertIn("Current password is incorrect", error)

    def test_check_permission_with_valid_permission(self):
        """Test checking a valid permission for the current user."""
        # Set up mocks
        user_data = {
            "id": self.test_user_id,
            "username": self.test_username,
            "email": self.test_email,
            "role": "ADMIN"  # Admin has all permissions
        }
        session_data = {
            "user_id": self.test_user_id,
            "data": user_data
        }
        self.mock_session_manager.get_session.return_value = session_data
        self.mock_permission_service.user_has_permission.return_value = True
        
        # Call check_permission
        result = self.auth_service.check_permission(
            session_token=self.test_session_token,
            permission=Permission.DELETE_USERS
        )
        
        # Verify result
        self.assertTrue(result)

    def test_check_permission_with_invalid_permission(self):
        """Test checking an invalid permission for the current user."""
        # Set up mocks
        user_data = {
            "id": self.test_user_id,
            "username": self.test_username,
            "email": self.test_email,
            "role": "STUDENT"  # Student doesn't have MANAGE_USERS permission
        }
        session_data = {
            "user_id": self.test_user_id,
            "data": user_data
        }
        self.mock_session_manager.get_session.return_value = session_data
        self.mock_permission_service.user_has_permission.return_value = False
        
        # Call check_permission
        result = self.auth_service.check_permission(
            session_token=self.test_session_token,
            permission=Permission.DELETE_USERS
        )
        
        # Verify result
        self.assertFalse(result)

    def test_check_permission_with_invalid_session(self):
        """Test checking permission with invalid session."""
        # Set up mocks
        self.mock_session_manager.get_session.return_value = None
        
        # Call check_permission
        result = self.auth_service.check_permission(
            session_token=self.test_session_token,
            permission=Permission.DELETE_USERS
        )
        
        # Verify result
        self.assertFalse(result)

    @patch('src.services.auth_service.generate_temporary_password')
    @patch('src.services.auth_service.hash_password')
    def test_generate_temp_password(self, mock_hash_password, mock_generate_temp_password):
        """Test generating a temporary password for a user."""
        # Set up mocks
        self.mock_user_repo.get_by_id.return_value = self.mock_user
        temp_password = "Temp!P@ss123"
        mock_generate_temp_password.return_value = temp_password
        hashed_temp_password = hash_password(temp_password)
        mock_hash_password.return_value = hashed_temp_password
        
        # Make sure UUID conversion works properly
        self.test_user_id = str(uuid.uuid4())
        
        # Call generate_temp_password
        success, password = self.auth_service.generate_temp_password(self.test_user_id)
        
        # Verify result
        self.assertTrue(success)
        self.assertEqual(password, temp_password)
        
        # Verify method calls
        self.mock_user_repo.get_by_id.assert_called_once()
        mock_generate_temp_password.assert_called_once()
        mock_hash_password.assert_called_once_with(temp_password)
        
        # Verify user update
        self.mock_user_repo.update_user.assert_called_once()

    def test_generate_temp_password_user_not_found(self):
        """Test generating a temporary password for a nonexistent user."""
        # Set up mocks
        self.mock_user_repo.get_by_id.return_value = None
        
        # Call generate_temp_password
        success, password = self.auth_service.generate_temp_password("nonexistent-id")
        
        # Verify result
        self.assertFalse(success)
        self.assertIsNone(password)

    @patch('src.services.auth_service.generate_reset_token')
    def test_request_password_reset_success(self, mock_generate_token):
        """Test successful password reset request."""
        # Set up mocks
        self.mock_user_repo.get_user_by_email.return_value = self.mock_user
        mock_generate_token.return_value = self.test_reset_token
        
        # Call request_password_reset
        success, token = self.auth_service.request_password_reset(self.test_email)
        
        # Verify result
        self.assertTrue(success)
        self.assertEqual(token, self.test_reset_token)
        
        # Verify method calls
        self.mock_user_repo.get_user_by_email.assert_called_once_with(self.auth_service.db, self.test_email)
        mock_generate_token.assert_called_once()

    def test_request_password_reset_invalid_email(self):
        """Test password reset request with invalid email."""
        # Set up mocks
        self.mock_user_repo.get_user_by_email.return_value = None
        
        # Call request_password_reset
        success, token = self.auth_service.request_password_reset("nonexistent@email.com")
        
        # Verify result - note: we return True for non-existent emails for security reasons
        # but the token is None
        self.assertTrue(success)
        self.assertIsNone(token)
        
        # Verify method calls
        self.mock_user_repo.get_user_by_email.assert_called_once()

    @patch('src.services.auth_service.validate_password_strength')
    @patch('src.services.auth_service.hash_password')
    def test_reset_password_success(self, mock_hash_password, mock_validate_password):
        """Test successful password reset."""
        # Set up mocks
        mock_validate_password.return_value = (True, [])
        new_hashed_password = hash_password("NewSecureP@ss456")
        mock_hash_password.return_value = new_hashed_password
        
        # Prepare reset token
        user_id = str(uuid.uuid4())
        self.mock_user.id = uuid.UUID(user_id)
        self.mock_user_repo.get_by_id.return_value = self.mock_user
        
        # Manually add a reset token
        reset_token = self.test_reset_token
        expiry = datetime.now() + timedelta(hours=1)
        self.auth_service._reset_tokens[reset_token] = {
            "user_id": user_id,
            "expires_at": expiry
        }
        
        # Call reset_password
        success, error = self.auth_service.reset_password(
            token=reset_token,
            new_password="NewSecureP@ss456"
        )
        
        # Verify result
        self.assertTrue(success)
        self.assertIsNone(error)
        
        # Verify method calls
        mock_validate_password.assert_called_once_with("NewSecureP@ss456")
        mock_hash_password.assert_called_once_with("NewSecureP@ss456")
        self.mock_user_repo.update_user.assert_called_once()
        
        # Verify token was removed
        self.assertNotIn(reset_token, self.auth_service._reset_tokens)

    def test_reset_password_invalid_token(self):
        """Test password reset with invalid token."""
        # Call reset_password with invalid token
        success, error = self.auth_service.reset_password(
            token="invalid-token",
            new_password="NewSecureP@ss456"
        )
        
        # Verify result
        self.assertFalse(success)
        self.assertIn("Invalid or expired reset token", error)

    def test_reset_password_expired_token(self):
        """Test password reset with expired token."""
        # Set up expired token
        user_id = str(uuid.uuid4())
        reset_token = self.test_reset_token
        expiry = datetime.now() - timedelta(hours=1)  # 1 hour ago
        self.auth_service._reset_tokens[reset_token] = {
            "user_id": user_id,
            "expires_at": expiry
        }
        
        # Call reset_password
        success, error = self.auth_service.reset_password(
            token=reset_token,
            new_password="NewSecureP@ss456"
        )
        
        # Verify result
        self.assertFalse(success)
        self.assertIn("Reset token has expired", error)
        
        # Verify token was removed
        self.assertNotIn(reset_token, self.auth_service._reset_tokens)


if __name__ == '__main__':
    unittest.main() 