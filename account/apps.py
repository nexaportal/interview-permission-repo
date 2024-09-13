from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "account"

    def ready(self):
        from .models.user import User
        from .models.role import Role
        from .models.perm import Perm
        from .models.role_perm import RolePerm
