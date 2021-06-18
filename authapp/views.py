from django.urls import reverse
from rest_framework.generics import GenericAPIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from .utils import Helper


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
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relative_link = reverse("email-verification")
            abs_url = 'http://' + current_site + relative_link + "?token=" + str(token)
            email_body = 'Hi ' + user.username + ' User link below to verify your email \n' + abs_url
            data = {
                'email_subject': 'Verify your email',
                'email_body': email_body,
                'email': user.email
            }
            Helper.send_account_verification_email(data)
            return Response(user_data, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            return Response(errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class VerifyEmail(GenericAPIView):
    """
    Verify User Email
    """

    def post(self, request):
        pass
