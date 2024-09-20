# from django.test import TestCase
# from django.core.exceptions import ObjectDoesNotExist, ValidationError
# from account.models import Role
# from account.controllers import RoleController
# from django.db import IntegrityError

# class RoleControllerTests(TestCase):
#     def setUp(self):
#         # Set up initial data for the tests
#         self.existing_role = Role.objects.create(name='Admin')

#     def test_create_role(self):
#         # Test creating a new role
#         data = {'name': 'User'}
#         role = RoleController.create_role(data)
#         self.assertIsInstance(role, Role)
#         self.assertEqual(role.name, 'User')
#         self.assertTrue(Role.objects.filter(id=role.id).exists())

#     def test_create_role_with_existing_name(self):
#         data = {'name': 'Admin'}
#         with self.assertRaises(IntegrityError):
#             RoleController.create_role(data)

#     def test_get_role(self):
#         # Test retrieving an existing role
#         role = RoleController.get_role(self.existing_role.id)
#         self.assertEqual(role, self.existing_role)

#         # Test retrieving a non-existent role
#         role = RoleController.get_role(999)
#         self.assertIsNone(role)

#     def test_update_role(self):
#         # Test updating an existing role
#         data = {'name': 'SuperAdmin'}
#         updated_role = RoleController.update_role(self.existing_role.id, data)
#         self.assertIsNotNone(updated_role)
#         self.assertEqual(updated_role.name, 'SuperAdmin')

#         # Test updating a non-existent role
#         updated_role = RoleController.update_role(999, data)
#         self.assertIsNone(updated_role)

#     def test_delete_role(self):
#         # Test deleting an existing role
#         result = RoleController.delete_role(self.existing_role.id)
#         self.assertTrue(result)
#         self.assertFalse(Role.objects.filter(id=self.existing_role.id).exists())

#         # Test deleting a non-existent role
#         result = RoleController.delete_role(999)
#         self.assertFalse(result)
