from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from content.models import Language


class ContentBaseSerializer(serializers.ModelSerializer):
    items = serializers.DictField(write_only=True)
    child_serializer = None

    def to_internal_value(self, data):
        for lang_code in data["items"]:
            data["items"][lang_code]["author"] = self.context["request"].user
        return data

    def validate(self, attrs):
        attrs = super().validate(attrs)
        for lang_code in attrs["items"]:
            language = Language.get_by_code(lang_code)
            if not language:
                raise serializers.ValidationError({lang_code: _("Not found.")})
            attrs["items"][lang_code]["lang"] = language
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        items: dict = validated_data.pop("items")
        instance = super().create(validated_data)
        new_items = []
        item_model = instance.__class__.items.field.model
        for item in items.values():
            item[instance.__class__.__name__.lower()] = instance
            new_items.append(item_model(**item))
        item_model.objects.bulk_create(new_items)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["items"] = {}
        for item in instance.items.all():
            representation["items"][item.lang.code] = self.child_serializer(item).data
        return representation
