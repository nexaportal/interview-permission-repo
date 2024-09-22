from rest_framework import serializers

from content.models import Category, CategoryItem

from .common import ContentBaseSerializer, ContentItemBaseSerializer


class CategoryItemSerializer(ContentItemBaseSerializer):
    class Meta(ContentItemBaseSerializer.Meta):
        model = CategoryItem
        fields = ("name", "author")


class CategorySerializer(ContentBaseSerializer):
    child_serializer = CategoryItemSerializer
    items = serializers.DictField(child=CategoryItemSerializer(), write_only=True)

    class Meta:
        model = Category
        fields = "__all__"
