from django.urls import path
from .views import OrderCreateView


urlpatterns = [
    path("", OrderCreateView.as_view())
]
