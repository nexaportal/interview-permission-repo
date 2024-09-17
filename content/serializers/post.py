from rest_framework import serializers
from rest_framework.exceptions import NotFound

from content.models.post import Post, PostItem
from content.models.lang import Language
from content.utils import get_languages_for_user, get_not_permitted_fields_for_user


from .lang import LanguageSerializer


"""
    Post Item Will be Created/Updated in Post CRUD requests
"""


class PostItemSerializer(serializers.ModelSerializer):
    lang = LanguageSerializer(read_only=True)

    class Meta:
        model = PostItem
        fields = ["lang", "author", "title", "content"]


"""
    Create and update method customized to handle post item creation/update
"""


class PostSerializer(serializers.ModelSerializer):
    post_items = serializers.SerializerMethodField()
    items = serializers.DictField(child=serializers.DictField(), write_only=True)

    class Meta:
        model = Post
        fields = ["id", "items", "post_items", "created_at", "updated_at"]

    """
        Method added to get post items based on permitted fields and languages
        user with permission to get post items of english language are just able to 
        list/retrieve post items which their language in english
    """

    def get_post_items(self, obj):
        allowed_languages = get_languages_for_user(self.context["request"].user)
        not_permitted_fields = get_not_permitted_fields_for_user(self.context["request"].user)
        post_items = obj.post_items.filter(lang__code__in=allowed_languages)

        """
            DynamicSerializer added from BaseSerializer Class to remove non permitted fields
        """

        class DynamicPostItemSerializer(PostItemSerializer):
            class Meta(PostItemSerializer.Meta):
                fields = [field for field in PostItemSerializer.Meta.fields if field not in not_permitted_fields]

        return DynamicPostItemSerializer(post_items, many=True).data

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        post = Post.objects.create(**validated_data)
        author = self.context["request"].user

        for lang_code, item_data in items_data.items():
            try:
                language = Language.objects.get(code=lang_code)
                PostItem.objects.create(
                    post=post, lang=language, title=item_data["title"], content=item_data["content"], author=author
                )
            except Language.DoesNotExist:
                raise NotFound(detail="Item not found", code=404)

        return post

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items")
        instance.save()

        for language, value in items_data.items():
            language = Language.objects.get(code=language)
            item = PostItem.objects.get(post=instance, lang=language)
            item.title = value["title"]
            item.content = value["content"]
            item.save()

        return instance
