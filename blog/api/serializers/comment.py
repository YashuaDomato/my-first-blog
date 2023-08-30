from ...models import Comment
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'post',
            'pk',
            'author',
            'text',
            'created_date',
            'approved_comment',
        ]
