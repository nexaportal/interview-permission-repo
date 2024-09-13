from django.contrib import admin
from .models import User, Role, Perm, RolePerm

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Perm)
admin.site.register(RolePerm)
# Register your models here.
