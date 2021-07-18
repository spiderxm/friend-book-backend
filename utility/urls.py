from django.urls import path
from .views import PrivacyPolicyView

urlpatterns = [
    path('privacy-policy', PrivacyPolicyView.as_view())
]
