from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from django.contrib.contenttypes.models import ContentType

from .models.role_perm import RolePerm
from content.models.lang import Language
from content.utils import get_languages_for_user, get_category_request_data_languages, get_post_request_data_languages


class HasLanguagePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        model_ct = ContentType.objects.get_for_model(view.queryset.model)
        data = request.data
        user_roles = user.roles.all()
        if "post" in model_ct.name:
            language_codes, _ = get_post_request_data_languages(data)
        if "category" in model_ct.name:
            language_codes, _ = get_category_request_data_languages(data)

        for role in user_roles:
            role_perms = RolePerm.objects.filter(
                role=role,
                perm__perm_model=model_ct,
                perm__lang__code__in=language_codes,
                perm__field__isnull=True,
                value=True,
            )
            if role_perms:
                return True


class PermissionManager:
    def __init__(self, user, lang_codes, content_type, action, fields=[]):
        self.user = user
        self.lang_codes = lang_codes
        self.fields = fields
        self.action = action
        self.content_type = content_type

    """
        Check User Roles To Validate Languages To Create/Update Post/Category
    """

    def validate_lang_permission(self):
        user_roles = self.user.roles.all()
        languages = []
        for lang_code in self.lang_codes:
            lang = Language.objects.get(code=lang_code)
            languages.append(lang)

        for role in user_roles:
            for lang in languages:
                if RolePerm.objects.filter(role=role, perm__lang=lang).exists():
                    pass
                else:
                    raise PermissionDenied(
                        f"You do not have permission to {self.action} {self.content_type} in {lang.name} language."
                    )
        return

    """
        Check User Roles To validate fields for updating
    """

    def validate_field_permission(self):
        user_roles = self.user.roles.all()
        languages = []

        for lang_code in self.lang_codes:
            lang = Language.objects.get(code=lang_code)
            languages.append(lang)

        role_perms = RolePerm.objects.filter(role__in=user_roles).all()
        for role in role_perms:
            for lang in languages:
                for field in self.fields:
                    if RolePerm.objects.filter(
                        role=role.role, perm__lang=lang, perm__field=field, value=False
                    ).exists():
                        raise PermissionDenied(
                            f"You do not have permission to {self.action} {self.content_type} Field {field} in {lang.name} language."
                        )
