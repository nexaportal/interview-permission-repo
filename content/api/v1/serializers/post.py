from rest_framework import serializers

from content.models import Post, PostItem

from .common import ContentBaseSerializer, ContentItemBaseSerializer


class PostItemSerializer(ContentItemBaseSerializer):
    class Meta(ContentItemBaseSerializer.Meta):
        model = PostItem
        fields = ("title", "content", "author")


class PostSerializer(ContentBaseSerializer):
    child_serializer = PostItemSerializer
    items = serializers.DictField(child=PostItemSerializer(), write_only=True)

    class Meta:
        model = Post
        fields = "__all__"
