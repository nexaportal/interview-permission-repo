from django.urls import path

from account.api.v1 import views

app_name = "v1.account"


urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("role", views.RoleListCreateView.as_view(), name="role"),
    path("role/<int:pk>", views.RoleRetrieveUpdateDestroyView.as_view(), name="role-detail"),
    path("role/<int:pk>/permission", views.RolePermissionListUpdateView.as_view(), name="role-permission"),
]
