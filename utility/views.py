from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

# Create your views here.
from posts.serializers import UserSerializer
from authapp.models import User


class PrivacyPolicyView(APIView):
    """
    Get Privacy Policy
    """

    def get(self, request):
        return Response({"privacy_policy": render_to_string("privacy_policy.html")}, status=status.HTTP_200_OK)


class SearchUsers(GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = None

    def get(self, request):
        username = request.GET.get('username', '')
        users = self.queryset.filter(username__contains=username)[:20]
        return Response(self.serializer_class(users, many=True).data, status=status.HTTP_200_OK)
