
from rest_framework.test import APIClient
from django.test import TestCase
from account.models.user import User
from account.models.role import Role

class TestRoleViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin_user = User.objects.create_superuser(
            mobile="9111111111",
            password="admin123",
            first_name="Admin",
            last_name="User",
            email="admin@example.com"
        )
        self.client.force_authenticate(user=self.admin_user)

        self.role = Role.objects.create(name="Test Role")

    def test_permission_list(self):
        response = self.client.get(f'/api/v1/role/{self.role.id}/permission/')
        self.assertEqual(response.status_code, 200)

    def test_permission_update(self):
        data = {
            "name": "CP3"
        }
        response = self.client.patch(f'/api/v1/role/{self.role.id}/permission/', data, format='json')
        self.assertEqual(response.status_code, 200)
