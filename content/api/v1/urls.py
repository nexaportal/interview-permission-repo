from django.urls import path

from content.api.v1 import views

app_name = "v1.content"


urlpatterns = [
    path("post", views.PostListCreateView.as_view(), name="post"),
    path("post/<int:post_id>/<str:lang>", views.PostRetrieveUpdateDestroyView.as_view(), name="post-detail"),
    path("category", views.CategoryListCreateView.as_view(), name="category"),
    path(
        "category/<int:category_id>/<str:lang>",
        views.CategoryRetrieveUpdateDestroyView.as_view(),
        name="category-detail",
    ),
]
