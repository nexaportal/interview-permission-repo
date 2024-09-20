from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from account.models import Role, Perm, RolePerm
from account.models.perm import PermissionActionChoices  
from content.models import Post, PostItem, Language
from account.permissions import check_user_is_owner, check_user_permission_for_object

class CheckUserIsOwnerTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user1 = self.User.objects.create_user(
            username='user1',
            password='pass',
            mobile='1111111111'  # Assign a unique mobile number
        )
        self.user2 = self.User.objects.create_user(
            username='user2',
            password='pass',
            mobile='2222222222'  # Assign a different unique mobile number
        )

        # Create a language instance
        self.language_en = Language.objects.create(code='en', name='English')

        # Create a Post instance
        self.post = Post.objects.create()

        # Create a PostItem authored by user1
        self.post_item = PostItem.objects.create(
            post=self.post,
            author=self.user1,
            lang=self.language_en,
            title='Test Post',
            content='This is a test post.'
        )

    def test_user_is_owner(self):
        self.assertTrue(check_user_is_owner(self.user1, self.post_item))

    def test_user_is_not_owner(self):
        self.assertFalse(check_user_is_owner(self.user2, self.post_item))

class CheckUserPermissionForObjectTestCase(TestCase):
    def setUp(self):
        # Create users with unique mobile numbers
        self.User = get_user_model()
        self.user1 = self.User.objects.create_user(
            username='user1',
            password='pass',
            mobile='1111111111'
        )
        self.user2 = self.User.objects.create_user(
            username='user2',
            password='pass',
            mobile='2222222222'
        )

        # Create Languages
        self.language_en = Language.objects.create(code='en', name='English')
        self.language_fr = Language.objects.create(code='fr', name='French')

        # Create ContentType for PostItem
        self.content_type_postitem = ContentType.objects.get_for_model(PostItem)

        # Create Roles
        self.role_editor = Role.objects.create(name='Editor')
        self.role_viewer = Role.objects.create(name='Viewer')

        # Create Permissions
        self.perm_update_en = Perm.objects.create(
            name='Update English Posts',
            codename='update_en_posts',
            perm_model=self.content_type_postitem,
            action=PermissionActionChoices.UPDATE,
            lang=self.language_en
        )

        self.perm_retrieve_en = Perm.objects.create(
            name='Retrieve English Posts',
            codename='retrieve_en_posts',
            perm_model=self.content_type_postitem,
            action=PermissionActionChoices.RETRIEVE,
            lang=self.language_en
        )

        self.perm_delete_en = Perm.objects.create(
            name='Delete English Posts',
            codename='delete_en_posts',
            perm_model=self.content_type_postitem,
            action=PermissionActionChoices.DELETE,
            lang=self.language_en
        )

        # Create RolePerms
        self.role_perm_editor_update = RolePerm.objects.create(role=self.role_editor, perm=self.perm_update_en)
        self.role_perm_editor_delete = RolePerm.objects.create(role=self.role_editor, perm=self.perm_delete_en)
        self.role_perm_viewer_retrieve = RolePerm.objects.create(role=self.role_viewer, perm=self.perm_retrieve_en)

        # Assign RolePerms to Users via User's ManyToManyField role_perms
        self.user1.role_perms.add(self.role_perm_editor_update, self.role_perm_editor_delete)
        self.user2.role_perms.add(self.role_perm_viewer_retrieve)

        # Create Post instances
        self.post_en = Post.objects.create()
        self.post_fr = Post.objects.create()

        # Create PostItem objects authored by user1
        self.post_item = PostItem.objects.create(
            post=self.post_en,
            author=self.user1,
            lang=self.language_en,
            title='Test Post',
            content='This is a test post in English.'
        )

        # Create a PostItem in French
        self.post_item_fr = PostItem.objects.create(
            post=self.post_fr,
            author=self.user1,
            lang=self.language_fr,
            title='French Test Post',
            content='Ceci est un post de test en français.'
        )

    def test_user_has_permission_and_is_owner(self):
        mapped_action = 'update'
        action = 'update'
        result = check_user_permission_for_object(self.user1, self.post_item, mapped_action, action)
        self.assertTrue(result)

    def test_user_has_permission_but_not_owner(self):
        mapped_action = 'retrieve'
        action = 'retrieve'
        result = check_user_permission_for_object(self.user2, self.post_item, mapped_action, action)
        self.assertTrue(result)

    def test_user_lacks_permission(self):
        mapped_action = 'delete'
        action = 'destroy'
        result = check_user_permission_for_object(self.user2, self.post_item, mapped_action, action)
        self.assertFalse(result)

    def test_user_not_owner_cannot_update(self):
        # User2 does not have update permission and is not the owner
        mapped_action = 'update'
        action = 'update'
        result = check_user_permission_for_object(self.user2, self.post_item, mapped_action, action)
        self.assertFalse(result)

    def test_user_has_permission_but_not_owner_update(self):
        # Give user2 update permission
        self.perm_update_en_user2 = Perm.objects.create(
            name='Update English Posts User2',
            codename='update_en_posts_user2',
            perm_model=self.content_type_postitem,
            action=PermissionActionChoices.UPDATE,
            lang=self.language_en
        )
        self.role_perm_viewer_update = RolePerm.objects.create(
            role=self.role_viewer,
            perm=self.perm_update_en_user2
        )
        self.user2.role_perms.add(self.role_perm_viewer_update)

        mapped_action = 'update'
        action = 'update'
        result = check_user_permission_for_object(self.user2, self.post_item, mapped_action, action)
        self.assertFalse(result)  # Should be False because user2 is not the owner

    def test_user_is_owner_but_lacks_permission(self):
        # Remove update permission from user1
        self.user1.role_perms.remove(self.role_perm_editor_update)

        mapped_action = 'update'
        action = 'update'
        result = check_user_permission_for_object(self.user1, self.post_item, mapped_action, action)
        self.assertFalse(result)  # Should be False because user1 lacks permission

    def test_user_has_permission_and_is_owner_delete(self):
        mapped_action = 'delete'
        action = 'destroy'
        result = check_user_permission_for_object(self.user1, self.post_item, mapped_action, action)
        self.assertTrue(result)

    def test_user_has_permission_but_not_owner_delete(self):
        # Give user2 delete permission
        self.perm_delete_en_user2 = Perm.objects.create(
            name='Delete English Posts User2',
            codename='delete_en_posts_user2',
            perm_model=self.content_type_postitem,
            action=PermissionActionChoices.DELETE,
            lang=self.language_en
        )
        self.role_perm_viewer_delete = RolePerm.objects.create(
            role=self.role_viewer,
            perm=self.perm_delete_en_user2
        )
        self.user2.role_perms.add(self.role_perm_viewer_delete)

        mapped_action = 'delete'
        action = 'destroy'
        result = check_user_permission_for_object(self.user2, self.post_item, mapped_action, action)
        self.assertFalse(result)  # Should be False because user2 is not the owner

    def test_user_has_permission_and_is_owner_different_language(self):
        # Give user1 update permission for French
        self.perm_update_fr = Perm.objects.create(
            name='Update French Posts',
            codename='update_fr_posts',
            perm_model=self.content_type_postitem,
            action=PermissionActionChoices.UPDATE,
            lang=self.language_fr
        )
        self.role_perm_editor_update_fr = RolePerm.objects.create(
            role=self.role_editor,
            perm=self.perm_update_fr
        )
        self.user1.role_perms.add(self.role_perm_editor_update_fr)

        mapped_action = 'update'
        action = 'update'
        result = check_user_permission_for_object(self.user1, self.post_item_fr, mapped_action, action)
        self.assertTrue(result)

    def test_user_has_permission_but_different_language(self):
        mapped_action = 'update'
        action = 'update'
        # User1 lacks update permission for French language
        result = check_user_permission_for_object(self.user1, self.post_item_fr, mapped_action, action)
        self.assertFalse(result)
