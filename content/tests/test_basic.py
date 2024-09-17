from django.test import TestCase
from account.models import User


class UserCreationTestCase(TestCase):
    def test_create_user(self):
        # Create a user
        user = User.objects.create_user(username='testuser', password='testpass')

        # Check if the user was created
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass'))
