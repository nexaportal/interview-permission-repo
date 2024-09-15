from django.urls import path

from account.api.v1 import views

app_name = "v1.account"


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
