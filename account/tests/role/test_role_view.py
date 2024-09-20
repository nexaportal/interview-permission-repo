from rest_framework.test import APIClient
from django.test import TestCase
from account.models.user import User
from account.models.role import Role

class TestRoleViewSet(TestCase):
    def setUp(self):
        # Set up client and admin user for authentication
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            mobile="9111111111",
            password="admin123",
            first_name="Admin",
            last_name="User",
            email="admin@example.com"
        )
        self.client.force_authenticate(user=self.admin_user)

        # Create a role for testing
        self.role = Role.objects.create(name="Test Role")

    def test_permission_list(self):
        # Test the permission list GET request
        response = self.client.get(f'/api/v1/role/{self.role.id}/permission/')
        self.assertEqual(response.status_code, 200)

    def test_permission_update(self):
        # Test the permission PATCH request
        data = {
            "permissions": [
                {
                    "perm_id": 1,
                    "value": True
                }
            ]
        }
        response = self.client.patch(f'/api/v1/role/{self.role.id}/permission/', data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_role_create(self):
        # Test role creation
        data = {
            "name": "New Role"
        }
        response = self.client.post('/api/v1/role/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], "New Role")

    def test_role_retrieve(self):
        # Test retrieving a specific role
        response = self.client.get(f'/api/v1/role/{self.role.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Test Role")

    def test_role_update(self):
        # Test updating a role
        data = {
            "name": "Updated Role"
        }
        response = self.client.put(f'/api/v1/role/{self.role.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Updated Role")

    def test_role_partial_update(self):
        # Test partially updating a role
        data = {
            "name": "Partially Updated Role"
        }
        response = self.client.patch(f'/api/v1/role/{self.role.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Partially Updated Role")

    def test_role_delete(self):
        response = self.client.delete(f'/api/v1/role/{self.role.id}/')
        self.assertEqual(response.status_code, 204)
        # Check that the role no longer exists
        self.assertFalse(Role.objects.filter(id=self.role.id).exists())
