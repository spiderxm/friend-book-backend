from django.urls import path
from .views import RegisterView, VerifyEmailView, LoginAPIView, LogoutApiView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('email-verify/', VerifyEmailView.as_view(), name="email-verification"),
    path('login/', LoginAPIView.as_view(), name="Login"),
    path('token/refresh/', TokenRefreshView.as_view(), name="Refresh Token"),
    path('logout/', LogoutApiView.as_view())
]
