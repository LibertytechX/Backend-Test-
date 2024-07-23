from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationEndpoint


urlpatterns =[
    path('signup', UserRegistrationEndpoint.as_view(), name='signup'),
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('refresh/token', TokenRefreshView.as_view())
]