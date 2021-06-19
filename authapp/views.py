import datetime

from django.urls import reverse
from rest_framework.generics import GenericAPIView
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializerClass
from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from .utils import Helper
import jwt
from django.conf import settings
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterView(GenericAPIView):
    """
    Users creation View
    """
    serializer_class = RegisterSerializer

    def post(self, request):
        """
        Create a new User
        :param request: Incoming request
        :return:
        """
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            token = jwt.encode(
                {"user_id": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=86400)},
                settings.SECRET_KEY, algorithm="HS256")
            print(token)
            current_site = get_current_site(request).domain
            relative_link = reverse("email-verification")
            abs_url = 'http://' + current_site + relative_link + "?token=" + str(token)
            email_body = 'Hi ' + user.username + ' User link below to verify your email \n' + abs_url
            data = {
                'email_subject': 'Verify your email',
                'email_body': email_body,
                'email': user.email
            }
            # Helper.send_account_verification_email(data)
            return Response(user_data, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            return Response(errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class VerifyEmailView(APIView):
    """
    Verify User Account
    """

    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[
        token_param_config
    ])
    def get(self, request):
        """
        Receive a token from user and verify it.
        """
        token = request.GET.get('token', None)
        try:
            data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=data['user_id'], )
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({"message": "Account verified successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Already activated"})
        except jwt.ExpiredSignatureError:
            return Response({"message": "Token has expired. "}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializerClass

    def post(self, request):
        """
        Login a user via token
        :return: user data with tokens if valid credentials
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

