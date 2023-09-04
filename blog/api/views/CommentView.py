from rest_framework import generics, status
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from ..serializers.comment import CommentSerializer, CommentCreateSerializer
from ...models import Comment, Post
from rest_framework.authentication import TokenAuthentication 
from rest_framework.response import Response

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

comment_list_create_view = CommentListCreateView.as_view()

class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

comment_retrieve_update_destroy_view = CommentRetrieveUpdateDestroyView.as_view()

class PostCommentListCreateView(generics.ListCreateAPIView):
     queryset = Comment.objects.all()
     serializer_class = CommentSerializer

     def get_queryset(self):
        # Get the post_id (pk) from the URL parameter
        post_id = self.kwargs.get('pk')
        
        # Filter comments based on the post_id
        queryset = Comment.objects.filter(post=post_id)
        if not queryset.exists():
            raise Http404("Post does not exist")

        return queryset

     def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer  
        return super().get_serializer_class()

     def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        list = Post.objects.filter(pk=self.kwargs.get('pk'))
        if not list.exists():
            raise Http404("Post does not exist")

        serializer.save(post=list[0])
post_comment_list_create_view = PostCommentListCreateView.as_view()