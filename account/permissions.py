"""
permissions.py

This module defines custom permission classes and helper functions for role-based access control in a Django REST framework application.

Classes:
    - HasRolePermission: Custom permission class to check if a user has the required role-based permission for specific actions, object types, and languages.

Functions:
    - check_user_is_owner(user, obj): Check if the user is the owner of the object.
    - check_user_permission_for_object(user, obj, mapped_action, action): Check if the user has the required permission for the object and action.

Dependencies:
    - rest_framework.permissions.BasePermission: Base class for creating custom permissions.
    - .models.RolePerm: Model representing role-based permissions.
    - content.models.Language: Model representing languages.
    - django.contrib.contenttypes.models.ContentType: Model for handling generic relations.
"""

from rest_framework.permissions import BasePermission
from .models import RolePerm
from content.models import Language
from django.contrib.contenttypes.models import ContentType


class HasRolePermission(BasePermission):
    """
    Custom permission class to check if a user has the required role-based permission
    for a specific action, object type, and language.
    """

    def check_permission_for_list(self, request, view, queryset):
        """
        Filter the queryset to only include objects the user has permission to list.

        Args:
            request: The HTTP request object.
            view: The view being accessed.
            queryset: The queryset to be filtered.

        Returns:
            Filtered queryset containing only objects the user has permission to list.
        """
        user = request.user
        user_permissions = user.role_perms.all()

        # Get the ContentType for the model associated with the view (e.g., PostItem)
        obj_content_type = ContentType.objects.get_for_model(queryset.model)

        # Create a list of languages the user has permission to list
        allowed_languages = []

        for user_permission in user_permissions:
            # Compare the permission model with the queryset's content type
            if user_permission.perm.perm_model == obj_content_type and user_permission.perm.action == "list":
                allowed_languages.append(user_permission.perm.lang)

        # Filter the queryset based on allowed languages
        return queryset.filter(lang__in=allowed_languages)

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted for object-level actions (e.g., retrieve, update).

        Args:
            request: The HTTP request object.
            view: The view being accessed.
            obj: The object being accessed.

        Returns:
            Boolean indicating whether the user has permission for the object-level action.
        """
        user = request.user
        user_permissions = user.role_perms.all()

        # Get the ContentType for the object (e.g., PostItem)
        obj_content_type = ContentType.objects.get_for_model(obj)

        mapped_view_action = {
            "retrieve": "retrieve",
            "update": "update",
            "partial_update": "update",
            "destroy": "delete",
        }
        if check_user_permission_for_object(user, obj, view.action, mapped_view_action):
            return True
        return False

    def check_superuser(self, user):
        """
        Check if the user is a superuser.

        Args:
            user: The user object.

        Returns:
            Boolean indicating whether the user is a superuser.
        """
        return user.is_superuser

    def has_permission(self, request, view):
        """
        Check for general permissions before object-level checks.
        Handles actions like 'create' where language comes from request data.

        Args:
            request: The HTTP request object.
            view: The view being accessed.

        Returns:
            Boolean indicating whether the user has general permission for the action.
        """
        user = request.user
        action = view.action

        if self.check_superuser(user):
            return True

        if action == "list":
            return True  # We'll handle filtering in the queryset

        elif action == "create":
            try:
                if hasattr(view, "get_lang"):
                    languages = view.get_lang()
                else:
                    raise ValueError("get_lang not found in view")
                for language in languages:
                    if not self.check_user_language_permission(user, language, action):
                        return False
                return True
            except ValueError as e:
                return False
        elif user.is_authenticated:
            return True
        return False

    def check_user_language_permission(self, user, language, action):
        """
        Check if the user has permission for the given action and language.

        Args:
            user: The user object.
            language: The language object.
            action: The action being performed.

        Returns:
            Boolean indicating whether the user has permission for the action and language.
        """
        user_permissions = user.role_perms.all()

        for user_permission in user_permissions:
            # Check if the permission matches the action ('create') and the given language
            if user_permission.perm.action == action and user_permission.perm.lang == language:
                return True

        # If no permission matches, return False for this language
        return False


def check_user_is_owner(user, obj):
    """
    Check if the user is the owner of the object.

    Args:
        user: The user object.
        obj: The object being accessed.

    Returns:
        Boolean indicating whether the user is the owner of the object.
    """
    return obj.author == user


def check_user_permission_for_object(user, obj, mapped_action, action):
    """
    Check if the user has the required permission for the object and action.

    Args:
        user: The user object.
        obj: The object being accessed.
        mapped_action: The action mapped from the view.
        action: The action being performed.

    Returns:
        Boolean indicating whether the user has the required permission for the object and action.
    """
    user_permissions = user.role_perms.all()
    obj_content_type = ContentType.objects.get_for_model(obj)
    for user_permission in user_permissions:
        if user_permission.perm.perm_model == obj_content_type:
            if obj.lang == user_permission.perm.lang:
                if mapped_action == user_permission.perm.action:
                    if action in ["update", "partial_update", "destroy"]:
                        return check_user_is_owner(user, obj)
                    else:
                        return True
    return False