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
    
    def check_user_language_permission(self, user, language, action):
        """
        Check if the user has permission for the given action and language.
        """
        # Assuming you have a 'perm' model that links a user role to language permissions
        user_permissions = user.role_perms.all()

        for user_permission in user_permissions:
            # Check if the permission matches the action ('create') and the language
            if user_permission.perm.action == action and user_permission.perm.lang == language:
                return True

        # If no permission matches, return False
        return False

    def has_permission(self, request, view):
        """
        Check for general permissions before object-level checks.
        Handles actions like 'create' where language comes from request data.
        """

        # Get the action the user is trying to perform (e.g., 'create', 'update', etc.)
        action = view.action

        if action == "list":
            print(action)

        if action == "create":
            try:
                # Check if the view has the 'get_lang' method to retrieve the languages
                if hasattr(view, 'get_lang'):
                    languages = view.get_lang()
                else:
                    raise ValueError("get_lang not found in view")
                
                # Check if the user has permission for each language in the request
                for language in languages:
                    # Ensure user has permission for the 'create' action and the given language
                    if not self.check_user_language_permission(
                        request.user, language, action):
                        return False
                return True

            except ValueError as e:
                # Handle the case where language is not properly provided
                return False

        return True



        # Get the model class (e.g., PostItem) from the view's queryset
        model_class = view.get_queryset().model

        # Get the language using the `get_lang` method in the view
        try:
            language = view.get_lang()
        except ValueError as e:
            return False  # Handle language extraction failure as needed

        # Fetch the user's role(s)
        user_roles = request.user.role_perms.all()

        # Check if the user has permission for the action, model, and language
        content_type = ContentType.objects.get_for_model(model_class)
        
        return True