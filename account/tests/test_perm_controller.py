# from django.test import TestCase
# from django.core.exceptions import ObjectDoesNotExist, ValidationError
# from django.contrib.contenttypes.models import ContentType
# from django.db.utils import IntegrityError
# from account.controllers import Perm, PermController
# from account.models.perm import PermissionActionChoices
# from content.models import Language

# class PermControllerTests(TestCase):
#     def setUp(self):
#         # Create necessary foreign key objects
#         self.content_type = ContentType.objects.get_for_model(Perm)
#         self.language = Language.objects.create(name='English', code='en')

#         # Create an existing permission
#         self.existing_perm = Perm.objects.create(
#             name='Can View Perm',
#             codename='can_view_perm',
#             perm_model=self.content_type,
#             action=PermissionActionChoices.RETRIEVE,
#             field='',
#             lang=self.language,
#         )

#     def test_create_perm(self):
#         # Test creating a new permission with valid data
#         data = {
#             'name': 'Can Add Perm',
#             'codename': 'can_add_perm',
#             'perm_model': self.content_type,
#             'action': PermissionActionChoices.CREATE,
#             'field': '',
#             'lang': self.language,
#         }
#         perm = PermController.create_perm(data)
#         self.assertIsInstance(perm, Perm)
#         self.assertEqual(perm.name, 'Can Add Perm')
#         self.assertTrue(Perm.objects.filter(id=perm.id).exists())

#     def test_create_perm_with_existing_name(self):
#         # Test creating a permission with a name that already exists (should raise ValidationError)
#         data = {
#             'name': 'Can View Perm',  # Name already exists
#             'codename': 'can_view_perm_duplicate',
#             'perm_model': self.content_type,
#             'action': PermissionActionChoices.RETRIEVE,
#             'field': '',
#             'lang': self.language,
#         }
#         with self.assertRaises(ValidationError):
#             PermController.create_perm(data)

#     def test_create_perm_with_invalid_action(self):
#         # Test creating a permission with an invalid action (should raise ValidationError)
#         data = {
#             'name': 'Invalid Action Perm',
#             'codename': 'invalid_action_perm',
#             'perm_model': self.content_type,
#             'action': 'invalid_action',  # Invalid action choice
#             'field': '',
#             'lang': self.language,
#         }
#         with self.assertRaises(ValidationError):
#             PermController.create_perm(data)

#     def test_get_perm(self):
#         # Test retrieving an existing permission
#         perm = PermController.get_perm(self.existing_perm.id)
#         self.assertEqual(perm, self.existing_perm)

#         # Test retrieving a non-existent permission
#         perm = PermController.get_perm(9999)
#         self.assertIsNone(perm)

#     def test_update_perm(self):
#         # Test updating an existing permission
#         data = {
#             'name': 'Can Edit Perm',
#             'action': PermissionActionChoices.UPDATE,
#         }
#         updated_perm = PermController.update_perm(self.existing_perm.id, data)
#         self.assertIsNotNone(updated_perm)
#         self.assertEqual(updated_perm.name, 'Can Edit Perm')
#         self.assertEqual(updated_perm.action, PermissionActionChoices.UPDATE)

#         # Test updating a permission to a name that already exists (should raise ValidationError)
#         another_perm = Perm.objects.create(
#             name='Can Delete Perm',
#             codename='can_delete_perm',
#             perm_model=self.content_type,
#             action=PermissionActionChoices.DELETE,
#             field='',
#             lang=self.language,
#         )
#         data = {'name': 'Can Edit Perm'}  # Name already used by updated_perm
#         with self.assertRaises(ValidationError):
#             PermController.update_perm(another_perm.id, data)

#         # Test updating a non-existent permission
#         updated_perm = PermController.update_perm(9999, data)
#         self.assertIsNone(updated_perm)

#     def test_delete_perm(self):
#         # Test deleting an existing permission
#         result = PermController.delete_perm(self.existing_perm.id)
#         self.assertTrue(result)
#         self.assertFalse(Perm.objects.filter(id=self.existing_perm.id).exists())

#         # Test deleting a non-existent permission
#         result = PermController.delete_perm(9999)
#         self.assertFalse(result)
