from rest_framework.routers import DefaultRouter
from .views import CategoryItemViewSet, PostItemViewSet

router = DefaultRouter()
router.register(r"category", CategoryItemViewSet, basename="category")
router.register(r"post", PostItemViewSet, basename="post")

urlpatterns = router.urls
