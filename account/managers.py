from django.contrib.auth.models import BaseUserManager

"""
    Manager added to handle Create Super user based on user manager changes
"""


class UserManager(BaseUserManager):
    def create_user(self, mobile, password=None, **extra_fields):
        mobile = self.normalize_email(mobile)
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(mobile, password, **extra_fields)
