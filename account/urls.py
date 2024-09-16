
from django.urls import path
from .views import MyObtainTokenPairView, RegisterView


urlpatterns = [
    path('auth/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
]

