from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from authapp.models import User
from posts.serializers import UserSerializer

from .models import Friends


class UnFriendSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate(self, attrs):
        username = self.context['request'].user.username
        friend_username = attrs.get('username')
        if User.objects.all().filter(username=friend_username).exists() is False:
            raise ValidationError({"User": ("Invalid Username provided",)})
        if username == friend_username:
            raise ValidationError({"Follower": ("You cant Unfollow yourself",)})
        if len(Friends.objects.all().filter(follower__username=username, follows__username=friend_username)) == 0:
            raise ValidationError({"Friends": ("Already UnFollowed",)})

        return attrs

    def save(self, **kwargs):
        friend_username = self.validated_data.get('username')
        username = self.context['request'].user.username
        Friends.objects.get(follower=User.objects.get(username=username),
                            follows=User.objects.get(username=friend_username)).delete()


class FriendSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate(self, attrs):
        username = self.context['request'].user.username
        friend_username = attrs.get('username')
        if User.objects.all().filter(username=friend_username).exists() is False:
            raise ValidationError({"User": ("Invalid Username provided",)})
        if Friends.objects.all().filter(follower__username=username, follows__username=friend_username).exists():
            raise ValidationError({"Friends": ("Already Followed",)})
        if username == friend_username:
            raise ValidationError({"Follower": ("You cant follow yourself",)})
        return attrs

    def save(self, **kwargs):
        friend_username = self.validated_data.get('username')
        username = self.context['request'].user.username
        Friends.objects.all().create(follower=User.objects.get(username=username),
                                     follows=User.objects.get(username=friend_username)).save()


class FollowersSerializer(serializers.ModelSerializer):
    follower = UserSerializer()

    class Meta:
        model = Friends
        fields = ['follower', 'created_at']


class FollowsSerializer(serializers.ModelSerializer):
    follows = UserSerializer()

    class Meta:
        model = Friends
        fields = ['follows', 'created_at']


class FollowSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate(self, attrs):
        username = self.context['request'].user.username
        friend_username = attrs.get('username')
        if User.objects.all().filter(username=friend_username).exists() is False:
            raise ValidationError({"User": ("Invalid Username provided",)})
        if username == friend_username:
            raise ValidationError({"Follower": ("You cant check for yourself",)})
        return attrs
