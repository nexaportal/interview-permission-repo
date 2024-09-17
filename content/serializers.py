from rest_framework import serializers
from .models import CategoryItem, PostItem
from account.serializers import FieldPermissionSerializer



class CategoryItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryItem
        fields = ['name']


class CategoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryItem
        fields = ['id', 'category', 'lang', 'author', 'name', 'created_at', 'updated_at']


class PostItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostItem
        fields = ['title', 'content']


class PostItemSerializer(FieldPermissionSerializer):
    class Meta:
        model = PostItem
        fields = ['post', 'lang', 'title', 'content', 'author', 'created_at', 'updated_at']