from rest_framework import serializers
from .models.category import Category, CategoryItem
from .models.lang import Language

'''
    Category Item Will be Created/Updated in category CRUD requests
'''
class CategoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryItem
        fields = ['lang', 'author', 'name']

    
'''
    Create and update method customized to handle category item creation/update
'''
class CategorySerializer(serializers.ModelSerializer):
    items = serializers.DictField(child=serializers.DictField(), write_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'items', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user 
        items_data = validated_data.pop('items')
        category = Category.objects.create(**validated_data)
        author = self.context['request'].user
        
        for lang_code, item_data in items_data.items():
            try:
                langugage = Language.objects.get(code=lang_code)
                CategoryItem.objects.create(
                    category=category,
                    lang=langugage,
                    name=item_data['name'],
                    author=author
                    )
            except Exception as e:
                print(e)
                pass
            
        return category

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance.save()

        for item_data in items_data:
            language = item_data.get('lang')
            item = CategoryItem.objects.get(category=instance, lang=language)
            item.name = item_data.get('name', item.name)
            item.save()

        return instance