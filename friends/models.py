from django.db import models
from authapp.models import User


class Friends(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    follows = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.follower.username + " " + self.follows.username
