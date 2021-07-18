from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from authapp.models import User


class Post(models.Model):
    """
     Model to store user posts
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=255)
    image = models.FileField()
    likes = models.JSONField(default=[])
    created_at = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(decimal_places=10, null=True, blank=True, max_digits=15,
                                   validators=[
                                       MaxValueValidator(90.0, message="Latitude should be less than or equal to 90"),
                                       MinValueValidator(-90.0,
                                                         message="Latitude should be greater than or equal to -90")])
    longitude = models.DecimalField(decimal_places=10, null=True, blank=True, max_digits=15,
                                    validators=[
                                        MaxValueValidator(180.0,
                                                          message="Longitude should be less than or equal to 180"),
                                        MinValueValidator(-180.0,
                                                          message="Longitude should be greater than or equal to -180")])

    def __str__(self):
        return self.user.email


class Comment(models.Model):
    """
    Model to store user comment
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
