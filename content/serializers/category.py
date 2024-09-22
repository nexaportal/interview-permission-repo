from rest_framework import serializers
from rest_framework.exceptions import NotFound

from content.models.category import Category, CategoryItem
from content.models.lang import Language
from .lang import LanguageSerializer
from content.utils import get_languages_for_user, get_not_permitted_fields_for_user


"""
    Category Item Will be Created/Updated in category CRUD requests
"""


class CategoryItemSerializer(serializers.ModelSerializer):
    lang = LanguageSerializer(read_only=True)

    class Meta:
        model = CategoryItem
        fields = ["lang", "author", "name"]


"""
    Create and update method customized to handle category item creation/update
"""


class CategorySerializer(serializers.ModelSerializer):
    category_items = serializers.SerializerMethodField()
    items = serializers.DictField(child=serializers.DictField(), write_only=True)

    class Meta:
        model = Category
        fields = ["id", "category_items", "items", "created_at", "updated_at"]

    """
        Method added to get category items based on permitted fields and languages
        user with permission to get cateory items of english language are just able to 
        list/retrieve category items which their language in english
    """

    def get_category_items(self, obj):
        allowed_languages = get_languages_for_user(self.context["request"].user)
        not_permitted_fields = get_not_permitted_fields_for_user(self.context["request"].user)
        category_items = obj.category_items.filter(lang__code__in=allowed_languages)

        """
            DynamicSerializer added from BaseSerializer Class to remove non permitted fields
        """

        class DynamicCategoryItemSerializer(CategoryItemSerializer):
            class Meta(CategoryItemSerializer.Meta):
                fields = [field for field in CategoryItemSerializer.Meta.fields if field not in not_permitted_fields]

        return DynamicCategoryItemSerializer(category_items, many=True).data

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        items_data = validated_data.pop("items")
        category = Category.objects.create(**validated_data)
        author = self.context["request"].user

        for lang_code, item_data in items_data.items():
            try:
                language = Language.objects.get(code=lang_code)
                CategoryItem.objects.create(category=category, lang=language, name=item_data["name"], author=author)
            except Language.DoesNotExist:
                raise NotFound(detail="Item not found", code=404)

        return category

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items")
        instance.save()
        for language, value in items_data.items():
            language = Language.objects.get(code=language)
            item = CategoryItem.objects.filter(category=instance, lang=language).first()
            item.name = value["name"]
            item.save()

        return instance
