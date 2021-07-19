from django.urls import path
from .views import PrivacyPolicyView, SearchUsers

urlpatterns = [
    path('privacy-policy', PrivacyPolicyView.as_view()),
    path('users/', SearchUsers.as_view())
]
