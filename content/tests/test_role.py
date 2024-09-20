# from django.test import TestCase
# from django.contrib.contenttypes.models import ContentType
# from account.models import User, Role, RolePerm, Perm
# from content.models import Language  # Assuming you have this model
# from content.models import PostItem  # Assuming you have this model

# class UserRolePermAssignmentTestCase(TestCase):
#     def setUp(self):
#         # Create a user
#         self.user = User.objects.create_user(username='testuser', password='testpass', mobile='9112223344')

#         # Create a role
#         self.role = Role.objects.create(name="Editor")

#         # Create a language
#         self.language = Language.objects.create(name="en")

#         # Get the content type for PostItem model (assuming this is a model you're using)
#         self.content_type = ContentType.objects.get_for_model(PostItem)

#         # Create a permission (Perm object)
#         self.permission = Perm.objects.create(
#             name="Can Create PostItem",
#             codename="create_postitem",
#             perm_model=self.content_type,
#             action="create",
#             lang=self.language
#         )

#         # Create a RolePerm object (assigning a role and permission)
#         self.role_perm = RolePerm.objects.create(role=self.role, perm=self.permission)

#         # Assign the RolePerm to the user
#         self.user.role_perms.add(self.role_perm)

#     def test_role_perm_assignment(self):
#         # Check if the user has the assigned RolePerm
#         self.assertEqual(self.user.role_perms.count(), 1)
#         self.assertEqual(self.user.role_perms.first(), self.role_perm)

#         # Verify the RolePerm details
#         self.assertEqual(self.role_perm.role, self.role)
#         self.assertEqual(self.role_perm.perm, self.permission)

#         # Verify the permission details
#         self.assertEqual(self.permission.name, "Can Create PostItem")
#         self.assertEqual(self.permission.codename, "create_postitem")
