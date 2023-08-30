from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.forms.models import model_to_dict

from ...models import Post
from ..serializers.blog import PostListSerializer, PostCreateSerializer, PostDetailSerializer

class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    # authentication_classes = [TokenAuthentication]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer  
        return super().get_serializer_class()

post_list_create_view = PostListCreateAPIView.as_view()

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    authentication_classes = []
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return PostCreateSerializer  
        return super().get_serializer_class()

post_retrieve_update_destroy_view = PostRetrieveUpdateDestroyAPIView.as_view()


@api_view(["GET"])
def blog_home(request, *args, **kwargs):
    model_data = Post.objects.all().order_by("?").first()
    data = {}
    if model_data:
        data = model_to_dict(model_data, fields=['author', 'title', 'text', 'created_date', 'published_date'])
    return Response(data)
