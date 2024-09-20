from account.models import Role, RolePerm, Perm
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError



class RoleController:
    @staticmethod
    def create_role(data):
        role = Role.objects.create(**data)
        return role

    @staticmethod
    def get_role(role_id):
        try:
            return Role.objects.get(id=role_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def update_role(role_id, data):
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
        try:
            role = Role.objects.get(id=role_id)
            role.delete()
            return True
        except ObjectDoesNotExist:
            return False


class PermController:

    @staticmethod
    def create_perm(data):
        perm = Perm(**data)  # Create an instance without saving
        perm.full_clean()    # Perform validation
        perm.save()          # Save to database
        return perm

    @staticmethod
    def get_perm(perm_id):
        try:
            return Perm.objects.get(id=perm_id)
        except ObjectDoesNotExist:
            return None

    # @staticmethod
    # def update_perm(perm_id, data):
    #     try:
    #         perm = Perm.objects.get(id=perm_id)
    #         for key, value in data.items():
    #             setattr(perm, key, value)
    #         perm.save()
    #         return perm
    #     except ObjectDoesNotExist:
    #         return None
        
    @staticmethod
    def update_perm(perm_id, data):
        try:
            perm = Perm.objects.get(id=perm_id)
            for key, value in data.items():
                setattr(perm, key, value)
            perm.full_clean()
            perm.save()
            return perm
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_perm(perm_id):
        try:
            perm = Perm.objects.get(id=perm_id)
            perm.delete()
            return True
        except ObjectDoesNotExist:
            return False


class RolePermController:
    # @staticmethod
    # def create_role_perm(data):
    #     role_perm = RolePerm.objects.create(**data)
    #     return role_perm

    @staticmethod
    def create_role_perm(data):
        role_perm = RolePerm(**data)
        try:
            role_perm.full_clean()  # Perform model validation
            role_perm.save()
            return role_perm
        except ValidationError as e:
            # You can choose to handle the exception or re-raise it
            raise e

    @staticmethod
    def get_role_perm(role_perm_id):
        try:
            return RolePerm.objects.get(id=role_perm_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def filter_role_perms(role):
        return RolePerm.objects.filter(role=role)

    # @staticmethod
    # def update_role_perm(role_perm_id, data):
    #     try:
    #         role_perm = RolePerm.objects.get(id=role_perm_id)
    #         for key, value in data.items():
    #             setattr(role_perm, key, value)
    #         role_perm.save()
    #         return role_perm
    #     except ObjectDoesNotExist:
    #         return None

    @staticmethod
    def update_role_perm(role_perm_id, data):
        try:
            role_perm = RolePerm.objects.get(id=role_perm_id)
            for key, value in data.items():
                setattr(role_perm, key, value)
            role_perm.full_clean()  # Validate before saving
            role_perm.save()
            return role_perm
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_role_perm(role_perm_id):
        try:
            role_perm = RolePerm.objects.get(id=role_perm_id)
            role_perm.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def list_role_perms():
        return RolePerm.objects.all()