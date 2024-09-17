from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from content.api.v1.serializers import PostSerializer, PostItemSerializer
from content.models import Post, PostItem


class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    lookup_field = "post_id"
    lookup_url_kwarg = "post_id"

    queryset = PostItem.objects.select_related("post", "lang", "author").all()
    serializer_class = PostItemSerializer

    def get_queryset(self):
        return self.queryset.filter(lang__code=self.kwargs["lang"])
