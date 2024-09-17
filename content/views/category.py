from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from account.permissions import HasLanguagePermission, PermissionManager
from content.models.category import Category
from content.serializers.category import CategorySerializer
from content.utils import get_languages_for_user, get_category_request_data_languages


"""
    ViewSet To Handle Category CRUD request
    request data To Create or update
        - items -> dict: {
            "en": {
                "name": "Cat1"
            },
            "ru": {
                "name": "Cat2"
            }
        }
"""


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, HasLanguagePermission]

    # Get categories which has the same language as user role permission language
    def get_queryset(self):
        allowed_languages = get_languages_for_user(self.request.user)
        queryset = (
            Category.objects.prefetch_related("category_items")
            .filter(category_items__lang__code__in=allowed_languages)
            .distinct()
        )

        return queryset

    # Check user role permission language to create category object
    def create(self, request, *args, **kwargs):
        language_codes, _ = get_category_request_data_languages(request.data)

        permission_manager = PermissionManager(request.user, language_codes, "category", "create")
        permission_manager.validate_lang_permission()

        return super().create(request, *args, **kwargs)

    # Check user role permission language to update category object
    def update(self, request, *args, **kwargs):
        language_codes, fields = get_category_request_data_languages(request.data)

        permission_manager = PermissionManager(request.user, language_codes, "category", "update", fields)

        permission_manager.validate_lang_permission()
        permission_manager.validate_field_permission()

        return super().update(request, *args, **kwargs)
