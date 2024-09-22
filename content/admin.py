from django.contrib import admin
from django.contrib.admin import register

from content.models import Language, Post, PostItem, Category, CategoryItem


@register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "code")


class PostItemInline(admin.TabularInline):
    model = PostItem


@register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "created")
    inlines = (PostItemInline,)


class CategoryItemInline(admin.TabularInline):
    model = CategoryItem


@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "created")
    inlines = (CategoryItemInline,)
