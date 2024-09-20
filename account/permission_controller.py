from django.contrib.contenttypes.models import ContentType


class HasRolePermissionController:
    @staticmethod
    def check_permission_for_list(user, queryset):
        """
        Filter the queryset to only include objects the user has permission to list.
        """
        user_permissions = user.role_perms.all()

        # Get the ContentType for the model associated with the queryset
        obj_content_type = ContentType.objects.get_for_model(queryset.model)

        # Create a list of languages the user has permission to list
        allowed_languages = []

        for user_permission in user_permissions:
            # Compare the permission model with the queryset's content type
            if (
                user_permission.perm.perm_model == obj_content_type
                and user_permission.perm.action == 'list'
            ):
                allowed_languages.append(user_permission.perm.lang)

        # Filter the queryset based on allowed languages
        return queryset.filter(lang__in=allowed_languages)

    @staticmethod
    def has_object_permission(user, view, obj):
        """
        Return `True` if permission is granted for object-level actions (e.g., retrieve, update).
        """
        user_permissions = user.role_perms.all()

        # Get the ContentType for the object
        obj_content_type = ContentType.objects.get_for_model(obj)

        mapped_view_action = {
            'retrieve': 'retrieve',
            'update': 'update',
            'partial_update': 'update',
            'destroy': 'delete',
        }

        for user_permission in user_permissions:
            # Compare the permission model with the object's content type
            if user_permission.perm.perm_model == obj_content_type:
                # Compare the permission's language with the object's language
                if obj.lang == user_permission.perm.lang:
                    if mapped_view_action.get(view.action) == user_permission.perm.action:
                        if view.action in ['update', 'partial_update', 'destroy']:
                            if obj.author == user:
                                return True
                        else:
                            return True
        return False

    @staticmethod
    def check_superuser(user):
        """
        Check if the user is a superuser.
        """
        return user.is_superuser

    @staticmethod
    def has_permission(user, view):
        """
        Check for general permissions before object-level checks.
        Handles actions like 'create' where language comes from request data.
        """
        action = view.action

        if HasRolePermissionController.check_superuser(user):
            return True

        if action == "list":
            return True  # We'll handle filtering in the queryset

        elif action == "create":
            try:
                if hasattr(view, 'get_lang'):
                    languages = view.get_lang()
                else:
                    raise ValueError("get_lang not found in view")
                for language in languages:
                    if not HasRolePermissionController.check_user_language_permission(user, language, action):
                        return False
                return True
            except ValueError:
                return False
        elif user.is_authenticated:
            return True
        return False

    @staticmethod
    def check_user_language_permission(user, language, action):
        """
        Check if the user has permission for the given action and language.
        """
        user_permissions = user.role_perms.all()

        for user_permission in user_permissions:
            # Check if the permission matches the action and the given language
            if (
                user_permission.perm.action == action
                and user_permission.perm.lang == language
            ):
                return True

        # If no permission matches, return False for this language
        return False


# def check_permission_for_object(user , object):
#     obj_content_type = ContentType.objects.get_for_model(object)
#     if user_permission.perm.perm_model == obj_content_type:
#                 # Compare the permission's language with the object's language
#                 if object.lang == user_permission.perm.lang:
#                     if mapped_view_action.get(view.action) == user_permission.perm.action:
#                         if view.action in ['update', 'partial_update', 'destroy']:
#                             if object.author == user:
#                                 return True
#                         else:
#                             return True