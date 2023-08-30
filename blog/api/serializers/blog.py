from ...models import Post
from rest_framework import serializers
from django.utils import timezone
from .comment import CommentSerializer

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'title',
            'text',
            'created_date',
            'published_date',
        ]

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
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
    # comments = serializers.HyperlinkedRelatedField(many=True, view_name='comment-detail', read_only=True)
    class Meta:
        model = Post
        fields = [
            'id',
            'url',
            'author',
            'title',
            'text',
            'created_date',
            'published_date',
            'comments',
        ]