from django.contrib import admin
from .models.lang import Language
from .models.category import Category, CategoryItem
from .models.post import Post, PostItem


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ["code", "name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["user"]


@admin.register(CategoryItem)
class CategoryItemAdmin(admin.ModelAdmin):
    list_display = ["category", "lang", "author", "name"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at", "updated_at"]


@admin.register(PostItem)
class PostItemAdmin(admin.ModelAdmin):
    list_display = ["post", "lang", "title", "content", "author"]
