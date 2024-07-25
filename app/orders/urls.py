from django.urls import path

from .views import OrderCreateView, OrderHistoryView

urlpatterns = [
    path("", OrderCreateView.as_view()),
    path("history/", OrderHistoryView.as_view()),
]
