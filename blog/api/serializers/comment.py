from ...models import Comment
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'post',
            'id',
            'author',
            'text',
            'created_date',
            'approved_comment',
        ]
        # read_only_fields = ['post', 'id', 'created_date'] 
class CommentCreateSerializer(serializers.ModelSerializer):
    # post = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
            'author',
            'approved_comment',
        ]

    # def validate(self, data):
    #     # Check if the Post with the specified pk exists
    #     pk = data.get('post')  # Assuming you have a 'post' field in your serializer
    #     if not Post.objects.filter(pk=pk).exists():
    #         raise ValidationError({"post": "Post with this ID does not exist."}, code=status.HTTP_404_NOT_FOUND)
    #     return data