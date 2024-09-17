from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from content.api.v1.serializers import CategorySerializer, CategoryItemSerializer
from content.models import Category, CategoryItem


class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    lookup_field = "category_id"
    lookup_url_kwarg = "category_id"

    queryset = CategoryItem.objects.select_related("category", "lang", "author").all()
    serializer_class = CategoryItemSerializer

    def get_queryset(self):
        return self.queryset.filter(lang__code=self.kwargs["lang"])
