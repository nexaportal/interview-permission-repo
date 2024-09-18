from rest_framework.test import APITestCase
from rest_framework import status
from content.models.category import Category, CategoryItem
from content.models.lang import Language
from account.models import User
from account.models.role import Role
from account.models.perm import Perm
from account.models.role_perm import RolePerm
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from django.contrib.contenttypes.models import ContentType


class CategoryCreateTest(APITestCase):
    def setUp(self):
        # Create user, language, and token
        self.role = Role.objects.create(name='TestRole')
        self.user = User.objects.create_user(
            mobile="9111111111",
            password="admin123",
            first_name="Admin",
            last_name="User",
            email="admin@example.com"
        )
        self.category_content = ContentType.objects.filter(app_label='content', model='category').first()
        self.user.roles.set([self.role])
        self.language = Language.objects.create(name='English', code='en')
        self.create_perm = Perm.objects.create(
            name='CreatePerm',
            lang=self.language,
            perm_model=self.category_content,
            action='CREATE'
        )
        self.list_perm = Perm.objects.create(
            name='ListPerm',
            lang=self.language,
            perm_model=self.category_content,
            action='LIST',
            field='name'
        )
        self.create_role_perm = RolePerm.objects.create(
            role=self.role,
            perm=self.create_perm
        )
        self.list_role_perm = RolePerm.objects.create(
            role=self.role,
            perm=self.list_perm
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        # Initialize API client
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')


    '''
        Create A category That User Role Has permission To create a category in that language
    '''
    def test_create_category(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        url = '/api/v1/category/'
        data = {
            "items": {
                "en": {
                    "name": "Test Category"
                }
            }
        }
        response = self.client.post(url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category = Category.objects.get()
        category_item = CategoryItem.objects.get(category=category, lang=self.language)
        self.assertEqual(category_item.name, "Test Category")

    '''
        Create A category That User Role Doesn`t have permission To create a category in that language
    '''
    def test_create_category_without_permission(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        url = '/api/v1/category/'
        data = {
            "items": {
                "ru": {
                    "name": "Test Category Without Permission"
                }
            }
        }
        response = self.client.post(url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_get_category_without_fields(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        url = '/api/v1/category/'
        response = self.client.get(url, headers=headers)
        for category in response.json():
            assert 'name' not in category, f"'name' field found in category with id {category['id']}"
