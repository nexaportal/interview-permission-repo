from account.models import Role, RolePerm, Perm
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError


class RoleController:
    """
    Controller for handling Role-related operations.

    This class contains static methods to create, retrieve, update, and delete Role objects.
    """

    @staticmethod
    def create_role(data):
        """
        Create a new Role object.

        Args:
            data (dict): A dictionary containing the data required to create a new Role object.

        Returns:
            Role: The newly created Role object.
        """
        role = Role.objects.create(**data)
        return role

    @staticmethod
    def get_role(role_id):
        """
        Retrieve a Role object by its ID.

        Args:
            role_id (int): The ID of the Role to retrieve.

        Returns:
            Role: The Role object if found, or None if the Role does not exist.
        """
        try:
            return Role.objects.get(id=role_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def update_role(role_id, data):
        """
        Update an existing Role object with new data.

        Args:
            role_id (int): The ID of the Role to update.
            data (dict): A dictionary containing the updated data for the Role.

        Returns:
            Role: The updated Role object if found, or None if the Role does not exist.
        """
        try:
            role = Role.objects.get(id=role_id)
            for key, value in data.items():
                setattr(role, key, value)
            role.save()
            return role
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_role(role_id):
        """
        Delete a Role object by its ID.

        Args:
            role_id (int): The ID of the Role to delete.

        Returns:
            bool: True if the Role was successfully deleted, or False if the Role does not exist.
        """
        try:
            role = Role.objects.get(id=role_id)
            role.delete()
            return True
        except ObjectDoesNotExist:
            return False



class PermController:
    """
    Controller for handling Permission (Perm) related operations.

    This class provides static methods to create, retrieve, update, and delete Perm objects.
    """

    @staticmethod
    def create_perm(data):
        """
        Create a new Perm object.

        Args:
            data (dict): A dictionary containing the data required to create a new Perm object.

        Returns:
            Perm: The newly created Perm object after it has been validated and saved.
        """
        perm = Perm(**data)
        perm.full_clean()
        perm.save()
        return perm

    @staticmethod
    def get_perm(perm_id):
        """
        Retrieve a Perm object by its ID.

        Args:
            perm_id (int): The ID of the Perm to retrieve.

        Returns:
            Perm: The Perm object if found, or None if the Perm does not exist.
        """
        try:
            return Perm.objects.get(id=perm_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def update_perm(perm_id, data):
        """
        Update an existing Perm object with new data.

        Args:
            perm_id (int): The ID of the Perm to update.
            data (dict): A dictionary containing the updated data for the Perm.

        Returns:
            Perm: The updated Perm object if found, or None if the Perm does not exist.
        """
        try:
            perm = Perm.objects.get(id=perm_id)
            for key, value in data.items():
                setattr(perm, key, value)
            perm.full_clean()  # Validate the updated data before saving
            perm.save()
            return perm
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_perm(perm_id):
        """
        Delete a Perm object by its ID.

        Args:
            perm_id (int): The ID of the Perm to delete.

        Returns:
            bool: True if the Perm was successfully deleted, or False if the Perm does not exist.
        """
        try:
            perm = Perm.objects.get(id=perm_id)
            perm.delete()
            return True
        except ObjectDoesNotExist:
            return False


class RolePermController:
    """
    Controller for handling RolePerm-related operations.

    This class provides static methods to create, retrieve, filter, update, and delete RolePerm objects.
    """

    @staticmethod
    def create_role_perm(data):
        """
        Create a new RolePerm object.

        Args:
            data (dict): A dictionary containing the data required to create a new RolePerm object.

        Returns:
            RolePerm: The newly created RolePerm object after it has been validated and saved.

        Raises:
            ValidationError: If the provided data is invalid.
        """
        role_perm = RolePerm(**data)
        try:
            role_perm.full_clean()  # Validate the data before saving
            role_perm.save()
            return role_perm
        except ValidationError as e:
            raise e

    @staticmethod
    def get_role_perm(role_perm_id):
        """
        Retrieve a RolePerm object by its ID.

        Args:
            role_perm_id (int): The ID of the RolePerm to retrieve.

        Returns:
            RolePerm: The RolePerm object if found, or None if the RolePerm does not exist.
        """
        try:
            return RolePerm.objects.get(id=role_perm_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def filter_role_perms(role):
        """
        Retrieve a queryset of RolePerm objects filtered by a specific Role.

        Args:
            role (Role): The Role object used to filter the RolePerms.

        Returns:
            QuerySet: A queryset of RolePerm objects that belong to the specified Role.
        """
        return RolePerm.objects.filter(role=role)

    @staticmethod
    def update_role_perm(role_perm_id, data):
        """
        Update an existing RolePerm object with new data.

        Args:
            role_perm_id (int): The ID of the RolePerm to update.
            data (dict): A dictionary containing the updated data for the RolePerm.

        Returns:
            RolePerm: The updated RolePerm object if found, or None if the RolePerm does not exist.
        """
        try:
            role_perm = RolePerm.objects.get(id=role_perm_id)
            for key, value in data.items():
                setattr(role_perm, key, value)
            role_perm.full_clean()
            role_perm.save()
            return role_perm
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_role_perm(role_perm_id):
        """
        Delete a RolePerm object by its ID.

        Args:
            role_perm_id (int): The ID of the RolePerm to delete.

        Returns:
            bool: True if the RolePerm was successfully deleted, or False if the RolePerm does not exist.
        """
        try:
            role_perm = RolePerm.objects.get(id=role_perm_id)
            role_perm.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def list_role_perms():
        """
        Retrieve all RolePerm objects.

        Returns:
            QuerySet: A queryset of all RolePerm objects.
        """
        return RolePerm.objects.all()

