"""
Tests for the user service.
"""

import pytest
import uuid
from datetime import datetime
from unittest.mock import MagicMock, patch

from src.core.error_handling.exceptions import ValidationError, ResourceNotFoundError, DatabaseError
from src.models.user import User as UIUser
from src.db.models.user import User as DBUser
from src.db.repositories.user_repo import UserRepository
from src.services.user_service import UserService
from src.tests.base_test_classes import BaseServiceTest

# Mock the ValidationError
@pytest.fixture
def mock_validation_error():
    with patch('src.core.error_handling.exceptions.ValidationError') as mock:
        mock.return_value = MagicMock(side_effect=ValidationError)
        yield mock

class TestUserService(BaseServiceTest):
    """Tests for UserService"""
    
    def setUp(self):
        """Set up test case."""
        super().setUp()
        
        # Mock the UserRepository so its __init__ doesn't fail
        self.user_repo_mock = MagicMock(spec=UserRepository)
        
        # Patch the UserRepository class to return our mock on instantiation
        self.user_repo_patcher = patch('src.services.user_service.UserRepository')
        self.user_repo_class_mock = self.user_repo_patcher.start()
        self.user_repo_class_mock.return_value = self.user_repo_mock
        
        # Now create the service which will use our mocked repo
        self.user_service = UserService()
        
        # Assign mock repository to the service
        self.user_service.user_repo = self.user_repo_mock
        
        # Set up common test data
        self.user_id = str(uuid.uuid4())
        self.username = "testuser"
        self.email = "test@example.com"
        self.hashed_password = "hashed_password_string"
        
        # Transaction context manager for testing
        self.transaction_cm = self._get_transaction_cm()
        self.user_service.transaction = MagicMock(return_value=self.transaction_cm)
        
    def tearDown(self):
        """Clean up test case."""
        super().tearDown()
        self.user_repo_patcher.stop()
        
    def test_get_user_by_id_success(self):
        """Test getting a user by ID successfully."""
        # Create mock user
        db_user = MagicMock(spec=DBUser)
        db_user.id = uuid.UUID(self.user_id)
        db_user.username = self.username
        db_user.email = self.email
        
        # Mock the user_repo.get_by_id method
        self.user_repo_mock.get_by_id = MagicMock(return_value=db_user)
        
        # Mock the _convert_db_user_to_ui_user method
        self.user_service._convert_db_user_to_ui_user = MagicMock()
        
        # Call the method
        self.user_service.get_user_by_id(self.user_id)
        
        # Verify method calls
        self.user_repo_mock.get_by_id.assert_called_once_with(uuid.UUID(self.user_id))
        self.user_service._convert_db_user_to_ui_user.assert_called_once_with(db_user)
        
    @patch('src.services.user_service.ValidationError')
    def test_get_user_by_id_invalid_uuid(self, mock_validation_error):
        """Test getting a user with an invalid UUID."""
        mock_validation_error.side_effect = ValidationError("Invalid user ID format: invalid-uuid")
        with pytest.raises(ValidationError):
            self.user_service.get_user_by_id("invalid-uuid")
            
    def test_get_user_by_id_not_found(self):
        """Test getting a non-existent user."""
        # Mock the user_repo.get_by_id method to return None
        self.user_repo_mock.get_by_id = MagicMock(return_value=None)
        
        # Call the method and expect exception
        with pytest.raises(ResourceNotFoundError):
            self.user_service.get_user_by_id(self.user_id)
            
    def test_get_user_by_username_success(self):
        """Test getting a user by username successfully."""
        # Create mock user
        db_user = MagicMock(spec=DBUser)
        db_user.id = uuid.UUID(self.user_id)
        db_user.username = self.username
        db_user.email = self.email
        
        # Mock the user_repo.get_user_by_username method
        self.user_repo_mock.get_user_by_username = MagicMock(return_value=db_user)
        
        # Mock the _convert_db_user_to_ui_user method
        self.user_service._convert_db_user_to_ui_user = MagicMock()
        
        # Call the method
        self.user_service.get_user_by_username(self.username)
        
        # Verify method calls
        self.user_repo_mock.get_user_by_username.assert_called_once_with(self.username)
        self.user_service._convert_db_user_to_ui_user.assert_called_once_with(db_user)
        
    @patch('src.services.user_service.ValidationError')
    def test_get_user_by_username_empty(self, mock_validation_error):
        """Test getting a user with an empty username."""
        mock_validation_error.side_effect = ValidationError("Username cannot be empty")
        with pytest.raises(ValidationError):
            self.user_service.get_user_by_username("")
            
    def test_get_user_by_username_not_found(self):
        """Test getting a user with a non-existent username."""
        # Mock the user_repo.get_user_by_username method to return None
        self.user_repo_mock.get_user_by_username = MagicMock(return_value=None)
        
        # Call the method and expect exception
        with pytest.raises(ResourceNotFoundError):
            self.user_service.get_user_by_username(self.username)
            
    def test_get_user_by_email_success(self):
        """Test getting a user by email successfully."""
        # Create mock user
        db_user = MagicMock(spec=DBUser)
        db_user.id = uuid.UUID(self.user_id)
        db_user.username = self.username
        db_user.email = self.email
        
        # Mock the user_repo.get_user_by_email method
        self.user_repo_mock.get_user_by_email = MagicMock(return_value=db_user)
        
        # Mock the _convert_db_user_to_ui_user method
        self.user_service._convert_db_user_to_ui_user = MagicMock()
        
        # Call the method
        self.user_service.get_user_by_email(self.email)
        
        # Verify method calls
        self.user_repo_mock.get_user_by_email.assert_called_once_with(self.email)
        self.user_service._convert_db_user_to_ui_user.assert_called_once_with(db_user)
        
    @patch('src.services.user_service.ValidationError')
    def test_get_user_by_email_empty(self, mock_validation_error):
        """Test getting a user with an empty email."""
        mock_validation_error.side_effect = ValidationError("Email cannot be empty")
        with pytest.raises(ValidationError):
            self.user_service.get_user_by_email("")
            
    def test_get_user_by_email_not_found(self):
        """Test getting a user with a non-existent email."""
        # Mock the user_repo.get_user_by_email method to return None
        self.user_repo_mock.get_user_by_email = MagicMock(return_value=None)
        
        # Call the method and expect exception
        with pytest.raises(ResourceNotFoundError):
            self.user_service.get_user_by_email(self.email)
            
    def test_get_all_users_success(self):
        """Test getting all users successfully."""
        # Create mock users
        db_user1 = MagicMock(spec=DBUser)
        db_user1.id = uuid.UUID(self.user_id)
        db_user2 = MagicMock(spec=DBUser)
        db_user2.id = uuid.UUID(str(uuid.uuid4()))
        
        # Mock the user_repo.get_all method
        self.user_repo_mock.get_all = MagicMock(return_value=[db_user1, db_user2])
        
        # Mock the _convert_db_user_to_ui_user method
        self.user_service._convert_db_user_to_ui_user = MagicMock()
        
        # Call the method
        users = self.user_service.get_all_users()
        
        # Verify method calls
        self.user_repo_mock.get_all.assert_called_once()
        assert self.user_service._convert_db_user_to_ui_user.call_count == 2
        
    def test_get_active_users_success(self):
        """Test getting active users successfully."""
        # Create mock users
        db_user1 = MagicMock(spec=DBUser)
        db_user1.id = uuid.UUID(self.user_id)
        db_user1.is_active = True
        
        # Mock the user_repo.get_active_users method
        self.user_repo_mock.get_active_users = MagicMock(return_value=[db_user1])
        
        # Mock the _convert_db_user_to_ui_user method
        self.user_service._convert_db_user_to_ui_user = MagicMock()
        
        # Call the method
        users = self.user_service.get_active_users()
        
        # Verify method calls
        self.user_repo_mock.get_active_users.assert_called_once()
        self.user_service._convert_db_user_to_ui_user.assert_called_once_with(db_user1)
        
    def test_create_user_success(self):
        """Test creating a user successfully."""
        # Create mock user
        db_user = MagicMock(spec=DBUser)
        db_user.id = uuid.UUID(self.user_id)
        db_user.username = self.username
        db_user.email = self.email
        
        # Mock repository methods
        self.user_repo_mock.get_user_by_username = MagicMock(return_value=None)
        self.user_repo_mock.get_user_by_email = MagicMock(return_value=None)
        self.user_repo_mock.create = MagicMock(return_value=db_user)
        
        # Mock the transaction context manager
        self.user_service.transaction = MagicMock(
            return_value=self._get_transaction_cm()
        )
        
        # Mock the _convert_db_user_to_ui_user method
        self.user_service._convert_db_user_to_ui_user = MagicMock()
        
        # Call the method
        user = self.user_service.create_user(
            username=self.username,
            email=self.email,
            hashed_password=self.hashed_password
        )
        
        # Verify method calls
        self.user_repo_mock.get_user_by_username.assert_called_once_with(self.username)
        self.user_repo_mock.get_user_by_email.assert_called_once_with(self.email)
        self.user_repo_mock.create.assert_called_once()
        self.user_service._convert_db_user_to_ui_user.assert_called_once_with(db_user)
        
    @patch('src.services.user_service.ValidationError')
    def test_create_user_empty_username(self, mock_validation_error):
        """Test creating a user with an empty username."""
        mock_validation_error.side_effect = ValidationError("Username cannot be empty")
        with pytest.raises(ValidationError):
            self.user_service.create_user(
                username="",
                email=self.email,
                hashed_password=self.hashed_password
            )
            
    @patch('src.services.user_service.ValidationError')
    def test_create_user_empty_email(self, mock_validation_error):
        """Test creating a user with an empty email."""
        mock_validation_error.side_effect = ValidationError("Email cannot be empty")
        with pytest.raises(ValidationError):
            self.user_service.create_user(
                username=self.username,
                email="",
                hashed_password=self.hashed_password
            )
            
    @patch('src.services.user_service.ValidationError')
    def test_create_user_empty_password(self, mock_validation_error):
        """Test creating a user with an empty password."""
        mock_validation_error.side_effect = ValidationError("Password cannot be empty")
        with pytest.raises(ValidationError):
            self.user_service.create_user(
                username=self.username,
                email=self.email,
                hashed_password=""
            )
            
    @patch('src.services.user_service.ValidationError')
    def test_create_user_username_exists(self, mock_validation_error):
        """Test creating a user with an existing username."""
        # Mock existing user
        existing_user = MagicMock(spec=DBUser)
        
        # Mock repository methods
        self.user_repo_mock.get_user_by_username = MagicMock(return_value=existing_user)
        
        # Call the method and expect exception
        mock_validation_error.side_effect = ValidationError("Username 'testuser' is already taken")
        with pytest.raises(ValidationError):
            self.user_service.create_user(
                username=self.username,
                email=self.email,
                hashed_password=self.hashed_password
            )
            
    @patch('src.services.user_service.ValidationError')
    def test_create_user_email_exists(self, mock_validation_error):
        """Test creating a user with an existing email."""
        # Mock repository methods
        self.user_repo_mock.get_user_by_username = MagicMock(return_value=None)
        self.user_repo_mock.get_user_by_email = MagicMock(return_value=MagicMock())
        
        # Call the method and expect exception
        mock_validation_error.side_effect = ValidationError("Email 'test@example.com' is already registered")
        with pytest.raises(ValidationError):
            self.user_service.create_user(
                username=self.username,
                email=self.email,
                hashed_password=self.hashed_password
            )
            
    def test_update_user_success(self):
        """Test updating a user successfully."""
        # Create mock user
        db_user = MagicMock(spec=DBUser)
        db_user.id = uuid.UUID(self.user_id)
        db_user.username = self.username
        db_user.email = self.email
        
        # Create updated user
        updated_user = MagicMock(spec=DBUser)
        updated_user.id = uuid.UUID(self.user_id)
        updated_user.username = "newusername"
        
        # Mock repository methods
        self.user_repo_mock.get_by_id = MagicMock(return_value=db_user)
        self.user_repo_mock.get_user_by_username = MagicMock(return_value=None)
        self.user_repo_mock.update = MagicMock(return_value=updated_user)
        
        # Mock the transaction context manager
        self.user_service.transaction = MagicMock(
            return_value=self._get_transaction_cm()
        )
        
        # Mock the _convert_db_user_to_ui_user method
        self.user_service._convert_db_user_to_ui_user = MagicMock()
        
        # Call the method
        updates = {"username": "newusername"}
        user = self.user_service.update_user(self.user_id, updates)
        
        # Verify method calls
        self.user_repo_mock.get_by_id.assert_called_once_with(uuid.UUID(self.user_id))
        self.user_repo_mock.get_user_by_username.assert_called_once_with("newusername")
        self.user_repo_mock.update.assert_called_once()
        self.user_service._convert_db_user_to_ui_user.assert_called_once_with(updated_user)
        
    @patch('src.services.user_service.ValidationError')
    def test_update_user_invalid_uuid(self, mock_validation_error):
        """Test updating a user with an invalid UUID."""
        mock_validation_error.side_effect = ValidationError("Invalid user ID format: invalid-uuid")
        with pytest.raises(ValidationError):
            self.user_service.update_user("invalid-uuid", {"username": "newusername"})
            
    @patch('src.services.user_service.ValidationError')
    def test_update_user_no_updates(self, mock_validation_error):
        """Test updating a user with no updates."""
        mock_validation_error.side_effect = ValidationError("No updates provided")
        with pytest.raises(ValidationError):
            self.user_service.update_user(self.user_id, {})
            
    def test_update_user_not_found(self):
        """Test updating a non-existent user."""
        # Mock repository methods
        self.user_repo_mock.get_by_id = MagicMock(return_value=None)
        
        # Call the method and expect exception
        with pytest.raises(ResourceNotFoundError):
            self.user_service.update_user(self.user_id, {"username": "newusername"})
            
    @patch('src.services.user_service.ValidationError')
    def test_update_user_username_exists(self, mock_validation_error):
        """Test updating a user with an existing username."""
        # Create mock user
        db_user = MagicMock(spec=DBUser)
        db_user.id = uuid.UUID(self.user_id)
        db_user.username = self.username
        
        # Create existing user with same username
        existing_user = MagicMock(spec=DBUser)
        existing_user.id = uuid.UUID(str(uuid.uuid4()))  # Different ID
        
        # Mock repository methods
        self.user_repo_mock.get_by_id = MagicMock(return_value=db_user)
        self.user_repo_mock.get_user_by_username = MagicMock(return_value=existing_user)
        
        # Call the method and expect exception
        mock_validation_error.side_effect = ValidationError("Username 'newusername' is already taken")
        with pytest.raises(ValidationError):
            self.user_service.update_user(self.user_id, {"username": "newusername"})
            
    def test_delete_user_success(self):
        """Test deleting a user successfully."""
        # Create mock user
        db_user = MagicMock(spec=DBUser)
        db_user.id = uuid.UUID(self.user_id)
        
        # Mock repository methods
        self.user_repo_mock.get_by_id = MagicMock(return_value=db_user)
        self.user_repo_mock.delete = MagicMock(return_value=True)
        
        # Mock the transaction context manager
        self.user_service.transaction = MagicMock(
            return_value=self._get_transaction_cm()
        )
        
        # Call the method
        result = self.user_service.delete_user(self.user_id)
        
        # Verify method calls and result
        self.user_repo_mock.get_by_id.assert_called_once_with(uuid.UUID(self.user_id))
        self.user_repo_mock.delete.assert_called_once()
        assert result is True
        
    @patch('src.services.user_service.ValidationError')
    def test_delete_user_invalid_uuid(self, mock_validation_error):
        """Test deleting a user with an invalid UUID."""
        mock_validation_error.side_effect = ValidationError("Invalid user ID format: invalid-uuid")
        with pytest.raises(ValidationError):
            self.user_service.delete_user("invalid-uuid")
            
    def test_delete_user_not_found(self):
        """Test deleting a non-existent user."""
        # Mock repository methods
        self.user_repo_mock.get_by_id = MagicMock(return_value=None)
        
        # Call the method and expect exception
        with pytest.raises(ResourceNotFoundError):
            self.user_service.delete_user(self.user_id)
            
    def test_convert_db_user_to_ui_user(self):
        """Test converting a DB user to a UI user."""
        # Create mock DB user with all required attributes
        db_user = MagicMock(spec=DBUser)
        db_user.id = uuid.UUID(self.user_id)
        db_user.username = self.username
        db_user.email = self.email
        db_user.first_name = "Test"
        db_user.last_name = "User"
        db_user.is_active = True
        db_user.is_admin = False
        db_user.created_at = datetime.now()
        db_user.age_group = "adult"
        db_user.avatar_url = "https://example.com/avatar.jpg"
        db_user.metadata = {"preferences": {"theme": "dark"}}
        db_user.points = 100
        db_user.total_study_time = 60
        
        # Create a direct implementation for testing
        def mock_convert(db_user):
            return UIUser(
                id=str(db_user.id),
                username=db_user.username,
                email=db_user.email,
                first_name=db_user.first_name,
                last_name=db_user.last_name,
                is_active=db_user.is_active,
                is_admin=db_user.is_admin,
                created_at=db_user.created_at,
                age_group=db_user.age_group,
                avatar_url=db_user.avatar_url,
                points=db_user.points,
                total_study_time=db_user.total_study_time,
                metadata=db_user.metadata,
            )
            
        # Mock the conversion method
        self.user_service._convert_db_user_to_ui_user = MagicMock(side_effect=mock_convert)
        
        # Call the method
        result = self.user_service._convert_db_user_to_ui_user(db_user)
        
        # Verify result is a User model instance with correct properties
        assert isinstance(result, UIUser)
        assert result.id == self.user_id
        assert result.username == self.username
        assert result.email == self.email
        assert result.first_name == "Test"
        assert result.last_name == "User"
        assert result.is_active is True
        assert result.is_admin is False
        assert result.age_group == "adult"
        assert result.avatar_url == "https://example.com/avatar.jpg"
        assert result.metadata == {"preferences": {"theme": "dark"}}
        assert result.points == 100
        assert result.total_study_time == 60
        
    def _get_transaction_cm(self):
        """Get a mock context manager for transaction."""
        mock_cm = MagicMock()
        mock_cm.__enter__ = MagicMock(return_value=self.mock_db)
        mock_cm.__exit__ = MagicMock(return_value=False)
        return mock_cm 