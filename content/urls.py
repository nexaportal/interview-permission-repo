from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.category import CategoryViewSet
from .views.post import PostViewSet

router = DefaultRouter()
router.register(r"category", CategoryViewSet)
router.register(r"post", PostViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
