from ...models import Post
from rest_framework import serializers
from django.utils import timezone
from .comment import CommentSerializer
from .user import UserPublicSerializer

class PostListSerializer(serializers.ModelSerializer):
    author_details = UserPublicSerializer(source='author', read_only=True)
    class Meta:
        model = Post
        fields = [
            'id',
            'author_details',
            'title',
            'text',
            'created_date',
            'published_date',
        ]

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'text',
            'published_date',
        ]
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        validated_data['created_date'] = timezone.now()
        return super().create(validated_data)
        
class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author_details = UserPublicSerializer(source='author', read_only=True)
    class Meta:
        model = Post
        fields = [
            'id',
            'author_details',
            'title',
            'text',
            'created_date',
            'published_date',
            'comments',
        ]