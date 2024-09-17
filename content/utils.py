from account.models.role_perm import RolePerm


def get_languages_for_user(user):
    """
    Get the list of languages the user has permission to access.
    """
    user_roles = user.roles.all()
    permitted_language_codes = RolePerm.objects.filter(
        role__in=user_roles, perm__action__in=["list", "retrieve"]
    ).values_list("perm__lang__code", flat=True)

    return permitted_language_codes


def get_not_permitted_fields_for_user(user):
    """
    Get the list of fields the user has permission to access.
    """

    user_roles = user.roles.all()
    not_permitted_fields = list(
        RolePerm.objects.filter(
            role__in=user_roles, value=False, perm__action__in=["list", "retrieve"], perm__field__isnull=False
        ).values_list("perm__field", flat=True)
    )

    return not_permitted_fields


def get_post_request_data_languages(data):
    """
    Get valid languages based on post request data
    """

    language_codes = []
    fields = []
    for lang_code, values in data["items"].items():
        language_codes.append(lang_code)
        for field_name, _ in values.items():
            fields.append(field_name)

    return language_codes, fields


def get_category_request_data_languages(data):
    """
    Get valid languages based on category request data
    """

    language_codes = []
    fields = []
    for lang_code, values in data["items"].items():
        language_codes.append(lang_code)
        for field_name, _ in values.items():
            fields.append(field_name)
