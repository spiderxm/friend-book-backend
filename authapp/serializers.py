from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import DateTimeField, ModelSerializer, CharField, EmailField, FileField, \
    ValidationError, JSONField, \
    Serializer, CurrentUserDefault
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
    image = FileField(read_only=True)
    tokens = JSONField(read_only=True)
    created_at = DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens', 'image', 'created_at']

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
            'tokens': user.tokens(),
            'image': user.image,
            'created_at': user.created_at
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


class ResendEmailSerializer(Serializer):
    email = EmailField(max_length=256)
    user_not_present_error = {
        "email": ("User with this email id is not present",)
    }
    user_already_verified = {
        "email": ("User already verified",)
    }

    def validate(self, attrs):
        email = attrs.get('email', '')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError(self.user_not_present_error)
        if user.is_verified:
            raise ValidationError(self.user_already_verified)
        return super().validate(attrs)


class UserImageSerializer(Serializer):
    image = FileField(allow_empty_file=False, allow_null=False)


class ResetPasswordSerializer(Serializer):
    oldPassword = CharField(min_length=7)
    newPassword = CharField(min_length=7)

    samePasswordError = {"New Password": ("New Password can't be same as old password",)}

    def validate(self, attrs):
        newPassword = attrs.get('newPassword', '')
        oldPassword = attrs.get('oldPassword', '')
        user = self.context.get("request").user
        if newPassword == oldPassword:
            raise ValidationError(self.samePasswordError)
        if user.check_password(oldPassword) is False:
            raise ValidationError({"Old Pasword": ("Invalid Password. Please try again with correct password",)})
        return attrs

    def save(self, **kwargs):
        user = self.context.get("request").user
        oldPassword = self.validated_data['oldPassword']
        newPassword = self.validated_data['oldPassword']
        if user.check_password(oldPassword):
            user.set_password(newPassword)
            user.save()

