from django.urls import path
from .views import RegisterView, VerifyEmailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('email-verify/', VerifyEmailView.as_view(), name="email-verification")
]
