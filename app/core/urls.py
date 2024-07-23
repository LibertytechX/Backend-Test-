from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='users-register'),

    path('login/', TokenObtainPairView.as_view(), name='users-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
]
