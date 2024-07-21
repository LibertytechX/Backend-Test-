from django.urls import path
from core.views import homepage

urlpatterns = [
    path('', homepage, name='homepage'),
]
