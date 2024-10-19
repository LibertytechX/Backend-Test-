from django.urls import path
from .views import CreateUserAPIView, LoginUserAPIView

urlpatterns = [
    path("register", CreateUserAPIView.as_view(), name="register"),
    path("login", LoginUserAPIView.as_view(), name="login"),
]
