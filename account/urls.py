from django.urls import path
from .views import RegisterView, LoginView, RoleViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'roles', RoleViewSet)

# urlpatterns = router.urls

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
] + router.urls
