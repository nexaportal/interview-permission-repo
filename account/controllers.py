from .models import Role, RolePerm, Perm



class RoleService:
    def __init__(self, perm_service):
        self.perm_service = perm_service

    def create_perm(self, data):
        perm, created = self.perm_service.get_or_create_perm(
            name=data['name'],
            codename=data['codename'],
            perm_model=data['perm_model'],  # Assuming ContentType instance is passed
            action=data['action'],
            field=data.get('field', None),
            lang=data.get('lang', None)  # Assuming Language instance is passed
        )
        return perm

    def create_role_perm(self, role, perm_data):
        perm = self.create_perm(perm_data['perm'])
        role_perm, created = RolePerm.objects.get_or_create(
            role=role,
            perm=perm,
            value=perm_data.get('value', True)
        )
        return role_perm

    def create_role(self, data):
        role, created = Role.objects.get_or_create(name=data['name'])
        for perm_data in data.get('role_permset', []):
            self.create_role_perm(role, perm_data)
        return role


class PermService:
    def get_or_create_perm(self, name, codename, perm_model, action, field=None, lang=None):
        perm, created = Perm.objects.get_or_create(
            name=name,
            codename=codename,
            perm_model=perm_model,
            action=action,
            field=field,
            lang=lang
        )
        return perm, created