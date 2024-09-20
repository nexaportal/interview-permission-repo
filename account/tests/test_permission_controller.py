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
        self.user1 = self.User.objects.create_user(username="user1", password="pass", mobile="1111111111")
        self.user2 = self.User.objects.create_user(username="user2", password="pass", mobile="2222222222")

        # Create a language instance
        self.language_en = Language.objects.create(code="en", name="English")

        # Create a Post instance
        self.post = Post.objects.create()

        # Create a PostItem authored by user1
        self.post_item = PostItem.objects.create(
            post=self.post, author=self.user1, lang=self.language_en, title="Test Post", content="This is a test post."
        )

    def test_user_is_owner(self):
        self.assertTrue(check_user_is_owner(self.user1, self.post_item))

    def test_user_is_not_owner(self):
        self.assertFalse(check_user_is_owner(self.user2, self.post_item))


class CheckUserPermissionForObjectTestCase(TestCase):
    def setUp(self):
        # Create users with unique mobile numbers
        self.User = get_user_model()
        self.user1 = self.User.objects.create_user(username="user1", password="pass", mobile="1111111111")
        self.user2 = self.User.objects.create_user(username="user2", password="pass", mobile="2222222222")

        # Create Languages
        self.language_en = Language.objects.create(code="en", name="English")
        self.language_fr = Language.objects.create(code="fr", name="French")

        # Create ContentType for PostItem
        self.content_type_postitem = ContentType.objects.get_for_model(PostItem)

        # Create Roles
        self.role_editor = Role.objects.create(name="Editor")
        self.role_viewer = Role.objects.create(name="Viewer")
        self.role_other = Role.objects.create(name="OtherRole")

        # Create Permissions
        self.perm_update_en = Perm.objects.create(
            name="Update English Posts",
            codename="update_en_posts",
            perm_model=self.content_type_postitem,
            action=PermissionActionChoices.UPDATE,
            lang=self.language_en,
        )

        self.perm_retrieve_en = Perm.objects.create(
            name="Retrieve English Posts",
            codename="retrieve_en_posts",
            perm_model=self.content_type_postitem,
            action=PermissionActionChoices.RETRIEVE,
            lang=self.language_en,
        )

        self.perm_delete_en = Perm.objects.create(
            name="Delete English Posts",
            codename="delete_en_posts",
            perm_model=self.content_type_postitem,
            action=PermissionActionChoices.DELETE,
            lang=self.language_en,
        )

        # Permissions not related to the PostItem model or English language
        self.perm_unrelated = Perm.objects.create(
            name="Unrelated Permission",
            codename="unrelated_perm",
            perm_model=self.content_type_postitem,  # Or another ContentType
            action=PermissionActionChoices.CREATE,
            lang=self.language_fr,  # Different language
        )

        # Create RolePerms
        self.role_perm_editor_update = RolePerm.objects.create(role=self.role_editor, perm=self.perm_update_en)
        self.role_perm_editor_delete = RolePerm.objects.create(role=self.role_editor, perm=self.perm_delete_en)
        self.role_perm_viewer_retrieve = RolePerm.objects.create(role=self.role_viewer, perm=self.perm_retrieve_en)

        # Assign RolePerms to Users via User's ManyToManyField role_perms
        self.user1.role_perms.add(self.role_perm_editor_update, self.role_perm_editor_delete)
        self.user2.role_perms.add(self.role_perm_viewer_retrieve)

        # Assign unrelated permissions to user2
        self.role_perm_other_unrelated = RolePerm.objects.create(role=self.role_other, perm=self.perm_unrelated)
        self.user2.role_perms.add(self.role_perm_other_unrelated)

        # Create Post instances
        self.post_en = Post.objects.create()
        self.post_fr = Post.objects.create()

        # Create PostItem objects authored by user1
        self.post_item = PostItem.objects.create(
            post=self.post_en,
            author=self.user1,
            lang=self.language_en,
            title="Test Post",
            content="This is a test post in English.",
        )

        # Create a PostItem in French
        self.post_item_fr = PostItem.objects.create(
            post=self.post_fr,
            author=self.user1,
            lang=self.language_fr,
            title="French Test Post",
            content="Ceci est un post de test en français.",
        )

    def test_user_has_permission_and_is_owner(self):
        mapped_action = "update"
        action = "update"
        result = check_user_permission_for_object(self.user1, self.post_item, mapped_action, action)
        self.assertTrue(result)

    def test_user_has_permission_but_not_owner(self):
        mapped_action = "retrieve"
        action = "retrieve"
        result = check_user_permission_for_object(self.user2, self.post_item, mapped_action, action)
        self.assertTrue(result)

    def test_user_lacks_permission(self):
        mapped_action = "delete"
        action = "destroy"
        result = check_user_permission_for_object(self.user2, self.post_item, mapped_action, action)
        self.assertFalse(result)

    def test_user_not_owner_cannot_update(self):
        # User2 does not have update permission and is not the owner
        mapped_action = "update"
        action = "update"
        result = check_user_permission_for_object(self.user2, self.post_item, mapped_action, action)
        self.assertFalse(result)

    def test_user_has_permission_but_not_owner_update(self):
        # Give user2 update permission
        self.perm_update_en_user2 = Perm.objects.create(
            name="Update English Posts User2",
            codename="update_en_posts_user2",
            perm_model=self.content_type_postitem,
            action=PermissionActionChoices.UPDATE,
            lang=self.language_en,
        )
        self.role_perm_viewer_update = RolePerm.objects.create(role=self.role_viewer, perm=self.perm_update_en_user2)
        self.user2.role_perms.add(self.role_perm_viewer_update)

        mapped_action = "update"
        action = "update"
        result = check_user_permission_for_object(self.user2, self.post_item, mapped_action, action)
        self.assertFalse(result)  # Should be False because user2 is not the owner

    def test_user_is_owner_but_lacks_permission(self):
        # Remove update permission from user1
        self.user1.role_perms.remove(self.role_perm_editor_update)

        mapped_action = "update"
        action = "update"
        result = check_user_permission_for_object(self.user1, self.post_item, mapped_action, action)
        self.assertFalse(result)  # Should be False because user1 lacks permission

    def test_user_has_permission_and_is_owner_delete(self):
        mapped_action = "delete"
        action = "destroy"
        result = check_user_permission_for_object(self.user1, self.post_item, mapped_action, action)
        self.assertTrue(result)

    def test_user_has_permission_but_not_owner_delete(self):
        # Give user2 delete permission
        self.perm_delete_en_user2 = Perm.objects.create(
            name="Delete English Posts User2",
            codename="delete_en_posts_user2",
            perm_model=self.content_type_postitem,
            action=PermissionActionChoices.DELETE,
            lang=self.language_en,
        )
        self.role_perm_viewer_delete = RolePerm.objects.create(role=self.role_viewer, perm=self.perm_delete_en_user2)
        self.user2.role_perms.add(self.role_perm_viewer_delete)

        mapped_action = "delete"
        action = "destroy"
        result = check_user_permission_for_object(self.user2, self.post_item, mapped_action, action)
        self.assertFalse(result)  # Should be False because user2 is not the owner

    def test_user_has_permission_and_is_owner_different_language(self):
        # Give user1 update permission for French
        self.perm_update_fr = Perm.objects.create(
            name="Update French Posts",
            codename="update_fr_posts",
            perm_model=self.content_type_postitem,
            action=PermissionActionChoices.UPDATE,
            lang=self.language_fr,
        )
        self.role_perm_editor_update_fr = RolePerm.objects.create(role=self.role_editor, perm=self.perm_update_fr)
        self.user1.role_perms.add(self.role_perm_editor_update_fr)

        mapped_action = "update"
        action = "update"
        result = check_user_permission_for_object(self.user1, self.post_item_fr, mapped_action, action)
        self.assertTrue(result)

    def test_user_has_permission_but_different_language(self):
        mapped_action = "update"
        action = "update"
        # User1 lacks update permission for French language
        result = check_user_permission_for_object(self.user1, self.post_item_fr, mapped_action, action)
        self.assertFalse(result)

    def test_user_with_multiple_roleperms_but_missing_needed_permission(self):
        """
        User has multiple role_perms, but not the one needed for the object and action.
        """
        mapped_action = "update"
        action = "update"

        # user2 has retrieve permission and an unrelated permission, but lacks update permission
        result = check_user_permission_for_object(self.user2, self.post_item, mapped_action, action)
        self.assertFalse(result)  # Should be False because user2 lacks update permission

    def test_permission_assigned_then_removed(self):
        """
        A permission is assigned to the user, and permission is checked correctly.
        Then the permission is removed from the user, and again the permission is checked correctly.
        """
        mapped_action = "update"
        action = "update"

        # Initially, user2 cannot update any post_item
        result_before = check_user_permission_for_object(self.user2, self.post_item, mapped_action, action)
        self.assertFalse(result_before)

        # Assign update permission to user2
        perm_update_en_user2 = Perm.objects.create(
            name="Update English Posts for User2",
            codename="update_en_posts_user2",
            perm_model=self.content_type_postitem,
            action=PermissionActionChoices.UPDATE,
            lang=self.language_en,
        )
        role_perm_update_user2 = RolePerm.objects.create(role=self.role_viewer, perm=perm_update_en_user2)
        self.user2.role_perms.add(role_perm_update_user2)

        # Create a new Post for user2
        post_user2 = Post.objects.create()

        # Create a PostItem authored by user2 with a unique post and lang combination
        post_item_user2 = PostItem.objects.create(
            post=post_user2,
            author=self.user2,
            lang=self.language_en,
            title="User2 Test Post",
            content="This is a test post by user2.",
        )

        # Now user2 should be able to update their own post
        result_after_assignment = check_user_permission_for_object(self.user2, post_item_user2, mapped_action, action)
        self.assertTrue(result_after_assignment)

        # Remove the update permission from user2
        self.user2.role_perms.remove(role_perm_update_user2)

        # Now user2 should not be able to update their own post
        result_after_removal = check_user_permission_for_object(self.user2, post_item_user2, mapped_action, action)
        self.assertFalse(result_after_removal)

    def test_object_language_changed_user_loses_permission(self):
        """
        Test that if an object's language is changed to one the user lacks permission for,
        the user can no longer perform the action.
        """
        # User1 has update permission for English
        mapped_action = "update"
        action = "update"

        # Ensure user1 can update the post_item initially
        can_update_before = check_user_permission_for_object(self.user1, self.post_item, mapped_action, action)
        self.assertTrue(can_update_before)

        # Change the language of post_item to French (user1 lacks update permission for French)
        self.post_item.lang = self.language_fr
        self.post_item.save()

        # Now, user1 should not be able to update the post_item
        can_update_after = check_user_permission_for_object(self.user1, self.post_item, mapped_action, action)
        self.assertFalse(can_update_after)

    def test_object_author_changed_user_loses_ownership(self):
        """
        Test that if an object's author is changed, the original author can no longer perform actions requiring ownership.
        """
        mapped_action = "update"
        action = "update"

        # Ensure user1 can update the post_item initially
        can_update_before = check_user_permission_for_object(self.user1, self.post_item, mapped_action, action)
        self.assertTrue(can_update_before)

        # Change the author of post_item to user2
        self.post_item.author = self.user2
        self.post_item.save()

        # Now, user1 should not be able to update the post_item
        can_update_after = check_user_permission_for_object(self.user1, self.post_item, mapped_action, action)
        self.assertFalse(can_update_after)

    def test_permission_deleted_user_loses_access(self):
        """
        Test that if a permission is deleted, the user can no longer perform the associated action.
        """
        mapped_action = "update"
        action = "update"

        # Ensure user1 can update the post_item initially
        can_update_before = check_user_permission_for_object(self.user1, self.post_item, mapped_action, action)
        self.assertTrue(can_update_before)

        # Delete the 'update' permission
        self.perm_update_en.delete()

        # Now, user1 should not be able to update the post_item
        can_update_after = check_user_permission_for_object(self.user1, self.post_item, mapped_action, action)
        self.assertFalse(can_update_after)

    def test_permission_action_modified_user_access_updated(self):
        """
        Test that if a permission's action is modified, the user's access is updated accordingly.
        """
        # Initially, user1 has 'update' permission
        mapped_action_update = "update"
        action_update = "update"

        # Ensure user1 can update the post_item
        can_update_before = check_user_permission_for_object(
            self.user1, self.post_item, mapped_action_update, action_update
        )
        self.assertTrue(can_update_before)

        # Change the permission's action from 'update' to 'delete'
        self.perm_update_en.action = PermissionActionChoices.DELETE
        self.perm_update_en.save()

        # Now, user1 should not be able to update the post_item
        can_update_after = check_user_permission_for_object(
            self.user1, self.post_item, mapped_action_update, action_update
        )
        self.assertFalse(can_update_after)

        # But user1 should be able to delete the post_item
        mapped_action_delete = "delete"
        action_delete = "destroy"
        can_delete = check_user_permission_for_object(self.user1, self.post_item, mapped_action_delete, action_delete)
        self.assertTrue(can_delete)

    def test_role_deleted_user_loses_permissions(self):
        """
        Test that if a role is deleted, the user loses the permissions associated with that role.
        """
        mapped_action = "update"
        action = "update"

        # Ensure user1 can update the post_item initially
        can_update_before = check_user_permission_for_object(self.user1, self.post_item, mapped_action, action)
        self.assertTrue(can_update_before)

        # Delete the role 'Editor' (which user1 has)
        self.role_editor.delete()

        # Now, user1 should not be able to update the post_item
        can_update_after = check_user_permission_for_object(self.user1, self.post_item, mapped_action, action)
        self.assertFalse(can_update_after)

    def test_concurrent_modification_of_permissions(self):
        """
        Simulate concurrent modification where a user's permission is changed during a permission check.
        """
        mapped_action = "update"
        action = "update"

        # Ensure user1 can update the post_item initially
        can_update_before = check_user_permission_for_object(self.user1, self.post_item, mapped_action, action)
        self.assertTrue(can_update_before)

        # Simulate another process removing user1's permission
        self.user1.role_perms.remove(self.role_perm_editor_update)

        # Now, user1 should not be able to update the post_item
        can_update_after = check_user_permission_for_object(self.user1, self.post_item, mapped_action, action)
        self.assertFalse(can_update_after)

    def test_permission_check_performance_with_many_permissions(self):
        """
        Test the performance of the permission check when the user has many permissions.
        """
        mapped_action = "update"
        action = "update"

        # Add a large number of irrelevant permissions to user1
        for i in range(1000):
            perm = Perm.objects.create(
                name=f"Irrelevant Permission {i}",
                codename=f"irrelevant_perm_{i}",
                perm_model=self.content_type_postitem,
                action=PermissionActionChoices.CREATE,
                lang=self.language_en,
            )
            role_perm = RolePerm.objects.create(role=self.role_editor, perm=perm)
            self.user1.role_perms.add(role_perm)

        # Ensure that the permission check still functions correctly
        can_update = check_user_permission_for_object(self.user1, self.post_item, mapped_action, action)
        self.assertTrue(can_update)

    def test_permission_checks_with_caching(self):
        """
        Test that caching mechanisms do not interfere with permission checks.
        """
        from django.core.cache import cache

        mapped_action = "update"
        action = "update"

        # Cache the user's permissions
        cache_key = f"user_permissions_{self.user1.id}"
        cache.set(cache_key, list(self.user1.role_perms.all()), timeout=60)

        # Ensure user1 can update the post_item initially
        can_update_before = check_user_permission_for_object(self.user1, self.post_item, mapped_action, action)
        self.assertTrue(can_update_before)

        # Remove the update permission from user1
        self.user1.role_perms.remove(self.role_perm_editor_update)
        # Update the cache to simulate stale data
        cache.set(cache_key, list(self.user1.role_perms.all()), timeout=60)

        # Ensure that the permission check does not use stale cache data
        can_update_after = check_user_permission_for_object(self.user1, self.post_item, mapped_action, action)
        self.assertFalse(can_update_after)
