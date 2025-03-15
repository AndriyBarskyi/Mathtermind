import unittest
from unittest.mock import patch, MagicMock, call
import sys
from PyQt5 import QtWidgets
from src.services.credentials_manager import CredentialsManager
from src.services.user_service import UserService
from main import MathtermindApp


class TestAutoLogin(unittest.TestCase):
    """Unit tests for the auto-login functionality."""

    def setUp(self):
        """Set up test environment before each test."""
        # Create a QApplication instance for testing
        self.app = QtWidgets.QApplication.instance()
        if not self.app:
            self.app = QtWidgets.QApplication(sys.argv)
        
        # Test data
        self.test_email = "test@example.com"
        self.test_password = "test_password"
        self.test_user = MagicMock()
        self.test_user.id = "test_user_id"
        self.test_user.username = "test_user"
        
        # Create patches
        self.main_ui_patch = patch('main.MainWindowUI')
        self.init_db_patch = patch('main.init_db')
        self.seed_courses_patch = patch('main.seed_courses')
        self.seed_users_patch = patch('main.seed_users')
        self.get_db_patch = patch('main.get_db')
        self.qmessagebox_patch = patch('main.QMessageBox')
        self.login_dialog_patch = patch('main.LoginDialog')
        self.credentials_manager_patch = patch('main.CredentialsManager')
        self.user_service_patch = patch('main.UserService')
        
        # Start patches
        self.main_ui_mock = self.main_ui_patch.start()
        self.init_db_mock = self.init_db_patch.start()
        self.seed_courses_mock = self.seed_courses_patch.start()
        self.seed_users_mock = self.seed_users_patch.start()
        self.get_db_mock = self.get_db_patch.start()
        self.qmessagebox_mock = self.qmessagebox_patch.start()
        self.login_dialog_mock = self.login_dialog_patch.start()
        self.credentials_manager_class_mock = self.credentials_manager_patch.start()
        self.user_service_mock = self.user_service_patch.start()
        
        # Set up specific mocks
        self.credentials_manager_mock = MagicMock()
        self.credentials_manager_class_mock.return_value = self.credentials_manager_mock
        
        # Set up UserService mock methods
        self.user_service_mock.authenticate_user = MagicMock()
        self.user_service_mock.get_user = MagicMock()

    def tearDown(self):
        """Clean up after each test."""
        self.main_ui_patch.stop()
        self.init_db_patch.stop()
        self.seed_courses_patch.stop()
        self.seed_users_patch.stop()
        self.get_db_patch.stop()
        self.qmessagebox_patch.stop()
        self.login_dialog_patch.stop()
        self.credentials_manager_patch.stop()
        self.user_service_patch.stop()

    def test_auto_login_success(self):
        """Test successful auto-login with saved credentials."""
        # Set up mocks for successful auto-login
        self.credentials_manager_mock.load_credentials.return_value = {
            "email": self.test_email,
            "password": self.test_password
        }
        self.user_service_mock.authenticate_user.return_value = self.test_user
        self.user_service_mock.get_user.return_value = self.test_user
        
        # Create MathtermindApp instance
        app = MathtermindApp()
        
        # Reset mocks to clear initialization calls
        self.credentials_manager_mock.reset_mock()
        self.user_service_mock.authenticate_user.reset_mock()
        self.login_dialog_mock.reset_mock()
        
        # Call login_user with auto-login
        app.login_user(force_show_dialog=False, show_success_message=False)
        
        # Verify auto-login was attempted
        self.credentials_manager_mock.load_credentials.assert_called_once()
        self.user_service_mock.authenticate_user.assert_called_once_with(
            self.test_email, self.test_password
        )
        
        # Verify login dialog was not shown
        self.login_dialog_mock.assert_not_called()

    def test_auto_login_failure(self):
        """Test auto-login failure with invalid credentials."""
        # Set up mocks for failed auto-login
        self.credentials_manager_mock.load_credentials.return_value = {
            "email": self.test_email,
            "password": self.test_password
        }
        self.user_service_mock.authenticate_user.return_value = None
        
        # Create mock login dialog
        mock_login_dialog_instance = MagicMock()
        self.login_dialog_mock.return_value = mock_login_dialog_instance
        mock_login_dialog_instance.exec_.return_value = QtWidgets.QDialog.Rejected
        
        # Create MathtermindApp instance
        app = MathtermindApp()
        
        # Reset mocks to clear initialization calls
        self.credentials_manager_mock.reset_mock()
        self.user_service_mock.authenticate_user.reset_mock()
        self.login_dialog_mock.reset_mock()
        
        # Call login_user with auto-login
        app.login_user(force_show_dialog=False, show_success_message=False)
        
        # Verify auto-login was attempted
        self.credentials_manager_mock.load_credentials.assert_called_once()
        self.user_service_mock.authenticate_user.assert_called_once_with(
            self.test_email, self.test_password
        )
        
        # Verify login dialog was shown after auto-login failure
        self.login_dialog_mock.assert_called_once()
        mock_login_dialog_instance.exec_.assert_called_once()

    def test_force_show_dialog(self):
        """Test that login dialog is shown when force_show_dialog is True."""
        # Create mock login dialog
        mock_login_dialog_instance = MagicMock()
        self.login_dialog_mock.return_value = mock_login_dialog_instance
        mock_login_dialog_instance.exec_.return_value = QtWidgets.QDialog.Rejected
        
        # Create MathtermindApp instance
        app = MathtermindApp()
        
        # Reset mocks to clear initialization calls
        self.credentials_manager_mock.reset_mock()
        self.user_service_mock.authenticate_user.reset_mock()
        self.login_dialog_mock.reset_mock()
        
        # Call login_user with force_show_dialog=True
        app.login_user(force_show_dialog=True, show_success_message=False)
        
        # Verify auto-login was not attempted
        self.credentials_manager_mock.load_credentials.assert_not_called()
        self.user_service_mock.authenticate_user.assert_not_called()
        
        # Verify login dialog was shown
        self.login_dialog_mock.assert_called_once()
        mock_login_dialog_instance.exec_.assert_called_once()


if __name__ == '__main__':
    unittest.main() 