from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("signup/", views.RegisterView.as_view(), name="registration"),
]
