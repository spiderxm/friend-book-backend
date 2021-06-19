from django.urls import path
from .views import RegisterView, VerifyEmailView, LoginAPIView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('email-verify/', VerifyEmailView.as_view(), name="email-verification"),
    path('login-api-view/', LoginAPIView.as_view(), name="Login ")
]


