from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Post, Comment
from authapp.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    User Model Serializer
    """

    class Meta:
        model = User
        fields = ['image', 'username']


class PostSerializer(serializers.ModelSerializer):
    """
    Post Model Serializer
    """
    likes = serializers.JSONField(read_only=True)
    user = UserSerializer(read_only=True)


    class Meta:
        model = Post
        fields = ['caption', 'image', 'created_at', 'id', 'latitude', 'longitude', 'likes', 'user']


class AllPostSerializer(serializers.ModelSerializer):
    """
    Post Model Serializer
    """
    user = UserSerializer()

    class Meta:
        model = Post
        fields = ['user', 'caption', 'image', 'created_at', 'user', 'likes', 'id']


class CommentSerializer(serializers.ModelSerializer):
    """
        Comment Model Serializer
    """
    created_at = serializers.DateTimeField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ['post', 'body', 'created_at', 'id']


class CommentDetailSerializer(serializers.ModelSerializer):
    """
        Comment Details Serializer
    """
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['post', 'body', 'created_at', 'id', 'user']


class LikeSerializer(serializers.Serializer):
    """
    Like Serializer
    """
    id = serializers.IntegerField(required=True)

    def validate(self, attrs):
        id = attrs.get('id', None)
        if id is None:
            raise ValidationError({"Post": ("Please Provide Valid Post",)})
        if len(Post.objects.all().filter(id=id)) == 0:
            raise ValidationError({"Post": ("Invalid Post Provided",)})
        return attrs