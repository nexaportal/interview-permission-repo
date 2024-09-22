from django.contrib import admin
from .models import Post, PostItem, Language, Category, CategoryItem

admin.site.register(Post)
admin.site.register(PostItem)
admin.site.register(Language)
admin.site.register(Category)
admin.site.register(CategoryItem)
# Register your models here.
