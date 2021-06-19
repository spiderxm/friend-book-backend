from rest_framework.serializers import ModelSerializer, CharField, EmailField, ValidationError
from .models import User


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
            raise ValidationError("The username should only contain alpha numeric characters")

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(ModelSerializer):
    token = CharField(max_length=1024)

    class Meta:
        model = User
        fields = ['token']


