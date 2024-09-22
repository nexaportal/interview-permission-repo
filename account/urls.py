from django.urls import path
from .views import RegisterView, LoginView, RolePermViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"roleperms", RolePermViewSet, basename="roleperm")


urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
]

urlpatterns += router.urls
