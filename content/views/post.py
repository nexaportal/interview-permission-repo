from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from content.models.post import Post
from content.serializers.post import PostSerializer
from account.permissions import HasLanguagePermission, PermissionManager
from content.utils import get_languages_for_user, get_not_permitted_fields_for_user, get_post_request_data_languages


"""
    ViewSet To Handle Post CRUD request
    request data To Create or update
        - items -> dict: {
            "en": {
                "title": "P1",
                "content": "P1Content"
            },
            "ru": {
                "title": "P2",
                "content": "P2Content"
            }
        }
"""


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, HasLanguagePermission]

    # Get posts which has the same language as user role permission language
    def get_queryset(self):
        allowed_languages = get_languages_for_user(self.request.user)
        queryset = (
            Post.objects.prefetch_related("post_items").filter(post_items__lang__code__in=allowed_languages).distinct()
        )

        return queryset

    # Check user role permission language to create post object
    def create(self, request, *args, **kwargs):
        language_codes, _ = get_post_request_data_languages(request.data["items"])
        permission_manager = PermissionManager(request.user, language_codes, "post", "create")
        permission_manager.validate_lang_permission()

        return super().create(request, *args, **kwargs)

    # Check user role permission language to update post object
    def update(self, request, *args, **kwargs):
        language_codes, fields = get_post_request_data_languages(request.data["items"])

        permission_manager = PermissionManager(request.user, language_codes, "post", "update", fields)

        permission_manager.validate_lang_permission()
        permission_manager.validate_field_permission()

        return super().update(request, *args, **kwargs)
