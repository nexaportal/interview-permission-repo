from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from account.models import Perm, Role, RolePerm, User


@register(Perm)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("name", "codename", "perm_model", "lang", "action", "field")


class RolePermInline(admin.TabularInline):
    model = RolePerm


@register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = (RolePermInline,)


@register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "get_full_name",
        "mobile",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("mobile", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "roles",
                ),
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined")},
        ),
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
    )
    search_fields = ("first_name", "last_name", "mobile")
