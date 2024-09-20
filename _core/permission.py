from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from account.models.perm import PermissionActionChoices, Perm
from account.models.role_perm import RolePerm
from account.models.user import User


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


def get_permissions(user: User, action: str, perm_model, lang_code: str = None) -> QuerySet[RolePerm]:
    queryset = RolePerm.objects.select_related("perm").filter(
        perm__perm_model=ContentType.objects.get_for_model(perm_model),
        perm__action=action,
        role__in=user.roles.values_list("id", flat=True),
    )
    if lang_code is not None:
        queryset = queryset.filter(perm__lang__code=lang_code)
    return queryset


class ListPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        role_permissions = get_permissions(request.user, PermissionActionChoices.LIST, view.queryset.model)
        request.excluded_langs = role_permissions.filter(perm__field="*", value=False).values_list("perm__lang", flat=True)
        request.excluded_fields = {}
        for role_permission in role_permissions.filter(value=False).exclude(perm__field="*"):
            request.excluded_fields.setdefault(role_permission.perm.lang.code, [])
            request.excluded_fields[role_permission.perm.lang.code].append(role_permission.perm.field)
        return True


class CreatePermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        role_permissions = get_permissions(request.user, PermissionActionChoices.CREATE, view.queryset.model)
        data = request.data.copy()
        request.excluded_fields = {}
        for lang_code in data.get("items", []):
            lang_role_permissions = role_permissions.filter(perm__lang__code=lang_code)
            if lang_role_permissions.filter(perm__field="*", value=False).exists():
                return False
            for field in lang_role_permissions.filter(value=False).values_list("perm__field", flat=True):
                data["items"][lang_code].pop(field, None)
            request.excluded_fields[lang_code] = list(
                role_permissions.filter(value=False).values_list("perm__field", flat=True)
            )

        request._full_data = data
        return True


class RetrievePermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        lang_code: str = view.kwargs["lang"]
        role_permissions = get_permissions(
            request.user, PermissionActionChoices.RETRIEVE, view.queryset.model, lang_code
        )
        if not all(role_permission.value for role_permission in role_permissions.filter(perm__field="*")):
            return False

        request.excluded_fields = {
            lang_code: list(role_permissions.filter(value=False).values_list("perm__field", flat=True))
        }
        return True


class UpdatePermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        role_permissions = get_permissions(
            request.user, PermissionActionChoices.UPDATE, view.queryset.model, view.kwargs["lang"]
        )
        if not (
            all(role_permission.value for role_permission in role_permissions.filter(perm__field="*"))
            and view.get_object().author == request.user
        ):
            return False

        data = request.data.copy()
        for field in role_permissions.filter(value=False).values_list("perm__field", flat=True):
            data.pop(field, None)
        request._full_data = data  # Can not set data in request object
        return True


class DeletePermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        return (
            all(
                permission.value
                for permission in get_permissions(
                    request.user, PermissionActionChoices.DELETE, view.queryset.model, view.kwargs["lang"]
                )
            )
            and view.get_object().author == request.user
        )
