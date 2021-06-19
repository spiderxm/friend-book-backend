from django.db import models
from authapp.models import User


class Post(models.Model):
    """
     Model to store user posts
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=255)
    imageUrl = models.URLField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """
    Model to store user comment
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
