from django.contrib import admin
from .models.lang import Language
from .models.category import Category, CategoryItem


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['user']
    

@admin.register(CategoryItem)
class CategoryItemAdmin(admin.ModelAdmin):
    list_display = ['category', 'lang', 'author', 'name']