from rest_framework.serializers import ModelSerializer, CharField, EmailField, ValidationError, JSONField, Serializer
from rest_framework_simplejwt.exceptions import TokenError

from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(ModelSerializer):
    """
    Serializer to handle User Creation Logic
    """
    password = CharField(min_length=7, max_length=68, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise ValidationError({"username": ("The username should only contain alpha numeric characters",)})

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(ModelSerializer):
    """
    Email Verification Serializer
    """
    token = CharField(max_length=1024)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializerClass(ModelSerializer):
    """
    Login Serializer
    """
    email = EmailField(max_length=100, min_length=3)
    password = CharField(min_length=7, max_length=68, write_only=True)
    username = CharField(max_length=255, read_only=True)
    tokens = JSONField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials. Please try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled')
        if not user.is_verified:
            raise AuthenticationFailed('Account not verified')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }


class LogoutSerializer(Serializer):
    refresh_token = CharField(max_length=256)
    default_error_messages = {
        "bad_token": ("Token is expired or invalid",)
    }

    def validate(self, attrs):
        self.token = attrs['refresh_token']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise ValidationError(self.default_error_messages)
