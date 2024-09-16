from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models.category import Category
from .serializers import CategorySerializer


'''
    ViewSet To Handle Category CRUD request
    request data To Create or update
        - items -> dict: {
            "en": {
                "name": "Cat1"
            },
            "ru": {
                "name": "Cat2"
            }
        }
'''
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()