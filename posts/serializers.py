from rest_framework import serializers

from .models import Post, Comment
from authapp.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    User Model Serializer
    """

    class Meta:
        model = User
        fields = ['email']


class PostSerializer(serializers.ModelSerializer):
    """
    Post Model Serializer
    """

    class Meta:
        model = Post
        fields = ['caption', 'imageUrl', 'created_at', 'id']


class AllPostSerializer(serializers.ModelSerializer):
    """
    Post Model Serializer
    """
    user = UserSerializer()

    class Meta:
        model = Post
        fields = ['user', 'caption', 'imageUrl', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment Model Serializer
    """

    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['user', 'post', 'body', 'created_at']
