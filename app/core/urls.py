from .views.register_view import RegisterAPIView

from django.urls import path


# Your urls pattern(s) here.
urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
]
