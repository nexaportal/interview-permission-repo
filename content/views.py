from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CategoryItem, Category, Language, PostItem, Post
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    CategoryItemSerializer,
    CategoryItemUpdateSerializer,
    PostItemUpdateSerializer,
    PostItemSerializer
)
from account.permissions import HasRolePermission 


class PostItemViewSet(viewsets.ModelViewSet):
    queryset = PostItem.objects.all()
    serializer_class = PostItemSerializer
    permission_classes = [HasRolePermission]

    def get_lang(self):
        # check action before getting the languages
        data = self.request.data
        # Define language names based on the payload keys
        language_names = data.keys()

        # Fetch the languages from the database
        languages = Language.objects.filter(name__in=language_names)

        # Check if all the requested languages exist
        if len(languages) != len(language_names):
            return Response(
                {"detail": "One or more languages do not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return languages


    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "en": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "title": openapi.Schema(type=openapi.TYPE_STRING, description="Title in English"),
                        "content": openapi.Schema(type=openapi.TYPE_STRING, description="Content in English"),
                    }
                ),
                "fa": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "title": openapi.Schema(type=openapi.TYPE_STRING, description="Title in Farsi"),
                        "content": openapi.Schema(type=openapi.TYPE_STRING, description="Content in Farsi"),
                    }
                ),
                "ru": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "title": openapi.Schema(type=openapi.TYPE_STRING, description="Title in Russian"),
                        "content": openapi.Schema(type=openapi.TYPE_STRING, description="Content in Russian"),
                    }
                ),
            },
            example={
                "en": {"title": "English Title", "content": "English content"},
                "fa": {"title": "عنوان فارسی", "content": "محتوای فارسی"},
                "ru": {"title": "Русский заголовок", "content": "Русский контент"}
            },
        )
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        languages = self.get_lang()

        # Create a Post object
        post = Post.objects.create()

        # Create PostItem objects for each language
        post_items = []
        for name, item_data in data.items():
            language = get_object_or_404(languages, name=name)

            # Create a PostItem for the current language
            post_item = PostItem.objects.create(
                post=post,
                lang=language,
                title=item_data['title'],
                content=item_data['content'],
                author=request.user,  # Assumes the current user is the author
            )
            post_items.append(post_item)

        # Serialize the created PostItem objects
        serializer = self.get_serializer(post_items, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CategoryItemViewSet(viewsets.ModelViewSet):
    queryset = CategoryItem.objects.all()
    serializer_class = CategoryItemSerializer
    permission_classes = [IsAuthenticated]


    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return CategoryItemUpdateSerializer
        return CategoryItemSerializer
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "en": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "name": openapi.Schema(type=openapi.TYPE_STRING, description="Name in English")
                    }
                ),
                "fa": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "name": openapi.Schema(type=openapi.TYPE_STRING, description="Name in Farsi")
                    }
                ),
                "ru": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "name": openapi.Schema(type=openapi.TYPE_STRING, description="Name in Russian")
                    }
                ),
            },
            required=["en", "fa", "ru"],  # Add required fields here
            example={
                "en": {"name": "New Category"},
                "fa": {"name": "دسته‌بندی جدید"},
                "ru": {"name": "Новая категория"},
            },
        )
    )
    
    def create(self, request, *args, **kwargs):
        # Extract the languages and data from the request
        data = request.data

        # Define language codes based on the payload keys
        language_names = data.keys()
        
        # Fetch the languages from the database
        languages = Language.objects.filter(name__in=language_names)
        
        # Check if all the requested languages exist
        if len(languages) != len(language_names):
            return Response(
                {"detail": "One or more languages do not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create a single category object
        category = Category.objects.create()

        # Create CategoryItem objects for each language
        category_items = []
        for name, item_data in data.items():
            language = get_object_or_404(languages, name=name)

            # Here, you would replace `request.user` with the actual author
            category_item = CategoryItem.objects.create(
                category=category,
                lang=language,
                author=request.user,  # Assumes the current user is the author
                name=item_data['name'],
            )
            category_items.append(category_item)

        # Serialize the created items to return in the response
        serializer = self.get_serializer(category_items, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
