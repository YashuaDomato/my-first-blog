from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import exception_handler

from django.forms.models import model_to_dict

from django.utils import timezone

from ...models import Post
from ..serializers.blog import PostListSerializer, PostCreateSerializer, PostDetailSerializer
from ..permissions import IsAuthorOrReadOnly

class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer  
        return super().get_serializer_class()

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(published_date__lte=timezone.now()).order_by('published_date')

post_list_create_view = PostListCreateAPIView.as_view()

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes  = [IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return PostCreateSerializer  
        return super().get_serializer_class()
        
    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        if response is not None  and 'detail' in response.data and response.status_code == 403:
            method = self.request.method.lower()
            response.data['message'] =  response.data.pop('detail')
            if method == "put" or method == "patch":
                response.data["message"] = f"You are not authorized to edit this post"
            if method == "delete":
                response.data['message']= f"You are not authorized to delete this post"

        return response
post_retrieve_update_destroy_view = PostRetrieveUpdateDestroyAPIView.as_view()


@api_view(["GET"])
def blog_home(request, *args, **kwargs):
    model_data = Post.objects.all().order_by("?").first()
    data = {}
    if model_data:
        data = model_to_dict(model_data, fields=['author', 'title', 'text', 'created_date', 'published_date'])
    return Response(data)
