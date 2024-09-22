from django.contrib.auth.backends import ModelBackend

from account.models import User


class ModelBackendWithMobile(ModelBackend):
    """
    An auth backend with phone number and password
    """

    def authenticate(self, request, mobile=None, password=None, **kwargs):
        if mobile is None or password is None:
            return
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


def default_user_authentication_rule(user: User):
    """
    Will be used in USER_AUTHENTICATION_RULE of Simple JWT
    :param user: user obj
    :return: True on valid rule
    """
    return user is not None and user.is_active
