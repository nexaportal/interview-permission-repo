from rest_framework.permissions import BasePermission
from .models import RolePerm
from content.models import Language
from rest_framework.permissions import BasePermission
from django.contrib.contenttypes.models import ContentType


class HasRolePermission(BasePermission):
    """
    Custom permission class to check if a user has the required role-based permission
    for a specific action, object type, and language.
    """

    def check_permission_for_list(self, request, view):
        """
        Check if the user has permission for the 'list' action.
        """
        pass

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        user = request.user
        user_permissions = user.role_perms.all()

        # Get the ContentType for the object (e.g., PostItem)
        obj_content_type = ContentType.objects.get_for_model(obj)

        for user_permission in user_permissions:
            # Compare the permission model with the object's content type
            if user_permission.perm.perm_model == obj_content_type:
                # Compare the permission's language with the object's language
                if obj.lang == user_permission.perm.lang:
                    if view.action == user_permission.perm.action:
                        return True
        
        return False
    
    def has_permission(self, request, view):
        """
        Check for general permissions before object-level checks.
        Handles actions like 'create' where language comes from request data.
        """
        user = request.user
        action = view.action

        if action == "create":
            try:
                # Check if the view has the 'get_lang' method to retrieve the languages
                if hasattr(view, 'get_lang'):
                    languages = view.get_lang()
                else:
                    raise ValueError("get_lang not found in view")
                
                # Iterate through the languages and check if the user has permission for each one
                for language in languages:
                    # If the user lacks permission for any language, return False immediately
                    if not self.check_user_language_permission(user, language, action):
                        return False
                
                # If all language checks pass, return True
                return True

            except ValueError as e:
                # Handle the case where language is not properly provided
                return False

        return True  # For other actions, you can add additional checks as needed

    def check_user_language_permission(self, user, language, action):
        """
        Check if the user has permission for the given action and language.
        """
        user_permissions = user.role_perms.all()

        for user_permission in user_permissions:
            # Check if the permission matches the action ('create') and the given language
            if user_permission.perm.action == action and user_permission.perm.lang == language:
                return True

        # If no permission matches, return False for this language
        return False