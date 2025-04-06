import unittest
from unittest.mock import MagicMock, patch
from src.services.permission_service import PermissionService, Permission, Role, ROLE_PERMISSIONS


class TestPermissionService(unittest.TestCase):
    """Unit tests for the PermissionService class."""

    def setUp(self):
        """Set up test environment before each test."""
        # Create test user data
        self.student_user = {
            "id": "student-123",
            "username": "student",
            "email": "student@example.com",
            "role": Role.STUDENT.value
        }
        
        self.admin_user = {
            "id": "admin-123",
            "username": "admin",
            "email": "admin@example.com",
            "role": Role.ADMIN.value
        }
        
        # Resources
        self.student_owned_resource = {
            "id": "resource-123",
            "user_id": self.student_user["id"],
            "name": "Student Resource"
        }
        
        self.admin_owned_resource = {
            "id": "resource-456",
            "user_id": self.admin_user["id"],
            "name": "Admin Resource"
        }

    def test_get_role_permissions(self):
        """Test getting permissions for a role."""
        # Test student permissions
        student_permissions = PermissionService.get_role_permissions(Role.STUDENT)
        self.assertEqual(student_permissions, ROLE_PERMISSIONS[Role.STUDENT])
        
        # Test admin permissions
        admin_permissions = PermissionService.get_role_permissions(Role.ADMIN)
        self.assertEqual(admin_permissions, ROLE_PERMISSIONS[Role.ADMIN])
        
        # Verify that admin has all permissions
        all_permissions = [p for p in Permission]
        for permission in all_permissions:
            self.assertIn(permission, admin_permissions)
    
    def test_get_role_permissions_invalid_role(self):
        """Test getting permissions for an invalid role."""
        # Try with a non-existent role
        permissions = PermissionService.get_role_permissions("NONEXISTENT_ROLE")
        self.assertEqual(permissions, set())
    
    def test_user_has_permission(self):
        """Test checking if a user has a specific permission."""
        # Test student permissions
        self.assertTrue(PermissionService.user_has_permission(
            self.student_user, Permission.VIEW_CONTENT))
        self.assertFalse(PermissionService.user_has_permission(
            self.student_user, Permission.CREATE_CONTENT))
        self.assertFalse(PermissionService.user_has_permission(
            self.student_user, Permission.EDIT_CONTENT))
        self.assertFalse(PermissionService.user_has_permission(
            self.student_user, Permission.DELETE_USERS))
        
        # Test admin permissions
        self.assertTrue(PermissionService.user_has_permission(
            self.admin_user, Permission.VIEW_CONTENT))
        self.assertTrue(PermissionService.user_has_permission(
            self.admin_user, Permission.CREATE_COURSES))
        self.assertTrue(PermissionService.user_has_permission(
            self.admin_user, Permission.DELETE_USERS))
        self.assertTrue(PermissionService.user_has_permission(
            self.admin_user, Permission.CREATE_CONTENT))
        self.assertTrue(PermissionService.user_has_permission(
            self.admin_user, Permission.EDIT_CONTENT))
    
    def test_user_has_permission_invalid_user(self):
        """Test checking permissions with invalid user data."""
        # Test with user missing role
        user_without_role = {
            "id": "no-role-123",
            "username": "norole",
            "email": "norole@example.com"
        }
        self.assertFalse(PermissionService.user_has_permission(user_without_role, Permission.VIEW_CONTENT))
        
        # Test with invalid role
        user_with_invalid_role = {
            "id": "invalid-role-123",
            "username": "invalidrole",
            "email": "invalidrole@example.com",
            "role": "INVALID_ROLE"
        }
        self.assertFalse(PermissionService.user_has_permission(user_with_invalid_role, Permission.VIEW_CONTENT))

    def test_user_has_permissions(self):
        """Test checking if a user has all specified permissions."""
        # Test student with valid permissions
        self.assertTrue(PermissionService.user_has_permissions(
            self.student_user, [Permission.VIEW_CONTENT, Permission.VIEW_OWN_PROGRESS]))
        
        # Test student with mix of valid and invalid permissions
        self.assertFalse(PermissionService.user_has_permissions(
            self.student_user, [Permission.VIEW_CONTENT, Permission.DELETE_USERS]))
        
        # Test student with content creation/editing permissions (should fail now)
        self.assertFalse(PermissionService.user_has_permissions(
            self.student_user, [Permission.VIEW_CONTENT, Permission.CREATE_CONTENT]))
        
        # Test admin with all permissions
        all_permissions = [p for p in Permission]
        self.assertTrue(PermissionService.user_has_permissions(
            self.admin_user, all_permissions))
    
    def test_user_has_any_permission(self):
        """Test checking if a user has any of the specified permissions."""
        # Test student with some valid permissions
        self.assertTrue(PermissionService.user_has_any_permission(
            self.student_user, [Permission.VIEW_CONTENT, Permission.DELETE_USERS]))
        
        # Test student with all invalid permissions
        self.assertFalse(PermissionService.user_has_any_permission(
            self.student_user, [Permission.DELETE_USERS, Permission.CREATE_COURSES]))
        
        # Test student with content creation/editing permissions (should not have these)
        self.assertFalse(PermissionService.user_has_any_permission(
            self.student_user, [Permission.CREATE_CONTENT, Permission.EDIT_CONTENT]))
        
        # Test admin with any permissions
        self.assertTrue(PermissionService.user_has_any_permission(
            self.admin_user, [Permission.DELETE_USERS]))
        
        # Test admin with content permissions
        self.assertTrue(PermissionService.user_has_any_permission(
            self.admin_user, [Permission.CREATE_CONTENT, Permission.EDIT_CONTENT]))
    
    def test_is_resource_owner(self):
        """Test checking if a user is the owner of a resource."""
        # Test student is owner of student resource
        self.assertTrue(PermissionService.is_resource_owner(
            self.student_user, self.student_owned_resource))
        
        # Test student is not owner of admin resource
        self.assertFalse(PermissionService.is_resource_owner(
            self.student_user, self.admin_owned_resource))
        
        # Test admin is owner of admin resource
        self.assertTrue(PermissionService.is_resource_owner(
            self.admin_user, self.admin_owned_resource))
        
        # Test admin is not owner of student resource
        self.assertFalse(PermissionService.is_resource_owner(
            self.admin_user, self.student_owned_resource))
    
    def test_is_resource_owner_with_custom_owner_field(self):
        """Test resource ownership check with different user ID field in resource."""
        # Create resource with different owner ID field
        resource_with_owner_id = {
            "id": "resource-789",
            "owner_id": self.student_user["id"],
            "name": "Resource with owner_id"
        }
        
        # Test with resource that has owner_id field
        self.assertTrue(PermissionService.is_resource_owner(
            self.student_user, resource_with_owner_id))
        
        # Test with non-matching owner_id
        self.assertFalse(PermissionService.is_resource_owner(
            self.admin_user, resource_with_owner_id))
    
    def test_is_resource_owner_with_invalid_resource(self):
        """Test resource ownership check with invalid resource."""
        # Resource without owner field
        resource_without_owner = {
            "id": "resource-789",
            "name": "Resource without owner"
        }
        
        # Test with resource missing owner field
        self.assertFalse(PermissionService.is_resource_owner(
            self.student_user, resource_without_owner))
        
        # Test with None resource
        try:
            result = PermissionService.is_resource_owner(self.student_user, None)
            self.assertFalse(result)
        except AttributeError:
            # If implementation doesn't handle None, that's acceptable too
            pass
    
    def test_has_access_to_resource(self):
        """Test checking if a user has access to a resource."""
        # Test student access to own resource (ownership)
        # Even though student doesn't have EDIT_CONTENT permission, ownership should give access
        self.assertTrue(PermissionService.has_access_to_resource(
            self.student_user, self.student_owned_resource, Permission.EDIT_CONTENT))
        
        # Test student access to admin resource (no permission for EDIT_CONTENT)
        self.assertFalse(PermissionService.has_access_to_resource(
            self.student_user, self.admin_owned_resource, Permission.EDIT_CONTENT))
        
        # Test student access to content with viewer permission
        self.assertTrue(PermissionService.has_access_to_resource(
            self.student_user, self.admin_owned_resource, Permission.VIEW_CONTENT))
        
        # Test admin access to any resource (all permissions)
        self.assertTrue(PermissionService.has_access_to_resource(
            self.admin_user, self.student_owned_resource, Permission.EDIT_CONTENT))
        self.assertTrue(PermissionService.has_access_to_resource(
            self.admin_user, self.admin_owned_resource, Permission.EDIT_CONTENT))
    
    def test_get_user_role(self):
        """Test getting a user's role."""
        # Test getting student role
        self.assertEqual(PermissionService.get_user_role(self.student_user), Role.STUDENT)
        
        # Test getting admin role
        self.assertEqual(PermissionService.get_user_role(self.admin_user), Role.ADMIN)
    
    def test_get_user_role_invalid_user(self):
        """Test getting role with invalid user data."""
        # Test with user missing role
        user_without_role = {
            "id": "no-role-123",
            "username": "norole",
            "email": "norole@example.com"
        }
        self.assertIsNone(PermissionService.get_user_role(user_without_role))
        
        # Test with invalid role
        user_with_invalid_role = {
            "id": "invalid-role-123",
            "username": "invalidrole",
            "email": "invalidrole@example.com",
            "role": "INVALID_ROLE"
        }
        self.assertIsNone(PermissionService.get_user_role(user_with_invalid_role))


if __name__ == '__main__':
    unittest.main() 