from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..serializers.comment import CommentSerializer
from ...models import Comment
from rest_framework.authentication import TokenAuthentication 

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

comment_list_create_view = CommentListCreateView.as_view()

class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

comment_retrieve_update_destroy_view = CommentRetrieveUpdateDestroyView.as_view()