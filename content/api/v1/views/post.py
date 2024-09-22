from content.api.v1.serializers import PostSerializer, PostItemSerializer
from content.models import Post, PostItem

from .common import BaseListCreateView, BaseRetrieveUpdateDestroyView


class PostListCreateView(BaseListCreateView):
    queryset = Post.objects.all().order_by("-created")
    serializer_class = PostSerializer


class PostRetrieveUpdateDestroyView(BaseRetrieveUpdateDestroyView):
    lookup_field = "post_id"
    lookup_url_kwarg = "post_id"

    queryset = PostItem.objects.select_related("post", "lang", "author").all()
    serializer_class = PostItemSerializer

    def get_queryset(self):
        return self.queryset.filter(lang__code=self.kwargs["lang"])
