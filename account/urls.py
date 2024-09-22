from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views.user import MyObtainTokenPairView, RegisterView
from .views.role import RoleViewSet

router = SimpleRouter()
router.register(r"role", RoleViewSet, basename="role")

urlpatterns = [
    path("auth/login/", MyObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("auth/register/", RegisterView.as_view(), name="auth_register"),
    path("", include(router.urls)),
]
