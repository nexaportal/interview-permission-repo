from rest_framework.test import APITestCase
from rest_framework import status
from content.models.post import Post, PostItem
from content.models.lang import Language
from account.models import User
from account.models.role import Role
from account.models.perm import Perm, PermissionActionChoices
from account.models.role_perm import RolePerm
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from django.contrib.contenttypes.models import ContentType


class PostCreateTest(APITestCase):
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
        self.post_content = ContentType.objects.filter(app_label='content', model='post').first()
        self.user.roles.set([self.role])
        self.language = Language.objects.create(name='English', code='en')
        self.create_perm = Perm.objects.create(
            name='CreatePerm',
            lang=self.language,
            perm_model=self.post_content,
            action=PermissionActionChoices.CREATE
        )
        self.list_perm = Perm.objects.create(
            name='ListPerm',
            lang=self.language,
            perm_model=self.post_content,
            action=PermissionActionChoices.LIST,
            field='title'
        )
        self.update_field_perm = Perm.objects.create(
            name='UpdateFieldPerm',
            lang=self.language,
            perm_model=self.post_content,
            action=PermissionActionChoices.UPDATE,
            field='title'
        )
        self.create_role_perm = RolePerm.objects.create(
            role=self.role,
            perm=self.create_perm
        )
        self.list_role_perm = RolePerm.objects.create(
            role=self.role,
            perm=self.list_perm
        )
        self.update_role_perm = RolePerm.objects.create(
            role=self.role,
            perm=self.update_field_perm,
            value=False
        )
        self.post = Post.objects.create()

        # Create a PostItem for the language
        self.post_item = PostItem.objects.create(
            post=self.post,
            lang=self.language,
            title="Original Title",
            content="Original Content",
            author=self.user
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        # Initialize API client
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')


    '''
        Create A Post That User Role Has permission To create a post in that language
    '''
    def test_create_post(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        url = '/api/v1/post/'
        data = {
            "items": {
                "en": {
                    "title": "Test Post Title",
                    "content": "Test Post Content"
                }
            }
        }
        response = self.client.post(url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(id=response.json()['id'])
        post_item = PostItem.objects.get(post=post, lang=self.language)
        self.assertEqual(post_item.title, "Test Post Title")

    def test_update_title_post_forbidden(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        url = f'/api/v1/post/{self.post.id}/'
        data = {
            "items": {
                "en": {
                    "title": "Updated Post Title",
                    "content": "Updated Post Content"
                }
            }
        }
        response = self.client.patch(url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_content_post(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        url = f'/api/v1/post/{self.post.id}/'
        data = {
            "items": {
                "en": {
                    "content": "Updated Post Content"
                }
            }
        }
        response = self.client.patch(url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_post(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        url = f'/api/v1/post/{self.post.id}/'
        data = {
            "items": {
                "en": {
                    "title": "Updated Post Title",
                    "content": "Updated Post Content"
                }
            }
        }
        response = self.client.patch(url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    '''
        Create A post That User Role Doesn`t have permission To create a post in that language
    '''
    def test_create_post_without_permission(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        url = '/api/v1/post/'
        data = {
            "items": {
                "ru": {
                    "title": "Test Post Without Permission",
                    "content" : "Test Post Without Permission Content"
                }
            }
        }
        response = self.client.post(url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_get_post_without_fields(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        url = '/api/v1/post/'
        response = self.client.get(url, headers=headers)
        for post in response.json():
            assert 'title' not in post, f"'name' field found in post with id {post['id']}"
