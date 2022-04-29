from .views.coin_view import CoinAPIView

from django.urls import path


# Your urls pattern(s) here.
urlpatterns = [
    path('coins/', CoinAPIView.as_view(), name='coins'),
]
