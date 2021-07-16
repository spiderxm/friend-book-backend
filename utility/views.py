from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

class PrivacyPolicyView(APIView):
    """
    Get Privacy Policy
    """

    def get(self, request):
        return Response({"privacy_policy": render_to_string("privacy_policy.html")}, status=status.HTTP_200_OK)
