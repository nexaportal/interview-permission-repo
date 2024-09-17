from django.contrib import admin
from .models.user import User
from .models.role import Role
from .models.perm import Perm
from .models.role_perm import RolePerm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "mobile",
        "first_name",
        "last_name"
    ]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name"
    ]


@admin.register(Perm)
class PermAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "lang",
        "perm_model",
        "action",
        "field"
    ]


@admin.register(RolePerm)
class RolePermAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "role",
        "perm",
        "value"
    ]
