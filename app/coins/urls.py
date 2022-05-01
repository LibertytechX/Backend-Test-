from .views.coin_view import CoinAPIView
from .views.favourite_view import(
    AddFavouriteAPIView, ViewFavouriteAPIView)

from django.urls import path


# Your urls pattern(s) here.
urlpatterns = [
    path('', CoinAPIView.as_view(), name='coins'),
    path('favourites/', ViewFavouriteAPIView.as_view(), name='view-favourites'),
    path('favourites-add/', AddFavouriteAPIView.as_view(), name='add-favourites'),
]
