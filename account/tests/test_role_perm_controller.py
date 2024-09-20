from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils import IntegrityError
from account.models import Role, Perm, RolePerm
from account.controllers import RoleController, PermController, RolePermController
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

class RolePermControllerTests(TestCase):
    def setUp(self):
        # Set up Roles
        self.role_admin = RoleController.create_role({'name': 'Admin'})
        self.role_user = RoleController.create_role({'name': 'User'})
        
        # Set up Permissions
        self.content_type = ContentType.objects.get_for_model(Perm)
        self.perm_view = PermController.create_perm({
            'name': 'Can View',
            'codename': 'can_view',
            'perm_model': self.content_type,
            'action': 'retrieve',
            'field': '',
            'lang': None,
        })
        self.perm_edit = PermController.create_perm({
            'name': 'Can Edit',
            'codename': 'can_edit',
            'perm_model': self.content_type,
            'action': 'update',
            'field': '',
            'lang': None,
        })
        
        # Create an existing RolePerm
        self.existing_role_perm = RolePermController.create_role_perm({
            'role': self.role_admin,
            'perm': self.perm_view,
            'value': True,
        })

    def test_create_role_perm(self):
        # Test creating a new RolePerm with valid data
        data = {
            'role': self.role_user,
            'perm': self.perm_edit,
            'value': True,
        }
        role_perm = RolePermController.create_role_perm(data)
        self.assertIsInstance(role_perm, RolePerm)
        self.assertEqual(role_perm.role, self.role_user)
        self.assertEqual(role_perm.perm, self.perm_edit)
        self.assertTrue(RolePerm.objects.filter(id=role_perm.id).exists())

    def test_create_role_perm_with_duplicate(self):
        # Test creating a RolePerm with duplicate role and perm (should raise ValidationError)
        data = {
            'role': self.role_admin,
            'perm': self.perm_view,  # Same as existing_role_perm
            'value': False,
        }
        with self.assertRaises(ValidationError):
            RolePermController.create_role_perm(data)

    def test_get_role_perm(self):
        # Test retrieving an existing RolePerm
        role_perm = RolePermController.get_role_perm(self.existing_role_perm.id)
        self.assertEqual(role_perm, self.existing_role_perm)

        # Test retrieving a non-existent RolePerm
        role_perm = RolePermController.get_role_perm(9999)
        self.assertIsNone(role_perm)

    def test_update_role_perm(self):
        # Test updating an existing RolePerm
        data = {'value': False}
        updated_role_perm = RolePermController.update_role_perm(self.existing_role_perm.id, data)
        self.assertIsNotNone(updated_role_perm)
        self.assertFalse(updated_role_perm.value)

        # Test updating a non-existent RolePerm
        updated_role_perm = RolePermController.update_role_perm(9999, data)
        self.assertIsNone(updated_role_perm)

    def test_delete_role_perm(self):
        # Test deleting an existing RolePerm
        result = RolePermController.delete_role_perm(self.existing_role_perm.id)
        self.assertTrue(result)
        self.assertFalse(RolePerm.objects.filter(id=self.existing_role_perm.id).exists())

        # Test deleting a non-existent RolePerm
        result = RolePermController.delete_role_perm(9999)
        self.assertFalse(result)

    def test_list_role_perms(self):
        # Test listing all RolePerms
        role_perms = RolePermController.list_role_perms()
        self.assertEqual(role_perms.count(), 1)  # Only existing_role_perm exists initially

    def test_filter_role_perms(self):
        # Test filtering RolePerms by role
        role_perms = RolePermController.filter_role_perms(self.role_admin)
        self.assertEqual(role_perms.count(), 1)
        self.assertEqual(role_perms.first(), self.existing_role_perm)

        # Test filtering RolePerms for a role with no permissions
        role_perms = RolePermController.filter_role_perms(self.role_user)
        self.assertEqual(role_perms.count(), 0)
