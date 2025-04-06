import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from src.services.credentials_manager import CredentialsManager


class TestCredentialsManager(unittest.TestCase):
    """Unit tests for the CredentialsManager class."""

    def setUp(self):
        """Set up test environment before each test."""
        # Create a temporary file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, ".test_credentials")
        
        # Create an instance of CredentialsManager
        self.manager = CredentialsManager(app_data_dir=self.temp_dir)
        
        # Set the credentials_file directly 
        self.manager.credentials_file = self.temp_file
        
        # Test data
        self.test_email = "test@example.com"
        self.test_password = "test_password"

    def tearDown(self):
        """Clean up after each test."""
        # Remove the temporary file if it exists
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        
        # Remove the temporary directory
        os.rmdir(self.temp_dir)

    def test_save_and_load_credentials(self):
        """Test saving and loading credentials."""
        # Save credentials
        result = self.manager.save_credentials(self.test_email, self.test_password)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.temp_file))
        
        # Load credentials
        loaded_credentials = self.manager.load_credentials()
        self.assertIsNotNone(loaded_credentials)
        self.assertEqual(loaded_credentials.get("email"), self.test_email)
        self.assertEqual(loaded_credentials.get("password"), self.test_password)

    def test_clear_credentials(self):
        """Test clearing credentials."""
        # Save credentials first
        self.manager.save_credentials(self.test_email, self.test_password)
        self.assertTrue(os.path.exists(self.temp_file))
        
        # Clear credentials
        result = self.manager.clear_credentials()
        self.assertTrue(result)
        self.assertFalse(os.path.exists(self.temp_file))
        
        # Try to load credentials after clearing
        loaded_credentials = self.manager.load_credentials()
        self.assertIsNone(loaded_credentials)

    def test_load_nonexistent_credentials(self):
        """Test loading credentials when the file doesn't exist."""
        # Make sure the file doesn't exist
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        
        # Try to load credentials
        loaded_credentials = self.manager.load_credentials()
        self.assertIsNone(loaded_credentials)

    @patch('src.services.credentials_manager.Fernet')
    def test_encryption_decryption(self, mock_fernet):
        """Test that encryption and decryption are used correctly."""
        # Set up mock Fernet
        mock_fernet_instance = MagicMock()
        mock_fernet.return_value = mock_fernet_instance
        
        # Mock encrypt and decrypt methods
        mock_fernet_instance.encrypt.return_value = b"encrypted_data"
        mock_fernet_instance.decrypt.return_value = b'{"email":"test@example.com","password":"test_password"}'
        
        # Save credentials
        self.manager.save_credentials(self.test_email, self.test_password)
        
        # Verify encrypt was called
        mock_fernet_instance.encrypt.assert_called_once()
        
        # Load credentials
        loaded_credentials = self.manager.load_credentials()
        
        # Verify decrypt was called
        mock_fernet_instance.decrypt.assert_called_once()
        
        # Verify loaded credentials
        self.assertEqual(loaded_credentials.get("email"), self.test_email)
        self.assertEqual(loaded_credentials.get("password"), self.test_password)


if __name__ == '__main__':
    unittest.main() 